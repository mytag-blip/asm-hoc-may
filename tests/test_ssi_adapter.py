"""SSI adapter tests use local fixtures and mocked transport only; no market data or network calls."""
from __future__ import annotations

from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory
import json
import unittest
from unittest.mock import patch

import pandas as pd

from src.data.providers.ssi import SSIClient, SSIConfig, SSIDataError
from src.data.quality import audit_ohlcv
from src.data.staging import StagingStore
from scripts.ssi_probe import PROBE_TICKERS, build_parser
import scripts.ssi_probe as ssi_probe


class SSIFixtureTests(unittest.TestCase):
    def test_probe_requires_one_allowed_ticker_and_defaults_to_project_period(self):
        args = build_parser().parse_args(["--ticker", "FPT"])
        self.assertEqual(args.ticker, "FPT")
        self.assertEqual(args.from_date, "2021-11-19")
        self.assertEqual(args.to_date, "2026-11-18")
        self.assertEqual(len(PROBE_TICKERS), 5)
        with self.assertRaises(SystemExit):
            build_parser().parse_args(["--ticker", "ACB"])

    def test_probe_run_rejects_out_of_allowlist_before_credentials_or_network(self):
        with patch.object(ssi_probe, "SSIClient") as client:
            with self.assertRaisesRegex(SSIDataError, "allowlist"):
                ssi_probe.run("ACB", "2021-11-19", "2026-11-18")
            client.assert_not_called()

    def test_probe_records_success_only_in_staging_without_network(self):
        frame = pd.DataFrame([{"Date":"2021-11-19", "Ticker":"FPT", "Open":10, "High":11,
                               "Low":9, "Close":10.5, "Volume":100}])
        with TemporaryDirectory() as tmp:
            store = StagingStore(tmp)
            fake_client = unittest.mock.Mock()
            fake_client.fetch_ohlcv.return_value = (frame, {"source":"SSI FastConnect", "ticker":"FPT",
                "retrieved_at":"2026-11-20T00:00:00+00:00", "status":"success", "error":None})
            with patch.object(ssi_probe, "PROJECT_ROOT", Path(tmp)), \
                 patch.object(ssi_probe, "StagingStore", return_value=store), \
                 patch.object(ssi_probe, "load_cafef_comparison", return_value=(frame.copy(), "available", None)), \
                 patch.object(ssi_probe.SSIConfig, "from_env", return_value=SSIConfig("fixture", "fixture")), \
                 patch.object(ssi_probe, "SSIClient", return_value=fake_client):
                result = ssi_probe.run("FPT", "2021-11-19", "2026-11-18")
            fake_client.authenticate.assert_called_once_with()
            fake_client.fetch_ohlcv.assert_called_once_with("FPT", "2021-11-19", "2026-11-18")
            self.assertEqual(result["status"], "success")
            self.assertEqual(result["cafeF_comparison"]["status"], "compared")
            self.assertEqual(result["cafeF_comparison"]["compared_rows"], 1)
            self.assertTrue(store.rows_path.exists())
            self.assertTrue(store.manifest_path.exists())
            self.assertFalse((Path(tmp)/"data"/"raw"/"stock_data_raw.csv").exists())
            self.assertFalse((Path(tmp)/"data"/"processed"/"stock_data_processed.csv").exists())

    def test_probe_records_empty_result_without_claiming_data_available(self):
        empty = pd.DataFrame(columns=["Date", "Ticker", "Open", "High", "Low", "Close", "Volume"])
        with TemporaryDirectory() as tmp:
            store = StagingStore(tmp)
            fake_client = unittest.mock.Mock()
            fake_client.fetch_ohlcv.return_value = (empty, {"source":"SSI FastConnect", "ticker":"VIC",
                "retrieved_at":"2026-11-20T00:00:00+00:00", "status":"success", "error":None})
            with patch.object(ssi_probe, "PROJECT_ROOT", Path(tmp)), \
                 patch.object(ssi_probe, "StagingStore", return_value=store), \
                 patch.object(ssi_probe.SSIConfig, "from_env", return_value=SSIConfig("fixture", "fixture")), \
                 patch.object(ssi_probe, "SSIClient", return_value=fake_client):
                result = ssi_probe.run("VIC", "2021-11-19", "2026-11-18")
            self.assertEqual(result["status"], "empty")
            manifest = json.loads(store.manifest_path.read_text(encoding="utf-8").splitlines()[0])
            self.assertEqual(manifest["status"], "empty")

    def test_probe_failure_log_contains_no_credentials(self):
        with TemporaryDirectory() as tmp:
            store = StagingStore(tmp)
            with patch.object(ssi_probe, "PROJECT_ROOT", Path(tmp)), \
                 patch.object(ssi_probe, "StagingStore", return_value=store), \
                 patch.object(ssi_probe.SSIConfig, "from_env", side_effect=SSIDataError("Thiếu SSI_API_KEY hoặc SSI_API_SECRET trong environment.")):
                with self.assertRaisesRegex(SSIDataError, "Thiếu SSI_API_KEY"):
                    ssi_probe.run("FPT", "2021-11-19", "2026-11-18")
            content = store.manifest_path.read_text(encoding="utf-8")
            self.assertNotIn("fixture-secret", content)
            self.assertIn("Thiếu SSI_API_KEY", content)

    def test_auth_then_paginate_and_normalize_fixture(self):
        requests = []
        def transport(method, url, headers, body, timeout):
            requests.append((method, url, headers, body))
            if url.endswith("/auth/token"):
                return 200, {}, json.dumps({"accessToken": "fixture-token"}).encode()
            page = 1 if "pageIndex=1" in url else 2
            rows = ([{"symbol":"FPT","tradingDate":"2021-11-19","open":"10","high":"11","low":"9","close":"10.5","volume":"100"},
                     {"symbol":"FPT","tradingDate":"2021-11-22","open":"10.5","high":"12","low":"10","close":"11","volume":"120"}] if page == 1 else
                    [{"symbol":"FPT","tradingDate":"2021-11-23","open":"11","high":"12","low":"10","close":"11.5","volume":"130"}])
            return 200, {"X-RATELIMIT-REMAINING":"20"}, json.dumps({"data":rows,"pageCount":2,"pageIndex":page}).encode()
        client = SSIClient(SSIConfig("fixture-key", "fixture-secret", page_size=2), transport)
        client.authenticate()
        frame, meta = client.fetch_ohlcv("fpt", "2021-11-19", "2021-11-23")
        self.assertEqual(len(frame), 3)
        self.assertEqual(frame.columns.tolist(), ["Date","Ticker","Open","High","Low","Close","Volume"])
        self.assertEqual(frame["Ticker"].unique().tolist(), ["FPT"])
        self.assertEqual(frame["Close"].iloc[-1], 11.5)
        self.assertEqual(meta["pages"], 2)
        self.assertEqual(meta["rate_limit_headers"]["X-RATELIMIT-REMAINING"], "20")
        self.assertEqual(len(requests), 3)
        self.assertNotIn("fixture-secret", str(requests[1][2]))

    def test_missing_credentials_and_auth_failure(self):
        with self.assertRaises(SSIDataError):
            SSIConfig.from_env({})
        secret = "fixture-secret"
        client = SSIClient(SSIConfig("fixture-key", secret), lambda *args: (401, {}, b'{"message":"fixture-secret"}'))
        with self.assertRaisesRegex(SSIDataError, "HTTP 401") as caught:
            client.authenticate()
        self.assertNotIn(secret, str(caught.exception))

    def test_environment_limits_are_bounded_until_provider_quota_is_confirmed(self):
        with self.assertRaisesRegex(SSIDataError, "SSI_PAGE_SIZE tạm giới hạn"):
            SSIConfig.from_env({"SSI_API_KEY":"k", "SSI_API_SECRET":"s", "SSI_PAGE_SIZE":"11"})
        with self.assertRaisesRegex(SSIDataError, "SSI_MAX_PAGES tạm giới hạn"):
            SSIConfig.from_env({"SSI_API_KEY":"k", "SSI_API_SECRET":"s", "SSI_MAX_PAGES":"501"})

    def test_page_loop_and_schema_errors_are_reported(self):
        client = SSIClient(SSIConfig("k", "s", page_size=1, max_pages=2), lambda *args: (200, {}, json.dumps({"data":[{"bad":"schema"}],"pageCount":1}).encode()))
        client._access_token = "token"
        with self.assertRaisesRegex(SSIDataError, "thiếu một hoặc nhiều"):
            client.fetch_ohlcv("FPT", "2021-01-01", "2021-01-02")

    def test_repeated_page_stops_pagination(self):
        repeated = {"data":[{"symbol":"FPT","tradingDate":"2021-11-19","open":10,"high":11,"low":9,"close":10,"volume":100}],"pageCount":3}
        client = SSIClient(SSIConfig("k", "s", page_size=1), lambda *args: (200, {}, json.dumps(repeated).encode()))
        client._access_token = "fixture-token"
        with self.assertRaisesRegex(SSIDataError, "trang; dừng"):
            client.fetch_ohlcv("FPT", "2021-11-19", "2021-11-22")

    def test_quality_flags_without_mutating_rows(self):
        frame = pd.DataFrame([
            {"Date":"2021-11-19","Ticker":"FPT","Open":10,"High":9,"Low":8,"Close":10,"Volume":-2},
            {"Date":"2021-11-19","Ticker":"FPT","Open":10,"High":12,"Low":8,"Close":11,"Volume":100},
        ])
        original = frame.copy(deep=True)
        result = audit_ohlcv(frame, expected_dates={date(2021,11,19),date(2021,11,22)}, corporate_action_dates={date(2021,11,19)})
        self.assertEqual(result["summary"]["duplicate_rows"], 2)
        self.assertEqual(result["summary"]["invalid_ohlc_rows"], 1)
        self.assertEqual(result["summary"]["negative_volume_rows"], 1)
        self.assertEqual(len(result["summary"]["missing_dates_by_ticker"]["FPT"]), 1)
        self.assertEqual(int(result["row_flags"]["corporate_action_date"].sum()), 2)
        pd.testing.assert_frame_equal(frame, original)

    def test_missing_dates_are_explicitly_unassessed_without_calendar(self):
        frame = pd.DataFrame([{"Date":"2021-11-19","Ticker":"FPT","Open":10,"High":11,
                               "Low":9,"Close":10,"Volume":100}])
        result = audit_ohlcv(frame)
        self.assertIsNone(result["summary"]["missing_dates_by_ticker"])

    def test_staging_is_idempotent_and_attempts_are_audited(self):
        rows = pd.DataFrame([{"Date":"2021-11-19","Ticker":"FPT","Open":1,"High":2,"Low":1,"Close":2,"Volume":100}])
        with TemporaryDirectory() as tmp:
            store = StagingStore(tmp)
            meta = {"source":"SSI FastConnect","retrieved_at":"2026-11-20T00:00:00+00:00","status":"success","ticker":"FPT"}
            store.save(rows, meta)
            store.save(rows, {**meta,"retrieved_at":"2026-11-21T00:00:00+00:00"})
            saved = pd.read_csv(store.rows_path)
            self.assertEqual(len(saved), 1)
            self.assertEqual(saved.iloc[0]["RetrievedAt"], "2026-11-21T00:00:00+00:00")
            self.assertEqual(len(store.manifest_path.read_text(encoding="utf-8").splitlines()), 2)
            self.assertFalse((Path(tmp)/"data"/"raw"/"stock_data_raw.csv").exists())
            self.assertFalse((Path(tmp)/"data"/"processed"/"stock_data_processed.csv").exists())

if __name__ == "__main__":
    unittest.main()
