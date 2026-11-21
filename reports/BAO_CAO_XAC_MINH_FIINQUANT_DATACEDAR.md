# Báo cáo xác minh FiinQuant và DataCedar

**Giai đoạn:** 2.15 – Xác minh nhà cung cấp dữ liệu  
**Ngày truy cập tài liệu:** 20/11/2026  
**Phạm vi cần đáp ứng:** OHLCV ngày cho 43 mã HOSE, từ 19/11/2021 đến 18/11/2026; nghiên cứu rủi ro biến động giá cổ phiếu.

## 1. Kết luận

Chưa có đủ căn cứ để đăng ký/mua và dùng dữ liệu của bất kỳ nhà cung cấp nào cho đồ án. Tài liệu công khai xác nhận năng lực kỹ thuật ở các mức khác nhau, nhưng chưa xác nhận đồng thời quyền lưu dữ liệu nguồn, quyền nộp bản dữ liệu cho giảng viên và quyền hiển thị kết quả trên website demo.

- **FiinQuant:** ứng viên ưu tiên để xin xác nhận bằng văn bản. Tài liệu chính thức mô tả OHLCV lịch sử, lựa chọn adjusted/unadjusted và gói lịch sử tới 5 năm trở lên. Tuy nhiên, bảng giá có các thông tin độ sâu không đồng nhất; 43 mã và quyền sử dụng cụ thể của nhóm chưa được xác minh. Điều khoản nói được tạo sản phẩm phái sinh có trích nguồn, nhưng đồng thời hạn chế chuyển giao thông tin liên quan hệ thống và cung cấp dịch vụ cho bên thứ ba.
- **DataCedar:** ứng viên dự phòng về kỹ thuật và chi phí niêm yết. Tài liệu API mô tả OHLCV, raw/adjusted, corporate actions, Volume tính bằng shares và gói Quant $29/tháng có daily history back-to-listing. Nhưng trang giá tổng quát và trang lịch sử/API có thông tin cửa sổ dữ liệu khác nhau; điều khoản quyền sử dụng cho đồ án, lưu trữ và hiển thị chưa được xác minh. DataCedar nêu rõ truy cập API không tự cấp quyền sở hữu hay tái phân phối dữ liệu.
- **Quyết định:** chưa chọn nguồn chính thức. “Ưu tiên” dưới đây chỉ là thứ tự cần xác minh, không phải phê duyệt dữ liệu.

Không liên hệ nhà cung cấp, đăng ký tài khoản, thanh toán, gọi API hoặc tải dữ liệu trong giai đoạn này. Không sửa Raw/Processed; không thực hiện Feature Engineering hoặc clustering.

## 2. Cách phân loại bằng chứng

- **Đã xác minh từ tài liệu:** nội dung có thể đọc trực tiếp trên trang/tài liệu chính thức; đây là xác minh nội dung công bố, không phải xác minh chất lượng response thực tế.
- **Chưa xác minh:** tài liệu không trả lời, không đủ rõ, mâu thuẫn, hoặc cần xác nhận bằng văn bản/hợp đồng.
- **Nhận định:** đánh giá khả năng phù hợp với phạm vi ASM, không phải cam kết của nhà cung cấp.

Không có thử nghiệm API nên chưa thể xác minh thực tế 43 mã, ngày đầu/cuối, dữ liệu thiếu/trùng, OHLC, volume, corporate actions hay sai khác so với CafeF.

## 3. Bảng so sánh theo câu hỏi bắt buộc

