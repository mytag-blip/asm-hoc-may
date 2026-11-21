"""Read-only access to the checked-in CafeF research dataset."""
from __future__ import annotations

from pathlib import Path
import pandas as pd

PROJECT_ROOT = Path(__file__).resolve().parents[2]
PROCESSED_PATH = PROJECT_ROOT / "data" / "processed" / "stock_data_processed.csv"


def load_processed(path: str | Path = PROCESSED_PATH) -> pd.DataFrame:
    source = Path(path)
    if not source.exists():
        raise FileNotFoundError(f"Không tìm thấy dữ liệu Processed: {source}")
    frame = pd.read_csv(source, low_memory=False)
    required = {"Date", "Ticker", "Open", "High", "Low", "Close", "Volume"}
    missing = required - set(frame.columns)
    if missing:
        raise ValueError(f"Processed thiếu cột: {', '.join(sorted(missing))}")
    return frame


def known_ohlc_flags(frame: pd.DataFrame) -> pd.DataFrame:
    """Read the pre-existing quality flags; do not recreate/guess their keys."""
    if "Data_Quality_Flag" not in frame:
        return pd.DataFrame(columns=["Ticker", "Date"])
    flagged = frame.loc[
        frame["Data_Quality_Flag"].notna()
        & frame["Data_Quality_Flag"].astype("string").str.strip().ne(""),
        ["Ticker", "Date"],
    ].copy()
    flagged["Date"] = pd.to_datetime(flagged["Date"], errors="coerce")
    return flagged.dropna(subset=["Date"]).drop_duplicates(["Ticker", "Date"])
