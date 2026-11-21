# KẾ HOẠCH XÁC MINH NHÀ CUNG CẤP DỮ LIỆU

**Giai đoạn:** 2.8 – chuẩn bị xác minh nhà cung cấp  
**Ngày lập:** 20/11/2026  
**Phạm vi dự kiến:** OHLCV của 43 doanh nghiệp HOSE trong giai đoạn 19/11/2021–18/11/2026.

## 1. Mục tiêu

Chuẩn bị bộ câu hỏi và bảng ghi nhận bằng chứng để nhóm chủ động xác minh CafeF, SSI FastConnect và DNSE OpenAPI. Mục tiêu là biết nguồn nào có dữ liệu OHLCV đủ độ phủ, cơ sở giá có thể giải thích, và điều khoản cho phép dùng trong đồ án.

Tài liệu này chỉ chuẩn bị nội dung liên hệ. **Chưa liên hệ nhà cung cấp, chưa gọi API, chưa nhận/tạo credentials, chưa tải dữ liệu, và chưa lựa chọn nguồn thay thế CafeF.** Kết luận Giai đoạn 2.6 vẫn giữ nguyên: chưa đủ bằng chứng sử dụng Adjusted Close hoặc OHLC để tính Daily Return/Volatility.

## 2. Câu hỏi dành cho CafeF

Khi nhóm liên hệ, nên yêu cầu trả lời bằng email/tài liệu có thể lưu làm bằng chứng và nêu phiên bản/ngày áp dụng.

1. Công thức chính xác và quy tắc làm tròn của trường **Adjusted Close/Điều chỉnh** là gì? Đơn vị của giá là gì?
2. Trường này điều chỉnh những sự kiện nào: cổ tức tiền mặt, cổ tức bằng cổ phiếu, cổ phiếu thưởng, quyền mua, chia/tách/gộp, phát hành khác, hay sự kiện nào khác?
3. **Open, High, Low** có được điều chỉnh cùng basis, cùng hệ số và cùng lịch sử với Adjusted Close không? **Close** là giá khớp thực tế chưa điều chỉnh hay có xử lý khác?
4. Khi có corporate action, CafeF có back-adjust toàn bộ chuỗi quá khứ không? Nếu có, thời điểm cập nhật, phạm vi lịch sử và cách xử lý nhiều sự kiện đồng thời là gì?
5. Có data dictionary, methodology note, ví dụ tính đã được kiểm chứng hoặc mô tả thay đổi phương pháp theo thời gian không?
6. Các trường giá và Volume có đơn vị/định nghĩa nào; Volume gồm khớp lệnh, thỏa thuận hay cả hai? Các giá trị lịch sử có thể được sửa hồi tố không?
7. Có thể xuất/được cấp OHLCV cho 43 mã trong toàn kỳ 19/11/2021–18/11/2026 không? Có giới hạn export, phí hoặc yêu cầu tài khoản không?
8. Điều khoản hiện hành cho phép lưu trữ, phân tích học thuật, đưa trích đoạn/biểu đồ vào báo cáo và slide, trình bày demo, hoặc chia sẻ bộ dữ liệu với giảng viên/nhóm ở mức nào?

## 3. Câu hỏi dành cho SSI FastConnect