| Câu hỏi | FiinQuant | DataCedar |
|---|---|---|
| **1. OHLCV ngày cho 43 mã HOSE?** | **Một phần đã xác minh:** tài liệu Python có trường open/high/low/close/volume, chu kỳ `1d`; bảng giá ghi dữ liệu lịch sử OHLCV, số mã lịch sử “không giới hạn” ở gói trả phí. Chưa có xác nhận coverage từng mã trong universe HOSE hoặc response cho 43 mã. | **Công bố chính thức, chưa kiểm tra response:** trang HOSE tuyên bố 405 listings, mỗi mã có trang/API; API có OHLCV ngày. Trang cũng cảnh báo daily coverage thay đổi theo mã/phiên có nguồn, nên số listings không bảo đảm dữ liệu liên tục. Chưa đối chiếu đủ 43 mã. |
| **2. Lịch sử 19/11/2021–18/11/2026?** | Trang giá có bảng ghi độ sâu 1/3/5/10 năm và bảng khác ghi 1/10/10/15/15 năm; tài liệu/báo giá giáo dục trước đó nêu EOD tới 15 năm. Do các bảng không khớp và giá trị gói web không hiển thị đầy đủ, chưa kết luận gói cụ thể đáp ứng chính xác cửa sổ 5 năm cho OHLCV. | Tài liệu API/historical-data ghi gói Quant có daily bars back-to-listing; Explorer miễn phí một năm. Tuy vậy, trang Pricing tổng quát ghi “30 days of history” cho Quant trong khi tài liệu lịch sử chuyên biệt nói daily back-to-listing. Cần xác nhận entitlement áp dụng cho HOSE và thời điểm 2021. |
| **3. Giá chưa điều chỉnh và điều chỉnh?** | **Đã xác minh ở mức giao diện:** hàm lịch sử nhận `adjusted=True/False`. Không thấy công thức điều chỉnh hoặc cam kết rõ rằng từng trường OHLC được điều chỉnh nhất quán thế nào. | **Đã xác minh theo mô tả API:** hỗ trợ `raw`, `split`, `dividend`, `all`; tài liệu giải thích `all` áp dụng factor tích lũy split và dividend cho các bar trước ngày sự kiện. Cần làm rõ phạm vi event, cách xử lý từng loại quyền và độ bao phủ HOSE thực tế. |
| **4. Corporate Actions?** | **Một phần:** FiinGroup có sản phẩm/API Datafeed đề cập Corporate Actions; tài liệu công khai được xem chưa chứng minh bộ sự kiện, lịch sử 43 mã, event types, công thức điều chỉnh giá hay khả năng truy cập trong gói FiinQuant được báo giá. | **Một phần:** API có endpoint actions cho cash dividends và splits. Chưa thấy tài liệu chứng minh đầy đủ quyền mua, cổ tức/cổ phiếu thưởng, event corrections hoặc mức bao phủ lịch sử; không suy ra endpoint này bao gồm mọi loại sự kiện. |
| **5. Định nghĩa/đơn vị Volume?** | Tài liệu định nghĩa `volume` là **matching order volume**. Kiểu trả về/đơn vị cổ phiếu hay lô, và việc có/không gồm giao dịch thỏa thuận chưa được xác nhận. Không coi là tổng volume tương đương CafeF khi chưa đối chiếu. | Schema ghi `volume` là số shares, được serialize dưới dạng chuỗi. Trang thị trường HOSE ghi tiền tệ VND. Chưa thấy tách matched/negotiated hoặc xác nhận đầy đủ quy tắc cộng gộp volume của HOSE. |
| **6. Được tải và lưu dữ liệu trên máy?** | API trả dữ liệu để người dùng xử lý trong Python là năng lực kỹ thuật, không tự chứng minh quyền giữ bản raw. Điều khoản được xem chưa nói rõ thời hạn lưu CSV cục bộ, lưu sau khi hết gói hoặc lưu bản gửi giảng viên. **Chưa xác minh quyền.** | API trả JSON qua key; tài liệu nói không có file export/anonymous download. Tài liệu công khai chưa cấp quyền rõ cho lưu cache/raw lâu dài, giữ sau khi kết thúc gói hay lưu bản nộp. **Chưa xác minh quyền.** |
| **7. Dùng cho đồ án sinh viên?** | Trang giới thiệu hướng tới hỗ trợ trường đại học/giảng dạy (theo khảo sát trước) và Terms cho phép sản phẩm phái sinh có trích nguồn. Đây không thay thế giấy phép cụ thể về dữ liệu nguồn, bản nộp, hoặc điều kiện của gói sinh viên. **Cần xác nhận.** | Tài liệu mô tả mục tiêu research/screening/backtesting, nhưng mục tiêu sản phẩm không phải giấy phép học thuật. Data Rights nói quyền phụ thuộc rights registry theo nguồn. **Chưa có bằng chứng cấp phép cụ thể cho nhóm.** |
| **8. Hiển thị biểu đồ/kết quả trên website demo?** | Điều khoản cho phép sản phẩm phái sinh có trích nguồn, song cũng cấm chuyển giao/tiết lộ thông tin/tài liệu liên quan hệ thống và dùng hệ thống cung cấp dịch vụ cho bên thứ ba. Chưa rõ dashboard demo riêng tư/công khai, số liệu tổng hợp hay biểu đồ được phép đến đâu. **Không hiển thị dữ liệu trước khi có văn bản.** | Không tìm thấy quyền công khai rõ ràng cho hiển thị dữ liệu hoặc kết quả dẫn xuất trên demo. Website có trang mã công khai không chứng minh khách hàng được tái xuất dữ liệu trong sản phẩm riêng. **Chưa xác minh.** |
| **9. Lưu dữ liệu trong phát triển/kiểm thử?** | Chưa có điều khoản công khai rõ về cache, fixture trích từ dữ liệu thực, bản local staging hoặc thời gian lưu. Sự cho phép tạo sản phẩm phái sinh không được tự diễn giải thành quyền giữ raw. | Chưa xác minh quyền lưu trong staging/dev/test. Data Rights nhấn mạnh API transport không làm phát sinh quyền sở hữu/tái phân phối; cần license/rights cho chính các source responses. |
| **10. Chi phí đúng phạm vi?** | **Chưa có giá chính xác cho 43 mã × OHLCV ngày × 5 năm.** Trang giá xác nhận nhiều tier/lịch sử nhưng số tiền trong bản công khai truy cập được không hiển thị; các bảng độ sâu mâu thuẫn. Báo giá giáo dục XLSX được khảo sát trước nêu **87.080.832 VND/12 tháng** cho gói Chuyên nghiệp rộng (sau chiết khấu và VAT), nhưng không phải báo giá OHLCV-only, thông tin người nhận/ngày phát hành còn trống và không thể dùng làm quote ràng buộc. Cần quote mới cho đúng scope. | Giá niêm yết ở trang lịch sử chuyên biệt/API: **Quant $29/tháng**. Thuế được tính trước thanh toán; chưa xác minh chi phí cuối, entitlement 2021–2026 cho HOSE, quyền lưu trữ/hiển thị, hay việc cần đăng ký bổ sung. Giá trang Pricing tổng quát có mô tả cửa sổ lịch sử không đồng nhất với tài liệu chuyên biệt. |

