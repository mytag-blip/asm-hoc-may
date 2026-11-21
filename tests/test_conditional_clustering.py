"""Synthetic fixtures here test software mechanics only, never market findings."""
import unittest

import numpy as np
import pandas as pd

from src.features.risk_features import build_conditional_features
from src.models.clustering import PRICE_FEATURES, run_clustering


class ConditionalFeatureTests(unittest.TestCase):
    def setUp(self):
        dates = pd.bdate_range("2024-01-01", periods=55)
        rows = []
        for ticker, drift, scale in (("AAA", .001, .008), ("BBB", -.0005, .02)):
            close = 100.0
            for i, date in enumerate(dates):
                if i:
                    close *= 1 + drift + scale * np.sin(i * .73)
                rows.append({"Ticker": ticker, "Date": date, "Close": close, "Volume": 1000 + i})
        self.frame = pd.DataFrame(rows)

    def test_feature_output_has_one_row_per_ticker_and_does_not_mutate_input(self):
        original = self.frame.copy(deep=True)
        features, sensitivity, diagnostics = build_conditional_features(self.frame)
        self.assertEqual(set(features.Ticker), {"AAA", "BBB"})
        self.assertEqual(len(features), 2)
        self.assertIn("Daily_Return_Std_Conditional", features)
        self.assertEqual(len(sensitivity), 2)
        self.assertGreater(diagnostics["return_rows"], 0)
        pd.testing.assert_frame_equal(self.frame, original)

    def test_union_calendar_gap_skips_return_instead_of_filling(self):
        gapped = self.frame.loc[~((self.frame.Ticker == "AAA") & (self.frame.Date == pd.Timestamp("2024-01-10")))].copy()
        features, _, diagnostics = build_conditional_features(gapped)
        aaa = features.loc[features.Ticker.eq("AAA")].iloc[0]
        self.assertEqual(aaa.N_Adjacent_Returns, 52)
        self.assertEqual(diagnostics["gap_skipped_pairs"], 1)

    def test_ohlc_flag_excludes_returns_touching_both_endpoints_only_in_sensitivity(self):
        flagged_date = pd.Timestamp("2024-01-29")
        flags = pd.DataFrame([{"Ticker": "AAA", "Date": flagged_date}])
        features, sensitivity, _ = build_conditional_features(self.frame, ohlc_flags=flags)
        aaa = sensitivity.loc[sensitivity.Ticker.eq("AAA")].iloc[0]
        self.assertEqual(aaa.N_Returns_Excluded_Sensitivity, 2)
        self.assertEqual(features.loc[features.Ticker.eq("AAA"), "N_Adjacent_Returns"].iloc[0], 54)

    def test_duplicate_key_and_invalid_values_fail_closed(self):
        duplicated = pd.concat([self.frame, self.frame.iloc[[0]]], ignore_index=True)
        with self.assertRaisesRegex(ValueError, "trùng"):
            build_conditional_features(duplicated)
        invalid = self.frame.copy()
        invalid.loc[0, "Close"] = 0
        with self.assertRaisesRegex(ValueError, "dương"):
            build_conditional_features(invalid)


class ClusteringTests(unittest.TestCase):
    def setUp(self):
        rng = np.random.default_rng(42)
        rows = []
        for i in range(12):
            center = (0.01, 0.02, 0.04, -0.10) if i < 6 else (0.03, 0.05, 0.09, -0.45)
            rows.append({"Ticker": f"T{i:02d}", **dict(zip(PRICE_FEATURES, np.array(center) + rng.normal(0, .002, 4))), "Volume_CV_Descriptive": 0.2 + i * .03})
        self.features = pd.DataFrame(rows)

    def test_all_algorithms_return_metrics_labels_and_profiles(self):
        run = run_clustering(self.features)
        self.assertEqual(set(run.metrics.Algorithm), {"KMeans", "Agglomerative", "DBSCAN"})
        self.assertEqual(set(run.labels.Ticker), set(self.features.Ticker))
        self.assertFalse(run.profiles.empty)
        self.assertTrue(run.metadata["random_state"] == 42)

    def test_missing_feature_is_not_imputed(self):
        bad = self.features.copy()
        bad.loc[0, PRICE_FEATURES[0]] = np.nan
        with self.assertRaisesRegex(ValueError, "missing"):
            run_clustering(bad)


if __name__ == "__main__":
    unittest.main()
