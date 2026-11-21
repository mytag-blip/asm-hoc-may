import streamlit as st
from pathlib import Path
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from src.dashboard_ui import render_empty_panel, render_page_header, render_section_heading
from src.data.research import load_processed, known_ohlc_flags
from src.features.risk_features import build_conditional_features


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EDA_DIR = PROJECT_ROOT / "reports" / "eda"

render_page_header(
    "KHÁM PHÁ",
    "Phân tích dữ liệu",
    "Không gian EDA cho xu hướng giá, khối lượng giao dịch và phân phối các biến.",
)

tabs = st.tabs(["Giá & khối lượng", "Phân phối biến", "Tương quan", "Đặc trưng thăm dò"])
with tabs[0]:
    render_section_heading("Biểu đồ Close và Volume đã lập", "Biểu đồ EDA hiện có, không tính return/volatility.")
    if EDA_DIR.exists():
        all_charts = sorted(EDA_DIR.glob("*.png"))
        chart_kind = st.radio(
            "Nhóm biểu đồ", ["Tất cả", "Giá đóng cửa", "Khối lượng", "Tổng quan"],
            horizontal=True,
        )
        prefixes = {
            "Giá đóng cửa": "close_",
            "Khối lượng": "volume_",
            "Tổng quan": "phan_phoi_",
        }
        choices = [
            path for path in all_charts
            if chart_kind == "Tất cả" or path.stem.startswith(prefixes[chart_kind])
        ]
        if choices:
            selected = st.selectbox(
                "Chọn biểu đồ", choices,
                format_func=lambda path: path.stem.replace("close_", "Giá đóng cửa · ").replace("volume_", "Khối lượng · ").replace("_", " ").upper(),
            )
            st.image(str(selected), caption=selected.stem.replace("_", " ").upper(), width="stretch")
        else:
            render_empty_panel("Chưa có biểu đồ phù hợp", "Chọn nhóm biểu đồ khác hoặc kiểm tra thư mục reports/eda.")
    else:
        render_empty_panel("Chưa có biểu đồ", "Thư mục reports/eda chưa có artifact.")
with tabs[1]:
    render_section_heading("Phân phối biến", "Tham khảo báo cáo EDA đã hoàn thành.")
    report = PROJECT_ROOT / "reports" / "BAO_CAO_EDA.md"
    if report.exists():
        st.markdown(report.read_text(encoding="utf-8")[:6000])
    else:
        render_empty_panel("Chưa có báo cáo EDA", "Không tìm thấy reports/BAO_CAO_EDA.md.")
with tabs[2]:
    render_section_heading("Tương quan đặc trưng thăm dò", "Pearson correlation trên tối đa 43 dòng tổng hợp; đây không phải phân tích nhân quả.")
    st.warning("Đặc trưng giá có điều kiện trên Close chưa xác minh basis. Heatmap chỉ hỗ trợ khám phá quan hệ giữa các biến đã tạo.")
    try:
        source = load_processed()
        features, _, _ = build_conditional_features(source, known_ohlc_flags(source))
        selected = [
            "Daily_Return_Std_Conditional",
            "Rolling_Volatility_20D_Median_Conditional",
            "Rolling_Volatility_20D_P95_Conditional",
            "Maximum_Drawdown_Close_Conditional",
        ]
        correlation = features[selected].corr(method="pearson")
        fig, ax = plt.subplots(figsize=(8, 5.5))
        sns.heatmap(correlation, annot=True, fmt=".2f", cmap="vlag", center=0, vmin=-1, vmax=1, ax=ax)
        ax.set_title("Tương quan Pearson — feature giá có điều kiện")
        fig.tight_layout()
        st.pyplot(fig)
        plt.close(fig)
        st.dataframe(correlation, width="stretch")
    except (FileNotFoundError, ValueError, KeyError, OSError) as exc:
        st.error(f"Chưa thể tạo heatmap: {exc}")

with tabs[3]:
    render_section_heading("Đặc trưng giá có điều kiện", "Kết quả chỉ để khảo sát pipeline; chưa phải ước lượng rủi ro đã xác minh.")
    st.warning("Close CafeF chưa xác minh cơ sở qua corporate actions. Không dùng Adjusted Close, không nội suy, không dùng OHLC/ATR.")
    try:
        source = load_processed()
        features, sensitivity, diagnostics = build_conditional_features(source, known_ohlc_flags(source))
        st.caption(f"{len(features)} mã · {diagnostics['return_rows']:,} return kề hợp lịch · {diagnostics['gap_skipped_pairs']:,} cặp bỏ qua vì ngày vắng.")
        st.dataframe(features, hide_index=True, width="stretch")
        st.markdown("**Phân tích độ nhạy** — return chạm cờ OHLC hoặc |return| ≥ 10% bị loại khỏi bản tóm tắt này; dữ liệu nguồn giữ nguyên.")
        st.dataframe(sensitivity, hide_index=True, width="stretch")
        st.download_button("Tải bảng đặc trưng khám phá", features.to_csv(index=False).encode("utf-8-sig"), file_name="features_conditional.csv", mime="text/csv")
    except (FileNotFoundError, ValueError, KeyError, OSError) as exc:
        st.error(f"Chưa thể tính bảng đặc trưng: {exc}")

st.caption("Không có biểu đồ hoặc số liệu minh họa giả trong trang này.")

