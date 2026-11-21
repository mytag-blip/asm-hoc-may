from __future__ import annotations

import streamlit as st

from src.dashboard_ui import apply_dashboard_style

st.set_page_config(
    page_title="ASM Machine Learning",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded",
)

apply_dashboard_style()

with st.sidebar:
    st.markdown(
        """
        <div class="sidebar-brand">
            <div class="sidebar-brand-icon">📈</div>
            <div>
                <div class="sidebar-brand-title">ASM Machine Learning</div>
                <div class="sidebar-brand-caption">Phân tích chứng khoán</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
    st.caption("Đồ án Học Máy Cơ Bản")

pages = {
    "Không gian ASM": [
        st.Page("pages/01_Tong_quan.py", title="Tổng quan", icon="🏠", default=True),
        st.Page("pages/02_Quan_ly_du_lieu.py", title="Quản lý dữ liệu", icon="🗂️"),
        st.Page("pages/03_Chat_luong_du_lieu.py", title="Chất lượng dữ liệu", icon="🔎"),
        st.Page("pages/04_Phan_tich_du_lieu.py", title="Phân tích dữ liệu", icon="📊"),
        st.Page("pages/05_Machine_Learning.py", title="Machine Learning", icon="🧠"),
        st.Page("pages/06_Du_bao.py", title="Đánh giá rủi ro", icon="🎯"),
    ]
}

page = st.navigation(pages, position="sidebar")
page.run()
