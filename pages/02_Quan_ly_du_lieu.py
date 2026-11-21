from pathlib import Path

import pandas as pd
import streamlit as st

from src.dashboard_ui import render_empty_panel, render_page_header, render_section_heading
from src.data.stock_data import (
    CANONICAL_FIELDS,
    PLANNED_TICKERS,
    StockFileError,
    file_digest,
    read_stock_file,
    save_confirmed_copy,
    save_original_file,
    suggest_column_mapping,
    validate_stock_frame,
)


PROJECT_ROOT = Path(__file__).resolve().parents[1]
NO_COLUMN = "— Chưa chọn cột —"
USE_TICKER_SELECTION = "Không có cột mã (chọn mã bên dưới)"


def list_local_files(relative_path: str) -> list[dict[str, str | int]]:
    folder = PROJECT_ROOT / relative_path
    if not folder.exists():
        return []
    return [
        {"Tên file": path.name, "Kích thước (byte)": path.stat().st_size}
        for path in sorted(folder.iterdir(), key=lambda item: item.stat().st_mtime, reverse=True)
        if path.is_file() and not path.name.startswith(".")
    ]


render_page_header(
    "DỮ LIỆU",
    "Quản lý dữ liệu",
    "Quản lý dữ liệu OHLCV, ánh xạ cột và kiểm tra trước khi xác nhận sử dụng.",
)

render_section_heading("Nhập dữ liệu", "Hỗ trợ CSV và XLSX. File gốc được lưu nguyên byte trong data/raw/.")
uploaded_file = st.file_uploader(
    "Chọn file lịch sử giao dịch",
    type=["csv", "xlsx"],
    accept_multiple_files=False,
    help="File có thể chứa một hoặc nhiều mã nếu có cột Ticker.",
)

if uploaded_file is None:
    st.info("Chưa chọn file. Không có dữ liệu mẫu trong ứng dụng.")
else:
    content = uploaded_file.getvalue()
    digest = file_digest(content)
    st.session_state.setdefault("saved_raw_uploads", {})
    st.session_state.setdefault("confirmed_uploads", {})

    upload_key = f"{digest}:{uploaded_file.name}"
    if upload_key not in st.session_state.saved_raw_uploads:
        try:
            saved_path = save_original_file(uploaded_file.name, content, PROJECT_ROOT)
            st.session_state.saved_raw_uploads[upload_key] = str(saved_path)
        except OSError as exc:
            st.error(f"Không thể lưu file gốc vào data/raw/: {exc}")
            saved_path = None
    else:
        saved_path = Path(st.session_state.saved_raw_uploads[upload_key])

    file_columns = st.columns(3)
    file_columns[0].metric("Tên file", uploaded_file.name)
    file_columns[1].metric("Định dạng", Path(uploaded_file.name).suffix.upper().lstrip("."))
    file_columns[2].metric("Dung lượng", f"{len(content):,} byte")
    if saved_path:
        st.caption(f"Đã giữ nguyên file gốc tại: {saved_path.relative_to(PROJECT_ROOT)}")

    try:
        raw_frame = read_stock_file(uploaded_file.name, content)
    except StockFileError as exc:
        st.error(str(exc))
        raw_frame = None

    if raw_frame is not None:
        st.write(f"**Số dòng đọc được:** {len(raw_frame):,}  ·  **Số cột:** {len(raw_frame.columns)}")
        st.markdown("**Bản xem trước file gốc**")
        st.dataframe(raw_frame.head(20), hide_index=True, width="stretch")

        suggestions = suggest_column_mapping(raw_frame.columns)
        columns = [str(column) for column in raw_frame.columns]
        mapping: dict[str, str | None] = {}

        render_section_heading(
            "Ánh xạ trường dữ liệu",
            "Các tên cột chỉ được tự nhận diện khi khớp alias đã biết; trường chưa rõ cần chọn thủ công.",
        )
        mapping_columns = st.columns(2, gap="large")
        for index, field in enumerate(CANONICAL_FIELDS):
            with mapping_columns[index % 2]:
                choices = [NO_COLUMN, *columns]
                if field == "Ticker":
                    choices = [NO_COLUMN, USE_TICKER_SELECTION, *columns]
                suggestion = suggestions.get(field)
                default_choice = suggestion if suggestion in choices else NO_COLUMN
                selected = st.selectbox(
                    f"{field} — { {'Date':'Ngày giao dịch','Open':'Giá mở cửa','High':'Giá cao nhất','Low':'Giá thấp nhất','Close':'Giá đóng cửa','Volume':'Khối lượng','Ticker':'Mã cổ phiếu'}[field] }",
                    choices,
                    index=choices.index(default_choice),
                    key=f"column_map_{digest}_{field}",
                )
                if selected not in (NO_COLUMN, USE_TICKER_SELECTION):
                    mapping[field] = selected
                else:
                    mapping[field] = None

        ticker_override = None
        if mapping.get("Ticker") is None:
            ticker_choice = st.selectbox(
                "Chọn mã để gắn cho các dòng trong file",
                ["— Chọn mã cổ phiếu —", *PLANNED_TICKERS],
                key=f"ticker_override_{digest}",
            )
            if ticker_choice != "— Chọn mã cổ phiếu —":
                ticker_override = ticker_choice

        result = validate_stock_frame(raw_frame, mapping, ticker_override=ticker_override)
        render_section_heading("Kết quả kiểm tra")

        summary_columns = st.columns(4)
        summary_columns[0].metric("Tổng số dòng", f"{len(raw_frame):,}")
        summary_columns[1].metric("Mã cổ phiếu", result.ticker or "Chưa xác định")
        date_range = (
            f"{result.date_min:%Y-%m-%d} → {result.date_max:%Y-%m-%d}"
            if result.date_min is not None and result.date_max is not None
            else "Chưa xác định"
        )
        summary_columns[2].metric("Khoảng thời gian", date_range)
        summary_columns[3].metric(
            "Trạng thái",
            "Đạt kiểm tra" if result.is_valid else "Cần xử lý",
        )

        if result.errors:
            st.error("Chưa thể xác nhận dữ liệu. Sửa file nguồn hoặc ánh xạ lại các cột:")
            for issue in result.errors:
                st.markdown(f"- {issue}")
        elif not saved_path:
            st.error("Không thể xác nhận vì chưa lưu được file gốc.")
        else:
            st.success("Các kiểm tra bắt buộc đã đạt. File gốc vẫn được giữ nguyên.")
        for warning in result.warnings:
            st.warning(warning)

        if result.missing_counts:
            with st.expander("Chi tiết giá trị thiếu và kiểu dữ liệu"):
                st.dataframe(
                    pd.DataFrame(
                        {
                            "Trường": list(result.missing_counts),
                            "Giá trị thiếu": list(result.missing_counts.values()),
                            "Giá trị số không hợp lệ": [
                                result.invalid_type_counts.get(field, 0)
                                for field in result.missing_counts
                            ],
                        }
                    ),
                    hide_index=True,
                    width="stretch",
                )

        st.markdown("**Bản xem trước sau ánh xạ (không xóa dòng)**")
        st.dataframe(result.data.head(20), hide_index=True, width="stretch")

        confirmation_key = f"{digest}:{result.ticker}:{tuple(mapping.items())}"
        confirmed = st.session_state.confirmed_uploads.get(confirmation_key)
        if confirmed:
            st.success(f"Đã xác nhận bản dữ liệu: {Path(confirmed).relative_to(PROJECT_ROOT)}")
        elif result.is_valid and saved_path:
            if st.button(
                "Xác nhận dữ liệu để sử dụng",
                type="primary",
                key=f"confirm_{digest}_{result.ticker}",
                help="Lưu bản CSV đã ánh xạ vào data/processed/. File gốc không bị sửa.",
            ):
                try:
                    confirmed_path = save_confirmed_copy(
                        result.data,
                        uploaded_file.name,
                        result.ticker if result.ticker and ", " not in result.ticker else "MULTI",
                        PROJECT_ROOT,
                    )
                    st.session_state.confirmed_uploads[confirmation_key] = str(confirmed_path)
                    st.success(
                        f"Đã xác nhận dữ liệu: {confirmed_path.relative_to(PROJECT_ROOT)}"
                    )
                except OSError as exc:
                    st.error(f"Không thể lưu bản dữ liệu đã xác nhận: {exc}")

