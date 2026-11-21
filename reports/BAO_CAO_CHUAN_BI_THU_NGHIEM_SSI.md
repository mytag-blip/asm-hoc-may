# Báo cáo chuẩn bị thử nghiệm SSI FastConnect

**Ngày kiểm tra:** 20/11/2026  
**Phạm vi:** Giai đoạn 2.12, chuẩn bị kỹ thuật trước khi nhóm có credentials.  
**Kết luận ngắn:** Probe đơn mã và staging đã sẵn sàng ở mức code/fixture. Chưa có credentials nên không gọi API thật và chưa có dữ liệu SSI để đánh giá.

## 1. Những thành phần đã rà soát

- `src/data/providers/ssi.py`: cấu hình từ `SSI_API_KEY`, `SSI_API_SECRET`; lấy token qua endpoint xác thực; lấy OHLC bằng GET; chuẩn hóa Date/Ticker/OHLCV; lỗi HTTP chỉ hiện status, không hiện response body. Chi tiết transport được rút gọn để không đưa dữ liệu môi trường vào thông báo.
- `src/data/staging.py`: ghi riêng vào `data/staging/ssi/ohlcv.csv`; nhật ký từng lần thử ở `load_manifest.jsonl`; tránh bản ghi trùng theo Source/Ticker/Date nhưng vẫn giữ từng lần chạy trong manifest.
- `src/data/quality.py`: đánh dấu thiếu/null, trùng Ticker+Date, OHLC không hợp lệ, Volume âm/cờ Volume lớn; hỗ trợ lịch ngày kỳ vọng, corporate-action dates và so sánh nguồn nếu được truyền vào. Chức năng chỉ tạo cờ, không sửa dữ liệu.
- Nếu không truyền lịch phiên đã xác minh, `missing_dates_by_ticker` là `null` và probe ghi `date_gap_check.status=not_assessed`; ngày cuối tuần/ngày nghỉ không bị tự động gọi là ngày thiếu.
- `.gitignore`: loại `.env`, `.env.*` (trừ `.env.example`), `data/staging/ssi/*`; dữ liệu probe không được đưa vào Raw/Processed.
- `README.md`: hướng dẫn dùng biến môi trường và nhập credentials ẩn trong phiên PowerShell; không cần lưu key/secret vào file dự án.

## 2. Script probe

Đã tạo `scripts/ssi_probe.py` với các ràng buộc:

- Mỗi lần chạy phải có `--ticker` và chỉ chấp nhận đúng một mã trong allowlist `FPT`, `NLG`, `HPG`, `VNM`, `VIC`; allowlist được kiểm tra ở cả argparse và hàm `run()`.
- Không có chế độ batch hoặc tải tự động 43 mã.
- Khoảng mặc định `2021-11-19` đến `2026-11-18`; có thể chỉ định một khoảng khác bằng `--from-date` và `--to-date`.
- Chỉ dùng luồng xác thực và đọc OHLC; không có lệnh giao dịch.
- Ghi dữ liệu vào staging và ghi source, ticker, requested range, retrieved time, status, lỗi (nếu có), số trang và tóm tắt cờ chất lượng vào manifest.
- Tình trạng OHLC rỗng được ghi `empty`, không báo thành công có dữ liệu.
- Sau khi fetch thành công, probe đọc Processed CafeF ở chế độ chỉ đọc và so sánh các trường Date/Ticker/Open/High/Low/Close/Volume trên ngày trùng; kết quả ghi số dòng so sánh và mismatch vào manifest. Đây chỉ là đối chiếu mô tả: chưa xác minh price basis/corporate actions nên không dùng để kết luận nguồn nào tốt hơn.
- Ngày thiếu không được suy từ lịch ngày thường. Khi chưa truyền lịch phiên có bằng chứng, manifest ghi `date_gap_check.status=not_assessed`; ngày nghỉ và ngày không có bản ghi chưa thể phân biệt.
- Khi thiếu credentials, lỗi được ghi trạng thái an toàn vào manifest nếu chạy script; hiện chưa chạy probe thật hoặc tạo staging log trong dự án.
- CLI được cấu hình UTF-8 an toàn để `--help` và thông báo tiếng Việt không làm lỗi trên Windows.

Ví dụ sau chỉ minh họa cú pháp, không phải kết quả gọi API:

```powershell
python scripts/ssi_probe.py --ticker FPT
python scripts/ssi_probe.py --ticker NLG --from-date 2021-11-19 --to-date 2026-11-18
```

## 3. Phân trang và giới hạn truy vấn

- Adapter bắt đầu tại `pageIndex=1`, dùng `pageSize=10` mặc định theo tài liệu SSI đã khảo sát.
- Dừng theo `pageCount` nếu response cung cấp; nếu không, dừng khi trang trả về ít dòng hơn `pageSize`.
- Có phát hiện fingerprint trang lặp để dừng vòng lặp; cấu hình hiện chặn `SSI_PAGE_SIZE > 10` và `SSI_MAX_PAGES > 500`. Đây là ngưỡng an toàn nội bộ, không phải quota/giới hạn được SSI xác nhận.
- Rate-limit headers có tiền tố `X-RATELIMIT-` được giữ metadata. HTTP 429 được báo an toàn; adapter hiện không tự retry hoặc sleep. Không tăng page size hay tần suất trước khi SSI xác nhận giới hạn.
- Giới hạn tối đa pageSize, quota, request/minute, retry policy và phạm vi lịch sử vẫn cần xác minh với SSI hoặc bằng quyền truy cập được cấp.