## 4. Nhận định từng nguồn

### 4.1 FiinQuant

**Điểm phù hợp:** tài liệu chính thức nêu API Python lịch sử với OHLCV, chọn adjusted/unadjusted, khoảng ngày và timeframe ngày. Trang giá thể hiện gói lịch sử không giới hạn mã cho các gói trả phí, cùng một bảng có chiều sâu 5 năm; về mặt thiết kế có khả năng đáp ứng universe 43 mã và kỳ dữ liệu.

**Điểm chưa đủ:** chưa có xác nhận coverage 43 mã/đủ ngày; semantics price adjustment và Corporate Actions chưa đủ chi tiết; định nghĩa Volume mới dừng ở khớp lệnh; quyền lưu raw, nộp dữ liệu, cache phục vụ kiểm thử và demo website chưa rõ. Giá công khai không cho ra báo giá chính xác cho scope ASM và các bảng lịch sử mâu thuẫn. Điều khoản có các giới hạn về chuyển giao/tiết lộ và cung cấp dịch vụ bên thứ ba; không nên tự diễn giải rằng mọi dashboard đều bị cấm hoặc đều được phép.

**Đánh giá:** phù hợp làm **nguồn ưu tiên để xin xác nhận/quote**, chưa được phê duyệt làm nguồn nghiên cứu.

### 4.2 DataCedar

**Điểm phù hợp:** tài liệu API mô tả schema OHLCV, batch bars, phân trang/cursor, lịch sử daily, các lựa chọn giá raw/adjusted, actions endpoint, currency VND trên trang HOSE và Volume bằng shares. Gói Quant được tài liệu lịch sử chuyên biệt niêm yết $29/tháng và ghi daily history back-to-listing.

**Điểm chưa đủ:** trang Pricing chung và docs chuyên biệt không nhất quán về cửa sổ lịch sử của Quant; HOSE page là công bố coverage chứ chưa thay thế API audit 43 mã; adjustment/events chưa chứng minh đầy đủ các corporate actions cần thiết. Terms không truy xuất được trong lần khảo sát; Data Rights page không cấp quyền sử dụng cụ thể mà nói quyền phụ thuộc rights registry. Quyền lưu trữ, nộp dữ liệu, sử dụng học thuật và hiển thị demo vì thế vẫn là điểm chặn.