1. Với quyền truy cập dự kiến, endpoint OHLC có đủ dữ liệu daily cho 43 mã HOSE từ **19/11/2021** đến **18/11/2026** không? Có mã đổi tên, hủy niêm yết hoặc chưa đủ lịch sử được xử lý thế nào?
2. OHLC trả về là giá giao dịch **raw/chưa điều chỉnh** hay đã điều chỉnh? SSI có cung cấp Adjusted Close hoặc adjusted OHLC riêng không?
3. Endpoint OHLC xử lý cổ tức tiền mặt, cổ tức cổ phiếu/cổ phiếu thưởng, quyền mua, chia/tách/gộp và các đợt phát hành khác ra sao? Có back-adjust dữ liệu lịch sử không?
4. Open/High/Low/Close có cùng basis và cùng quy tắc điều chỉnh không? Có tài liệu/mẫu minh chứng được không?
5. Volume được tính theo định nghĩa nào, đơn vị gì, gồm giao dịch thỏa thuận không? Trường `value` có đơn vị gì?
6. Giới hạn OHLC cụ thể: pageSize tối đa, số ngày tối đa mỗi request, quota theo API key/endpoint, giới hạn đồng thời và hướng dẫn xử lý 429 là gì?
7. Tài liệu hiện có khác nhau về định dạng `from/to` (`YYYY/MM/DD` và `YYYY-MM-DD`) và quy trình đăng ký. Định dạng/API version cùng quy trình đăng ký/duyệt hiện hành nào áp dụng cho tài khoản của nhóm?
8. Có phí dịch vụ/API, phí market data hoặc điều kiện gói tài khoản nào ngoài phí API được FAQ nhắc đến không?
9. Điều khoản có cho phép tải, lưu trữ, phân tích và trình bày dữ liệu trong đồ án học tập; chia sẻ báo cáo/slide và file dữ liệu thô với giảng viên/nhóm không? Có yêu cầu ghi nguồn hoặc hạn chế tái phân phối nào?
10. Endpoint corporate actions có độ phủ/lịch sử bao lâu, gồm những loại sự kiện nào, và có thể tra cứu theo toàn thị trường hay chỉ phạm vi khác? Dữ liệu đó có liên kết chính thức với OHLC không?

## 4. Câu hỏi dành cho DNSE OpenAPI

1. Endpoint OHLC history có dữ liệu daily cho đủ 43 mã HOSE từ năm 2021, cụ thể từ **19/11/2021**, đến **18/11/2026** không? Yêu cầu quyền hoặc gói dịch vụ nào?
2. OHLC trả về là raw/chưa điều chỉnh hay đã điều chỉnh? Có trường Adjusted Close/adjusted OHLC hoặc phương pháp back-adjust được công bố không?
3. Cách xử lý cổ tức tiền, cổ tức cổ phiếu/cổ phiếu thưởng, quyền mua, chia/tách/gộp và các corporate actions khác là gì? Open/High/Low/Close có cùng basis không?
4. Timestamp của candle `1D` đại diện thời điểm nào; timezone là UTC, giờ Việt Nam hay quy ước khác? Việc ánh xạ timestamp sang ngày giao dịch phải thực hiện ra sao?
5. `nextTime` dùng để tiếp tục lấy lịch sử theo hướng thời gian nào? Điều kiện dừng là gì? Có maximum duration hoặc maximum bars cho mỗi request không?
6. Rate/quota riêng của `/price/ohlc` là bao nhiêu theo giờ/ngày, giới hạn đồng thời và retry/backoff thế nào? Bảng công khai có nêu giới hạn endpoint khác nhưng chưa thấy con số cụ thể cho OHLC.
7. `Volume` tính những giao dịch nào, có gồm thỏa thuận không, đơn vị ra sao? Có thay đổi định nghĩa theo thị trường/sàn không?
8. Header thời gian endpoint cần dùng chính xác là `Date` hay `X-Aux-Date`; version header nào hiện hành và signing string/nonce áp dụng theo tài liệu nào?
9. Có phí API/market data hoặc yêu cầu gói tài khoản nào? Điều khoản cho phép lưu trữ, nghiên cứu học thuật, đưa dữ liệu/biểu đồ vào báo cáo, slide/demo và chia sẻ với giảng viên ở mức nào?
10. API corporate action hiện được mô tả theo lịch sử quyền trên tài khoản. DNSE có nguồn lịch sử corporate actions toàn thị trường đủ cho 43 mã không? Nguồn đó có giải thích quan hệ với giá OHLC không?

## 5. Bảng theo dõi xác minh

Trạng thái khởi tạo cho tất cả mục là **Chưa liên hệ**. Sau khi gửi câu hỏi, chỉ đổi trạng thái khi có phản hồi/bằng chứng lưu lại. Gợi ý các trạng thái tiếp theo: `Đã gửi – chờ phản hồi`, `Đã trả lời – cần làm rõ`, `Đã xác minh`, `Không cung cấp`, `Chưa đủ bằng chứng`.