st.write("")
stored_column, confirmed_column = st.columns(2, gap="large")
with stored_column:
    render_section_heading("File gốc đã lưu", "File được giữ nguyên trong data/raw/.")
    raw_files = list_local_files("data/raw")
    if raw_files:
        st.dataframe(pd.DataFrame(raw_files), hide_index=True, width="stretch")
    else:
        render_empty_panel("Chưa có file gốc", "Tệp sẽ xuất hiện tại đây sau khi tải lên.")
with confirmed_column:
    render_section_heading("Dữ liệu đã xác nhận", "Chỉ chứa bản ánh xạ vượt qua kiểm tra bắt buộc.")
    processed_files = list_local_files("data/processed")
    if processed_files:
        st.dataframe(pd.DataFrame(processed_files), hide_index=True, width="stretch")
    else:
        render_empty_panel("Chưa có dữ liệu xác nhận", "Dữ liệu lỗi hoặc chưa đủ trường sẽ không được thêm.")

st.write("")
render_section_heading("Khám phá Processed hiện có", "Bộ lọc chỉ đọc; bảng bên dưới không thay đổi file nguồn.")
processed_path = PROJECT_ROOT / "data" / "processed" / "stock_data_processed.csv"
if processed_path.exists():
    try:
        browser = pd.read_csv(processed_path, low_memory=False)
        browser["Date"] = pd.to_datetime(browser["Date"], errors="coerce")
        ticker_options = sorted(browser["Ticker"].dropna().astype(str).unique())
        selected_tickers = st.multiselect("Lọc mã", ticker_options, default=ticker_options)
        date_min = browser["Date"].min().date()
        date_max = browser["Date"].max().date()
        date_range = st.date_input("Lọc khoảng ngày", value=(date_min, date_max), min_value=date_min, max_value=date_max)
        filtered = browser.loc[browser["Ticker"].isin(selected_tickers)]
        if isinstance(date_range, (tuple, list)) and len(date_range) == 2:
            start_date, end_date = pd.Timestamp(date_range[0]), pd.Timestamp(date_range[1])
            filtered = filtered.loc[filtered["Date"].between(start_date, end_date)]
        st.caption(f"{len(filtered):,} dòng phù hợp; hiển thị tối đa 1.000 dòng để giữ giao diện phản hồi tốt.")
        st.dataframe(filtered.head(1000), hide_index=True, width="stretch")
    except (OSError, ValueError, KeyError) as exc:
        st.error(f"Không thể hiển thị Processed: {exc}")
else:
    st.info("Chưa có stock_data_processed.csv.")




