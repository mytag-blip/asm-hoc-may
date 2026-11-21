# Nghiên cứu nguồn dữ liệu OHLCV: SSI FastConnect và DNSE OpenAPI

**Ngày nghiên cứu:** 18/11/2026  
**Phạm vi:** Đọc tài liệu chính thức và cấu trúc module ASM; không gọi API thật, không đăng ký dịch vụ, không tạo credential và không thay đổi code.

## 1. Bối cảnh dự án ASM hiện tại

Các tài liệu dự án đặt nguồn dữ liệu theo yêu cầu ASM là Vietstock. PDF/báo cáo phân tích cũng mô tả dữ liệu Vietstock CSV/XLSX; dự án hiện nhập file thủ công. Vì vậy SSI và DNSE có thể được nghiên cứu như lựa chọn kỹ thuật, nhưng thay nguồn dữ liệu bắt buộc trong bài nộp cần được giảng viên chấp thuận trước.

Đã đọc `PROJECT_CONTEXT.md`, `PROJECT_PROGRESS.md`, `CHANGELOG.md` và `BAO_CAO_PHAN_TICH.md`; đã kiểm tra cây file ứng dụng và mở `src/data/stock_data.py`, `pages/02_Quan_ly_du_lieu.py`. Module hiện có đọc CSV/XLSX, ánh xạ cột, kiểm tra dữ liệu, lưu file raw và bản xác nhận processed. Không thấy HTTP client, API credentials, crawler hoặc tích hợp SSI/DNSE. Thư mục `data/raw/` hiện chỉ có `.gitkeep`.

## 2. SSI FastConnect API

### 2.1 OHLCV endpoint và schema theo tài liệu

- Endpoint: `GET https://api.ssi.com.vn/api/v3/data/ohlc`.
- Query bắt buộc: `symbol`, `from`, `to`.
- Query tùy chọn: `timeFrame` (`1m`, `3m`, `5m`, `15m`, `30m`, `1h`, `1d`; mặc định `1d`), `pageIndex` (bắt đầu từ 1, mặc định 1), `pageSize` (mặc định 10).
- Xác thực: `Authorization: Bearer <JWT>` và `Content-Type: application/json`.
- Response thành công là JSON có `data[]`; mỗi bản ghi gồm `symbol`, `tradingDate`, `open`, `high`, `low`, `close`, `volume`, `value`. Các giá trị trong ví dụ schema là chuỗi; cần ép kiểu và kiểm tra khi tích hợp.
- Ánh xạ ASM: `tradingDate` → Date; `symbol` → Ticker; `open/high/low/close/volume` → các trường tương ứng. `value` là trường bổ sung, không bắt buộc cho ASM.
- Tài liệu endpoint nêu OHLCV ngày có sẵn từ ngày mã bắt đầu giao dịch; intraday chỉ trong năm gần nhất. Điều này phù hợp về lý thuyết với cửa sổ 2–3 năm cho các mã đã giao dịch đủ lâu.
- Phân trang có `pageIndex`/`pageSize`; tài liệu API trả các metadata phân trang. Mặc định 10 bản ghi/trang; giới hạn `pageSize` tối đa chưa thấy nêu trong tài liệu đã đọc.
- `from`/`to`: endpoint reference ghi định dạng ngày `YYYY/MM/DD` cho dữ liệu ngày; Quick Start lại dùng ví dụ `YYYY-MM-DD`. Đây là khác biệt tài liệu cần kiểm tra bằng một request được cấp phép trước khi chốt client.

### 2.2 Đăng ký và xác thực theo tài liệu

