from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from hashlib import sha256
from io import BytesIO
from pathlib import Path
import re
import unicodedata
import uuid
from typing import Mapping

import numpy as np
import pandas as pd

from src.data.universe import RESEARCH_TICKERS


CANONICAL_FIELDS = ("Date", "Open", "High", "Low", "Close", "Volume", "Ticker")
NUMERIC_FIELDS = ("Open", "High", "Low", "Close", "Volume")
REQUIRED_FIELDS = CANONICAL_FIELDS
# Giữ tên export cũ để không phá import hiện hữu; nội dung là universe nghiên cứu hiện tại.
PLANNED_TICKERS = RESEARCH_TICKERS

_NO_COLUMN = "— Chưa chọn cột —"
_USE_TICKER_SELECTION = "Không có cột mã (chọn mã bên dưới)"

_ALIASES = {
    "Date": {
        "date", "trading_date", "trading_day", "ngay", "ngay_giao_dich",
        "ngay_gd", "ngay_thang",
    },
    "Open": {
        "open", "opening_price", "gia_mo_cua", "mo_cua", "gia_mo",
    },
    "High": {
        "high", "highest", "highest_price", "gia_cao_nhat", "cao_nhat",
    },
    "Low": {
        "low", "lowest", "lowest_price", "gia_thap_nhat", "thap_nhat",
    },
    "Close": {
        "close", "close_price", "closing_price", "gia_dong_cua", "dong_cua",
    },
    "Volume": {
        "volume", "trading_volume", "khoi_luong", "khoi_luong_giao_dich",
        "kl_giao_dich",
    },
    "Ticker": {
        "ticker", "symbol", "stock_code", "ma_ck", "ma_co_phieu",
        "ma_chung_khoan", "ma_cp",
    },
}


class StockFileError(ValueError):
    """Lỗi đọc tệp dữ liệu cổ phiếu."""


@dataclass
class ValidationResult:
    data: pd.DataFrame
    errors: list[str]
    warnings: list[str]
    missing_counts: dict[str, int]
    invalid_type_counts: dict[str, int]
    duplicate_row_count: int
    duplicate_key_count: int
    invalid_price_count: int
    invalid_date_count: int
    ticker: str | None
    date_min: pd.Timestamp | None
    date_max: pd.Timestamp | None

    @property
    def is_valid(self) -> bool:
        return not self.errors


def _normalize_label(label: object) -> str:
    text = str(label).strip().replace("đ", "d").replace("Đ", "D")
    text = unicodedata.normalize("NFKD", text)
    text = "".join(char for char in text if not unicodedata.combining(char))
    return re.sub(r"[^a-zA-Z0-9]+", "_", text).strip("_").lower()


def suggest_column_mapping(columns: list[object] | pd.Index) -> dict[str, str]:
    """Gợi ý ánh xạ theo tên cột trùng chính xác alias đã biết; không đoán gần đúng."""
    by_normalized: dict[str, list[str]] = {}
    for column in columns:
        by_normalized.setdefault(_normalize_label(column), []).append(str(column))

    suggestions: dict[str, str] = {}
    used_sources: set[str] = set()
    for canonical, aliases in _ALIASES.items():
        matches = [
            source
            for alias in aliases
            for source in by_normalized.get(_normalize_label(alias), [])
        ]
        unique_matches = list(dict.fromkeys(matches))
        if len(unique_matches) == 1 and unique_matches[0] not in used_sources:
            suggestions[canonical] = unique_matches[0]
            used_sources.add(unique_matches[0])
    return suggestions


def read_stock_file(filename: str, content: bytes) -> pd.DataFrame:
    """Đọc CSV/XLSX vào bộ nhớ; không sửa file gốc đã tải lên."""
    if not content:
        raise StockFileError("File rỗng, không có dữ liệu để đọc.")

    suffix = Path(filename).suffix.lower()
    try:
        if suffix == ".csv":
            frame: pd.DataFrame | None = None
            decode_errors: list[str] = []
            for encoding in ("utf-8-sig", "utf-8", "cp1258"):
                try:
                    frame = pd.read_csv(BytesIO(content), encoding=encoding, sep=None, engine="python")
                    break
                except UnicodeDecodeError as exc:
                    decode_errors.append(str(exc))
                except pd.errors.EmptyDataError as exc:
                    raise StockFileError("File CSV không có tiêu đề hoặc dữ liệu.") from exc
                except pd.errors.ParserError as exc:
                    raise StockFileError(f"Không thể phân tích cấu trúc CSV: {exc}") from exc
            if frame is None:
                raise StockFileError(
                    "Không đọc được bảng mã CSV. Hãy xuất lại file dưới dạng UTF-8 từ Vietstock."
                )
        elif suffix == ".xlsx":
            try:
                frame = pd.read_excel(BytesIO(content), sheet_name=0, engine="openpyxl")
            except ImportError as exc:
                raise StockFileError("Thiếu openpyxl để đọc XLSX. Cài các thư viện trong requirements.txt.") from exc
            except Exception as exc:
                raise StockFileError(f"Không thể đọc sheet đầu tiên của file XLSX: {exc}") from exc
        else:
            raise StockFileError("Chỉ hỗ trợ file CSV hoặc XLSX.")

        if frame is None or frame.empty:
            raise StockFileError("File không có dòng dữ liệu.")
        frame.columns = [str(column).strip() for column in frame.columns]
        return frame
    except StockFileError:
        raise
    except Exception as exc:
        raise StockFileError(f"Không thể đọc file: {exc}") from exc


