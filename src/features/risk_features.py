"""Conditional, exploratory risk features from the existing CafeF Close/Volume.

These functions never modify source frames. Outputs are research artifacts and
must not be interpreted as verified market-risk estimates until price basis and
corporate actions are established.
"""
from __future__ import annotations

import numpy as np
import pandas as pd


REQUIRED = {"Date", "Ticker", "Close", "Volume"}


def _validate(frame: pd.DataFrame) -> pd.DataFrame:
    missing = REQUIRED - set(frame.columns)
    if missing:
        raise ValueError(f"Thiếu cột bắt buộc: {', '.join(sorted(missing))}")
    data = frame[["Date", "Ticker", "Close", "Volume"]].copy()
    data["Date"] = pd.to_datetime(data["Date"], errors="coerce")
    data["Ticker"] = data["Ticker"].astype("string").str.strip().str.upper()
    data["Close"] = pd.to_numeric(data["Close"], errors="coerce")
    data["Volume"] = pd.to_numeric(data["Volume"], errors="coerce")
    if data[["Date", "Ticker", "Close", "Volume"]].isna().any().any():
        raise ValueError("Có giá trị thiếu/không hợp lệ trong Date, Ticker, Close hoặc Volume.")
    if (data["Close"] <= 0).any() or (data["Volume"] < 0).any():
        raise ValueError("Close phải dương và Volume không âm.")
    if data.duplicated(["Ticker", "Date"]).any():
        raise ValueError("Khóa Ticker + Date bị trùng; không tự xóa bản ghi.")
    return data.sort_values(["Ticker", "Date"], kind="stable").reset_index(drop=True)


