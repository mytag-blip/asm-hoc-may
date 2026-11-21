# Kế hoạch tích hợp SSI FastConnect API

**Trạng thái:** Kế hoạch; chưa triển khai, chưa gọi API, chưa đăng ký hoặc tạo credentials.  
**Ngày:** 18/11/2026

## 1. Quyết định và phạm vi

- Theo xác nhận mới nhất của người dùng, giảng viên đã đồng ý dùng nguồn ngoài Vietstock; SSI FastConnect là nguồn chính, DNSE dự phòng.
- Chỉ triển khai luồng lấy dữ liệu thị trường OHLCV; không bật chức năng đặt/sửa/hủy lệnh, không cần API trading scope.
- Mã dự kiến: ACB, BID, CTG, MBB, TCB, VCB, VPB, STB, HDB, SHB.
- Khoảng ngày: người dùng chọn 2 hoặc 3 năm; ưu tiên lấy một mã ACB trong bước xác minh trước khi chạy batch 10 mã.
- Schema chuẩn cuối: `Date, Ticker, Open, High, Low, Close, Volume`.
- Upload CSV/XLSX đang có vẫn được giữ làm phương án dự phòng và không bị thay thế.

## 2. Vị trí tích hợp trong cấu trúc hiện tại

Đã kiểm tra:

- `src/data/stock_data.py`: định nghĩa `CANONICAL_FIELDS`, danh sách mã, đọc CSV/XLSX, gợi ý ánh xạ, `validate_stock_frame`, lưu file gốc bằng `save_original_file`, lưu bản hợp lệ bằng `save_confirmed_copy`.
- `pages/02_Quan_ly_du_lieu.py`: hiện có uploader, xem trước, ánh xạ cột, validation, xác nhận và hiển thị file raw/processed.
- `requirements.txt`: hiện không có `requests` hoặc `httpx`; các thư viện đang khai báo gồm Streamlit, Pandas, NumPy, Matplotlib, Seaborn, Scikit-learn, openpyxl.
- Không có HTTP client hoặc collector API trong `src/data/` hiện tại.

Đề xuất khi được phép triển khai:

1. Thêm `src/data/ssi_client.py` làm client riêng: cấu hình endpoint, lấy/refresh token, gọi OHLC, phân trang, xử lý lỗi và chuẩn hóa response.
2. Giữ `src/data/stock_data.py` làm validator/lưu trữ dùng chung; chỉ bổ sung hàm nếu có thiếu sót xác định được, không viết lại luồng nhập file.
3. Mở rộng `pages/02_Quan_ly_du_lieu.py` bằng hai lựa chọn trong cùng trang: “Tải file CSV/XLSX” đang có và “Lấy dữ liệu SSI”. Form SSI cho phép chọn mã, ngày bắt đầu/kết thúc và trạng thái tiến trình.
4. Ghi response gốc để truy vết dưới `data/raw/ssi/`; chỉ lưu bảng chuẩn hóa vào `data/processed/` sau khi qua validation. File upload cũ không thay đổi.
5. Không cần FastAPI, database, queue worker hoặc thư viện ML mới cho client này. Có thể dùng `urllib.request` của Python chuẩn; nếu chọn thư viện HTTP ngoài thì chỉ bổ sung sau khi thống nhất và cập nhật `requirements.txt` ở giai đoạn triển khai.

## 3. Luồng tích hợp theo giai đoạn

### Giai đoạn 0 — Chuẩn bị quyền và cấu hình

- Người dùng hoàn tất tài khoản giao dịch SSI và đăng ký FastConnect.
- Tạo một API Key riêng cho dự án ASM, chỉ dùng Market Data nếu portal hỗ trợ lựa chọn quyền.
- Lưu API Key/Secret tại máy chạy ứng dụng bằng biến môi trường hoặc Streamlit Secrets; không ghi vào source, Git, log hoặc chat.
- Xác nhận với SSI điều khoản dùng/lưu dữ liệu cho bài tập, báo cáo và chia sẻ nội bộ. API miễn phí (nếu áp dụng) không tự đồng nghĩa quyền tái phân phối dữ liệu.

### Giai đoạn 1 — Kiểm tra kết nối an toàn bằng ACB