| Nhà cung cấp | Câu hỏi | Trạng thái | Câu trả lời | Tài liệu minh chứng | Kết luận | Ghi chú |
|---|---|---|---|---|---|---|
| CafeF | Công thức Adjusted Close và quy tắc làm tròn? | Chưa liên hệ | — | — | Chưa xác minh | Yêu cầu tài liệu phương pháp bằng văn bản. |
| CafeF | Corporate actions nào được điều chỉnh? | Chưa liên hệ | — | — | Chưa xác minh | Tách riêng từng loại sự kiện. |
| CafeF | OHLC có cùng basis với Adjusted Close không? Close là raw hay có điều chỉnh? | Chưa liên hệ | — | — | Chưa xác minh | Cần trả lời cho từng trường. |
| CafeF | Có back-adjust toàn lịch sử? Thời điểm/cách cập nhật? | Chưa liên hệ | — | — | Chưa xác minh | Hỏi xử lý nhiều sự kiện cùng ngày. |
| CafeF | Có data dictionary/methodology và đơn vị dữ liệu không? | Chưa liên hệ | — | — | Chưa xác minh | Bao gồm định nghĩa Volume/value. |
| CafeF | Coverage/export 43 mã, phí và giới hạn? | Chưa liên hệ | — | — | Chưa xác minh | Kiểm tra đủ kỳ nghiên cứu. |
| CafeF | Quyền dùng/lưu/chia sẻ trong đồ án? | Chưa liên hệ | — | — | Chưa xác minh | Hỏi cả báo cáo, slide, demo và file dữ liệu. |
| SSI | Coverage 43 mã HOSE trong 19/11/2021–18/11/2026? | Chưa liên hệ | — | — | Chưa xác minh | Cần xác minh từng mã và trường hợp đổi/hủy mã. |
| SSI | OHLC raw hay adjusted? Có adjusted series riêng? | Chưa liên hệ | — | — | Chưa xác minh | Không suy luận từ endpoint/schema. |
| SSI | Xử lý từng corporate action và back-adjust? | Chưa liên hệ | — | — | Chưa xác minh | Cổ tức tiền/cổ phiếu, thưởng, quyền mua, split/reverse split. |
| SSI | OHLC cùng basis? Định nghĩa/đơn vị Volume và value? | Chưa liên hệ | — | — | Chưa xác minh | Hỏi riêng thành phần thỏa thuận. |
| SSI | Page size, range/request, quota, concurrency, 429? | Chưa liên hệ | — | — | Chưa xác minh | Xin giới hạn riêng endpoint OHLC. |
| SSI | Định dạng ngày và thủ tục đăng ký hiện hành? | Chưa liên hệ | — | — | Chưa xác minh | Docs đang có ví dụ không thống nhất. |
| SSI | Phí API/market data và quyền sử dụng học thuật? | Chưa liên hệ | — | — | Chưa xác minh | Xin điều khoản áp dụng cho account. |
| SSI | Coverage/lịch sử corporate-action API và liên kết với OHLC? | Chưa liên hệ | — | — | Chưa xác minh | Phân biệt event data với adjusted price. |
| DNSE | Coverage 43 mã từ 19/11/2021 đến 18/11/2026? | Chưa liên hệ | — | — | Chưa xác minh | Tài liệu public chưa chốt history depth. |
| DNSE | OHLC raw hay adjusted? Có adjusted series? | Chưa liên hệ | — | — | Chưa xác minh | Không suy luận từ tên trường. |
| DNSE | Corporate actions và back-adjust được xử lý ra sao? | Chưa liên hệ | — | — | Chưa xác minh | Hỏi riêng từng loại sự kiện và OHLC basis. |
| DNSE | Timestamp daily candle và timezone? | Chưa liên hệ | — | — | Chưa xác minh | Cần quy tắc ánh xạ ngày giao dịch. |
| DNSE | `nextTime`, maximum duration/bars và pagination? | Chưa liên hệ | — | — | Chưa xác minh | Xin ví dụ lấy liên tiếp khoảng lịch sử. |
| DNSE | Rate/quota OHLC, concurrency và retry? | Chưa liên hệ | — | — | Chưa xác minh | Không áp hạn mức endpoint khác. |
| DNSE | Định nghĩa và đơn vị Volume? | Chưa liên hệ | — | — | Chưa xác minh | Hỏi bao gồm giao dịch thỏa thuận hay không. |
| DNSE | Header thời gian/version/signature hiện hành? | Chưa liên hệ | — | — | Chưa xác minh | Đối chiếu endpoint docs với auth guide/SDK. |
| DNSE | Phí và quyền sử dụng trong đồ án? | Chưa liên hệ | — | — | Chưa xác minh | Xin phạm vi lưu, trích dẫn, công bố/chia sẻ. |
| DNSE | Có corporate-action history toàn thị trường và quan hệ với OHLC? | Chưa liên hệ | — | — | Chưa xác minh | Tách khỏi lịch sử quyền theo tài khoản. |

