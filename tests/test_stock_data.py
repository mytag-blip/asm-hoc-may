"""Fixture dữ liệu tổng hợp chỉ dùng kiểm thử module nhập liệu; không phải dữ liệu thị trường."""
from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

import pandas as pd

from src.data.stock_data import (
    StockFileError,
    PLANNED_TICKERS,
    read_stock_file,
    save_original_file,
    suggest_column_mapping,
    validate_stock_frame,
)
from src.data.universe import RESEARCH_TICKERS


class StockDataImportTests(unittest.TestCase):
    def test_research_universe_has_43_unique_tickers(self):
        self.assertEqual(len(RESEARCH_TICKERS), 43)
        self.assertEqual(len(set(RESEARCH_TICKERS)), 43)

    def test_importer_uses_research_universe_for_ticker_override_scope(self):
        self.assertEqual(tuple(PLANNED_TICKERS), RESEARCH_TICKERS)

    def test_research_ticker_is_not_flagged_as_out_of_scope(self):
        frame = self.fixture.copy()
        frame["Mã CK"] = "FPT"
        result = self._validate(frame)
        self.assertTrue(result.is_valid, result.errors)
        self.assertFalse(any("ngoài danh sách" in warning for warning in result.warnings))

    def setUp(self):
        # Fixture nhỏ, tổng hợp và chỉ dùng trong test.
        self.fixture = pd.DataFrame(
            {
                "Ngày giao dịch": ["2025-01-02", "2025-01-03"],
                "Giá mở cửa": [10.0, 10.5],
                "Giá cao nhất": [11.0, 11.5],
                "Giá thấp nhất": [9.5, 10.0],
                "Giá đóng cửa": [10.5, 11.0],
                "Khối lượng": [1000, 1200],
                "Mã CK": ["ACB", "ACB"],
            }
        )

    def _validate(self, frame):
        mapping = suggest_column_mapping(frame.columns)
        return validate_stock_frame(frame, mapping)

    def test_valid_csv(self):
        content = self.fixture.to_csv(index=False).encode("utf-8")
        raw = read_stock_file("fixture_test.csv", content)
        result = self._validate(raw)
        self.assertTrue(result.is_valid, result.errors)
        self.assertEqual(len(result.data), 2)
        self.assertEqual(result.ticker, "ACB")

    def test_valid_xlsx(self):
        buffer = BytesIO()
        self.fixture.to_excel(buffer, index=False, engine="openpyxl")
        raw = read_stock_file("fixture_test.xlsx", buffer.getvalue())
        result = self._validate(raw)
        self.assertTrue(result.is_valid, result.errors)
        self.assertEqual(result.ticker, "ACB")
        self.assertEqual(len(result.data), 2)

    def test_multiple_tickers_are_recognized_when_ticker_column_exists(self):
        frame = self.fixture.copy()
        frame.loc[1, "Mã CK"] = "BID"
        result = self._validate(frame)
        self.assertTrue(result.is_valid, result.errors)
        self.assertEqual(result.ticker, "ACB, BID")
    def test_missing_required_column_is_rejected(self):
        frame = self.fixture.drop(columns=["Giá cao nhất"])
        result = self._validate(frame)
        self.assertFalse(result.is_valid)
        self.assertTrue(any("High" in error for error in result.errors))

    def test_non_numeric_value_is_rejected(self):
        frame = self.fixture.copy()
        frame["Giá mở cửa"] = frame["Giá mở cửa"].astype(object)
        frame.loc[0, "Giá mở cửa"] = "không phải số"
        result = self._validate(frame)
        self.assertFalse(result.is_valid)
        self.assertEqual(result.invalid_type_counts["Open"], 1)

    def test_invalid_date_is_rejected(self):
        frame = self.fixture.copy()
        frame.loc[0, "Ngày giao dịch"] = "31/02/2025"
        result = self._validate(frame)
        self.assertFalse(result.is_valid)
        self.assertEqual(result.invalid_date_count, 1)

    def test_duplicate_ticker_date_is_detected_without_deleting_rows(self):
        frame = pd.concat([self.fixture, self.fixture.iloc[[0]]], ignore_index=True)
        result = self._validate(frame)
        self.assertFalse(result.is_valid)
        self.assertEqual(result.duplicate_key_count, 2)
        self.assertEqual(len(result.data), 3)

    def test_missing_value_is_reported(self):
        frame = self.fixture.copy()
        frame.loc[0, "Giá đóng cửa"] = float("nan")
        result = self._validate(frame)
        self.assertFalse(result.is_valid)
        self.assertEqual(result.missing_counts["Close"], 1)

    def test_invalid_ohlc_relationship_is_reported(self):
        frame = self.fixture.copy()
        frame.loc[0, "Giá thấp nhất"] = 12.0
        result = self._validate(frame)
        self.assertFalse(result.is_valid)
        self.assertEqual(result.invalid_price_count, 1)
    def test_infinite_price_is_rejected(self):
        frame = self.fixture.copy()
        frame.loc[0, "Giá đóng cửa"] = float("inf")
        result = self._validate(frame)
        self.assertFalse(result.is_valid)
        self.assertEqual(result.invalid_price_count, 1)
    def test_empty_file_is_rejected(self):
        with self.assertRaisesRegex(StockFileError, "File rỗng"):
            read_stock_file("empty.csv", b"")


    def test_original_file_is_saved_exactly_and_never_overwritten(self):
        content = b"original test fixture bytes"
        with TemporaryDirectory() as temp_dir:
            first = save_original_file("fixture_test.csv", content, temp_dir)
            second = save_original_file("fixture_test.csv", content, temp_dir)
            self.assertNotEqual(first, second)
            self.assertEqual(first.read_bytes(), content)
            self.assertEqual(second.read_bytes(), content)


if __name__ == "__main__":
    unittest.main()





