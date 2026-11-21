# BÁO CÁO ĐÁNH GIÁ NGUỒN DỮ LIỆU THAY THẾ

**Giai đoạn:** 2.11 – lựa chọn và kiểm chứng nguồn dữ liệu thay thế  
**Ngày truy cập tài liệu:** 20/11/2026  
**Phạm vi:** 43 mã hiện có; OHLCV ngày 19/11/2021–18/11/2026; rủi ro biến động giá; không thay đổi đề tài.

## 1. Kết luận điều hành

Giảng viên đã cho phép nhóm dùng nguồn khác CafeF. Tuy nhiên, **chưa có API credentials trong môi trường** (`SSI_API_KEY`, `SSI_API_SECRET`, `SSI_ACCESS_TOKEN` đều không hiện diện; không có `.env`) nên không truy vấn thật. Báo cáo này đánh giá tài liệu chính thức, không tuyên bố đã thử nghiệm OHLCV. Không nguồn nào được chọn chính thức vì chưa chứng minh price basis/corporate actions, quyền học thuật và coverage thực 43 mã.

SSI được ưu tiên cho bước thử nghiệm tiếp theo vì tài liệu nói daily history từ ngày symbol bắt đầu giao dịch và có pagination rõ. DNSE là phương án sau đó; độ sâu lịch sử và semantics lấy tiếp còn chưa rõ trong tài liệu. Cả hai đều chưa chứng minh OHLC đã corporate-action adjusted.

## 2. SSI FastConnect Data

### Tài liệu API