1. Cần tài khoản giao dịch SSI đang hoạt động, đăng ký/được kích hoạt FastConnect qua Developer Portal và chấp thuận điều khoản. Tài liệu FAQ hiện hành mô tả tạo tài khoản developer, chấp thuận điều khoản, tạo API Key và chọn môi trường trực tuyến; trang registration khác vẫn đề cập liên hệ/đến chi nhánh. Quy trình hiện hành vì vậy nên được xác nhận trong portal hoặc trực tiếp với SSI.
2. Tạo API Key; API Secret chỉ hiển thị một lần theo trang tạo khóa.
3. Gọi `POST https://api.ssi.com.vn/api/v3/auth/token` với JSON `{apiKey, apiSecret}` để lấy `accessToken` và `refreshToken`.
4. Gọi OHLCV với Bearer access token; refresh token khi cần theo endpoint refresh.
5. Tài liệu nói OTP không cần nếu token chỉ dùng truy vấn dữ liệu; OTP áp dụng khi cần token có quyền giao dịch. Tích hợp ASM chỉ cần Market Data read-only.

Không có key/token nào được tạo hoặc thử trong nghiên cứu này.

### 2.3 Rate limit, chi phí và điều kiện

- SSI công bố rate limit theo API Key/endpoint; response có `X-RATELIMIT-LIMIT`, `X-RATELIMIT-REMAINING`, `X-RATELIMIT-RESET`; vượt giới hạn trả HTTP 429. Quota cụ thể không được nêu cố định ở trang OHLC mà được trả qua header.
- FAQ FastConnect được đọc trong lần nghiên cứu này nói SSI hiện không thu phí cho dịch vụ FastConnect. Đây là thông tin dịch vụ API, không đủ để kết luận mọi quyền sử dụng/khai thác dữ liệu thị trường đều miễn phí hoặc cho phép tái phân phối.
- Tài liệu yêu cầu bảo vệ API Key/Secret/token và tuân thủ điều khoản, rate limit, quy định chứng khoán.

## 3. DNSE OpenAPI

### 3.1 OHLC endpoint và schema theo tài liệu

- Endpoint: `GET https://openapi.dnse.com.vn/price/ohlc`.
- Query bắt buộc: `symbol` (ví dụ ACB), `resolution` (`1`, `3`, `5`, `15`, `30`, `1H`, `1D`, `1W`), `from`, `to` (Unix timestamp giây). `type` xác định thị trường, ví dụ `STOCK`.
- Header endpoint yêu cầu: `X-API-Key`, `X-Aux-Date`, `X-Signature`; `version` theo ngày là tùy chọn trong schema.
- Response JSON gồm các mảng song song: `t` (timestamp), `o`, `h`, `l`, `c`, `v`, và `nextTime`. Cần ghép các phần tử cùng chỉ số thành một nến; `t` là Unix timestamp giây. Response không mang ticker trong từng phần tử nên client cần gắn `symbol` đã yêu cầu vào Ticker.
- Ánh xạ ASM: `t` → Date (cần xác nhận múi giờ/định nghĩa thời điểm nến), `symbol` request → Ticker; `o/h/l/c/v` → Open/High/Low/Close/Volume.
- Đề cập `resolution=1D` đáp ứng chu kỳ ngày. Tài liệu trang OHLC mô tả truy vấn theo khoảng thời gian, nhưng không nêu rõ giới hạn lịch sử tối đa, kích thước tối đa một response hoặc giới hạn `from` xa nhất.
- Response `nextTime` được mô tả là timestamp cây nến tiếp theo khi dữ liệu hiện tại chưa đủ để đáp ứng yêu cầu, bằng 0 nếu không còn dữ liệu. Tài liệu không mô tả rõ quy tắc chia trang/tiếp tục request bằng `nextTime` hay trần dữ liệu mỗi lần gọi; không được coi đây là phân trang đã kiểm chứng cho truy vấn 2–3 năm.

### 3.2 Đăng ký và xác thực theo tài liệu

