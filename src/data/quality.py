"""Non-destructive validation and source-comparison flags for staged OHLCV."""
from __future__ import annotations

import pandas as pd


def audit_ohlcv(frame: pd.DataFrame, expected_dates: set | None = None, corporate_action_dates: set | None = None,
                comparison: pd.DataFrame | None = None, price_unit: str | None = None, volume_unit: str | None = None) -> dict:
    data = frame.copy()
    required = ["Date", "Ticker", "Open", "High", "Low", "Close", "Volume"]
    missing_columns = [col for col in required if col not in data]
    if missing_columns:
        return {"errors": [f"Thiếu cột: {', '.join(missing_columns)}"], "row_flags": pd.DataFrame(), "summary": {"rows": len(data)}}
    data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
    numeric = ["Open", "High", "Low", "Close", "Volume"]
    nulls = data[required].isna().sum().to_dict()
    invalid_numeric = {col: int(pd.to_numeric(data[col], errors="coerce").isna().sum()) for col in numeric}
    duplicate_mask = data.duplicated(["Ticker", "Date"], keep=False)
    prices = data[numeric[:4]].apply(pd.to_numeric, errors="coerce")
    volume = pd.to_numeric(data["Volume"], errors="coerce")
    invalid_ohlc = ((prices["Open"] <= 0) | (prices["High"] <= 0) | (prices["Low"] <= 0) | (prices["Close"] <= 0)
                    | (prices["High"] < prices["Low"]) | (prices["High"] < prices["Open"]) | (prices["High"] < prices["Close"])
                    | (prices["Low"] > prices["Open"]) | (prices["Low"] > prices["Close"]))
    negative_volume = volume < 0
    row_flags = pd.DataFrame({"duplicate_ticker_date": duplicate_mask, "invalid_ohlc": invalid_ohlc.fillna(False), "negative_volume": negative_volume.fillna(False)})
    row_flags["volume_high_q3_3iqr"] = False
    for _, indexes in data.groupby("Ticker", dropna=False).groups.items():
        values = volume.loc[indexes].dropna()
        if len(values) >= 4:
            q1, q3 = values.quantile([0.25, 0.75])
            row_flags.loc[values.index, "volume_high_q3_3iqr"] = values > q3 + 3 * (q3 - q1)
    if expected_dates is not None:
        expected = {pd.Timestamp(d).date() for d in expected_dates}
        missing_dates = {}
        for ticker, part in data.groupby("Ticker", dropna=False):
            known = set(part["Date"].dropna().dt.date)
            absent = sorted(d.isoformat() for d in (expected - known))
            if absent:
                missing_dates[str(ticker)] = absent
    else:
        missing_dates = None
    if corporate_action_dates:
        ca_dates = {pd.Timestamp(d).date() for d in corporate_action_dates}
        row_flags["corporate_action_date"] = data["Date"].dt.date.isin(ca_dates)
    else:
        row_flags["corporate_action_date"] = False
    comparison_result = {"status": "not_checked", "compared_rows": 0, "mismatch_rows": 0}
    if comparison is not None:
        reference = comparison.copy()
        if "Date" in reference:
            reference["Date"] = pd.to_datetime(reference["Date"], errors="coerce")
        joined = data.merge(reference, on=["Ticker", "Date"], suffixes=("_ssi", "_other"), how="inner")
        comparable = [col for col in numeric if f"{col}_ssi" in joined and f"{col}_other" in joined]
        mismatch = pd.Series(False, index=joined.index)
        for col in comparable:
            a, b = pd.to_numeric(joined[f"{col}_ssi"], errors="coerce"), pd.to_numeric(joined[f"{col}_other"], errors="coerce")
            mismatch |= ~((a - b).abs() <= 1e-9)
        comparison_result = {"status": "compared", "compared_rows": len(joined), "mismatch_rows": int(mismatch.sum()), "fields": comparable}
    return {"errors": [], "row_flags": row_flags, "summary": {"rows": len(data), "nulls": nulls, "invalid_numeric": invalid_numeric,
        "duplicate_rows": int(duplicate_mask.sum()), "invalid_ohlc_rows": int(invalid_ohlc.fillna(False).sum()),
        "negative_volume_rows": int(negative_volume.fillna(False).sum()), "high_volume_flags": int(row_flags["volume_high_q3_3iqr"].sum()),
        "missing_dates_by_ticker": missing_dates, "price_unit": price_unit or "Chưa xác minh", "volume_unit": volume_unit or "Chưa xác minh",
        "comparison": comparison_result}}