def validate_stock_frame(
    raw_frame: pd.DataFrame,
    column_mapping: Mapping[str, str | None],
    ticker_override: str | None = None,
) -> ValidationResult:
    """Tạo bản chuẩn hóa để kiểm tra; không xóa hoặc ghi lại dòng của raw_frame."""
    errors: list[str] = []
    warnings: list[str] = []
    invalid_type_counts: dict[str, int] = {}
    missing_counts: dict[str, int] = {}

    if raw_frame.empty:
        empty = pd.DataFrame(columns=CANONICAL_FIELDS)
        return ValidationResult(
            empty, ["File không có dòng dữ liệu."], [], {}, {}, 0, 0, 0, 0, None, None, None
        )

    mapped: dict[str, str | None] = {}
    for field in CANONICAL_FIELDS:
        source = column_mapping.get(field)
        if source is not None and source not in raw_frame.columns:
            errors.append(f"Cột nguồn được chọn cho {field} không tồn tại trong file.")
            source = None
        mapped[field] = source

    selected_sources = [source for source in mapped.values() if source is not None]
    if len(selected_sources) != len(set(selected_sources)):
        errors.append("Một cột nguồn không thể được dùng cho nhiều trường chuẩn.")

    for field in CANONICAL_FIELDS:
        if mapped[field] is None and not (field == "Ticker" and ticker_override):
            errors.append(f"Chưa ánh xạ được cột bắt buộc {field}.")

    data = pd.DataFrame(index=raw_frame.index)
    for field in CANONICAL_FIELDS:
        source = mapped[field]
        if source is not None:
            data[field] = raw_frame[source].copy()

    for field in CANONICAL_FIELDS:
        if field in data:
            values = data[field]
            if values.dtype == object or pd.api.types.is_string_dtype(values.dtype):
                values = values.replace(r"^\s*$", pd.NA, regex=True)
            missing_counts[field] = int(values.isna().sum())
            data[field] = values

    if "Date" in data:
        original_dates = data["Date"]
        parsed_dates = pd.to_datetime(original_dates, format="mixed", errors="coerce", dayfirst=True)
        invalid_date_count = int((original_dates.notna() & parsed_dates.isna()).sum())
        data["Date"] = parsed_dates
    else:
        invalid_date_count = 0

    for field in NUMERIC_FIELDS:
        if field not in data:
            continue
        source_values = data[field]
        numeric_values = pd.to_numeric(source_values, errors="coerce")
        invalid_type_counts[field] = int((source_values.notna() & numeric_values.isna()).sum())
        data[field] = numeric_values

    ticker_source = mapped["Ticker"]
    if ticker_source is None and ticker_override:
        data["Ticker"] = str(ticker_override).strip().upper()
    elif "Ticker" in data:
        data["Ticker"] = (
            data["Ticker"].astype("string").str.strip().str.upper().replace("", pd.NA)
        )

    for field, count in missing_counts.items():
        if count:
            errors.append(f"Cột {field} có {count} giá trị thiếu.")
    if invalid_date_count:
        errors.append(f"Có {invalid_date_count} giá trị ngày không hợp lệ.")
    for field, count in invalid_type_counts.items():
        if count:
            errors.append(f"Cột {field} có {count} giá trị không chuyển được sang số.")

    if "Ticker" in data:
        ticker_values = data["Ticker"].dropna().unique().tolist()
        ticker_values = sorted(str(value) for value in ticker_values)
        ticker = ", ".join(ticker_values) if ticker_values else None
        if not ticker_values:
            errors.append("Không xác định được mã cổ phiếu.")
        else:
            outside_scope = [value for value in ticker_values if value not in PLANNED_TICKERS]
            if outside_scope:
                warnings.append(
                    "Mã ngoài danh sách 43 mã nghiên cứu hiện tại: " + ", ".join(outside_scope) + "."
                )
    else:
        ticker = str(ticker_override).strip().upper() if ticker_override else None

    missing_total = sum(missing_counts.values())
    if missing_total and not any("giá trị thiếu" in issue for issue in errors):
        errors.append(f"Có {missing_total} giá trị thiếu trong các cột bắt buộc.")

    duplicate_row_count = 0
    duplicate_key_count = 0
    if all(field in data for field in CANONICAL_FIELDS):
        duplicate_row_count = int(data.duplicated(subset=list(CANONICAL_FIELDS), keep=False).sum())
        duplicate_key_count = int(data.duplicated(subset=["Ticker", "Date"], keep=False).sum())
        if duplicate_key_count:
            errors.append(
                f"Có {duplicate_key_count} dòng thuộc khóa mã cổ phiếu/ngày bị trùng; "
                "không dòng nào bị tự động xóa."
            )

    invalid_price_count = 0
    if all(field in data for field in NUMERIC_FIELDS):
        prices = data[["Open", "High", "Low", "Close"]]
        infinite_rows = pd.Series(False, index=data.index)
        for field in NUMERIC_FIELDS:
            infinite_rows |= np.isinf(data[field]).fillna(False)
        invalid_rows = (
            infinite_rows
            | (prices <= 0).any(axis=1)
            | (data["Volume"] < 0)
            | (data["Low"] > data["High"])
            | (data["Low"] > data["Open"])
            | (data["Low"] > data["Close"])
            | (data["High"] < data["Open"])
            | (data["High"] < data["Close"])
        )
        invalid_price_count = int(invalid_rows.fillna(False).sum())
        if invalid_price_count:
            errors.append(
                f"Có {invalid_price_count} dòng vi phạm quy tắc giá OHLC dương/thứ tự High-Low "
                "hoặc Volume không âm."
            )

    if duplicate_row_count and not duplicate_key_count:
        warnings.append(
            f"Có {duplicate_row_count} dòng trùng hoàn toàn; cần kiểm tra nguồn trước khi xác nhận."
        )
        errors.append(
            f"Có {duplicate_row_count} dòng trùng hoàn toàn; không dòng nào bị tự động xóa."
        )

    valid_dates = data["Date"].dropna() if "Date" in data else pd.Series(dtype="datetime64[ns]")
    date_min = pd.Timestamp(valid_dates.min()) if not valid_dates.empty else None
    date_max = pd.Timestamp(valid_dates.max()) if not valid_dates.empty else None
    if len(valid_dates) > 1 and not valid_dates.is_monotonic_increasing:
        warnings.append("Ngày trong file chưa sắp xếp tăng dần; thứ tự dòng gốc được giữ nguyên.")

    return ValidationResult(
        data=data.loc[:, [field for field in CANONICAL_FIELDS if field in data]],
        errors=list(dict.fromkeys(errors)),
        warnings=warnings,
        missing_counts=missing_counts,
        invalid_type_counts=invalid_type_counts,
        duplicate_row_count=duplicate_row_count,
        duplicate_key_count=duplicate_key_count,
        invalid_price_count=invalid_price_count,
        invalid_date_count=invalid_date_count,
        ticker=ticker,
        date_min=date_min,
        date_max=date_max,
    )


