"""Run an explicitly conditional experiment on the existing CafeF Processed file."""
from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data.research import PROJECT_ROOT, known_ohlc_flags, load_processed
from src.features.risk_features import build_conditional_features
from src.models.clustering import run_clustering, save_run
from src.reporting.experiment_report import write_experiment_report


def main() -> None:
    source = load_processed()
    features, sensitivity, diagnostics = build_conditional_features(source, known_ohlc_flags(source))
    analysis_dir = PROJECT_ROOT / "data" / "analysis"
    analysis_dir.mkdir(parents=True, exist_ok=True)
    features.to_csv(analysis_dir / "features_conditional.csv", index=False, encoding="utf-8-sig")
    sensitivity.to_csv(analysis_dir / "features_sensitivity.csv", index=False, encoding="utf-8-sig")
    run = run_clustering(features, random_state=42)
    run.metadata["quality_diagnostics"] = diagnostics
    save_run(run, features, PROJECT_ROOT / "artifacts" / "clustering")
    report = write_experiment_report(features, run, diagnostics, PROJECT_ROOT / "reports", sensitivity=sensitivity)
    print(f"Feature rows: {len(features)}; tickers: {features['Ticker'].nunique()}")
    print(f"Run metrics: {len(run.metrics)} configurations; labels: {len(run.labels)}")
    print(f"Report: {report}")
    print(run.metrics.groupby("Algorithm")["Silhouette"].agg(["count", "max"]).to_string())


if __name__ == "__main__":
    main()
