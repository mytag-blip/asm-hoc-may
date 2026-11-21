import streamlit as st
import pandas as pd

from src.data.research import PROJECT_ROOT, load_processed
from src.data.universe import RESEARCH_TICKERS

from src.dashboard_ui import render_empty_panel, render_page_header, render_section_heading


TICKERS = RESEARCH_TICKERS

render_page_header(
    "ASM MACHINE LEARNING",
    "Tổng quan dự án",
    "Phân nhóm và đánh giá rủi ro biến động giá cổ phiếu của 43 doanh nghiệp niêm yết trên HOSE bằng học máy không giám sát.",
)

st.markdown(
    """
    <div class="muted-copy">
        <strong>Mục tiêu:</strong> phân nhóm doanh nghiệp theo đặc trưng rủi ro biến động giá; nhãn cụm chỉ được diễn giải sau khi mô hình được đánh giá.
    </div>
    """,
    unsafe_allow_html=True,
)
st.write("")

metric_columns = st.columns(4)
metric_columns[0].metric("Mã trong phạm vi", f"{len(TICKERS)}", help="Universe theo dữ liệu và cấu hình nghiên cứu hiện tại.")
try:
    overview_data = load_processed()
    observed_dates = pd.to_datetime(overview_data["Date"], errors="coerce")
    metric_columns[1].metric("Mã có dữ liệu", f"{overview_data['Ticker'].nunique():,}")
    metric_columns[2].metric("Bản ghi Processed", f"{len(overview_data):,}")
    metric_columns[3].metric(
        "Khoảng quan sát",
        f"{observed_dates.min():%d/%m/%Y} – {observed_dates.max():%d/%m/%Y}",
    )
except (FileNotFoundError, ValueError, OSError):
    overview_data = None
    metric_columns[1].metric("Mã có dữ liệu", "Chưa có dữ liệu")
    metric_columns[2].metric("Bản ghi Processed", "Chưa có dữ liệu")
    metric_columns[3].metric("Khoảng quan sát", "Chưa có dữ liệu")
metrics_path = PROJECT_ROOT / "artifacts" / "clustering" / "clustering_metrics.csv"

st.info(
    "Kết quả phân cụm hiện là thử nghiệm kỹ thuật có điều kiện. Cơ sở giá và corporate actions "
    "chưa được xác minh nên chưa thể xem các cụm là mức rủi ro thực tế.",
    icon="⚠️",
)

left, right = st.columns([1.1, 0.9], gap="large")
with left:
    render_section_heading("Doanh nghiệp trong nghiên cứu", "Danh sách lấy từ universe dùng chung trong dự án.")
    with st.container(border=True):
        st.markdown("".join(f'<span class="ticker-chip">{ticker}</span>' for ticker in TICKERS), unsafe_allow_html=True)
        st.caption("Dữ liệu CafeF: 19/11/2021–18/11/2026. Cơ sở giá cần xác minh trước khi tạo đặc trưng rủi ro.")

with right:
    render_section_heading("Trạng thái thí nghiệm")
    with st.container(border=True):
        if metrics_path.exists():
            try:
                config_count = len(pd.read_csv(metrics_path))
                st.metric("Cấu hình phân cụm đã chạy", f"{config_count:,}")
            except (OSError, ValueError):
                st.metric("Trạng thái phân cụm", "Cần kiểm tra artifact")
        else:
            st.metric("Trạng thái phân cụm", "Chưa chạy")
        st.caption("Chỉ số nội bộ giúp kiểm tra cấu hình; không chứng minh cụm có ý nghĩa kinh tế.")

render_section_heading("Lối tắt", "Đi thẳng đến các bước thường dùng trong dashboard.")
st.markdown(
    """
    <div class="quick-link-grid">
      <a class="quick-link" href="/Quan_ly_du_lieu"><span>🗂️</span><strong>Quản lý dữ liệu</strong><small>Nhập và duyệt dữ liệu</small></a>
      <a class="quick-link" href="/Phan_tich_du_lieu"><span>📊</span><strong>Phân tích EDA</strong><small>Khám phá biểu đồ và thống kê</small></a>
      <a class="quick-link" href="/Machine_Learning"><span>🧠</span><strong>Phân cụm</strong><small>Đánh giá cấu hình thăm dò</small></a>
    </div>
    """,
    unsafe_allow_html=True,
)

render_section_heading("Tiến độ dự án")
phase_columns = st.columns(4, gap="medium")
phases = [
    ("Phân tích yêu cầu", "Hoàn thành", "done"),
    ("Khởi tạo ứng dụng", "Hoàn thành", "done"),
    ("EDA mô tả", "Hoàn thành", "done"),
    ("Pipeline phân cụm thăm dò", "Đã chạy; chờ xác minh dữ liệu để kết luận nghiên cứu", "pending"),
]
for column, (name, status, state) in zip(phase_columns, phases):
    with column:
        with st.container(border=True):
            st.markdown(
                f'<div class="status-line"><span class="status-dot {state}"></span>{name}</div>',
                unsafe_allow_html=True,
            )
            st.caption(status)