def _safe_stem(filename: str) -> str:
    stem = Path(filename).stem.strip()
    stem = re.sub(r"[^\w.-]+", "_", stem, flags=re.UNICODE).strip("._")
    return stem[:80] or "vietstock_data"


def _unique_path(directory: Path, stem: str, suffix: str) -> Path:
    directory.mkdir(parents=True, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
    return directory / f"{stem}_{timestamp}_{uuid.uuid4().hex[:8]}{suffix}"


def save_original_file(
    filename: str,
    content: bytes,
    project_root: str | Path,
) -> Path:
    """Lưu nguyên byte file gốc dưới tên mới, không ghi đè file hiện có."""
    root = Path(project_root)
    suffix = Path(filename).suffix.lower()
    target = _unique_path(root / "data" / "raw", _safe_stem(filename), suffix)
    with target.open("xb") as output:
        output.write(content)
    return target


def save_confirmed_copy(
    frame: pd.DataFrame,
    source_filename: str,
    ticker: str,
    project_root: str | Path,
) -> Path:
    """Lưu bản CSV đã ánh xạ/kiểm tra riêng; không sửa hoặc ghi đè file raw."""
    root = Path(project_root)
    safe_ticker = re.sub(r"[^A-Z0-9_-]", "", ticker.upper()) or "UNKNOWN"
    target = _unique_path(
        root / "data" / "processed",
        f"{_safe_stem(source_filename)}_{safe_ticker}_validated",
        ".csv",
    )
    csv_content = frame.to_csv(index=False, encoding="utf-8-sig")
    with target.open("x", encoding="utf-8-sig", newline="") as output:
        output.write(csv_content)
    return target


def file_digest(content: bytes) -> str:
    return sha256(content).hexdigest()