`GET https://api.ssi.com.vn/api/v3/data/ohlc` nhận `symbol`, `from`, `to`, `timeFrame` (mặc định `1d`), `pageIndex` (từ 1) và `pageSize` (mặc định 10). Response mẫu có `tradingDate`, `open`, `high`, `low`, `close`, `volume`, `value`. SSI ghi daily data sẵn có từ ngày mã bắt đầu giao dịch; intraday chỉ trong năm gần nhất. Đây là mô tả tài liệu, chưa xác nhận tài khoản sẽ trả đủ 5 năm cho các mã nghiên cứu. API reference dùng format ngày `YYYY/MM/DD`, Quick Start minh họa `YYYY-MM-DD`; phải được xác nhận trước khi gọi. [SSI OHLC reference](https://developers.ssi.com.vn/en/docs/api-reference/data-ohlc), [SSI Quick Start](https://developers.ssi.com.vn/en/docs/getting-started/first-api-call).

Rate limit được trả qua `X-RATELIMIT-LIMIT`, `X-RATELIMIT-REMAINING`, `X-RATELIMIT-RESET`, vượt quota trả 429; docs không nêu pageSize max hay quota cụ thể OHLC. [SSI Terms/Data Limits](https://developers.ssi.com.vn/en/docs/getting-started/terms-and-environments).

### Xác thực, điều kiện, phí và quyền

SSI docs yêu cầu tài khoản SSI đang hoạt động và đăng ký/đồng ý Terms. Flow dữ liệu dùng API Key/Secret để lấy Bearer token. Registration guide mô tả liên hệ chi nhánh/hotline, trong khi FAQ nói activation online; cần SSI xác nhận quy trình thực tế của nhóm. FAQ hiện nói không thu phí dịch vụ FastConnect; đây không phải xác nhận quyền market-data license, quyền tải/lưu, công bố lại hoặc sử dụng dữ liệu trong báo cáo học thuật. [SSI registration](https://developers.ssi.com.vn/en/docs/getting-started/registration), [SSI auth](https://developers.ssi.com.vn/en/docs/getting-started/api-keys), [SSI FAQ](https://developers.ssi.com.vn/en/docs/faq/service-overview), [Terms](https://developers.ssi.com.vn/en/docs/getting-started/terms-and-environments).

### Price basis và corporate actions

OHLC docs không khẳng định giá raw hay adjusted, không nêu adjusted OHLC/Adjusted Close, adjustment factor hay cách back-adjust. SSI có endpoint `data-corporateActions` nhận symbol và date range, mô tả cash dividends, stock dividends, rights issues…; khoảng query tối đa 5 ngày, có phân trang. Đây là event feed theo mô tả, không phải bằng chứng OHLC được adjusted hay event history đầy đủ 2021–2026. Cần hỏi SSI về coverage corporate action, split/reverse split, giá cơ sở và liên kết với OHLC. [SSI corporate actions](https://developers.ssi.com.vn/en/docs/api-reference/data-corporateActions).

## 3. DNSE OpenAPI

Endpoint tài liệu `GET /price/ohlc` dùng `symbol`, `type=STOCK`, `resolution` (gồm `1D`), `from/to` Unix seconds; response là mảng song song `t,o,h,l,c,v` và `nextTime`. Docs chưa chốt độ sâu lịch sử tối thiểu, maximum query range/bars, daily timestamp timezone hoặc semantics lấy tiếp bằng `nextTime`. Không xác nhận OHLC raw/adjusted. [DNSE OHLC history](https://developers.dnse.com.vn/docs/dnse/get-ohlc-history/).

DNSE yêu cầu API Key, HMAC-SHA256 signature, Date/nonce; endpoint ghi header `X-Aux-Date`, hướng dẫn chung nói `Date` hoặc header tùy cấu hình. Cần xác nhận header cho endpoint cụ thể. Rate limits theo endpoint/API key nhưng bảng hiện xem không nêu quota riêng `/price/ohlc`; không áp mức của endpoint khác. [DNSE authentication](https://developers.dnse.com.vn/docs/guide/intro/authentication/), [DNSE rate limits](https://developers.dnse.com.vn/docs/guide/ratelimits/).

Đăng ký LightSpeed cần tài khoản DNSE hoạt động, quy trình Entrade X và OTP. Chưa xác minh phí dữ liệu hay quyền dùng trong nghiên cứu. Tài liệu corporate-action DNSE trước đó được khảo sát là lịch sử quyền của tài khoản; không xác nhận đây là feed corporate actions toàn thị trường hoặc adjusted OHLC. Cần hỏi điều khoản và provider. [DNSE FAQ](https://developers.dnse.com.vn/docs/guide/faq/).

## 4. So sánh

| Tiêu chí | SSI | DNSE | Kết luận hiện tại |
|---|---|---|---|
| OHLCV daily | Có schema OHLCV | Có schema OHLCV | Tài liệu xác nhận endpoint/schema, chưa có dữ liệu runtime |
| Lịch sử từ 2021 | Nói daily từ ngày mã bắt đầu giao dịch | Không nêu history depth | SSI triển vọng hơn theo tài liệu; chưa verify 43 mã |
| Coverage 43 mã | Chưa truy vấn | Chưa truy vấn | Chưa xác minh cả hai |
| Pagination | pageIndex/pageSize; max pageSize chưa nêu | `nextTime`; cách paging/backfill cần hỏi | SSI rõ hơn |
| Giá raw/adjusted | Không nêu | Không nêu | Chưa đủ điều kiện returns/risk features |
| Corporate actions | Endpoint events riêng, không chứng minh adjusted OHLC | Tài liệu hiện có không chứng minh feed thị trường và adjusted OHLC | Cần xác minh trực tiếp |
| Đơn vị/Volume semantics | response schema có trường; docs khảo sát chưa chốt đơn vị/cách tính giao dịch thỏa thuận | response có volume; chưa chốt đơn vị/phạm vi | Chưa đủ bằng chứng |
| Truy cập | tài khoản SSI active, đăng ký API, API key/secret | tài khoản DNSE active, đăng ký LightSpeed, key/secret/signature | Chưa có credentials trong môi trường |
| Chi phí | API service được FAQ ghi hiện không thu; license dữ liệu chưa rõ | Chưa xác minh | Hỏi về data licensing riêng |
| Quyền học thuật | Chưa xác minh | Chưa xác minh | Phải có điều khoản/trả lời rõ |

## 5. Thiết kế thử nghiệm đề xuất (chưa thực hiện)

Chọn tạm 5 mã trong universe hiện tại: **FPT, NLG, HPG, VNM, VIC**. FPT/NLG được chọn vì báo cáo cơ sở giá hiện có đã đối chiếu một số corporate-action cases (FPT cash dividend/stock issuance; NLG rights issue). HPG/VNM/VIC bổ sung mã đại diện để kiểm tra coverage và sai khác thông thường; các sự kiện cụ thể của ba mã này cần xác minh chính thức trước khi gắn nhãn event-window. Danh sách chỉ là thiết kế kiểm thử, không thay đổi universe.

Sau khi access/terms được chấp thuận: truy vấn 2021-11-19–2026-11-18 cho từng mã; giữ response gốc riêng theo provider; lưu params/version/timestamp/request ID/headers không nhạy cảm; không gửi credentials/log token. Kiểm tra số rows, ngày đầu/cuối, duplicate ticker-date, gaps so với calendar được xác minh, null/type, OHLC relation, negative/zero volume, units và timezone. Sau đó đối chiếu ngày thường và các event windows với CafeF hiện có. Không yêu cầu hai nguồn trùng tuyệt đối; phân loại chênh lệch theo unit, rounding, session/volume definition, corporate-action basis, missing coverage hoặc unexplained.

Corporate-action event list cần đối chiếu từ HOSE/VSDC/issuer. So sánh phải khóa các phiên bản cùng ngày tải vì historical data có thể được nhà cung cấp chỉnh hồi tố. Không suy ra chất lượng chỉ từ số dòng nhiều hơn.

**Trạng thái thử nghiệm:** chưa thực hiện. Không có dòng dữ liệu mới, số dòng trả về, first/last date hoặc quality metrics để báo cáo. Không tuyên bố API thành công.

## 6. Quyết định nguồn và điều kiện

- **Ưu tiên thử nghiệm kỹ thuật kế tiếp: SSI**, vì tài liệu historical daily depth và pagination tường minh hơn. Đây chưa phải nguồn chính thức đã được kiểm chứng.
- **DNSE: phương án kiểm tra tiếp sau SSI**, trừ khi SSI không cấp quyền/không đáp ứng điều khoản hoặc depth; DNSE phải làm rõ history, `nextTime`, timezone, quota OHLC và giá basis.
- **Chưa chọn nguồn thay thế chính thức**: không nguồn nào hiện đạt đủ 7 tiêu chí về coverage thực, 5-year history, price basis, corporate actions, units, explainable discrepancies và academic usage rights.

Trước thử nghiệm cần: nhóm đăng ký quyền hợp lệ với provider, giữ credentials trong environment/secret store; xác nhận điều khoản học thuật và market-data license; hỏi provider về raw/adjusted basis, corporate action coverage, volume units, lịch sử, giới hạn. Sau đó nhóm cho phép read-only test 5 mã. Chỉ sau khi báo cáo kiểm định mẫu được nhóm/giảng viên duyệt mới tính đến tải đủ 43 mã. Không ghi đè CafeF Raw/Processed; dataset mới phải nằm ở khu vực riêng có metadata/provenance.

## 7. Kiến trúc adapter nếu chưa có credentials

Đã triển khai `src/data/providers/ssi.py` (environment-based config, token POST, GET OHLC, pageIndex/pageSize, schema normalization, safe API errors); `src/data/staging.py` (CSV staging riêng và manifest JSONL; upsert idempotent theo source/ticker/date, lưu từng lần thử trong manifest); `src/data/quality.py` (cờ duplicate, null/type, OHLC, negative/high volume, missing per ticker khi truyền calendar, corporate-action date và so sánh nguồn). Không có API caller trong Streamlit; adapter không được gọi trong lượt này.

Các test bằng transport mock/fixture bao gồm auth, paging, normalization, lỗi status/schema, quality flags không sửa frame, staging idempotence và manifest. Toàn bộ `compileall` đạt; 20/20 unittest đạt; AppTest cả sáu trang không exception; Streamlit trả HTTP 200. Test fixtures không được ghi vào dữ liệu dự án. Dữ liệu staging thật bị gitignore và tách khỏi Raw/Processed. Chưa có unit metadata do provider xác nhận; báo cáo quality ghi `Chưa xác minh` nếu không truyền vào.

## 8. Tài liệu tham khảo

Truy cập ngày **20/11/2026**:

- [SSI data-ohlc](https://developers.ssi.com.vn/en/docs/api-reference/data-ohlc)
- [SSI corporate actions](https://developers.ssi.com.vn/en/docs/api-reference/data-corporateActions)
- [SSI terms, data limits and rate limits](https://developers.ssi.com.vn/en/docs/getting-started/terms-and-environments)
- [SSI registration](https://developers.ssi.com.vn/en/docs/getting-started/registration)
- [SSI API keys/access tokens](https://developers.ssi.com.vn/en/docs/getting-started/api-keys)
- [SSI FastConnect FAQ](https://developers.ssi.com.vn/en/docs/faq/service-overview)
- [DNSE OHLC history](https://developers.dnse.com.vn/docs/dnse/get-ohlc-history/)
- [DNSE authentication](https://developers.dnse.com.vn/docs/guide/intro/authentication/)
- [DNSE rate limits](https://developers.dnse.com.vn/docs/guide/ratelimits/)
- [DNSE FAQ](https://developers.dnse.com.vn/docs/guide/faq/)

**Kết luận:** Phần adapter/staging đã triển khai và kiểm thử bằng fixture riêng; kiểm chứng dữ liệu thực tế chưa thể thực hiện vì không có credentials. SHA-256 Raw `1B492296E31DB393DA80A8D2579887BBECB4AFB95F4F3A9FF9CECCBFB5186043`; Processed `3574059045FBD420FC0EF473FCC6671C16C3A6BDC9F57478F02A7241598FE953` vẫn khớp snapshot trước adapter. Không tải/thay dữ liệu và không tính Feature Engineering/clustering.
