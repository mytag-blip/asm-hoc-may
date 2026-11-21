# Báo cáo khảo sát nhà cung cấp dữ liệu chứng khoán

**Ngày khảo sát:** 20/11/2026  
**Mục tiêu:** Tìm nguồn OHLCV có quyền sử dụng rõ cho đồ án, không cần tài khoản chứng khoán hoặc giấy tờ định danh cá nhân.  
**Phạm vi được yêu cầu:** 43 mã HOSE, 19/11/2021–18/11/2026; không đổi đề tài/phạm vi.

## 1. Kết luận điều hành

Hai ứng viên đáng tiếp tục xác minh là **FiinQuant** và **DataCedar**; **chưa nguồn nào được chọn hoặc đủ điều kiện tải dữ liệu**.

- **FiinQuant** có Python API lịch sử OHLCV, tham số adjusted/unadjusted, tài liệu hướng tới trường đại học và điều khoản cho phép tạo sản phẩm phái sinh có trích nguồn. Tuy nhiên điều khoản hạn chế chuyển giao dữ liệu/cung cấp dịch vụ bên thứ ba. Báo giá giáo dục 2026 nêu 87.080.832 VND/12 tháng cho gói Chuyên nghiệp sau chiết khấu và VAT; đây là gói rộng, chưa phải báo giá riêng OHLCV. Đăng ký tài khoản online đang tạm ngừng. Cần hỏi quyền lưu Raw, demo website, giá basis, corporate actions và đơn vị Volume.
- **DataCedar** công bố API OHLCV, 405 mã HOSE, giá Quant 29 USD/tháng và daily history back-to-listing ở gói trả phí theo tài liệu stock-specific. Tuy nhiên cần account/API key; chưa xác minh giấy tờ đăng ký. Quan trọng hơn, tài liệu Data Rights nói truy cập API không đồng nghĩa quyền sử dụng/tái phân phối và dữ liệu tùy thuộc source-rights registry. Nguồn upstream, quyền học thuật/lưu trữ/hiển thị và nội dung Terms chưa được xác minh.
- **HOSE trực tiếp** là nguồn gốc phù hợp để hỏi nhưng không có bằng chứng về gói self-service 5 năm cho nhóm sinh viên. Biểu giá 2024 ghi 180 triệu VND/năm cho một nhóm dữ liệu thị trường không hiển thị cuối ngày; mức này không được coi là giá hiện hành.

Không gọi API, tải OHLCV, tạo adapter/staging hoặc sửa Raw/Processed. Nội dung coverage, schema và giá ở website nhà cung cấp được đánh dấu là **công bố của nhà cung cấp**, chưa được xác minh bằng response.

## 2. FiinQuant / FiinGroup

### Dữ liệu và phạm vi

- Tài liệu Python nêu dữ liệu lịch sử với các trường open, high, low, close, volume, ticker, timestamp; hỗ trợ adjusted True/False, timeframe 1 ngày, from_date/to_date hoặc period.
- Tài liệu định nghĩa Volume là khối lượng khớp lệnh. Không mặc định gồm giao dịch thỏa thuận hoặc cùng định nghĩa Volume tổng CafeF.
- FiinQuant/FiinGroup mô tả dữ liệu được chuẩn hóa từ HOSE/HNX và các đơn vị cung cấp dữ liệu chính thức; API Datafeed có Price Feed và Corporate Actions. Đây là mô tả nhà cung cấp, chưa phải lineage theo từng cột/mã/ngày hoặc bằng chứng giấy phép upstream.
- Trang Pricing công khai gói lịch sử EOD và số năm; các bảng trên cùng trang không đồng nhất về độ sâu (một bảng thể hiện 1/3/5/10 năm, bảng khác thể hiện 1 năm rồi 10–15 năm). Bảng báo giá XLSX cho giáo dục mô tả độ sâu EOD 15 năm ở các gói trả phí. Phải yêu cầu xác nhận gói cụ thể cung cấp ít nhất 5 năm cho đủ 43 mã.

### Quyền, tài khoản và chi phí

