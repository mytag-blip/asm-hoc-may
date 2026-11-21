from pathlib import Path

import pandas as pd
import streamlit as st

from src.dashboard_ui import render_empty_panel, render_page_header, render_section_heading
from src.data.research import load_processed


render_page_header(
    "KIỂM TRA", "Chất lượng dữ liệu",
    "Rà soát cấu trúc, độ phủ và các cờ chất lượng đã ghi nhận; không tự sửa dữ liệu.",
)
try:
    frame = load_processed()
except (FileNotFoundError, ValueError, OSError) as exc:
    render_empty_panel("Chưa đọc được Processed", str(exc))
    st.stop()

dates = pd.to_datetime(frame["Date"], errors="coerce")
ticker_date_dups = int(frame.duplicated(["Ticker", "Date"], keep=False).sum())
missing_cells = int(frame.isna().sum().sum())
numeric_cols = [c for c in ["Open", "High", "Low", "Close", "Volume"] if c in frame]
numeric = frame[numeric_cols].apply(pd.to_numeric, errors="coerce")
ohlc_bad = (
    (numeric["High"] < numeric["Open"])
    | (numeric["High"] < numeric["Close"])
    | (numeric["Low"] > numeric["Open"])
    | (numeric["Low"] > numeric["Close"])
)
flagged_ohlc = int(ohlc_bad.fillna(False).sum())
volume_flags = 0
if "Volume" in numeric:
    for _, group in frame.assign(_Volume=numeric["Volume"]).groupby("Ticker"):
        q1, q3 = group["_Volume"].quantile([.25, .75])
        volume_flags += int((group["_Volume"] > q3 + 3 * (q3 - q1)).sum())

metrics = st.columns(4)
metrics[0].metric("Dòng Processed", f"{len(frame):,}")
metrics[1].metric("Mã cổ phiếu", frame["Ticker"].nunique())
metrics[2].metric("Ô thiếu", f"{missing_cells:,}")
metrics[3].metric("Khóa mã-ngày trùng", f"{ticker_date_dups:,}")
st.caption(f"Khoảng ngày quan sát: {dates.min():%Y-%m-%d} – {dates.max():%Y-%m-%d}; đây không xác nhận lịch phiên HOSE đầy đủ.")

render_section_heading("Cờ chất lượng đã rà", "Cờ thống kê là tín hiệu kiểm tra, không tự động đồng nghĩa dữ liệu sai.")
quality = pd.DataFrame([
    {"Hạng mục": "Quan hệ OHLC vi phạm", "Số dòng": f"{flagged_ohlc:,}", "Xử lý": "Giữ nguyên; 16 dòng đã đối chiếu workbook nguồn nhưng chưa có feed độc lập."},
    {"Hạng mục": "Volume > Q3 + 3×IQR theo mã", "Số dòng": f"{volume_flags:,}", "Xử lý": "Giữ nguyên; cờ thống kê, chưa gán đơn vị/thanh khoản."},
    {"Hạng mục": "Ngày quan sát thiếu theo mã", "Số dòng": "Xem báo cáo", "Xử lý": "Không nội suy; hợp ngày không phải lịch HOSE độc lập."},
])
st.dataframe(quality, hide_index=True, width="stretch")
if "Data_Quality_Flag" in frame:
    flagged = frame.loc[frame["Data_Quality_Flag"].notna() & frame["Data_Quality_Flag"].astype("string").str.strip().ne("")]
else:
    flagged = frame.loc[ohlc_bad.fillna(False)]
st.markdown("**Các dòng có cờ OHLC**")
display_columns = [c for c in ["Ticker", "Date", "Open", "High", "Low", "Close", "Data_Quality_Flag", "Source_File", "Source_Row"] if c in flagged]
st.dataframe(flagged[display_columns], hide_index=True, width="stretch")
st.info("Adjusted Close/corporate actions, units, ngày vắng theo từng mã và một số cờ OHLC vẫn chưa được xác minh độc lập.")
report = Path(__file__).resolve().parents[1] / "reports" / "BAO_CAO_TONG_KET_PHUONG_AN_DU_LIEU.md"
if report.exists():
    st.download_button("Tải báo cáo tổng kết phương án dữ liệu", report.read_bytes(), file_name=report.name, mime="text/markdown")