**Đánh giá:** chỉ giữ làm **nguồn dự phòng để hỏi license**, không mua/chạy thử trước khi giải quyết quyền sử dụng và mâu thuẫn history window.

## 5. Câu hỏi cần gửi nhà cung cấp

### Gửi FiinQuant

1. Gói cụ thể nào cho phép OHLCV daily của đúng 43 ticker HOSE từ 19/11/2021 đến 18/11/2026? Xin xác nhận bằng danh sách mã và ngày khả dụng; giải thích bảng độ sâu lịch sử trên Pricing.
2. Giá của gói tối thiểu đáp ứng phạm vi trên là bao nhiêu, đã gồm VAT/chi phí cài đặt chưa; có gói sinh viên/nhóm đồ án hay chỉ gói tổ chức?
3. Xin data dictionary cho `adjusted=True/False`: công thức, loại Corporate Actions, thời điểm back-adjust, điều chỉnh từng trường OHLC và chính sách sửa lịch sử.
4. `volume` là số cổ phiếu hay lô; gồm khớp lệnh liên tục/định kỳ/thỏa thuận nào? Có trường total volume riêng không?
5. Nhóm có thể tải và lưu CSV raw trong máy/ổ nhóm, tạo bản staging trong thời gian phát triển, giữ bản sau khi hết gói và nộp cho giảng viên không?
6. Nhóm có thể đăng biểu đồ và kết quả dẫn xuất (không cung cấp CSV/raw) lên website demo không? Xin phân biệt demo nội bộ, link giới hạn truy cập và website công khai.
7. Điều khoản hiện tại có cần phụ lục/giấy phép riêng cho sử dụng học thuật và website demo không? Xin cung cấp văn bản áp dụng và yêu cầu attribution.

### Gửi DataCedar

1. Xác nhận đủ daily OHLCV cho danh sách 43 mã HOSE, từng mã có lịch sử bắt đầu không muộn hơn 19/11/2021 và kết thúc ít nhất 18/11/2026; nếu không, nêu mã/ngày thiếu.
2. Xác nhận Quant $29/tháng mở daily history back-to-listing cho HOSE. Vì Pricing tổng quát ghi 30 ngày trong khi trang API/historical ghi back-to-listing, điều khoản nào áp dụng?
3. Cung cấp Terms/contract và xác nhận rights registry hiện hành của từng mã HOSE; upstream provenance/rights cho phép nhà cung cấp cấp dữ liệu này ở phạm vi nào?
4. Nhóm được lưu raw local/staging, giữ dữ liệu sau khi subscription hết hạn, chia sẻ file với giảng viên, và dùng trong đồ án không thương mại không?
5. Có được hiển thị biểu đồ và metrics dẫn xuất trên dashboard demo; điều kiện khác nhau thế nào giữa demo nội bộ và website công khai? Có được xuất báo cáo/slide không?
6. Xin mô tả event ledger và công thức `split`, `dividend`, `all`: loại cổ tức tiền, cổ tức/cổ phiếu thưởng, quyền mua, split/reverse split nào được hỗ trợ; OHLC điều chỉnh nhất quán ra sao?
7. Xác nhận `volume` là shares và phản ánh loại giao dịch nào; có bao gồm thỏa thuận không?
8. Xác nhận tổng chi phí gồm VAT/thuế, và quota/hạn mức 43 mã, batch, cursor, lưu dữ liệu áp dụng cho tài khoản Quant.

Không có nhà cung cấp nào được liên hệ trong báo cáo này.

## 6. Ma trận quyết định hiện tại

