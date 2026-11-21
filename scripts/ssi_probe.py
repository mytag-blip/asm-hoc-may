"""Run one explicitly selected, read-only SSI OHLCV probe into staging."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
from pathlib import Path
import json
import sys

import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from src.data.providers.ssi import SSIClient, SSIConfig, SSIDataError
from src.data.quality import audit_ohlcv
from src.data.staging import StagingStore

PROBE_TICKERS = ("FPT", "NLG", "HPG", "VNM", "VIC")
DEFAULT_FROM = "2021-11-19"
DEFAULT_TO = "2026-11-18"
COMPARISON_FIELDS = ["Date", "Ticker", "Open", "High", "Low", "Close", "Volume"]


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Tải OHLCV SSI cho đúng một mã vào data/staging/ssi.")
    parser.add_argument("--ticker", required=True, choices=PROBE_TICKERS, help="Chỉ chạy một mã mỗi lần.")
    parser.add_argument("--from-date", default=DEFAULT_FROM, help="Ngày đầu YYYY-MM-DD.")
    parser.add_argument("--to-date", default=DEFAULT_TO, help="Ngày cuối YYYY-MM-DD.")
    return parser


def load_cafef_comparison(project_root: str | Path, ticker: str) -> tuple[pd.DataFrame, str, str | None]:
    """Read matching CafeF OHLCV rows without changing the processed dataset."""
    path = Path(project_root) / "data" / "processed" / "stock_data_processed.csv"
    if not path.exists():
        return pd.DataFrame(columns=COMPARISON_FIELDS), "unavailable", "Không tìm thấy Processed CafeF để đối chiếu."
    try:
        header = pd.read_csv(path, nrows=0).columns.tolist()
        absent = [field for field in COMPARISON_FIELDS if field not in header]
        if absent:
            return pd.DataFrame(columns=COMPARISON_FIELDS), "unavailable", f"Processed thiếu cột: {', '.join(absent)}."
        reference = pd.read_csv(path, usecols=COMPARISON_FIELDS)
    except (OSError, ValueError, pd.errors.ParserError):
        return pd.DataFrame(columns=COMPARISON_FIELDS), "unavailable", "Không đọc được Processed CafeF để đối chiếu."
    reference["Ticker"] = reference["Ticker"].astype(str).str.upper()
    reference = reference.loc[reference["Ticker"].eq(ticker.upper())].copy()
    reference["Date"] = pd.to_datetime(reference["Date"], errors="coerce").dt.normalize()
    return reference, "available", None


def run(ticker: str, date_from: str, date_to: str) -> dict:
    ticker = ticker.strip().upper()
    if ticker not in PROBE_TICKERS:
        raise SSIDataError("Ticker không nằm trong allowlist thử nghiệm SSI.")
    store = StagingStore(PROJECT_ROOT)
    metadata = {"source": "SSI FastConnect", "ticker": ticker, "requested_from": date_from, "requested_to": date_to,
                "retrieved_at": datetime.now(timezone.utc).isoformat(), "status": "error", "error": None}
    try:
        config = SSIConfig.from_env()
        client = SSIClient(config)
        client.authenticate()
        frame, result_metadata = client.fetch_ohlcv(ticker, date_from, date_to)
        reference, comparison_status, comparison_reason = load_cafef_comparison(PROJECT_ROOT, ticker)
        quality = audit_ohlcv(frame, comparison=reference if comparison_status == "available" else None)
        result_metadata["status"] = "success" if not frame.empty else "empty"
        result_metadata["quality_summary"] = quality["summary"]
        result_metadata["date_gap_check"] = {
            "status": "not_assessed",
            "reason": "Chưa có lịch phiên giao dịch được xác minh; không suy diễn ngày thiếu từ lịch ngày thường.",
        }
        result_metadata["price_unit"] = "Chưa xác minh"
        result_metadata["volume_unit"] = "Chưa xác minh"
        result_metadata["corporate_actions_status"] = "Chưa đối chiếu sự kiện/price basis"
        comparison = quality["summary"]["comparison"]
        if comparison_status == "available":
            comparison_status = "compared" if comparison["compared_rows"] else "no_overlap"
        result_metadata["cafeF_comparison"] = {
            **comparison,
            "status": comparison_status,
            "reason": comparison_reason or "So sánh OHLCV mô tả theo ngày; price basis/corporate actions chưa xác minh, không kết luận nguồn nào tốt hơn.",
        }
        store.save(frame, result_metadata)
        return result_metadata
    except (SSIDataError, ValueError, OSError) as exc:
        # SSIDataError messages intentionally exclude response bodies and credential values.
        metadata["error"] = str(exc)
        store.record_failure(metadata)
        raise SSIDataError(str(exc)) from exc


def main() -> int:
    # Windows consoles may default to cp1252; keep Vietnamese CLI text from crashing.
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    args = build_parser().parse_args()
    try:
        start, end = pd.Timestamp(args.from_date), pd.Timestamp(args.to_date)
        if start > end:
            raise SSIDataError("--from-date phải nhỏ hơn hoặc bằng --to-date.")
        result = run(args.ticker, start.date().isoformat(), end.date().isoformat())
    except (SSIDataError, ValueError) as exc:
        print(f"Không hoàn tất tải SSI cho {args.ticker}: {exc}", file=sys.stderr)
        return 2
    print(json.dumps({k: v for k, v in result.items() if k not in {"rate_limit_headers"}}, ensure_ascii=False, default=str))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