- Điều khoản sử dụng cho phép tạo sản phẩm phái sinh dựa trên dữ liệu với trích nguồn phù hợp.
- Điều khoản hạn chế bán/chuyển giao/cấp lại/tiết lộ thông tin, tài liệu liên quan đến việc sử dụng hệ thống; cấm dùng hệ thống để cung cấp dịch vụ cho bên thứ ba; và yêu cầu chấp thuận trước bằng văn bản cho mục đích thương mại. Điều khoản cho phép sản phẩm phái sinh có trích dẫn, nhưng chưa làm rõ quyền chia sẻ dữ liệu Raw hoặc cách áp dụng với website demo/biểu đồ công khai. Cần hỏi FiinGroup thay vì diễn giải rộng hơn nội dung điều khoản.
- File báo giá chính thức FiinQuant_Quotation_Website_2026.xlsx có worksheet tổ chức giáo dục: gói Chuyên nghiệp 12 tháng sau giảm 20% là 80.630.400 VND; VAT 8% là 6.450.432 VND; tổng 87.080.832 VND. Báo giá ghi độ sâu lịch sử EOD đến 15 năm ở bảng này. Tuy vậy, dòng OHLCV thể hiện bằng biểu tượng không trích xuất được từ worksheet, khách hàng/ngày phát hành để trống và báo giá có hiệu lực 1 tháng từ ngày phát hành. Đây là **ước tính tham khảo gói rộng**, không phải giá ràng buộc hoặc báo giá chỉ OHLCV.
- Trang web có thông tin gói 5 năm nhưng không render số giá trong bản đọc được. Trang chính cho biết đăng ký tài khoản online tạm ngừng và đề nghị liên hệ. Tài liệu không nói cần tài khoản chứng khoán/giấy tờ định danh, nhưng yêu cầu thông tin liên hệ khi xin dịch vụ.

**Đánh giá:** Ứng viên hỏi trước về tính phù hợp dữ liệu và quyền dẫn xuất. Chưa thử API và chưa đủ quyền để sử dụng dữ liệu.

## 3. DataCedar

### Dữ liệu và phạm vi theo công bố

- Trang HOSE nói có 405 listings; API bars có OHLCV, điều chỉnh raw/split/dividend/all, khoảng ngày và cursor.
- API key tạo trong dashboard, gắn với account. Tài liệu stock-specific nêu Explorer miễn phí có daily history một năm; Quant trở lên có daily history back-to-listing. Mức Quant công bố là 29 USD/tháng.
- Giới hạn docs: Explorer 1 request/giây và tối đa 3 mã/request; Quant 25 request/giây, 1.000/phút và tối đa 8 mã/request. Daily limit tối đa 50.000 bản ghi/request, có cursor khi phân trang.
- Trang công khai của FPT, NLG, HPG, VIC và VNM cho thấy ví dụ lịch sử vượt 5 năm; đây là claims của trang mã, không phải kiểm tra API. Chưa xác minh riêng toàn bộ 43 mã.
- Trang mã nói giá VND và Volume là shares traded trong phiên. Không nói rõ Volume bao gồm cả giao dịch thỏa thuận hay chỉ khớp lệnh.
- Docs mô tả adjustment cho split và cash dividend; actions route liệt kê dividend/split. Chưa thấy phương pháp xử lý quyền mua, cổ phiếu thưởng/cổ tức cổ phiếu, event coverage và công thức điều chỉnh OHLC đầy đủ.

### Quyền, tài khoản và chi phí

- Pricing công bố Quant 29 USD/tháng, hủy theo tháng; Explorer không cần thẻ. API docs yêu cầu account/dashboard API key. Không có thông tin công khai xác nhận form không hỏi giấy tờ ID; cũng không thấy yêu cầu tài khoản chứng khoán.
- Các trang sản phẩm có bảng lịch sử khác nhau: stock-specific docs ghi daily history một năm miễn phí và back-to-listing ở Quant; một số bảng khái quát mô tả cửa sổ 7/30/90 ngày. Cần xác nhận entitlement chính xác trước khi mua.
- Terms page không truy cập được trong khảo sát. Data Rights page nêu truy cập API/public page không làm phát sinh quyền sở hữu hoặc tái phân phối; response phụ thuộc source-rights registry. Chưa tìm được văn bản cấp quyền rõ cho sinh viên lưu 5 năm, phân tích, chia sẻ CSV với giảng viên hoặc hiển thị trên demo.

**Đánh giá:** Triển vọng chi phí/kỹ thuật, nhưng quyền dữ liệu và upstream provenance là chặn chính. Chưa tạo key hay gọi API.

## 4. Nguồn khác đã cân nhắc