## 6. Điều kiện cho phép thử nghiệm API

Chỉ đề xuất/tiến hành thử nghiệm nhỏ sau khi **đồng thời** đáp ứng các điều kiện sau:

1. Người dùng/nhóm có quyền truy cập hợp lệ do chính chủ tài khoản đăng ký; credentials không được đưa vào báo cáo, mã nguồn hay chat.
2. Nhóm đã đọc và hiểu điều khoản hiện hành, phí, quyền lưu trữ, phân tích, trình bày và chia sẻ kết quả phục vụ đồ án.
3. Cơ sở giá được provider giải thích bằng tài liệu; nếu chưa giải thích được, phải có phương án đối chiếu được nhóm/giảng viên chấp thuận và không được coi chuỗi là adjusted đã xác minh.
4. Coverage, giới hạn truy vấn, đơn vị giá/Volume, timestamp/timezone và cách lấy tiếp dữ liệu đã được làm rõ đủ để thiết kế thử nghiệm an toàn.
5. Nhóm đồng ý rõ ràng cho phép thử nghiệm phạm vi nhỏ (3–5 mã, gồm ngày thường và cửa sổ quanh sự kiện); chưa đồng ý tải toàn bộ 43 mã.

Khi thử nghiệm được duyệt, dữ liệu cần được lưu tách theo nguồn và kèm thời điểm tải, tham số, phiên bản tài liệu/API, mã nguồn gốc, điều khoản và response gốc. Kết quả phải được kiểm tra thực tế; HTTP 200 đơn lẻ không được coi là thu thập thành công.

## 7. Ranh giới và trạng thái

- Đây là tài liệu chuẩn bị; không gửi câu hỏi thay nhóm và không tự liên hệ CafeF, SSI hoặc DNSE.
- Không gọi API, tạo API Key/Secret, dùng OTP/token hoặc tải dữ liệu.
- Không thay đổi Raw, Processed, CSV hoặc cấu trúc ứng dụng.
- Không tính Daily Return/Volatility, không tạo Feature Engineering, không chạy phân cụm.
- Mọi câu hỏi trong bảng đang ở trạng thái **Chưa liên hệ**; chưa có câu trả lời hay kết luận mới từ nhà cung cấp.

## 8. Tài liệu nền đã đọc

Các tài liệu dự án được xem ngày 20/11/2026:

- `PROJECT_CONTEXT.md`
- `PROJECT_PROGRESS.md`
- `CHANGELOG.md`
- `reports/BAO_CAO_KHAO_SAT_NGUON_DU_LIEU_GIA.md`
- `reports/BAO_CAO_XAC_MINH_CO_SO_GIA.md`

Tham khảo các hướng dẫn chính thức đã liệt kê trong báo cáo khảo sát Giai đoạn 2.7. Báo cáo xác minh cơ sở giá là căn cứ duy trì trạng thái chưa được phép tính lợi suất/volatility.