1. Lấy token với `POST /api/v3/auth/token` bằng API Key/Secret; không truyền OTP vì chỉ yêu cầu quyền truy vấn dữ liệu theo tài liệu SSI.
2. Gọi dữ liệu ngày ACB trong khoảng ngắn (ví dụ 1 tháng), page size nhỏ ban đầu. Chưa chạy toàn bộ 2–3 năm hoặc 10 mã.
3. Xác minh response thực là JSON hợp lệ và có dữ liệu `data[]`; kiểm tra ngày, số và OHLC/volume hợp lý. HTTP 200 đơn lẻ không được coi là thành công.
4. Kiểm tra định dạng `from/to` thực tế. Reference ghi `YYYY/MM/DD` còn Quick Start minh họa `YYYY-MM-DD`; chỉ chốt định dạng sau request được cấp quyền thành công.
5. Kiểm tra page size tối đa được API chấp nhận. Reference mô tả metadata `pageIndex`, Quick Start có thêm `pageNumber/pageCount/itemsCount`; client cần đọc metadata thực tế và xử lý tương thích có kiểm soát.
6. Ghi raw response ACB và bản chuẩn hóa sau validation; báo cáo số dòng, cột, ngày đầu/cuối, kiểu dữ liệu và lỗi/warning.

### Giai đoạn 2 — ACB đủ 2–3 năm

1. Chọn ngày bắt đầu (2 hoặc 3 năm trước) và ngày kết thúc; chỉ dùng `timeFrame=1d`.
2. Tải tuần tự từng trang bằng `pageIndex=1...`; giữ `pageSize` ở mức API đã xác nhận. Ưu tiên metadata `pageCount`/số bản ghi nếu có; nếu thiếu, dừng an toàn khi trang rỗng hoặc không tiến triển, với trần trang cấu hình được để tránh vòng lặp vô hạn.
3. Gắn ticker `ACB`, chuyển ngày về kiểu ngày thống nhất và ép Open/High/Low/Close/Volume thành số; không làm tròn hay điều chỉnh giá trong bước lấy dữ liệu.
4. Xác minh đủ khoảng ngày, dữ liệu có giao dịch, không thiếu trường bắt buộc, giá và volume đúng kiểu, thứ tự OHLC hợp lệ. Không tạo hàng cho ngày nghỉ/không giao dịch.
5. Dùng `validate_stock_frame` trước khi lưu bản processed; file raw giữ nguyên response và provenance (provider, mã, tham số truy vấn, thời điểm lấy, số trang).

### Giai đoạn 3 — Mở rộng 10 mã

1. Sau khi ACB đủ thời gian và validation đạt, chạy tuần tự theo danh sách mã đã thống nhất.
2. Hiển thị tiến độ theo mã/trang, ngày, số dòng nhận, retry và trạng thái hoàn tất/lỗi. Một mã lỗi phải được báo rõ; không gộp trạng thái một phần thành “đã tải thành công toàn bộ”.
3. Tạo bản tổng hợp chuẩn chỉ khi từng mã có đủ dữ liệu và không có xung đột khóa `(Ticker, Date)`.
4. Tổng hợp khoảng ngày và số phiên riêng cho từng mã. Không giả định tất cả mã bắt đầu giao dịch cùng ngày.

## 4. Phân trang, lỗi, trùng lặp và rate limit

### Phân trang

- Mỗi ticker/range là một chuỗi page riêng; tăng `pageIndex` đúng một lần sau response thành công.
- Không giả định `pageSize` không giới hạn. Dùng giá trị đã thử và được SSI chấp nhận; nếu metadata phiên bản response không thống nhất, lưu payload, dừng khi cấu trúc lạ và báo lỗi thay vì đoán.
- Kiểm tra tiến triển: không nhận liên tiếp cùng trang/không tăng số ngày mới; áp dụng giới hạn số trang an toàn.
- Lưu tiến độ theo ticker/page để có thể tiếp tục sau lỗi mà không gọi lại vô ích; khi resume phải phát hiện overlap trước khi merge.

### Xử lý lỗi

- Timeout/kết nối và HTTP 5xx: retry hữu hạn với exponential backoff và jitter.
- HTTP 401: thử refresh access token một lần rồi lặp request một lần; nếu tiếp tục lỗi, dừng và yêu cầu người dùng kiểm tra trạng thái key/quyền.
- HTTP 400: không retry mù; hiển thị thông tin lỗi đã loại bỏ dữ liệu nhạy cảm và kiểm tra symbol, format ngày, timeframe, page parameters.
- HTTP 403: dừng; có thể là quyền hoặc quota, không tiếp tục spam request.
- HTTP 429: đọc `X-RATELIMIT-RESET`/header liên quan nếu có, chờ đến thời điểm reset, áp dụng giới hạn retry; không lặp request liên tục.
- Lỗi schema/JSON, dữ liệu rỗng bất thường hoặc giá không hợp lệ: giữ raw response, đánh dấu mã/trang lỗi và không đưa vào processed.
- Không log API Secret, access/refresh token hoặc header Authorization.

