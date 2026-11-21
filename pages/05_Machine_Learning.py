from pathlib import Path

import matplotlib.pyplot as plt
import streamlit as st

from src.dashboard_ui import render_page_header, render_section_heading
from src.data.research import PROJECT_ROOT, known_ohlc_flags, load_processed
from src.features.risk_features import build_conditional_features
from src.models.clustering import run_clustering, save_run
from src.reporting.experiment_report import plot_metrics, write_experiment_report


ARTIFACT_DIR = PROJECT_ROOT / "artifacts" / "clustering"
ANALYSIS_DIR = PROJECT_ROOT / "data" / "analysis"
REPORT_DIR = PROJECT_ROOT / "reports"

render_page_header(
    "MÔ HÌNH KHÔNG GIÁM SÁT", "Phân cụm doanh nghiệp",
    "Thử nghiệm K-Means, Agglomerative và DBSCAN trên đặc trưng giá tổng hợp theo mã.",
)
st.warning(
    "Đây là thử nghiệm có điều kiện trên Close CafeF chưa xác minh cơ sở giá/corporate actions. "
    "Không diễn giải các cụm thành mức rủi ro thực tế đã xác nhận. Raw và Processed chỉ được đọc."
)

try:
    source = load_processed()
    features, sensitivity, diagnostics = build_conditional_features(source, known_ohlc_flags(source))
except Exception as exc:
    st.error(f"Không thể chuẩn bị dữ liệu phân cụm: {exc}")
    st.stop()

overview = st.columns(3)
overview[0].metric("Dòng nguồn", f"{diagnostics['input_rows']:,}")
overview[1].metric("Mã được phân tích", f"{diagnostics['tickers']}")
overview[2].metric("Cặp return hợp lệ", f"{diagnostics['return_rows']:,}")
with st.expander("Xem ma trận đặc trưng", expanded=False):
    render_section_heading("Ma trận đặc trưng có điều kiện", "Một dòng cho mỗi mã; không đưa Ticker hoặc nhãn rủi ro làm đặc trưng.")
    st.dataframe(features, hide_index=True, width="stretch")
    st.caption("Volume chỉ là thống kê mô tả; chưa gọi là thanh khoản.")
with st.expander("Phương pháp và cảnh báo"):
    st.markdown(
        "- Return: Close(t)/Close(t-1)-1; chỉ tính khi ngày của mã kề nhau trong hợp ngày quan sát.\n"
        "- Rolling volatility: độ lệch chuẩn mẫu 20 return kề; cửa sổ không bắc qua gap.\n"
        "- Drawdown: tích lũy return Close theo đoạn liên tục, reset sau gap.\n"
        "- Bản nhạy cảm loại các return chạm cờ OHLC hoặc |return| ≥ 10% khỏi phần tóm tắt; không sửa nguồn.\n"
        "- Không dùng Adjusted Close, OHLC/ATR hoặc suy đoán corporate actions."
    )
with st.expander("Bản phân tích độ nhạy", expanded=False):
    st.caption("Return chạm cờ OHLC hoặc có |return| ≥ 10% được loại khỏi bản tóm tắt độ nhạy; dữ liệu nguồn không đổi.")
    st.dataframe(sensitivity, hide_index=True, width="stretch")

if st.button("Chạy đánh giá cấu hình phân cụm", type="primary"):
    with st.spinner("Đang chạy các cấu hình trên 43 mã..."):
        run = run_clustering(features, random_state=42)
        run.metadata["quality_diagnostics"] = diagnostics
        save_run(run, features, ARTIFACT_DIR)
        ANALYSIS_DIR.mkdir(parents=True, exist_ok=True)
        sensitivity.to_csv(ANALYSIS_DIR / "features_sensitivity.csv", index=False, encoding="utf-8-sig")
        write_experiment_report(features, run, diagnostics, REPORT_DIR, sensitivity=sensitivity)
        st.session_state["clustering_completed"] = True
    st.success("Đã lưu thử nghiệm riêng trong data/analysis, artifacts/clustering và reports; Raw/Processed không bị ghi.")

if (ARTIFACT_DIR / "clustering_metrics.csv").exists():
    metrics = __import__("pandas").read_csv(ARTIFACT_DIR / "clustering_metrics.csv")
    render_section_heading("So sánh cấu hình", "Chỉ số nội bộ không có nhãn chuẩn; DBSCAN noise được báo riêng.")
    result_tabs = st.tabs(["Bảng chỉ số", "Biểu đồ so sánh", "Tệp báo cáo"])
    with result_tabs[0]:
        filters = st.columns(2)
        algorithms = sorted(metrics["Algorithm"].dropna().unique())
        feature_sets = sorted(metrics["Feature_Set"].dropna().unique())
        selected_algorithms = filters[0].multiselect("Thuật toán", algorithms, default=algorithms)
        selected_sets = filters[1].multiselect("Bộ đặc trưng", feature_sets, default=feature_sets)
        visible = metrics.loc[
            metrics["Algorithm"].isin(selected_algorithms)
            & metrics["Feature_Set"].isin(selected_sets)
        ]
        st.caption(f"Đang hiển thị {len(visible):,}/{len(metrics):,} cấu hình.")
        st.dataframe(visible, hide_index=True, width="stretch")
    with result_tabs[1]:
        chart_metrics = metrics.loc[
            metrics["Algorithm"].isin(selected_algorithms)
            & metrics["Feature_Set"].isin(selected_sets)
        ] if "selected_algorithms" in locals() else metrics
        metrics_figure = plot_metrics(chart_metrics)
        st.pyplot(metrics_figure)
        plt.close(metrics_figure)
        st.caption("Biểu đồ hiển thị metric nội bộ; không tự động chọn mô hình hoặc gán cấp độ rủi ro.")
    with result_tabs[2]:
        st.caption("Tệp được tạo từ lần chạy gần nhất, kèm metadata và cảnh báo về cơ sở giá.")
        report = REPORT_DIR / "BAO_CAO_THU_NGHIEM_PHAN_CUM_CO_DIEU_KIEN.md"
        if report.exists():
            st.download_button("Tải báo cáo Markdown", report.read_bytes(), file_name=report.name, mime="text/markdown")
        metrics_path = ARTIFACT_DIR / "clustering_metrics.csv"
        if metrics_path.exists():
            st.download_button("Tải bảng chỉ số CSV", metrics_path.read_bytes(), file_name=metrics_path.name, mime="text/csv")
    st.caption("Xem danh sách doanh nghiệp và hồ sơ cấu hình tại trang Đánh giá rủi ro.")
else:
    st.info("Chưa có lần chạy phân cụm. Hãy xem ma trận đặc trưng, sau đó bấm nút chạy để tạo đầu ra có thể tái lập.")