| Nguồn | Bằng chứng | Lý do chưa đưa vào shortlist |
|---|---|---|
| HOSE trực tiếp | Trang HOSE có thống kê cuối ngày; biểu giá dịch vụ phân biệt mục đích hiển thị/không hiển thị và feed. Tài liệu 2024 ghi 180 triệu VND/năm cho một gói market data EOD/độ trễ không hiển thị. | Chưa thấy gói self-service lịch sử 5 năm; mức năm 2024 vừa cao vừa không phải báo giá hiện hành. Có thể hỏi trường về license học thuật. |
| FiinGroup API Datafeed doanh nghiệp | Tài liệu nêu Price Feed, Corporate Actions, financial/reference data; form dịch vụ yêu cầu thông tin liên hệ và tổ chức. | Quote và quyền dùng cho lớp học không công khai; FiinQuant là kênh Python dễ đánh giá hơn trong cùng hệ sinh thái. |
| CafeF/Vietstock | Báo cáo hiện có ghi chưa rõ Adjusted Close/OHLC basis và quyền sử dụng. | Không giải quyết các vấn đề dữ liệu đã ghi nhận; không coi file hiện tại là giấy phép hoặc price basis đã xác minh. |

## 5. So sánh

| Tiêu chí | FiinQuant | DataCedar |
|---|---|---|
| OHLCV ngày | Có trong tài liệu Python; Volume là khớp lệnh | Có theo API schema; Volume ghi shares/session |
| 5 năm | Bảng giá công bố gói 5 năm; quote giáo dục nêu EOD 15 năm nhưng phải xác nhận quyền OHLCV | Stock docs nói gói Quant từ phiên đầu có thể truy xuất; cửa sổ giữa các trang giá cần xác nhận |
| 43 mã | Một số gói không giới hạn số mã; exact entitlement cần hỏi | Website tuyên bố 405 mã HOSE; chưa đối chiếu 43 mã |
| Cơ sở giá | Có cờ adjusted, chưa có công thức/corporate-action details | Có raw/split/dividend/all; chưa đủ quy tắc với mọi event |
| Units | Volume là matching; giá/đơn vị cần xác nhận | Giá VND, Volume shares; negotiated inclusion cần hỏi |
| Tài khoản/ID | Có account/login; signup online tạm dừng. Không thấy yêu cầu tài khoản chứng khoán/ID trong docs | Cần dashboard account/API key, free no-card; giấy tờ đăng ký chưa biết |
| Giá tham khảo | 87.080.832 VND/năm cho báo giá giáo dục gói rộng; trang giá cá nhân không hiện số trong bản đọc | Quant 29 USD/tháng |
| Quyền lưu/hiển thị | Derivative có citation được nói tới; raw/website bên thứ ba chưa rõ | Chưa có license cụ thể; Data Rights khẳng định technical access không tự cấp rights |
| Trạng thái | Hỏi nhà cung cấp trước | Ứng viên dự phòng nếu có license bằng văn bản |

## 6. Shortlist tối đa hai nguồn

### 1) FiinQuant — ưu tiên hỏi trước

- **Chi phí dự kiến:** mốc công bố cho gói giáo dục Chuyên nghiệp là 87.080.832 VND/12 tháng gồm VAT. Đây là gói rộng, chưa phải OHLCV-only. Xin báo giá cho 43 mã, dữ liệu EOD và 5 năm, không realtime.
- **Điều kiện:** FiinQuant account/trial qua liên hệ vì signup online đang tạm ngừng. Tài liệu không cho thấy cần tài khoản chứng khoán hoặc giấy tờ ID; việc xin quote có thể cần thông tin cá nhân/tổ chức.
- **Cần xác minh:** coverage và 5 năm cho từng mã; raw/adjusted formula, corporate actions, units; quyền lưu Raw nội bộ, nộp CSV cho giảng viên, dẫn xuất feature/cluster, trích dẫn và hiển thị kết quả trên website demo.

### 2) DataCedar — chi phí thấp hơn, qua cổng quyền dữ liệu trước

- **Chi phí dự kiến:** Quant 29 USD/tháng theo trang giá; chỉ mua sau xác nhận bằng văn bản rằng gói đó mở lịch sử daily HOSE 2021–2026. Tính thêm thuế/phí thanh toán nếu áp dụng.
- **Điều kiện:** account dashboard và API key. Website nói Explorer không cần thẻ; không thấy thông tin yêu cầu tài khoản chứng khoán, nhưng chưa xác minh giấy tờ đăng ký.
- **Cần xác minh:** upstream/source-rights; quyền academic use, lưu trữ, dữ liệu dẫn xuất, báo cáo/demo website; full 5-year window và đủ 43 mã; volume units; điều chỉnh quyền mua/cổ phiếu thưởng và formula OHLC.