def build_conditional_features(
    frame: pd.DataFrame,
    ohlc_flags: pd.DataFrame | None = None,
    rolling_window: int = 20,
    jump_threshold: float = 0.10,
) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
    """Return (main per-ticker features, sensitivity, diagnostics).

    Returns and rolling volatility are computed only across adjacent dates in
    the observed union calendar. No exchange calendar is inferred and no gaps
    are filled. Drawdown resets after gaps.
    """
    if rolling_window < 2:
        raise ValueError("rolling_window phải >= 2")
    data = _validate(frame)
    union_dates = pd.Index(sorted(data["Date"].unique()))
    date_position = {date: pos for pos, date in enumerate(union_dates)}
    flag_keys: set[tuple[str, pd.Timestamp]] = set()
    if ohlc_flags is not None and not ohlc_flags.empty:
        if not {"Ticker", "Date"}.issubset(ohlc_flags.columns):
            raise ValueError("ohlc_flags phải có Ticker và Date")
        flag_keys = {
            (str(row.Ticker).upper(), pd.Timestamp(row.Date))
            for row in ohlc_flags[["Ticker", "Date"]].itertuples(index=False)
        }

    main_rows: list[dict] = []
    sensitivity_rows: list[dict] = []
    diagnostics: dict[str, object] = {
        "input_rows": len(data), "tickers": int(data["Ticker"].nunique()),
        "union_dates": len(union_dates), "rolling_window": rolling_window,
        "jump_threshold": jump_threshold, "return_rows": 0,
        "gap_skipped_pairs": 0, "ohlc_flag_rows": len(flag_keys),
        "suspicious_jump_count": 0,
        "calendar_note": "Hợp ngày quan sát trong tệp; không phải lịch giao dịch HOSE độc lập.",
    }
    for ticker, group in data.groupby("Ticker", sort=True):
        group = group.sort_values("Date", kind="stable").reset_index(drop=True)
        pos = group["Date"].map(date_position).to_numpy()
        close = group["Close"].to_numpy(dtype=float)
        volume = group["Volume"].to_numpy(dtype=float)
        ret = np.full(len(group), np.nan)
        log_ret = np.full(len(group), np.nan)
        volume_change = np.full(len(group), np.nan)
        adjacent = np.zeros(len(group), dtype=bool)
        for i in range(1, len(group)):
            if pos[i] == pos[i - 1] + 1:
                ret[i] = close[i] / close[i - 1] - 1.0
                log_ret[i] = np.log(close[i] / close[i - 1])
                adjacent[i] = True
                if volume[i - 1] > 0:
                    volume_change[i] = volume[i] / volume[i - 1] - 1.0
            else:
                diagnostics["gap_skipped_pairs"] += 1

        # Rolling standard deviation is computed separately within each
        # contiguous observed-calendar segment.
        rolling = np.full(len(group), np.nan)
        segments: list[tuple[int, int]] = []
        start = 0
        for i in range(1, len(group)):
            if not adjacent[i]:
                segments.append((start, i))
                start = i
        segments.append((start, len(group)))
        for left, right in segments:
            segment_returns = pd.Series(ret[left:right], dtype="float64")
            rolling[left:right] = segment_returns.rolling(
                rolling_window, min_periods=rolling_window
            ).std(ddof=1).to_numpy()

        # Drawdown from Close-based cumulative returns, independently per
        # contiguous segment; avoids treating gaps as a one-session return.
        worst_drawdown = 0.0
        for left, right in segments:
            segment_ret = ret[left:right]
            valid = np.isfinite(segment_ret)
            if valid.sum() < 1:
                continue
            wealth = np.cumprod(1.0 + segment_ret[valid])
            peak = np.maximum.accumulate(np.r_[1.0, wealth])[1:]
            dd = wealth / peak - 1.0
            worst_drawdown = min(worst_drawdown, float(dd.min(initial=0.0)))

        eligible_returns = ret[np.isfinite(ret)]
        eligible_log_returns = log_ret[np.isfinite(log_ret)]
        vol = rolling[np.isfinite(rolling)]
        main = {
            "Ticker": ticker,
            "N_Observed": len(group),
            "N_Adjacent_Returns": len(eligible_returns),
            "N_Rolling_Windows": len(vol),
            "Mean_Daily_Return_Conditional": float(eligible_returns.mean()) if len(eligible_returns) else np.nan,
            "Daily_Return_Std_Conditional": float(eligible_returns.std(ddof=1)) if len(eligible_returns) > 1 else np.nan,
            "Mean_Log_Return_Conditional": float(eligible_log_returns.mean()) if len(eligible_log_returns) else np.nan,
            "Log_Return_Std_Conditional": float(eligible_log_returns.std(ddof=1)) if len(eligible_log_returns) > 1 else np.nan,
            "Rolling_Volatility_20D_Median_Conditional": float(np.median(vol)) if len(vol) else np.nan,
            "Rolling_Volatility_20D_P95_Conditional": float(np.quantile(vol, .95)) if len(vol) else np.nan,
            "Maximum_Drawdown_Close_Conditional": worst_drawdown,
            "Mean_Volume_Descriptive": float(volume.mean()),
            "Volume_CV_Descriptive": float(volume.std(ddof=1) / volume.mean()) if len(volume) > 1 and volume.mean() else 0.0,
            "Median_Absolute_Volume_Change_Descriptive": float(np.nanmedian(np.abs(volume_change))) if np.isfinite(volume_change).any() else np.nan,
        }
        main_rows.append(main)

        # Conservative sensitivity: remove only return observations touching
        # an OHLC-flagged row or a >=10% absolute close jump. Source rows remain.
        flagged_rows = np.zeros(len(group), dtype=bool)
        for i, date in enumerate(group["Date"]):
            if (ticker, pd.Timestamp(date)) in flag_keys:
                flagged_rows[i] = True
        suspicious = np.zeros(len(group), dtype=bool)
        for i in range(1, len(group)):
            # A close-to-close return touches both endpoint rows.
            suspicious[i] = flagged_rows[i] or flagged_rows[i - 1]
        for i in range(1, len(group)):
            if i > 0 and np.isfinite(ret[i]) and abs(ret[i]) >= jump_threshold:
                suspicious[i] = True
                suspicious[i - 1] = True
                diagnostics["suspicious_jump_count"] += 1
        sens_ret = ret.copy()
        sens_keep = np.isfinite(sens_ret) & ~suspicious
        sens_rolling_parts = []
        for left, right in segments:
            sens_rolling_parts.append(
                pd.Series(sens_ret[left:right]).where(sens_keep[left:right]).rolling(
                    rolling_window, min_periods=rolling_window
                ).std(ddof=1).dropna()
            )
        sens_vol = pd.concat(sens_rolling_parts) if sens_rolling_parts else pd.Series(dtype=float)
        sensitivity_rows.append({
            "Ticker": ticker,
            "N_Returns_Excluded_Sensitivity": int((np.isfinite(ret) & ~sens_keep).sum()),
            "Daily_Return_Std_Conditional_Sensitivity": float(np.std(sens_ret[sens_keep], ddof=1)) if sens_keep.sum() > 1 else np.nan,
            "Rolling_Volatility_20D_Median_Sensitivity": float(sens_vol.median()) if len(sens_vol) else np.nan,
            "Rolling_Volatility_20D_P95_Sensitivity": float(sens_vol.quantile(.95)) if len(sens_vol) else np.nan,
            "Sensitivity_Rule": "Loại khỏi tóm tắt các return chạm cờ OHLC hoặc |return| >= ngưỡng; không sửa/xóa dữ liệu nguồn.",
        })
        diagnostics["return_rows"] += len(eligible_returns)

    main_frame = pd.DataFrame(main_rows)
    sensitivity_frame = pd.DataFrame(sensitivity_rows)
    if not np.isfinite(main_frame.select_dtypes(include="number").to_numpy()).all():
        raise ValueError("Có đặc trưng số thiếu/không hữu hạn; kiểm tra độ phủ dữ liệu trước khi phân cụm.")
    return main_frame, sensitivity_frame, diagnostics