## 4. Bảo vệ credentials và dữ liệu

- Không có `SSI_API_KEY`, `SSI_API_SECRET` hoặc `SSI_ACCESS_TOKEN` trong environment tại thời điểm kiểm tra (chỉ xác minh trạng thái có/không; không đọc/hiển thị giá trị).
- Không gọi API khi chưa có credentials hợp lệ. Không credentials nào được tạo hoặc lưu trong workspace.
- README khuyến nghị nhập secrets bằng `Read-Host -AsSecureString`, chuyển vào environment chỉ trong phiên hiện tại và xóa sau probe. Không đưa literal credentials vào terminal command, source code, logs, lỗi, README hoặc Git.
- Test dùng chuỗi credentials giả lập riêng và xác nhận response body có chứa chuỗi đó không xuất hiện trong lỗi hiển thị.
- Không ghi vào Raw/Processed; SHA-256 kiểm tra sau thay đổi: Raw `1B492296E31DB393DA80A8D2579887BBECB4AFB95F4F3A9FF9CECCBFB5186043`; Processed `3574059045FBD420FC0EF473FCC6671C16C3A6BDC9F57478F02A7241598FE953`.
- `D:\ASM_Hoc_May` hiện không phải Git working tree, vì vậy chưa thể kiểm tra Git index hoặc tracked-file status. `.gitignore` bỏ `.env`, `.env.*` (trừ file mẫu) và dữ liệu SSI staging; không có credential thật trong environment, credentials chưa được tạo hoặc ghi trong workspace.

## 5. Kiểm thử thực hiện

- `python -m compileall -q app.py src pages tests scripts`: đạt.
- `python -m unittest discover -s tests -v`: **28/28** đạt (fixture/mock, không gọi mạng thật).
- `python scripts/ssi_probe.py --help`: đạt sau khi sửa lỗi encoding CP1252 trên Windows.
- `python scripts/ssi_probe.py --ticker ACB`: bị argparse từ chối, exit code 2; không khởi tạo client hoặc kết nối mạng.
- Fixture kiểm tra: xác thực và phân trang; schema; phát hiện trang lặp; credentials không lộ qua lỗi; chỉ một ticker thuộc allowlist; staging idempotent và manifest; phản hồi rỗng; lỗi tải được ghi nhận; đối chiếu CafeF trên mẫu test; ngày thiếu được đánh dấu chưa đánh giá nếu thiếu calendar; Raw/Processed không được tạo trong thư mục test.
- Không có staging CSV/manifest mới trong dự án; không có SSI request thật.

## 6. Chưa được xác minh

Các mục này chỉ có thể kết luận sau khi nhóm có quyền truy cập hợp lệ, đọc điều khoản sử dụng, và nhóm cho phép chạy thử nghiệm read-only:

- API credentials hoạt động và quy trình cấp quyền thực tế.
- Runtime response, coverage của 5 mã, độ sâu lịch sử từ 2021, tổng số phiên và giới hạn truy vấn thực tế.
- Đơn vị giá/Volume, raw hay adjusted basis, cách xử lý corporate actions và việc OHLC có cùng basis.
- Lịch giao dịch/ngày thiếu và ý nghĩa phiên không có bản ghi.
- Đối chiếu với CafeF, bao gồm chênh lệch đơn vị/làm tròn/corporate actions.
- Quyền sử dụng dữ liệu trong đồ án và điều kiện lưu trữ/redistribution.

Vì vậy SSI chưa được chọn làm nguồn chính thức. Kết quả adapter và fixture không phải bằng chứng về chất lượng hay khả năng sử dụng dữ liệu SSI.

## 7. Điều kiện để bắt đầu probe thật

1. Nhóm tự đăng ký và nhận credentials SSI hợp lệ; không gửi API Secret qua chat.
2. Xác nhận quyền sử dụng dữ liệu và điều khoản phù hợp với mục đích học thuật.
3. Nhóm cho phép chạy lệnh read-only cho từng mã trong allowlist.
4. Cấu hình credentials trong process environment theo README; không commit secrets.
5. Chạy mỗi mã riêng lẻ, xem manifest và staging sau từng lượt. Không chạy batch 43 mã.
6. Trước khi xem xét dữ liệu nghiên cứu, đối chiếu số dòng/date coverage, duplicate/gap theo lịch có bằng chứng, OHLC, Volume/units, corporate actions, price basis và chênh lệch CafeF. Không tự động nhập staging vào Raw/Processed.

Feature Engineering, Daily Return/Volatility và clustering trên dữ liệu nghiên cứu vẫn chưa được thực hiện.