Không chọn nguồn chính thức trong giai đoạn khảo sát. Nếu nhà cung cấp không cấp quyền bằng văn bản phù hợp, loại nguồn đó dù API trả dữ liệu hoặc giá thấp.

## 7. Các câu hỏi cần nhóm gửi nhà cung cấp (chưa liên hệ)

1. Có daily OHLCV đủ 43 mã HOSE từ 19/11/2021 đến 18/11/2026 không? Xin xác nhận danh sách ticker, ngày đầu/cuối và hạn mức truy vấn/export.
2. Raw/adjusted được định nghĩa thế nào? OHLC có cùng cơ sở không? Cách xử lý cổ tức tiền mặt, cổ tức cổ phiếu/thưởng, quyền mua, split/reverse split? Có event ledger?
3. Giá theo VND? Volume là khớp lệnh, thỏa thuận hay tổng; có trường riêng từng loại?
4. Gói rẻ nhất đáp ứng chính xác 43 mã, EOD, 5 năm là gói nào; giá, VAT, phí setup, thời hạn, quota?
5. Nhóm có được lưu Raw nội bộ, giữ sau khi hết thuê bao, tính features/clusters và nộp CSV cho giảng viên không?
6. Có được trình bày trích đoạn trong báo cáo/slide và biểu đồ/metrics trên website demo; demo private/public khác nhau thế nào?
7. Xin gửi license/terms áp dụng, nguồn upstream và xác nhận rằng nhà cung cấp có quyền cấp các phạm vi trên.

Chưa gửi câu hỏi hoặc thông tin cá nhân thay mặt nhóm.

## 8. Việc chưa thực hiện và giới hạn

- Không gọi API, không tải dữ liệu cổ phiếu, không tạo key/adapter/staging.
- Không có số dòng/coverage API thực tế, kiểm tra missing/duplicate/OHLC/Volume hoặc so sánh CafeF.
- Không sửa Raw/Processed; không Feature Engineering, tính Daily Return/Volatility hoặc clustering.
- PROJECT_PROGRESS hiện ghi 43 mã, trong khi PROJECT_CONTEXT còn giữ phạm vi 50 từ bối cảnh trước. Báo cáo này tuân theo phạm vi 43 theo yêu cầu hiện tại; không tự sửa quyết định phạm vi.

## 9. Tài liệu chính thức

Ngày truy cập: **20/11/2026**.

1. [FiinQuant — giá và chi phí](https://fiinquant.vn/Pricing).
2. [FiinQuant — báo giá website 2026 (XLSX)](https://fiinquant.vn/docs/FiinQuant_Quotation_Website_2026.xlsx).
3. [FiinQuant — điều khoản sử dụng](https://fiinquant.vn/Home/Privacy).
4. [FiinQuant — trang chính và trạng thái đăng ký](https://fiinquant.vn/).
5. [FiinQuant — tài liệu dữ liệu lịch sử Python](https://docs.fiinquant.vn/fiinquant-en/function-and-formula/historical-data-function).
6. [FiinQuant — định nghĩa Volume](https://docs.fiinquant.vn/fiinquant-en/practical-application/data-retrieval).
7. [FiinGroup — API Datafeed](https://dff.fiingroup.vn/ApiDataFeed).
8. [DataCedar — dữ liệu HOSE](https://datacedar.com/markets/hose), [thị trường Việt Nam](https://datacedar.com/vi/markets/vietnam).
9. [DataCedar — API docs](https://datacedar.com/docs), [pricing](https://datacedar.com/pricing), [Data Rights](https://datacedar.com/data-rights).
10. Ví dụ trang mã DataCedar: [FPT](https://datacedar.com/markets/hose/fpt), [NLG](https://datacedar.com/markets/hose/nlg), [HPG](https://datacedar.com/markets/hose/hpg), [VIC](https://datacedar.com/markets/hose/vic), [VNM](https://datacedar.com/vi/markets/hose/vnm).
11. [HOSE — dữ liệu cuối ngày](https://www1.hsx.vn/vi/du-lieu-giao-dich/thong-ke/du-lieu-cuoi-ngay), [biểu giá thông tin HOSE (2024)](https://staticfile.hsx.vn/Uploads/UploadDocuments/2404028/20240326_Bieu%20gia%20dich%20vu%20thong%20tin%20ap%20dung%20tai%20So%20GDCK%20TPHCM.pdf).