| Tiêu chí | FiinQuant | DataCedar |
|---|---|---|
| Năng lực OHLCV daily theo tài liệu | Đã xác nhận mô tả API | Đã xác nhận schema API |
| Đủ 43 mã bằng response | Chưa xác minh | Chưa xác minh |
| Đủ kỳ 5 năm đúng gói | Chưa xác minh; bảng giá bất nhất | Chưa xác minh; history window bất nhất giữa trang |
| Raw/adjusted semantics | Có cờ lựa chọn; công thức chưa xác minh | Có mode raw/split/dividend/all; coverage event chưa xác minh |
| Volume/unit | Matching volume; unit và phạm vi giao dịch chưa rõ | Shares; phạm vi loại giao dịch chưa rõ |
| Quyền local storage/dev | Chưa xác minh | Chưa xác minh |
| Quyền dùng học thuật/nộp giảng viên | Chưa có giấy phép cụ thể | Chưa có giấy phép cụ thể |
| Quyền demo website | Chưa xác minh; điều khoản có giới hạn bên thứ ba | Chưa xác minh; rights tùy upstream registry |
| Chi phí phạm vi ASM | Chưa có quote chính xác | $29/tháng là giá niêm yết, entitlement/thuế/quyền còn mở |
| Trạng thái lựa chọn | **Ưu tiên xác minh** | **Dự phòng có điều kiện** |

## 7. Chi phí dự kiến và điều kiện

| Nhà cung cấp | Mốc chi phí có bằng chứng | Điều kiện trước khi chi |
|---|---:|---|
| FiinQuant | Báo giá giáo dục được khảo sát trước: 87.080.832 VND/12 tháng gồm VAT cho gói rộng; không phải quote dữ liệu riêng. Trang web hiện nêu các mức lịch sử nhưng không hiển thị giá số trong nội dung truy cập được. | Xin báo giá mới đúng 43 mã, EOD, ít nhất 5 năm; xác nhận quyền lưu, quyền dùng học thuật, nộp dữ liệu và demo. |
| DataCedar | Quant $29/tháng theo trang lịch sử/API; thuế tính trước thanh toán. | Làm rõ mâu thuẫn 30 ngày/back-to-listing, quyền upstream/source rights và quyền lưu/hiển thị; xác nhận 43 mã. |

> Không xem các giá trên là tổng chi phí được duyệt. Không thanh toán trước khi nhóm/giảng viên chấp thuận license và provider xác nhận phạm vi bằng văn bản.

## 8. Rủi ro quyền sử dụng dữ liệu

1. **Quyền truy cập khác quyền lưu trữ/phân phối.** Có thể gọi API không có nghĩa được giữ raw, đóng gói CSV hoặc đưa vào repository.
2. **Đồ án và demo có thể có phạm vi khác.** Nộp cho giảng viên, demo cho lớp, website public và chia sẻ file là các hành vi riêng cần được cấp quyền rõ.
3. **Dữ liệu nguồn/upstream.** DataCedar công khai cơ chế source-rights registry; cần biết quyền cụ thể gắn với response HOSE. FiinQuant mô tả nguồn thông tin chính thống nhưng chưa cung cấp lineage/license theo từng trường trong tài liệu đã xem.
4. **Giá hoặc gói không bảo đảm quyền.** Chi trả thuê bao không tự giải quyết quyền lưu, giữ sau thuê bao hoặc công bố kết quả.
5. **Sai khác phương pháp có thể làm sai risk features.** Dữ liệu adjusted, raw, volume khớp lệnh/tổng giao dịch và thời điểm sự kiện có thể khác nhau; không tính return/volatility cho đến khi chốt basis.
6. **Điều khoản thay đổi theo trang/gói/nguồn.** Lưu bản điều khoản, quote và câu trả lời chính thức có ngày hiệu lực trước khi dùng.

## 9. Đề xuất nguồn ưu tiên và dự phòng

- **Ưu tiên: FiinQuant để xin câu trả lời/quote trước.** Lý do: tài liệu Python có rõ tham số OHLCV, `adjusted`, timeframe và thời gian; có gói lịch sử 5 năm được nêu trong bảng giá. Điểm này chỉ làm FiinQuant ứng viên ưu tiên xác minh, không chứng minh API runtime hay quyền sử dụng phù hợp.
- **Dự phòng: DataCedar, chỉ khi rights/Terms được xác nhận bằng văn bản.** Lý do: API schema và price basis có mô tả chi tiết hơn, Volume được ghi theo shares và mức Quant niêm yết thấp hơn. Rào cản là quyền upstream/redistribution chưa rõ và mâu thuẫn lịch sử giữa trang giá chung với trang chuyên biệt.
- **Không chọn chính thức nguồn nào tại Stage 2.15.** Sau khi có trả lời, nếu một bên không xác nhận đủ quyền local storage, academic use, nộp báo cáo và website demo, loại bên đó dù có đủ dữ liệu hoặc giá thấp.