### Dữ liệu trùng và xung đột

- Khóa logic là `(Ticker, Date)`.
- Dòng trùng đúng hoàn toàn do giao trang có thể được nhận diện trong bước hợp nhất, ghi số lượng và trang nguồn; chỉ gộp một dòng vào processed nếu các giá trị của bản ghi giống hệt nhau.
- Nếu cùng mã/ngày có giá hoặc volume khác nhau, không chọn ngẫu nhiên và không ghi đè; giữ raw, đánh dấu lỗi và yêu cầu kiểm tra nguồn.
- Dùng validation hiện có để chặn khóa trùng trước khi xác nhận processed. Raw không bị sửa/xóa.

### Giới hạn truy vấn

- SSI cung cấp `X-RATELIMIT-LIMIT`, `X-RATELIMIT-REMAINING`, `X-RATELIMIT-RESET`; quota phụ thuộc key/endpoint và phải đọc từ response, không hard-code số suy đoán.
- Tải tuần tự cho 10 mã ở lần đầu; chỉ tăng concurrency nếu SSI xác nhận phù hợp và header/quota cho phép.
- Cache/token trong bộ nhớ theo thời hạn; tránh xin token cho từng trang. Không truy vấn lại mã/range đã có nếu người dùng không yêu cầu refresh.

## 5. Mapping và tiêu chí chấp nhận dữ liệu

| SSI response | Chuẩn ASM |
|---|---|
| `tradingDate` | `Date` |
| `symbol` hoặc ticker của request sau khi kiểm tra khớp | `Ticker` |
| `open` | `Open` |
| `high` | `High` |
| `low` | `Low` |
| `close` | `Close` |
| `volume` | `Volume` |

Một ticker chỉ được đánh dấu đạt khi có dữ liệu thực nhận, khoảng ngày thực tế được báo rõ, đủ bảy cột, trường số/ngày chuyển đổi được, không có giá trị thiếu hoặc mâu thuẫn OHLC, và khóa `(Ticker, Date)` duy nhất sau xử lý overlap có log. Không bù ngày không giao dịch. Cần ghi rõ đơn vị giá/volume và tình trạng điều chỉnh giá khi xác minh được từ SSI; nếu chưa rõ, lưu thành điểm cần hỏi và không gán diễn giải chắc chắn.

## 6. Trình tự kiểm thử khi bước triển khai được xác nhận

1. Kiểm tra thiếu/sai credential mà không lộ giá trị trong thông báo.
2. ACB, phạm vi ngắn: token → một trang OHLC → schema và mapping.
3. ACB, 2–3 năm: pagination, số trang, khoảng ngày, duplicate/missing/price checks.
4. Một ticker có chuỗi dài/ngày đầu muộn khác (ví dụ HDB) để đảm bảo không giả định độ phủ đồng đều.
5. Batch 10 mã tuần tự, mô phỏng các mã có lỗi, 401, 429, timeout và trang lặp bằng fixture test; không dùng dữ liệu test như dữ liệu ASM.
6. So sánh số phiên và giá ngẫu nhiên với màn hình/tài liệu SSI nếu người dùng có quyền xem, ghi nguồn đối chiếu.
7. Sau khi dữ liệu được xác nhận, mới chuyển vào EDA/Feature Engineering; giữ 20 phiên cuối tách biệt khỏi train/tuning theo yêu cầu ASM.

## 7. Việc người dùng cần làm để đăng ký và chuẩn bị quyền SSI

