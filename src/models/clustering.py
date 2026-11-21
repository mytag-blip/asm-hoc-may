"""Reproducible exploratory clustering for one-row-per-company features."""
from __future__ import annotations

from dataclasses import asdict, dataclass
from itertools import product
import json
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd
from sklearn.cluster import AgglomerativeClustering, DBSCAN, KMeans
from sklearn.metrics import (adjusted_rand_score, calinski_harabasz_score,
                             davies_bouldin_score, silhouette_score)
from sklearn.preprocessing import RobustScaler, StandardScaler
import sklearn


PRICE_FEATURES = [
    "Daily_Return_Std_Conditional",
    "Rolling_Volatility_20D_Median_Conditional",
    "Rolling_Volatility_20D_P95_Conditional",
    "Maximum_Drawdown_Close_Conditional",
]
FEATURE_SETS = {
    "Giá (cốt lõi)": PRICE_FEATURES,
    "Giá + CV Volume (độ nhạy)": PRICE_FEATURES + ["Volume_CV_Descriptive"],
}


@dataclass
class ClusteringRun:
    metrics: pd.DataFrame
    labels: pd.DataFrame
    profiles: pd.DataFrame
    stability: pd.DataFrame
    metadata: dict[str, Any]


def _score(x: np.ndarray, labels: np.ndarray, algorithm: str, params: dict, scaler: str) -> dict:
    labels = np.asarray(labels)
    noise = labels == -1 if algorithm == "DBSCAN" else np.zeros(len(labels), dtype=bool)
    included = ~noise
    observed_clusters = np.unique(labels[included])
    result = {
        "Algorithm": algorithm, "Scaler": scaler, "Parameters": json.dumps(params, sort_keys=True),
        "N_Samples": len(labels), "N_Clusters": len(observed_clusters),
        "Noise_Count": int(noise.sum()), "Noise_Fraction": float(noise.mean()),
        "Silhouette": np.nan, "Davies_Bouldin": np.nan, "Calinski_Harabasz": np.nan,
        "Metric_Sample_Count": int(included.sum()), "Status": "Đánh giá được" if len(observed_clusters) >= 2 and included.sum() > len(observed_clusters) else "Không đủ cụm/mẫu để tính metric",
    }
    if len(observed_clusters) >= 2 and included.sum() > len(observed_clusters):
        subset_x = x[included]
        subset_y = labels[included]
        result["Silhouette"] = float(silhouette_score(subset_x, subset_y))
        result["Davies_Bouldin"] = float(davies_bouldin_score(subset_x, subset_y))
        result["Calinski_Harabasz"] = float(calinski_harabasz_score(subset_x, subset_y))
    return result


