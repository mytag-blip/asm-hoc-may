# BÁO CÁO KHẢO SÁT NGUỒN DỮ LIỆU GIÁ

**Giai đoạn:** 2.7 – khảo sát nguồn dữ liệu giá  
**Ngày truy cập tài liệu:** 20/11/2026  
**Phạm vi khảo sát:** SSI FastConnect Data và DNSE OpenAPI; đối chiếu tiềm năng cho dữ liệu OHLCV của 43 doanh nghiệp HOSE giai đoạn 19/11/2021–18/11/2026.

## 1. Mục tiêu và giới hạn

Khảo sát tài liệu chính thức để đánh giá hai dịch vụ có thể dùng đối chiếu độc lập hoặc thay thế CafeF trong tương lai. Đây là nghiên cứu tài liệu, **không gọi API, không tạo/nhận credential, không tải dữ liệu và không thay đổi bộ Raw/Processed**. Tài liệu API chứng minh khả năng được thiết kế/công bố, nhưng chưa chứng minh dữ liệu thực tế cho đủ 43 mã trong tài khoản của nhóm.

Quyết định Giai đoạn 2.6 vẫn có hiệu lực: CafeF chưa công bố phương pháp Adjusted Close; chưa xác nhận OHLC cùng basis với trường này. Báo cáo này không cấp phép tính Daily Return, Volatility hay Feature Engineering.

## 2. SSI FastConnect Data

### 2.1 Endpoint và schema công bố

