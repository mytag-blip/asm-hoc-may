"""Read-only SSI FastConnect OHLCV adapter. This module never writes project Raw/Processed."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from os import environ
from typing import Any, Callable, Mapping
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode
from urllib.request import Request, urlopen
import json

import pandas as pd


class SSIDataError(RuntimeError):
    """Safe-to-display SSI request, authentication, or schema error."""


@dataclass(frozen=True)
class SSIConfig:
    MAX_SAFE_PAGE_SIZE = 10
    MAX_SAFE_PAGES = 500
    api_key: str
    api_secret: str
    base_url: str = "https://api.ssi.com.vn"
    timeout_seconds: float = 20.0
    page_size: int = 10
    max_pages: int = 500

    @classmethod
    def from_env(cls, env: Mapping[str, str] | None = None) -> "SSIConfig":
        values = env if env is not None else environ
        key, secret = values.get("SSI_API_KEY", "").strip(), values.get("SSI_API_SECRET", "").strip()
        if not key or not secret:
            raise SSIDataError("Thiếu SSI_API_KEY hoặc SSI_API_SECRET trong environment.")
        try:
            page_size = int(values.get("SSI_PAGE_SIZE", "10"))
            max_pages = int(values.get("SSI_MAX_PAGES", "500"))
        except ValueError as exc:
            raise SSIDataError("SSI_PAGE_SIZE và SSI_MAX_PAGES phải là số nguyên.") from exc
        if page_size < 1 or max_pages < 1:
            raise SSIDataError("SSI_PAGE_SIZE và SSI_MAX_PAGES phải lớn hơn 0.")
        if page_size > cls.MAX_SAFE_PAGE_SIZE:
            raise SSIDataError(f"SSI_PAGE_SIZE tạm giới hạn tối đa {cls.MAX_SAFE_PAGE_SIZE} cho đến khi SSI xác nhận quota.")
        if max_pages > cls.MAX_SAFE_PAGES:
            raise SSIDataError(f"SSI_MAX_PAGES tạm giới hạn tối đa {cls.MAX_SAFE_PAGES} để kiểm soát số request.")
        return cls(key, secret, page_size=page_size, max_pages=max_pages)


def _stdlib_transport(method: str, url: str, headers: Mapping[str, str], body: bytes | None, timeout: float) -> tuple[int, Mapping[str, str], bytes]:
    request = Request(url, data=body, headers=dict(headers), method=method)
    try:
        with urlopen(request, timeout=timeout) as response:
            return response.status, dict(response.headers.items()), response.read()
    except HTTPError as exc:
        return exc.code, dict(exc.headers.items()) if exc.headers else {}, exc.read()
    except URLError as exc:
        # Do not surface proxy/transport detail that could contain environment data.
        reason_type = type(exc.reason).__name__
        raise SSIDataError(f"Không kết nối được SSI (transport: {reason_type}).") from exc


class SSIClient:
    TOKEN_PATH = "/api/v3/auth/token"
    OHLC_PATH = "/api/v3/data/ohlc"

    def __init__(self, config: SSIConfig, transport: Callable = _stdlib_transport):
        self.config = config
        self._transport = transport
        self._access_token: str | None = None

    def _request_json(self, method: str, path: str, params: Mapping[str, Any] | None = None, payload: Mapping[str, Any] | None = None):
        url = self.config.base_url.rstrip("/") + path
        if params:
            url += "?" + urlencode(params)
        body = json.dumps(payload).encode() if payload is not None else None
        headers = {"Accept": "application/json", "Content-Type": "application/json"}
        if self._access_token:
            headers["Authorization"] = f"Bearer {self._access_token}"
        try:
            status, response_headers, raw = self._transport(method, url, headers, body, self.config.timeout_seconds)
        except SSIDataError:
            raise
        except Exception as exc:
            raise SSIDataError(f"Lỗi transport SSI: {type(exc).__name__}") from exc
        if status < 200 or status >= 300:
            suffix = " (rate limit 429)" if status == 429 else ""
            raise SSIDataError(f"SSI trả HTTP {status}{suffix}.")
        try:
            decoded = json.loads(raw.decode("utf-8-sig"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            raise SSIDataError("SSI trả response không phải JSON hợp lệ.") from exc
        if not isinstance(decoded, dict):
            raise SSIDataError("SSI JSON response không có dạng object.")
        return decoded, response_headers

    def authenticate(self) -> None:
        data, _ = self._request_json("POST", self.TOKEN_PATH, payload={"apiKey": self.config.api_key, "apiSecret": self.config.api_secret})
        token = data.get("accessToken")
        if not isinstance(token, str) or not token.strip():
            raise SSIDataError("SSI token response thiếu accessToken.")
        self._access_token = token

    def fetch_ohlcv(self, ticker: str, date_from: str, date_to: str) -> tuple[pd.DataFrame, dict[str, Any]]:
        if not self._access_token:
            raise SSIDataError("Chưa xác thực SSI; gọi authenticate() trước.")
        start, end = pd.Timestamp(date_from), pd.Timestamp(date_to)
        if start > end:
            raise SSIDataError("date_from phải nhỏ hơn hoặc bằng date_to.")
        symbol = ticker.strip().upper()
        if not symbol:
            raise SSIDataError("Ticker không được để trống.")
        rows: list[dict[str, Any]] = []
        seen_pages: set[str] = set()
        last_headers: Mapping[str, str] = {}
        page = 1
        while page <= self.config.max_pages:
            params = {"symbol": symbol, "from": start.strftime("%Y/%m/%d"), "to": end.strftime("%Y/%m/%d"), "timeFrame": "1d", "pageIndex": page, "pageSize": self.config.page_size}
            payload, last_headers = self._request_json("GET", self.OHLC_PATH, params=params)
            data = payload.get("data")
            if not isinstance(data, list):
                raise SSIDataError("SSI OHLC response thiếu danh sách data.")
            fingerprint = json.dumps(data, sort_keys=True, ensure_ascii=False)
            if fingerprint in seen_pages and data:
                raise SSIDataError("SSI trả lặp lại một trang; dừng để tránh vòng lặp phân trang.")
            seen_pages.add(fingerprint)
            rows.extend(data)
            page_count = payload.get("pageCount")
            if page_count is not None:
                try:
                    if page >= int(page_count):
                        break
                except (TypeError, ValueError) as exc:
                    raise SSIDataError("pageCount trong response SSI không hợp lệ.") from exc
            elif len(data) < self.config.page_size:
                break
            page += 1
        else:
            raise SSIDataError(f"Vượt quá max_pages={self.config.max_pages}; cần kiểm tra phân trang SSI.")

        frame = pd.DataFrame(rows)
        required = {"tradingDate", "open", "high", "low", "close", "volume"}
        if not frame.empty and not required.issubset(frame.columns):
            raise SSIDataError("SSI OHLC payload thiếu một hoặc nhiều trường bắt buộc.")
        if frame.empty:
            frame = pd.DataFrame(columns=["Date", "Ticker", "Open", "High", "Low", "Close", "Volume"])
        else:
            frame = frame.rename(columns={"tradingDate": "Date", "symbol": "_response_symbol", "open": "Open", "high": "High", "low": "Low", "close": "Close", "volume": "Volume"})
            frame["Date"] = pd.to_datetime(frame["Date"], errors="coerce", format="mixed")
            for col in ("Open", "High", "Low", "Close", "Volume"):
                frame[col] = pd.to_numeric(frame[col], errors="coerce")
            if frame["_response_symbol"].notna().any() and not frame.loc[frame["_response_symbol"].notna(), "_response_symbol"].astype(str).str.upper().eq(symbol).all():
                raise SSIDataError("Ticker trong response SSI khác với ticker được yêu cầu.")
            frame["Ticker"] = symbol
            frame = frame[["Date", "Ticker", "Open", "High", "Low", "Close", "Volume"]]
        retrieved_at = datetime.now(timezone.utc).isoformat()
        metadata = {"source": "SSI FastConnect", "ticker": symbol, "requested_from": start.date().isoformat(), "requested_to": end.date().isoformat(), "retrieved_at": retrieved_at, "status": "success", "error": None, "pages": page, "rate_limit_headers": {k: v for k, v in last_headers.items() if k.upper().startswith("X-RATELIMIT-")}}
        return frame, metadata