1. Có hoặc mở **tài khoản giao dịch SSI đang hoạt động**.
2. Đăng ký/được kích hoạt FastConnect API và chấp thuận điều khoản dịch vụ. Trang Terms nói đăng ký qua Developer Portal và cần được duyệt; trang Registration hiện vẫn hướng dẫn liên hệ SSI/đến chi nhánh. Do tài liệu chính thức chưa nhất quán, hãy đăng nhập Developer Portal kiểm tra luồng hiện tại; nếu không thấy đăng ký, gọi hotline SSI **1900 5454 71** hoặc hỏi chi nhánh về kích hoạt FastConnect. Trang Registration nêu thời gian xác nhận qua email 2–4 giờ làm việc sau khi đăng ký theo quy trình đó.
3. Hoàn thành hợp đồng/điều khoản và xác minh tài khoản theo hướng dẫn SSI hiện hành.
4. Đăng nhập [SSI Developer Portal](https://developers.ssi.com.vn), vào **Dashboard → API Key Management → Create New Key**. Đặt tên dễ nhận diện, ví dụ `ASM-Market-Data`; nếu có cấu hình scope, chỉ bật Market Data/read-only, không bật quyền giao dịch.
5. Lưu API Key và API Secret tại máy sẽ chạy ứng dụng. SSI ghi API Secret chỉ hiển thị một lần; lưu ngay vào nơi an toàn.
6. Kiểm tra với SSI rằng FastConnect hiện được cung cấp không thu phí API theo thông tin FAQ, đồng thời hỏi riêng điều khoản sử dụng dữ liệu lịch sử cho bài tập, báo cáo và chia sẻ nội bộ.
7. Không gửi API Key/Secret, token hoặc OTP trong chat. Khi sẵn sàng cho giai đoạn tích hợp, chỉ cần báo “đã kích hoạt” và chuẩn bị cấu hình credentials cục bộ. Nếu cần hỗ trợ debug, chia sẻ HTTP status/thông báo đã che mọi token/key.

**Thông tin cần có trước khi bắt đầu coding:** FastConnect đã active; quyền truy cập Market Data; xác nhận điều khoản sử dụng; API Key/Secret đã lưu cục bộ (không cần gửi cho trợ lý); ngày bắt đầu muốn lấy (2 hay 3 năm); và xác nhận chấp nhận việc client thực hiện request chỉ đọc.

## 8. Giả định, rủi ro và điểm cần xác minh

- Tài liệu SSI nói dữ liệu ngày có từ ngày mã bắt đầu giao dịch; chưa thực hiện request để chứng minh 10 mã trả đủ dữ liệu trong tài khoản cụ thể.
- Trang OHLC reference ghi `YYYY/MM/DD`, Quick Start dùng `YYYY-MM-DD`; kiểm thử ACB nhỏ sẽ chốt cách gọi.
- Reference response minh họa `pageIndex`; Quick Start minh họa `pageNumber/pageCount/itemsCount`; cần code tolerant có giới hạn và ghi schema thực tế.
- `pageSize` mặc định 10; mức tối đa chưa được tài liệu xác nhận.
- Tài liệu nói API FastConnect không thu phí ở FAQ hiện hành, nhưng mức phí/quyền sử dụng dữ liệu thị trường và tái phân phối phải được SSI xác nhận.
- Trang Terms và Registration đưa ra quy trình onboarding khác nhau; người dùng cần theo portal/hotline hiện hành.
- Giá đã điều chỉnh hay chưa, đơn vị giá/volume, timezone, corporate action và chính sách lưu trữ chưa được xác minh bằng API response.
- Credentials có rủi ro bị lộ; không ghi log, không commit, không dùng chung key trên môi trường công khai. Dùng secret cục bộ; nếu triển khai app trên hosting phải cấu hình secrets trong nền tảng đó.
- User đã xác nhận giảng viên cho phép đổi khỏi Vietstock; quyết định này là điều kiện đầu vào của kế hoạch. Dữ liệu vẫn phải được ghi nguồn SSI rõ ràng trong CSV/report.

## 9. Tài liệu SSI chính thức tham khảo

- [FastConnect data-ohlc](https://developers.ssi.com.vn/en/docs/api-reference/data-ohlc)
- [Getting API Keys / Access Tokens](https://developers.ssi.com.vn/en/docs/getting-started/api-keys)
- [Terms of Use & Environments](https://developers.ssi.com.vn/en/docs/getting-started/terms-and-environments)
- [Registration and Activation Process](https://developers.ssi.com.vn/en/docs/getting-started/registration)
- [FastConnect FAQ / Service Overview](https://developers.ssi.com.vn/en/docs/faq/service-overview)
- [Quick Start](https://developers.ssi.com.vn/en/docs/getting-started/first-api-call)

**Chưa gọi API thật. Kế hoạch này không thay đổi code, dependency hoặc cấu trúc thư mục. Chỉ bắt đầu triển khai sau yêu cầu/đồng ý ở bước tiếp theo.**