Tài liệu SSI công bố `GET https://api.ssi.com.vn/api/v3/data/ohlc` để truy vấn OHLCV theo `symbol`, `from`, `to`; `timeFrame` hỗ trợ `1d` (mặc định), ngoài các khung trong ngày. Phân trang bằng `pageIndex` bắt đầu từ 1 và `pageSize` (mặc định 10). Tài liệu mô tả daily OHLCV có lịch sử từ ngày mã bắt đầu giao dịch; dữ liệu intraday chỉ trong năm gần nhất. Response mẫu gồm `symbol`, `tradingDate`, `open`, `high`, `low`, `close`, `volume`, `value`. Giá/khối lượng trong response mẫu được biểu diễn dạng chuỗi. [Tài liệu data-ohlc](https://developers.ssi.com.vn/en/docs/api-reference/data-ohlc) và [Quick Start](https://developers.ssi.com.vn/en/docs/getting-started/first-api-call).

Trang API reference định dạng ngày `YYYY/MM/DD`, trong khi Quick Start minh họa `YYYY-MM-DD`. Cần xác minh với SSI hoặc thử nghiệm hợp lệ để chốt định dạng thực sự được chấp nhận; không nên tự chọn một định dạng chỉ từ một trong hai trang.

### 2.2 Xác thực và điều kiện truy cập

Tài liệu yêu cầu tài khoản giao dịch SSI đang hoạt động, đăng ký FastConnect và đồng ý điều khoản. Luồng API dùng API Key/Secret để lấy Bearer JWT tại `/api/v3/auth/token`, sau đó gửi `Authorization: Bearer ...`. [Hướng dẫn đăng ký](https://developers.ssi.com.vn/en/docs/getting-started/registration), [API keys/tokens](https://developers.ssi.com.vn/en/docs/getting-started/api-keys).

Có điểm không đồng nhất giữa các trang đăng ký: trang Registration mô tả liên hệ chi nhánh/hotline để đăng ký dịch vụ và nhận email kích hoạt sau 2–4 giờ làm việc; FAQ mới hơn mô tả quy trình trực tuyến qua Developer Portal. Vì vậy, thủ tục hiện hành cần được SSI xác nhận cho tài khoản cụ thể, không khẳng định một luồng duy nhất. [Registration](https://developers.ssi.com.vn/en/docs/getting-started/registration), [FAQ FastConnect](https://developers.ssi.com.vn/en/docs/faq/service-overview).

OTP/2FA được tài liệu gắn với token có quyền giao dịch; tài liệu này không yêu cầu OTP trong ví dụ token chỉ dùng dữ liệu. Không gửi API Secret, OTP hay token trong báo cáo/chat.

### 2.3 Lịch sử, phân trang, giới hạn, phí và điều khoản

- Lịch sử ngày từ ngày mã bắt đầu giao dịch, theo tài liệu SSI; chưa có kiểm tra response thực tế cho các mã và thời kỳ của dự án.
- Có phân trang `pageIndex/pageSize`; tài liệu đã xem không nêu mức `pageSize` tối đa hoặc số ngày tối đa cho một request.
- SSI áp dụng quota theo API key/endpoint và trả `X-RATELIMIT-LIMIT`, `X-RATELIMIT-REMAINING`, `X-RATELIMIT-RESET`; vượt giới hạn trả HTTP 429. Không thấy quota số cụ thể cho endpoint OHLC trong tài liệu đã tra. [Terms, limits and data limits](https://developers.ssi.com.vn/en/docs/getting-started/terms-and-environments).
- FAQ SSI nói hiện không thu phí dịch vụ FastConnect. Điều này chỉ xác nhận phí dịch vụ API theo FAQ, không đủ để kết luận về phí/giấy phép dữ liệu thị trường, quyền lưu trữ, công bố lại hoặc chia sẻ dữ liệu trong đồ án. [FAQ FastConnect](https://developers.ssi.com.vn/en/docs/faq/service-overview).
- Người dùng phải tuân thủ Terms of Service, giới hạn hệ thống và quy định chứng khoán Việt Nam. Phạm vi quyền sử dụng dữ liệu học tập/công bố trong báo cáo chưa được tài liệu truy cập làm rõ riêng; cần đọc hợp đồng/điều khoản được chấp thuận khi đăng ký hoặc hỏi SSI.

### 2.4 Corporate actions và cơ sở giá

SSI có API riêng `data-corporateActions` để truy vấn sự kiện quyền/corporate action. Đây là một nguồn có thể hỗ trợ lập danh sách sự kiện để đối chiếu. Tuy nhiên, tài liệu OHLC không nói OHLC đã được điều chỉnh theo các sự kiện đó; tài liệu corporate actions cũng không tuyên bố endpoint OHLC trả về adjusted OHLC hay Adjusted Close. Do đó không được coi sự tồn tại của API sự kiện là bằng chứng về phương pháp điều chỉnh chuỗi giá. [API overview](https://developers.ssi.com.vn/en/docs/api-reference), [data-corporateActions](https://developers.ssi.com.vn/en/docs/api-reference/data-corporateActions).

**Kết luận cơ sở giá SSI:** tài liệu xác nhận có OHLCV nhưng không xác định rõ chuỗi là giá chưa điều chỉnh hay đã điều chỉnh, không xác nhận cách xử lý cổ tức/quyền/chia tách, và không xác nhận Open/High/Low cùng basis với Close. Hỏi SSI trước khi dùng chuỗi cho returns/risk features.

## 3. DNSE OpenAPI

### 3.1 Endpoint, tham số và schema

Tài liệu DNSE công bố `GET https://openapi.dnse.com.vn/price/ohlc`, truy vấn lịch sử nến cho cổ phiếu, phái sinh và chỉ số. Tham số gồm `symbol`, `type` (cổ phiếu là `STOCK`), `resolution` (`1`, `3`, `5`, `15`, `30`, `1H`, `1D`, `1W`), `from`, `to` kiểu integer Unix timestamp. Response có các mảng song song `t`, `o`, `h`, `l`, `c`, `v` và `nextTime`; ghép giá trị theo cùng chỉ số mảng, còn ticker cần gắn từ request. `t` là Unix timestamp giây. [Tài liệu Lịch sử OHLC](https://developers.dnse.com.vn/docs/dnse/get-ohlc-history/).

API reference không ghi rõ múi giờ/ngữ nghĩa chính xác của timestamp daily candle, khoảng thời gian tối đa mỗi truy vấn, giới hạn số candle, hay quy tắc phân trang/tiếp tục dùng `nextTime` đối với dữ liệu lịch sử. `nextTime` được mô tả là mốc cây nến tiếp theo khi dữ liệu hiện tại chưa đủ, bằng 0 nếu hết dữ liệu; cần DNSE xác nhận cách dùng cho lịch sử nhiều năm.

### 3.2 Xác thực và điều kiện truy cập

Tài liệu hướng dẫn DNSE yêu cầu API Key, chữ ký HMAC-SHA256 và header thời gian UTC (Date hoặc header cấu hình theo tài liệu cụ thể). Mỗi request cần signature/nonce mới; Date phải gần giờ chuẩn trong giới hạn ±1 phút. Tài liệu endpoint OHLC hiển thị `X-API-Key`, `X-Aux-Date`, `X-Signature`, cùng header `version` tùy chọn. Có khác biệt tên header thời gian giữa hướng dẫn chung và endpoint; khi tích hợp phải tuân đúng đặc tả hiện hành/SDK cho endpoint, không tự thay tên header. [Hướng dẫn xác thực](https://developers.dnse.com.vn/docs/guide/intro/authentication/), [FAQ](https://developers.dnse.com.vn/docs/guide/faq/).

FAQ nêu đăng ký LightSpeed API từ tài khoản chứng khoán DNSE đang hoạt động trong Entrade X, chọn Smart OTP hoặc Email OTP, xác nhận đăng ký; API Key và Secret được hiển thị sau đó, Secret chỉ hiện một lần. Điều này là điều kiện dịch vụ, không phải API credential được cung cấp cho nhóm. [FAQ DNSE](https://developers.dnse.com.vn/docs/guide/faq/).

### 3.3 Lịch sử, giới hạn, phí và điều khoản

- Endpoint chứng minh DNSE công bố truy vấn OHLCV theo symbol và khoảng from/to, nhưng trang OHLC không cam kết thời lượng lịch sử tối thiểu/độ sâu cụ thể. **Chưa xác minh có dữ liệu từ 2021 cho cả 43 mã.**
- Hướng dẫn rate limits nói giới hạn theo API Key và endpoint, theo request/giờ và quota/24 giờ; response có header để theo dõi, vượt giới hạn có thể trả 429 hoặc 403 khi hết quota. Tuy nhiên bảng số đã công bố không đưa ra mức riêng cho `/price/ohlc`; không áp số của endpoint khác sang OHLC. [Rate Limits](https://developers.dnse.com.vn/docs/guide/ratelimits/), [FAQ](https://developers.dnse.com.vn/docs/guide/faq/).
- Chưa xác minh chi phí OpenAPI hoặc phí/quyền sử dụng dữ liệu lịch sử. Trang điều khoản dịch vụ chung nhắc người dùng cần đọc điều khoản/hợp đồng, nhưng tài liệu đã truy cập chưa đủ để xác nhận quyền sử dụng dữ liệu trong đồ án, lưu trữ nội bộ hay công bố lại. Cần DNSE trả lời rõ theo loại tài khoản và mục đích học thuật. [Điều khoản dịch vụ DNSE](https://www.dnse.com.vn/dieu-khoan-dich-vu).

### 3.4 Corporate actions và cơ sở giá

API “Lịch sử sự kiện quyền” DNSE được tài liệu mô tả là lịch sử quyền trên **tài khoản chứng khoán**, gồm cổ tức tiền, cổ tức cổ phiếu, cổ phiếu thưởng, rights offering. Đây không phải bằng chứng có corporate-action feed đầy đủ thị trường 43 mã, cũng không phải công cụ xác nhận giá OHLC lịch sử đã điều chỉnh. [DNSE corporate action history](https://developers.dnse.com.vn/docs/dnse/get-corporate-action-history/).

Trang OHLC chỉ mô tả Open/High/Low/Close/Volume; không công bố cơ sở giá điều chỉnh, Adjusted Close, cơ chế back-adjustment hay mối quan hệ basis giữa các trường. Không kết luận giá DNSE raw/adjusted chỉ dựa trên schema.

## 4. So sánh nguồn

| Tiêu chí | SSI FastConnect | DNSE OpenAPI | Trạng thái đối với dự án |
|---|---|---|---|
| Coverage 43 mã HOSE | API lấy theo symbol; tài liệu chung hỗ trợ market data. Chưa gọi API kiểm tra 43 symbol trong quyền truy cập dự kiến. | API nhận symbol/type=STOCK. Chưa gọi API kiểm tra 43 symbol. | Chưa xác minh dữ liệu thực tế đầy đủ cho 43/43. |
| Lịch sử từ 2021 | Tài liệu nói daily từ ngày mã bắt đầu giao dịch. | Không nêu độ sâu lịch sử tối thiểu. | SSI có lợi thế tài liệu rõ hơn; vẫn cần kiểm tra từng mã, ngày listing, response và quyền account. |
| OHLC | Có Open, High, Low, Close. | Có Open, High, Low, Close. | Có ở schema công bố. |
| Volume | Có Volume; thêm value. | Có Volume. | Có ở schema; cần xác nhận đơn vị/định nghĩa và cách bao gồm giao dịch thỏa thuận. |
| Giá điều chỉnh | Không nêu adjusted/raw hoặc corporate-action adjustment cho OHLC. | Không nêu adjusted/raw hoặc corporate-action adjustment cho OHLC. | Chưa đủ bằng chứng cho cả hai. |
| Corporate actions | Có endpoint market data riêng cho corporate-action events; không chứng minh OHLC được điều chỉnh. | API lịch sử quyền theo tài khoản; không phải market-wide event history theo mô tả đã xem. | SSI hữu ích hơn cho event reconciliation, nhưng completeness/history cần xác minh. |
| Tính nhất quán | Có ngày giao dịch, giá/volume trong record; kiểu dữ liệu chuỗi theo mẫu. | Timestamp arrays parallel; nối theo index và xác minh timezone. | Cần kiểm tra dữ liệu thực và mapping trước khi so. |
| Xác thực/truy cập | Tài khoản SSI active + đăng ký; API Key/Secret → Bearer JWT. Hướng dẫn đăng ký có mâu thuẫn giữa các trang. | Tài khoản DNSE active + đăng ký LightSpeed; API Key/Secret, HMAC-SHA256 signature, timestamp/nonce. | Cả hai cần tài khoản/quyền do chủ tài khoản hợp pháp đăng ký. |
| Giới hạn | Header rate limit động; không thấy quota OHLC cụ thể; phân trang có page index/size, max size chưa nêu. | Rate/Quota từng endpoint; OHLC-specific số chưa nêu; khoảng thời gian và phân trang chưa rõ. | Cần xác nhận với provider/đọc header khi có quyền. |
| Chi phí | SSI FAQ hiện nói dịch vụ FastConnect không thu phí; không đồng nghĩa quyền khai thác/tái phân phối dữ liệu miễn phí. | Chưa xác minh phí API/dữ liệu. | Cần xác nhận phí và license. |
| Quyền dùng trong đồ án | Chưa xác minh quyền lưu trữ, phân tích, trích dẫn hoặc phân phối dữ liệu. | Chưa xác minh quyền lưu trữ, phân tích, trích dẫn hoặc phân phối dữ liệu. | Xin xác nhận bằng văn bản/điều khoản áp dụng. |

## 5. Khả năng đáp ứng 43 mã trong gần 5 năm

**SSI:** documentation claim rằng daily OHLCV có từ ngày bắt đầu giao dịch của symbol, về mặt mô tả phù hợp hơn với kỳ 19/11/2021–18/11/2026. Tài liệu hỗ trợ phân trang, nhưng chưa biết page size tối đa và quota thực tế. Chưa xác minh response thực tế cho bất kỳ mã nào trong phiên khảo sát này, cũng chưa kiểm chứng symbols có đầy đủ, lịch sử liên tục hay cùng định nghĩa volume. Vì vậy đây là **khả năng theo tài liệu**, chưa phải coverage đã đạt.

**DNSE:** endpoint nhận khoảng thời gian tùy query nhưng không công bố độ sâu lịch sử/giới hạn query rõ trong trang đã xem. Chưa thể xác nhận năm năm hay 43 mã. `nextTime` không được hiểu như pagination chắc chắn nếu provider chưa xác nhận hướng/biên tiếp tục truy vấn.

Không tải dữ liệu thử vì phạm vi hiện tại là nghiên cứu tài liệu và chưa có quyền truy cập hợp lệ do nhóm cung cấp. Không có số dòng/thời điểm cuối thực tế để báo cáo.

## 6. Đánh giá cơ sở giá và corporate actions

Tài liệu của cả hai provider xác nhận schema OHLCV, nhưng không đủ bằng chứng xác định raw hay adjusted basis. Không thấy công bố trường Adjusted Close hay cam kết lịch sử OHLC được back-adjust cho cổ tức tiền, cổ phiếu thưởng, phát hành quyền mua hoặc chia/tách. SSI có endpoint corporate action events tách biệt; DNSE có endpoint sự kiện quyền gắn với tài khoản. Những endpoint sự kiện hỗ trợ lập event ledger, nhưng không xác nhận thuật toán điều chỉnh chuỗi OHLC.

Do kết luận 2.6 của dự án còn hiệu lực, **chưa tính Daily Return, Volatility, ATR hoặc đặc trưng rủi ro qua corporate actions** từ dữ liệu của hai nguồn. Phải có xác nhận của provider về basis giá và metadata sự kiện; nếu OHLC không được điều chỉnh, cần một chuỗi adjusted nhất quán và có nguồn/phương pháp hợp lệ trước khi tính các đặc trưng theo quyết định nhóm/giảng viên.

## 7. Phương pháp đối chiếu dự kiến (chưa thực hiện)

Khi được cấp quyền hợp lệ và nhóm cho phép thử nghiệm:

1. Chọn 3–5 mã đại diện trong 43 mã, ghi lý do chọn; trước hết xác minh symbol/sàn và ngày bắt đầu niêm yết.
2. Chọn một số ngày giao dịch bình thường và nhiều cửa sổ quanh corporate actions đã được xác nhận từ HOSE/VSDC/issuer; ghi ngày ex-right, loại sự kiện, tỷ lệ và ngày hiệu lực từ nguồn gốc.
3. Lấy cùng ticker, ngày, timeframe và phạm vi từ CafeF và provider; lưu response gốc, thời điểm tải, tham số, API version, nguồn, đơn vị được nhà cung cấp xác nhận và điều khoản. Không công bố secrets.
4. So sánh từng trường OHLCV sau khi xác minh đơn vị giá/khối lượng, timestamp timezone, cách tính daily candle, phiên giao dịch bao gồm thỏa thuận hay chỉ khớp lệnh, làm tròn và điều chỉnh quyền.
5. Phân loại sai khác thành: mapping/timezone, đơn vị/thang giá, làm tròn, coverage/missing, khác định nghĩa volume, corporate action/basis, hoặc chưa giải thích. Không ép hai nguồn trùng tuyệt đối và không tự sửa dữ liệu để khớp.
6. Chỉ lập kết luận nguồn đối chiếu độc lập sau khi xác định provider/feed upstream có độc lập thực sự; một wrapper/thư viện lấy lại cùng feed không phải nguồn độc lập.

## 8. Đề xuất lựa chọn và điều kiện trước khi dùng

- **Nguồn ưu tiên để thử đối chiếu: SSI FastConnect**, vì tài liệu công bố rõ daily history từ ngày listing, schema OHLCV, pagination và rate-limit headers; có endpoint corporate actions riêng. Đây là ưu tiên cho bước thử nghiệm, không phải quyết định thay nguồn chính thức hay xác nhận giá đã điều chỉnh.
- **DNSE:** nguồn dự phòng/đối chiếu thứ hai tiềm năng, có endpoint daily OHLCV với tham số from/to và schema rõ. Trước tiên cần xác minh history depth, OHLC paging semantics, endpoint-specific limits và phí/terms.
- **Không thay CafeF tự động.** Bất cứ thay đổi nguồn nào cho dự án phải được nhóm/giảng viên chấp thuận và có quyền sử dụng dữ liệu rõ.

Trước khi tích hợp hoặc dùng phân tích, cần xác nhận: (a) đủ 43 mã HOSE và đủ coverage từ 19/11/2021; (b) price basis và corporate-action handling; (c) định nghĩa/đơn vị Volume; (d) query/page/rate constraints; (e) phí, quyền lưu/trích dẫn/chia sẻ phục vụ đồ án; (f) dữ liệu historical có sửa hồi tố hay không; (g) nguồn feed thực tế và timezone.

## 9. Thông tin chưa xác minh và câu hỏi nhà cung cấp

### SSI

1. Daily OHLC endpoint trả giá raw hay adjusted? Adjusts các sự kiện nào và có hồi tố toàn lịch sử không?
2. Open/High/Low/Close có cùng cơ sở điều chỉnh không? Volume có điều chỉnh theo corporate action không?
3. Coverage cho 43 mã của nhóm tại đúng account/permission và giai đoạn từ 19/11/2021; symbol đã ngừng/đổi mã được xử lý ra sao?
4. Page size tối đa, giới hạn ngày/request, quota thực của data-ohlc, retry guidance; định dạng `from/to` chuẩn do docs đang có khác biệt.
5. Thủ tục đăng ký hiện tại do FAQ và registration guide mô tả khác nhau.
6. Chi phí dịch vụ/API so với market data license; quyền lưu trữ, phân tích, trình bày trong báo cáo/slides/demo và chia sẻ file với giảng viên.

### DNSE

1. Có historical daily data từ 2021 cho từng mã HOSE trong phạm vi không; mã mới niêm yết/đổi mã được xử lý thế nào?
2. OHLC là raw hay adjusted; có Adjusted Close/adjusted OHLC, corporate-action methodology/back-adjustment không?
3. `from/to` có giới hạn độ dài nào, daily timestamp theo timezone nào, `nextTime` dùng paging theo hướng nào và có maximum bars không?
4. Rate/Quota cụ thể cho `/price/ohlc`, concurrency/retry rules; hiện rate limits page không cho con số OHLC-specific.
5. Header timestamp phải là `Date` hay `X-Aux-Date` cho endpoint này; theo tài liệu chung và endpoint có khác biệt tên.
6. Có phí API/market data hoặc giới hạn theo gói tài khoản không; quyền dùng nội bộ trong nghiên cứu, công bố trong slide/báo cáo và lưu trữ bản tải.
7. Volume gồm giao dịch khớp lệnh nào, có bao gồm thỏa thuận không; đơn vị giá/khối lượng.

## 10. Hạn chế khảo sát

- Chỉ đọc tài liệu công khai chính thức; không xác thực bằng response API thực tế.
- Không có API Key/quyền tài khoản để kiểm tra coverage, lịch sử, quota hoặc schema runtime.
- Tài liệu có điểm bất nhất (SSI đăng ký, định dạng ngày; DNSE tên header thời gian) và khoảng trống (giới hạn/history depth, giá basis).
- “API không thu phí” không được diễn giải thành dữ liệu không có license/redistribution restriction.
- Không có nguồn nào trong tài liệu đã kiểm tra đủ căn cứ để xác nhận Adjusted Close hoặc adjusted OHLC đáng tin cậy cho chuỗi rủi ro hiện tại.

## 11. Bước tiếp theo

1. Nhóm liên hệ SSI và DNSE bằng các câu hỏi ở Mục 9, đặc biệt về basis giá, coverage lịch sử và quyền nghiên cứu/công bố.
2. Sau khi có trả lời/điều khoản và tài khoản hợp lệ, nhóm quyết định có cho phép một thử nghiệm nhỏ 3–5 mã hay không. Trước khi có quyết định đó không tải/nhập dữ liệu.
3. Nếu thử nghiệm được duyệt, lưu dữ liệu riêng biệt theo nguồn, giữ response/provenance và báo cáo kiểm định coverage/chất lượng trước khi cân nhắc thay nguồn.
4. Chỉ đề xuất tính risk features sau khi nhóm/giảng viên phê duyệt cơ sở giá và cách xử lý corporate actions.

## 12. Tài liệu tham khảo

Các trang dưới đây được truy cập ngày **20/11/2026**.

### SSI

- [data-ohlc API reference](https://developers.ssi.com.vn/en/docs/api-reference/data-ohlc)
- [Quick Start / First API Call](https://developers.ssi.com.vn/en/docs/getting-started/first-api-call)
- [Getting API Keys / Access Tokens](https://developers.ssi.com.vn/en/docs/getting-started/api-keys)
- [Registration and Activation Process](https://developers.ssi.com.vn/en/docs/getting-started/registration)
- [Terms of Use & Environments, rate and data limits](https://developers.ssi.com.vn/en/docs/getting-started/terms-and-environments)
- [FastConnect Service FAQ](https://developers.ssi.com.vn/en/docs/faq/service-overview)
- [Corporate Actions API](https://developers.ssi.com.vn/en/docs/api-reference/data-corporateActions)

### DNSE

- [Lịch sử OHLC](https://developers.dnse.com.vn/docs/dnse/get-ohlc-history/)
- [Hướng dẫn xác thực](https://developers.dnse.com.vn/docs/guide/intro/authentication/)
- [Rate Limits](https://developers.dnse.com.vn/docs/guide/ratelimits/)
- [FAQ DNSE OpenAPI](https://developers.dnse.com.vn/docs/guide/faq/)
- [Lịch sử sự kiện quyền theo tài khoản](https://developers.dnse.com.vn/docs/dnse/get-corporate-action-history/)
- [Điều khoản dịch vụ DNSE](https://www.dnse.com.vn/dieu-khoan-dich-vu)

**Kết luận Giai đoạn 2.7:** SSI hiện là ứng viên ưu tiên cho thử nghiệm đối chiếu nhờ cam kết tài liệu về daily history và phân trang rõ hơn. DNSE là phương án dự phòng khả thi ở mức endpoint schema. Tuy nhiên, chưa nguồn nào được kiểm thử thực tế trong dự án, chưa xác minh quyền/chi phí cho mục đích học thuật, coverage 43 mã, hoặc basis điều chỉnh. **Không nguồn nào được tự động chọn làm nguồn thay thế CafeF.**
