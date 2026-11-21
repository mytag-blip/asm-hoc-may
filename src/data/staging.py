"""Append-safe, idempotent CSV staging isolated from data/raw and data/processed."""
from __future__ import annotations

from pathlib import Path
from typing import Any
import json
import os
import tempfile

import pandas as pd


STAGING_FIELDS = ["Ticker", "Date", "Source", "RetrievedAt", "Open", "High", "Low", "Close", "Volume", "LoadStatus", "LoadError"]


class StagingStore:
    def __init__(self, root: str | Path):
        self.root = Path(root) / "data" / "staging" / "ssi"
        self.rows_path = self.root / "ohlcv.csv"
        self.manifest_path = self.root / "load_manifest.jsonl"

    def save(self, frame: pd.DataFrame, metadata: dict[str, Any]) -> int:
        self.root.mkdir(parents=True, exist_ok=True)
        rows = frame.copy()
        if not rows.empty:
            rows["Date"] = pd.to_datetime(rows["Date"], errors="coerce").dt.strftime("%Y-%m-%d")
        rows["Source"] = metadata.get("source", "SSI FastConnect")
        rows["RetrievedAt"] = metadata["retrieved_at"]
        rows["LoadStatus"] = metadata.get("status", "success")
        rows["LoadError"] = metadata.get("error")
        for field in STAGING_FIELDS:
            if field not in rows:
                rows[field] = pd.NA
        rows = rows[STAGING_FIELDS]

        if self.rows_path.exists():
            existing = pd.read_csv(self.rows_path)
            combined = pd.concat([existing, rows], ignore_index=True)
        else:
            combined = rows
        if not combined.empty:
            # Preserve the newest successful copy per provider/ticker/date; every attempt remains in manifest.
            combined = combined.drop_duplicates(["Source", "Ticker", "Date"], keep="last")
        self._atomic_csv(combined)
        with self.manifest_path.open("a", encoding="utf-8") as stream:
            stream.write(json.dumps(metadata, ensure_ascii=False, default=str) + "\n")
        return len(rows)

    def _atomic_csv(self, frame: pd.DataFrame) -> None:
        fd, temporary_name = tempfile.mkstemp(prefix="ssi_", suffix=".csv.tmp", dir=self.root)
        os.close(fd)
        temporary = Path(temporary_name)
        try:
            frame.to_csv(temporary, index=False, encoding="utf-8-sig")
            os.replace(temporary, self.rows_path)
        finally:
            temporary.unlink(missing_ok=True)

    def record_failure(self, metadata: dict[str, Any]) -> None:
        failed = {**metadata, "status": "error", "error": str(metadata.get("error") or "Unknown error")}
        self.save(pd.DataFrame(columns=["Ticker", "Date", "Open", "High", "Low", "Close", "Volume"]), failed)