## 10. Điều kiện cho phép bước xác minh tiếp theo

Chỉ đề xuất trial/API read-only sau khi nhóm nhận được và duyệt:

1. Điều khoản/giấy phép bằng văn bản cho đúng mục đích, quyền lưu local/staging, thời hạn lưu và quyền chia sẻ với giảng viên.
2. Xác nhận quyền hiển thị biểu đồ/kết quả trên demo (nội bộ hay public), attribution và giới hạn dữ liệu hiển thị.
3. Quote cho đúng 43 mã × daily OHLCV × kỳ nghiên cứu; xác nhận lịch sử và coverage theo ticker.
4. Data dictionary về raw/adjusted, OHLC basis, Corporate Actions, Volume/units và chính sách sửa dữ liệu.
5. Nhóm cho phép thử nghiệm; chỉ dùng credentials do nhóm tự cấu hình trong môi trường bảo mật. Thử trước 3–5 mã, tách staging, không thay Raw/Processed.

## 11. Tài liệu chính thức đã xem

Ngày truy cập tất cả liên kết: **20/11/2026**.

### FiinQuant

1. [Historical data function](https://docs.fiinquant.vn/fiinquant-en/function-and-formula/historical-data-function) — OHLCV fields, adjusted True/False, timeframe, tickers, date/period inputs.
2. [Data retrieval](https://docs.fiinquant.vn/fiinquant-en/practical-application/data-retrieval) — cách đăng nhập và định nghĩa Volume là matching order volume.
3. [Pricing](https://fiinquant.vn/Pricing) — danh mục historical OHLCV, ticker limits và các bảng độ sâu history; nội dung có mâu thuẫn như đã nêu.
4. [Terms and privacy](https://fiinquant.vn/Home/Privacy) — điều khoản sản phẩm phái sinh, attribution, hạn chế chuyển giao/cung cấp dịch vụ; chính sách thu thập thông tin người dùng.
5. [FiinQuant 2026 quotation](https://fiinquant.vn/docs/FiinQuant_Quotation_Website_2026.xlsx) — báo giá giáo dục tham khảo đã được tóm tắt ở mục chi phí; không phải quote ràng buộc cho phạm vi ASM.
6. [FiinGroup API Datafeed](https://dff.fiingroup.vn/ApiDataFeed) — thông tin sản phẩm, gồm Corporate Actions; chưa chứng minh entitlement tương ứng trong FiinQuant.

### DataCedar

7. [Historical Stock Data API reference](https://datacedar.com/docs) — schema, auth, bar fields, pagination, rate limits, adjustment modes, history plan windows, corporate actions endpoint.
8. [Historical stock data API](https://datacedar.com/historical-stock-data-api) — mô tả daily history, adjustment modes, plan feature và giá; cần đối chiếu với Pricing chung.
9. [HOSE market page](https://datacedar.com/markets/hose) — claims về 405 listings, daily history và coverage theo symbol.
10. [Pricing](https://datacedar.com/pricing) — giá niêm yết và điều khoản billing; có nội dung lịch sử tổng quát cần làm rõ với tài liệu chuyên biệt.
11. [Data Rights and Takedown Requests](https://datacedar.com/data-rights) — transport không đồng nghĩa permission; response theo source-rights registry.
12. [Terms](https://datacedar.com/terms) — liên kết Terms có trên trang provider nhưng nội dung không tải được trong lần khảo sát; không kết luận về điều khoản chưa đọc được.

## 12. Việc chưa thực hiện

- Chưa liên hệ, đăng ký, mua gói, tạo credentials, gọi API hoặc tải dữ liệu.
- Chưa xác minh runtime coverage, số bản ghi, missing/duplicate, OHLC/Volume, corporate actions hoặc so sánh CafeF.
- Không sửa Raw/Processed; không tính Daily Return/Volatility; chưa Feature Engineering hoặc clustering.
- Chưa xác nhận/giải quyết chênh lệch phạm vi lịch sử trong một số tài liệu quản lý dự án; báo cáo tuân thủ phạm vi 43 HOSE được nêu trong tiến độ hiện tại.