1. Cần tài khoản chứng khoán DNSE đang hoạt động.
2. Đăng nhập trang giao dịch DNSE/Entrade X, mở mục Thông tin tài khoản → LightSpeed API → Đăng ký; chọn Smart OTP hoặc Email OTP và xác thực để hoàn tất.
3. Sau đăng ký, hệ thống hiển thị API Key và API Secret; secret chỉ hiển thị một lần. Tài liệu phân biệt đăng ký API với OTP xác nhận giao dịch; dù chỉ gọi market data, REST request vẫn cần chữ ký API.
4. Mỗi request ký bằng HMAC-SHA256 với API Secret, gồm method + path, timestamp header và nonce theo hướng dẫn xác thực; gửi API Key và chữ ký trong header.
5. Có khác biệt cần lưu ý giữa endpoint OHLC (`X-Aux-Date`) và hướng dẫn xác thực chung (Date hoặc tên header cấu hình riêng, ví dụ Date). Cần bám sát phiên bản tài liệu/API hiện hành và kiểm tra request read-only đã ký hợp lệ; không tự suy đoán chuỗi ký.

Không có key/secret/OTP nào được tạo hoặc sử dụng trong nghiên cứu này.

### 3.3 Rate limit, chi phí và điều kiện

- Bảng Rate Limits chính thức nêu endpoint Lịch sử OHLC `/Get OHLC`: 50.000 request/giờ và 100.000 request/24 giờ trên mỗi API Key/endpoint. Response có `X-RateLimit-*`; vượt rate có thể trả 429, vượt quota ngày có thể trả 403.
- Tài liệu đăng ký/điều khoản đã xem không nêu mức phí cụ thể cho API hoặc giấy phép sử dụng dữ liệu cho mục đích học thuật/tái phân phối. Không suy ra “miễn phí” từ việc tài liệu truy cập công khai.
- DNSE yêu cầu bảo vệ API Key/Secret, tuân thủ điều khoản và versioning API theo ngày.

## 4. So sánh cho yêu cầu ASM

| Tiêu chí | SSI FastConnect | DNSE OpenAPI |
|---|---|---|
| Endpoint daily | `/api/v3/data/ohlc`, `timeFrame=1d` | `/price/ohlc`, `resolution=1D`, `type=STOCK` |
| Date range | `from`, `to` là ngày | `from`, `to` Unix seconds |
| OHLCV | Các trường từng row: `tradingDate`, `open`, `high`, `low`, `close`, `volume`, `symbol` | Các mảng `t/o/h/l/c/v`; ticker phải gắn từ request |
| Nguồn lịch sử 2–3 năm | Tài liệu nói daily từ ngày mã bắt đầu giao dịch; phù hợp trên giấy | Endpoint nhận khoảng thời gian nhưng không công bố lookback tối đa; chưa đủ dữ kiện để khẳng định 2–3 năm |
| Phân trang | `pageIndex/pageSize`; mặc định 10; trần page size chưa rõ | `nextTime` có trong response nhưng quy tắc tiếp tục/trần response chưa rõ |
| Xác thực | API Key/Secret đổi lấy Bearer access token; read-only không cần OTP theo docs | API Key + HMAC signature và timestamp/nonce cho mỗi REST request |
| Tài khoản | Yêu cầu tài khoản giao dịch SSI theo tài liệu Terms/FAQ | Yêu cầu tài khoản DNSE ACTIVE |
| Rate limit | Động theo key/endpoint, xem `X-RATELIMIT-*`; số quota cụ thể không thấy ở endpoint OHLC | OHLC công bố 50.000/giờ, 100.000/ngày/key/endpoint; xem `X-RateLimit-*` |
| Phí | FAQ hiện hành nói FastConnect API không thu phí; quyền sử dụng dữ liệu cần kiểm tra riêng | Tài liệu đã xem không công bố phí hoặc kết luận miễn phí |
| Độ phức tạp tích hợp | Thấp hơn: một lần lấy Bearer token, JSON row schema, pagination rõ | Cao hơn: ký mỗi request, timestamp/nonce chính xác, response song song, timezone và pagination chưa rõ |
| Đã gọi API thật? | Chưa | Chưa |

## 5. Khả năng đáp ứng 10 mã và 2–3 năm