def run_clustering(features: pd.DataFrame, random_state: int = 42) -> ClusteringRun:
    missing = set(["Ticker", *PRICE_FEATURES, "Volume_CV_Descriptive"]) - set(features.columns)
    if missing:
        raise ValueError(f"Thiếu đặc trưng: {', '.join(sorted(missing))}")
    if features["Ticker"].duplicated().any():
        raise ValueError("Mỗi Ticker chỉ được có một dòng đặc trưng.")
    if len(features) < 4:
        raise ValueError("Cần ít nhất 4 doanh nghiệp để khảo sát cấu hình phân cụm.")

    labels_rows: list[dict] = []
    metric_rows: list[dict] = []
    stability_rows: list[dict] = []
    profiles_rows: list[dict] = []
    for feature_set, feature_names in FEATURE_SETS.items():
        numeric = features[feature_names].apply(pd.to_numeric, errors="coerce")
        if numeric.isna().any().any() or not np.isfinite(numeric.to_numpy()).all():
            raise ValueError(f"Feature set {feature_set} có missing hoặc giá trị không hữu hạn; không tự điền.")
        for scaler_name, scaler_class in (("StandardScaler", StandardScaler), ("RobustScaler", RobustScaler)):
            x = scaler_class().fit_transform(numeric)
            for k in range(2, min(6, len(features) - 1) + 1):
                model = KMeans(n_clusters=k, random_state=random_state, n_init=20)
                labels = model.fit_predict(x)
                params = {"n_clusters": k, "random_state": random_state, "n_init": 20}
                metric_rows.append({"Feature_Set": feature_set, **_score(x, labels, "KMeans", params, scaler_name)})
                labels_rows.extend({"Ticker": t, "Feature_Set": feature_set, "Algorithm": "KMeans", "Scaler": scaler_name, "Parameters": json.dumps(params), "Cluster": int(label)} for t, label in zip(features["Ticker"], labels))
                for seed in (7, 21, 99):
                    other = KMeans(n_clusters=k, random_state=seed, n_init=20).fit_predict(x)
                    stability_rows.append({"Feature_Set":feature_set, "Algorithm":"KMeans", "Scaler":scaler_name, "n_clusters":k, "Compared_Seed":seed, "ARI_vs_42":float(adjusted_rand_score(labels, other))})

                agg = AgglomerativeClustering(n_clusters=k, linkage="ward").fit_predict(x)
                agg_params = {"n_clusters": k, "linkage": "ward"}
                metric_rows.append({"Feature_Set": feature_set, **_score(x, agg, "Agglomerative", agg_params, scaler_name)})
                labels_rows.extend({"Ticker": t, "Feature_Set": feature_set, "Algorithm": "Agglomerative", "Scaler": scaler_name, "Parameters": json.dumps(agg_params), "Cluster": int(label)} for t, label in zip(features["Ticker"], agg))

            for eps, min_samples in product((0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5), (3, 4, 5)):
                model = DBSCAN(eps=eps, min_samples=min_samples)
                labels = model.fit_predict(x)
                params = {"eps": eps, "min_samples": min_samples, "metric": "euclidean"}
                metric_rows.append({"Feature_Set": feature_set, **_score(x, labels, "DBSCAN", params, scaler_name)})
                labels_rows.extend({"Ticker": t, "Feature_Set": feature_set, "Algorithm": "DBSCAN", "Scaler": scaler_name, "Parameters": json.dumps(params), "Cluster": int(label)} for t, label in zip(features["Ticker"], labels))

    metrics = pd.DataFrame(metric_rows)
    labels_frame = pd.DataFrame(labels_rows)
    stability = pd.DataFrame(stability_rows)
    main = features.set_index("Ticker")
    for (feature_set, algorithm, scaler, params), group in labels_frame.groupby(["Feature_Set", "Algorithm", "Scaler", "Parameters"], sort=False):
        feature_names = FEATURE_SETS[feature_set]
        joined = group.set_index("Ticker").join(main[feature_names])
        for cluster, cluster_rows in joined.groupby("Cluster", sort=True):
            if cluster == -1:
                label_name = "Nhiễu DBSCAN (noise)"
            else:
                label_name = f"Cụm {cluster}"
            profiles_rows.append({
                "Feature_Set": feature_set, "Algorithm": algorithm, "Scaler": scaler, "Parameters": params,
                "Cluster": int(cluster), "Profile": label_name, "N_Tickers": len(cluster_rows),
                **{f"Median_{feature}": float(cluster_rows[feature].median()) for feature in feature_names},
                "Tickers": ", ".join(cluster_rows.index.astype(str)),
            })
    profiles = pd.DataFrame(profiles_rows)
    metadata = {
        "random_state": random_state, "features": PRICE_FEATURES,
        "feature_sets": FEATURE_SETS,
        "scalers": ["StandardScaler", "RobustScaler"],
        "interpretation": "Khám phá có điều kiện từ Close chưa xác minh basis; Cluster ID không phải nhãn rủi ro.",
        "n_companies": len(features), "algorithms": ["KMeans", "Agglomerative", "DBSCAN"],
    }
    return ClusteringRun(metrics, labels_frame, profiles, stability, metadata)


def save_run(run: ClusteringRun, features: pd.DataFrame, directory: str | Path) -> Path:
    output = Path(directory)
    output.mkdir(parents=True, exist_ok=True)
    # Stable filenames are confined to analysis artifacts, never Raw/Processed.
    features.to_csv(output / "features_conditional.csv", index=False, encoding="utf-8-sig")
    run.metrics.to_csv(output / "clustering_metrics.csv", index=False, encoding="utf-8-sig")
    run.labels.to_csv(output / "clustering_labels.csv", index=False, encoding="utf-8-sig")
    run.profiles.to_csv(output / "cluster_profiles.csv", index=False, encoding="utf-8-sig")
    run.stability.to_csv(output / "kmeans_stability.csv", index=False, encoding="utf-8-sig")
    source_path = Path(__file__).resolve().parents[2] / "data" / "processed" / "stock_data_processed.csv"
    run.metadata.update({
        "run_timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "source_file": "data/processed/stock_data_processed.csv",
        "source_sha256": sha256(source_path.read_bytes()).hexdigest() if source_path.exists() else None,
        "sklearn_version": sklearn.__version__,
        "conditional_price_basis_warning": "CafeF Close basis/corporate-action methodology chưa xác minh; kết quả chỉ thăm dò.",
    })
    (output / "metadata.json").write_text(json.dumps(run.metadata, ensure_ascii=False, indent=2), encoding="utf-8")
    return output
