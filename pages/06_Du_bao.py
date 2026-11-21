import json
from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd
import streamlit as st
from sklearn.decomposition import PCA
from sklearn.preprocessing import RobustScaler, StandardScaler

from src.dashboard_ui import render_empty_panel, render_page_header, render_section_heading
from src.data.research import PROJECT_ROOT
from src.models.clustering import FEATURE_SETS


ARTIFACT_DIR = PROJECT_ROOT / "artifacts" / "clustering"
FEATURE_PATH = ARTIFACT_DIR / "features_conditional.csv"
LABEL_PATH = ARTIFACT_DIR / "clustering_labels.csv"
PROFILE_PATH = ARTIFACT_DIR / "cluster_profiles.csv"

render_page_header(
    "HỒ SƠ CỤM", "Đánh giá đặc điểm doanh nghiệp",
    "Tra cứu các doanh nghiệp trong từng cấu hình phân cụm và so sánh hồ sơ đặc trưng.",
)
st.warning(
    "Các hồ sơ này là kết quả thăm dò có điều kiện trên Close chưa xác minh cơ sở giá. "
    "Cluster ID chỉ là định danh kỹ thuật, không phải mức rủi ro."
)

if not all(path.exists() for path in (FEATURE_PATH, LABEL_PATH, PROFILE_PATH)):
    render_empty_panel(
        "Chưa có hồ sơ phân cụm",
        "Chạy một lần đánh giá tại trang Machine Learning. Ứng dụng không tạo dự báo phân loại giả.",
    )
    st.stop()

features = pd.read_csv(FEATURE_PATH)
labels = pd.read_csv(LABEL_PATH)
profiles = pd.read_csv(PROFILE_PATH)
configurations = labels[["Feature_Set", "Algorithm", "Scaler", "Parameters"]].drop_duplicates().reset_index(drop=True)
configurations["display"] = configurations.apply(
    lambda r: f"{r.Feature_Set} · {r.Algorithm} · {r.Scaler} · {r.Parameters}", axis=1
)
selected_display = st.selectbox("Chọn cấu hình", configurations["display"].tolist())
config = configurations.loc[configurations["display"].eq(selected_display)].iloc[0]
mask = (
    labels["Feature_Set"].eq(config["Feature_Set"])
    &
    labels["Algorithm"].eq(config["Algorithm"])
    & labels["Scaler"].eq(config["Scaler"])
    & labels["Parameters"].eq(config["Parameters"])
)
selected_labels = labels.loc[mask, ["Ticker", "Cluster"]].copy()
selected_profiles = profiles.loc[
    profiles["Algorithm"].eq(config["Algorithm"])
    & profiles["Feature_Set"].eq(config["Feature_Set"])
    & profiles["Scaler"].eq(config["Scaler"])
    & profiles["Parameters"].eq(config["Parameters"])
].copy()

render_section_heading("Phân bố cụm", "Các chỉ số là mô tả có điều kiện; không ép DBSCAN thành ba nhóm.")
st.dataframe(selected_profiles, hide_index=True, width="stretch")
choice = st.selectbox("Chọn cụm để tra cứu", selected_profiles["Profile"].tolist())
cluster_value = selected_profiles.loc[selected_profiles["Profile"].eq(choice), "Cluster"].iloc[0]
members = selected_labels.loc[selected_labels["Cluster"].eq(cluster_value)].merge(features, on="Ticker", how="left")
st.markdown(f"**Doanh nghiệp trong {choice}:** {', '.join(members['Ticker'].astype(str))}")
st.dataframe(members, hide_index=True, width="stretch")

scaler = StandardScaler() if config["Scaler"] == "StandardScaler" else RobustScaler()
x = scaler.fit_transform(features[FEATURE_SETS[config["Feature_Set"]]])
coordinates = PCA(n_components=2, random_state=42).fit_transform(x)
plot_data = selected_labels.copy()
plot_data["PC1"] = coordinates[:, 0]
plot_data["PC2"] = coordinates[:, 1]
fig, ax = plt.subplots(figsize=(8, 5))
for cluster, group in plot_data.groupby("Cluster", sort=True):
    label = "Noise (-1)" if cluster == -1 else f"Cụm {cluster}"
    ax.scatter(group["PC1"], group["PC2"], label=label, s=55, alpha=.8)
    for row in group.itertuples():
        ax.annotate(row.Ticker, (row.PC1, row.PC2), fontsize=7, xytext=(3, 3), textcoords="offset points")
ax.set_title("PCA 2D — chỉ trực quan hóa đặc trưng đã scale")
ax.set_xlabel("Thành phần chính 1")
ax.set_ylabel("Thành phần chính 2")
ax.legend(fontsize=8, loc="best")
fig.tight_layout()
st.pyplot(fig)
plt.close(fig)
st.caption("PCA chỉ để hiển thị; hai trục không phải mức rủi ro và biểu đồ không thay thế kiểm tra độ ổn định.")

render_section_heading("Diễn giải")
st.info(
    "So sánh trung vị độ phân tán return, rolling volatility và drawdown trong bảng hồ sơ. "
    "Không gán ‘thấp/trung bình/cao’ cho đến khi price basis, corporate actions và dữ liệu được xác minh."
)