**SSI:** Tài liệu hỗ trợ OHLCV ngày từ khi mã bắt đầu giao dịch và có cơ chế pageIndex/pageSize, nên thiết kế có khả năng đáp ứng ACB/BID/CTG/MBB/TCB/VCB/VPB/STB/HDB/SHB nếu từng mã có trong universe và tài khoản được cấp quyền. Mỗi mã cần ít nhất một chuỗi trang; số request phụ thuộc pageSize tối đa và số dòng thực trả. 2–3 năm khoảng vài trăm đến gần 800 phiên/mã theo lịch giao dịch, nhưng đây chỉ là ước lượng quy mô, không phải số dòng đã lấy.

**DNSE:** Tài liệu xác nhận query theo ticker và khoảng thời gian, hỗ trợ resolution ngày; về thiết kế có thể gọi riêng cho từng mã. Tuy vậy, do không xác minh được lookback tối đa và quy tắc nextTime, khả năng lấy đủ 2–3 năm/10 mã chưa thể kết luận. Giới hạn rate công bố cao hơn nhiều so với khối lượng dự kiến, nhưng rate limit không chứng minh độ sâu lịch sử.

**Cả hai nguồn:** Chưa thử các mã hoặc truy vấn thực, nên sự hiện diện đầy đủ của 10 mã, lịch sử đủ dài, phản ứng mã ngừng giao dịch, adjustment giá, đơn vị giá/volume và tính nhất quán OHLCV chưa được xác minh.

## 6. Khả năng tích hợp với kiến trúc hiện tại

Về mặt kiến trúc, nên giữ importer CSV/XLSX hiện có và thêm client nguồn dữ liệu riêng dưới `src/data/` sau khi được phép triển khai. Client nên chuẩn hóa response về đúng thứ tự `Date, Ticker, Open, High, Low, Close, Volume`, lưu nguyên phản hồi hoặc dữ liệu raw theo mã/ngày, ghi metadata nguồn/thời gian tải, sau đó dùng lại `validate_stock_frame` để kiểm tra. Không cho dữ liệu đi thẳng vào processed trước khi qua validation.

Vì SSI/DNSE là nguồn khác Vietstock, nguồn/điều khoản cần được ghi vào metadata và báo cáo. Không trộn lẫn chuỗi từ nhiều nguồn trong cùng tập dữ liệu mà không kiểm tra điều chỉnh giá, đơn vị và khác biệt định nghĩa volume.

Đây là đề xuất, không phải thay đổi đã thực hiện. Không có code, dependency, file dữ liệu hay credential nào được tạo.

## 7. Nguồn nên ưu tiên và lý do

**Ưu tiên SSI nếu giảng viên chấp thuận nguồn thay thế Vietstock:** tài liệu chính thức nêu rõ lịch sử OHLCV ngày từ ngày mã bắt đầu giao dịch, có phân trang tường minh, schema gần như trùng trực tiếp với bộ cột ASM và quy trình xác thực read-only tương đối đơn giản. Điều kiện cần giải quyết trước là khác biệt định dạng `from/to` trong tài liệu, pageSize tối đa, phí/quyền dùng dữ liệu cụ thể và xác nhận API Key có quyền Market Data.

**DNSE là phương án thứ hai/đối chiếu:** tài liệu endpoint đúng bài toán, có mốc giới hạn request cụ thể và data schema đủ OHLCV. Tuy nhiên, signature, timestamp/nonce, header khác tên giữa trang endpoint và hướng dẫn auth, response dạng mảng và cơ chế phân trang/độ sâu lịch sử chưa rõ khiến rủi ro triển khai cao hơn.

**Điều kiện về yêu cầu học phần:** báo cáo ASM hiện đặt Vietstock là nguồn dữ liệu. Vì vậy khuyến nghị kỹ thuật SSI không đồng nghĩa được phép thay Vietstock. Cần xác nhận của giảng viên trước khi chọn một trong hai làm nguồn dữ liệu chính thức; nếu không được chấp thuận, tiếp tục dùng file Vietstock CSV/XLSX.

## 8. Rủi ro và thông tin chưa xác minh

1. Chưa có request thật vì chưa có credentials; tài liệu endpoint không chứng minh tài khoản cụ thể gọi được hoặc dữ liệu thực trả đủ.
2. Chưa xác nhận 10 mã trong security universe của từng nhà cung cấp, lịch sử 2–3 năm cụ thể và số dòng trả.
3. SSI có khác biệt định dạng ngày giữa endpoint reference và Quick Start; page size tối đa và giới hạn OHLC riêng chưa thấy công bố.
4. DNSE chưa nêu lookback limit, response cap, pagination tiếp bằng `nextTime`, timezone timestamp; header thời gian `X-Aux-Date` cần đối chiếu hướng dẫn signature tổng quát.
5. Chưa xác minh dữ liệu đã điều chỉnh hay chưa, điều chỉnh sự kiện doanh nghiệp/cổ tức, đơn vị giá, quy ước volume, ngày giao dịch của HOSE/HNX và chất lượng lịch sử.
6. Chưa xác minh chính sách lưu trữ/sử dụng dữ liệu cho bài tập, chia sẻ trong nhóm, đưa vào báo cáo hoặc tái phân phối; đặc biệt SSI API miễn phí không tự động đồng nghĩa dữ liệu có quyền tái phân phối miễn phí.
7. Credential có quyền nhạy cảm; cần tách key read-only, không commit vào Git, không đưa lên dashboard hoặc ghi log. DNSE Secret không hiển thị lại; SSI Secret theo docs chỉ hiển thị một lần.
8. Múi giờ/hệ thống máy sai có thể làm chữ ký DNSE bị từ chối; nonce/signature cũ không được tái sử dụng.
9. Thay nguồn dữ liệu có thể làm sai ràng buộc Vietstock trong PDF/báo cáo ASM nếu không có phê duyệt giảng viên.

## 9. Kết luận nghiên cứu

Theo tài liệu chính thức, cả hai nhà cung cấp đều mô tả API nến OHLCV ngày. SSI có thông tin lịch sử và phân trang rõ hơn cho mục tiêu 2–3 năm; DNSE có dữ liệu OHLCV và hạn mức request rõ, nhưng quy tắc độ sâu lịch sử/phân trang cần hỏi hoặc thử bằng tài khoản được cấp. Chưa khẳng định API nào hoạt động trong môi trường dự án vì không thực hiện request API.

Chưa tích hợp code. Bước tiếp theo cần có xác nhận giảng viên về việc dùng nguồn ngoài Vietstock, lựa chọn nhà cung cấp, tài khoản/API access do người dùng tự đăng ký, cùng điều khoản/chi phí dữ liệu được nhà cung cấp xác nhận. Khi tích hợp được cho phép, kiểm chứng ACB với phạm vi nhỏ, đối chiếu từng trường/ngày/giá/volume và kiểm tra đầy đủ trước khi mở rộng 10 mã.

## 10. Tài liệu chính thức đã tham khảo

### SSI

- [data-ohlc API reference](https://developers.ssi.com.vn/en/docs/api-reference/data-ohlc)
- [SSI API Overview](https://developers.ssi.com.vn/en/docs/api-reference)
- [Getting API Keys / Access Tokens](https://developers.ssi.com.vn/en/docs/getting-started/api-keys)
- [Terms of Use & Environments](https://developers.ssi.com.vn/en/docs/getting-started/terms-and-environments)
- [FastConnect FAQ / Service Overview](https://developers.ssi.com.vn/en/docs/faq/service-overview)
- [Quick Start](https://developers.ssi.com.vn/en/docs/getting-started/first-api-call)
- [Registration and Activation Process](https://developers.ssi.com.vn/en/docs/getting-started/registration)

### DNSE

- [Lịch sử OHLC](https://developers.dnse.com.vn/docs/dnse/get-ohlc-history/)
- [Xác thực](https://developers.dnse.com.vn/docs/guide/intro/authentication/)
- [Đăng ký & Quản lý dịch vụ](https://developers.dnse.com.vn/docs/guide/intro/register_guide/)
- [Rate Limits](https://developers.dnse.com.vn/docs/guide/ratelimits/)
- [FAQ](https://developers.dnse.com.vn/docs/guide/faq/)
- [API Versioning](https://developers.dnse.com.vn/docs/guide/versioning/api/)
