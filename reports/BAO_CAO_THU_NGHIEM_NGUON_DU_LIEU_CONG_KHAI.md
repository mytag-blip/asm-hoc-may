# Báo cáo khảo sát và thử nghiệm nguồn dữ liệu công khai

**Ngày khảo sát:** 20/11/2026 (UTC)  
**Mục tiêu thử:** OHLCV ngày cho FPT, NLG, HPG, VNM, VIC; 19/11/2021–18/11/2026.  
**Giới hạn:** Chỉ truy vấn đọc khi endpoint công bố cho phép; không dùng tài khoản chứng khoán, giấy tờ định danh, API key cá nhân, scraping giao diện hoặc dữ liệu giả.

## 1. Kết luận điều hành

Trong các nguồn ưu tiên, **chưa tìm thấy nguồn có thể cung cấp đủ OHLCV 5 năm bằng Python mà không cần thông tin truy cập cá nhân, đồng thời có tài liệu hiện hành và điều kiện sử dụng rõ ràng**.

- Các adapter VCI/KBS xuất hiện trong tài liệu Vnstock thế hệ cũ; tài liệu Vnstock 6 hiện hành báo các source cũ này không còn hỗ trợ. Không cài hoặc chạy phiên bản cũ đã hết thời hạn hỗ trợ.
- TCBS có tài liệu endpoint OHLCV dài hạn nhưng yêu cầu API Key/token từ TCInvest. Một GET không gửi credentials tới endpoint chính thức trả HTTP 401, không có bản ghi.
- Chưa xác định được nguồn công khai khác có API OHLCV Việt Nam 5 năm, quyền sử dụng nghiên cứu và không cần đăng ký. Không dùng endpoint không tài liệu hóa để thay thế.

Vì không có response OHLCV thành công, không thể báo số dòng, first/last date, gaps, duplicates, OHLC, volume, corporate actions, price basis hoặc đơn vị cho năm mã. Không có dữ liệu giả hay fixture nào được coi là dữ liệu tải thật.

## 2. Vnstock, VCI và KBS

### Phiên bản và vai trò

Tài liệu Vnstock hiện hành ghi phiên bản **6.0.1**, công bố ngày 16/11/2026. Vnstock là phần mềm phía client để kết nối nguồn bên thứ ba, không phải nhà cung cấp dữ liệu; giấy phép phần mềm không tự cấp quyền với dữ liệu nguồn. Vnstock Community dành cho học tập/nghiên cứu; với thế hệ 6, hàm Market/Reference không bắt buộc đăng nhập Vnstock, nhưng người dùng vẫn cần quyền/credentials do nguồn dữ liệu yêu cầu. Xem [giới thiệu Vnstock 6](https://www.vnstocks.com/docs/vnstock/v6/gioi-thieu), [cài đặt và thiết lập khóa nguồn](https://www.vnstocks.com/docs/vnstock/v6/cai-dat), [README chính thức](https://github.com/thinh-vu/vnstock/blob/main/README.md).

Môi trường Python của dự án hiện **chưa cài `vnstock`**. Không cài thư viện trong khảo sát này.

### VCI

Tài liệu chuyển đổi chính thức nêu `source="VCI"` là nguồn cũ và khi dùng với thế hệ 6 sẽ báo `VNSTOCK_SOURCE_OPERATION`; danh sách nguồn thay thế được tài liệu nêu không bao gồm VCI. Vì vậy VCI qua Vnstock không còn là lựa chọn dùng được trên phiên bản hiện hành. Không gọi endpoint VCI trực tiếp vì không tìm thấy hợp đồng API công khai hiện hành đủ để xác nhận quyền truy cập, hạn mức và điều khoản sử dụng.

### KBS

Tình trạng tương tự: `source="KBS"` thuộc nhóm source cũ và không còn được hỗ trợ trong Vnstock 6. Tài liệu cũ mô tả KBS như adapter OHLCV nhưng không tạo quyền sử dụng hay bảo đảm API vận hành hiện tại. Không thử gọi endpoint nội bộ hoặc không được tài liệu hiện hành công bố.

Tài liệu Vnstock thông báo các thế hệ trước V6 ngừng hoạt động từ **10/11/2026**. Ngày khảo sát là 20/11/2026 nên không dùng Vnstock 4/5 để cố truy cập VCI/KBS. Nguồn: [thông báo chính thức về Vnstock hiện hành](https://github.com/thinh-vu/vnstock/blob/main/README.md), [hướng dẫn chuyển từ thế hệ 5](https://www.vnstocks.com/docs/vnstock/v6/chuyen-doi/tu-the-he-5).

Tài liệu Vnstock hiện hành xác nhận các nguồn OHLCV được liệt kê là `dnse`, `fhsc`, `ssi`, `tcbs`; không liệt kê VCI hoặc KBS. Đây là adapter names, không phải bằng chứng rằng Vnstock sở hữu dữ liệu. Xem [tài liệu nguồn OHLCV](https://www.vnstocks.com/docs/vnstock/v6/thi-truong-market) và [danh sách nguồn/Open API](https://www.vnstocks.com/docs/vnstock/v6/tham-khao/nguon-du-lieu).

**Nguồn gốc dữ liệu:** Tài liệu hiện hành xác định Vnstock gửi yêu cầu từ máy người dùng tới nguồn bên thứ ba. Với các adapter VCI/KBS cũ, tài liệu đã khảo sát không xác nhận đủ endpoint owner/terms hiện hành để kết luận sâu hơn. Không gán Vnstock là nhà cung cấp và không suy đoán điều khoản của upstream.

## 3. TCBS

### Endpoint và quyền truy cập

TCBS công bố endpoint `GET /nyx/v2/stock/bars-long-term` để lấy OHLCV ngày/tuần/tháng; tham số gồm `ticker`, `type`, `resolution`, `to`, `countBack`. Response mẫu có `open/high/low/close/volume/tradingDate`. Tài liệu request minh họa `Authorization: Bearer <access token>`. Xem [tài liệu OHLCV bars dài hạn](https://developers.tcbs.com.vn/docs/v1.0.0/stock/bars-long-term/).

TCBS hướng dẫn tạo API Key trên TCInvest và đổi API Key cùng iOTP thành JWT token. Token có thời hạn tối đa 8 giờ theo FAQ của portal. Tài liệu không chứng minh việc truy vấn dài hạn có thể dùng ẩn danh hoặc không cần tài khoản TCInvest. Nguồn: [quy trình iFlash Open API](https://developers.tcbs.com.vn/docs/v1.0.0/workflow/), [TCBS OpenAPI FAQ](https://developers.tcbs.com.vn/).

### Thử nghiệm thật không credentials

Đã gửi đúng **một GET đọc** tới endpoint OHLCV dài hạn chính thức, mã FPT, resolution ngày, `to` giới hạn đến 18/11/2026, yêu cầu 3 nến, không có Authorization header/API key.

| Kết quả | Giá trị |
| --- | --- |
| HTTP status | 401 |
| Nội dung trả về | Không có JSON/bản ghi; body rỗng |
| Số dòng | 0 |
| Ngày đầu/ngày cuối | Không có |
| Credential được gửi | Không |

Đây là bằng chứng endpoint không cho truy vấn mẫu ẩn danh tại thời điểm thử; **không** chứng minh endpoint không hoạt động khi có quyền truy cập, và không cho phép kết luận về chất lượng OHLCV.

### Các thuộc tính dữ liệu chưa xác minh

- `countBack` được tài liệu mô tả là số nến lùi từ `to`, nhưng giới hạn tối đa và lịch sử tối thiểu chưa được xác nhận.
- Tài liệu endpoint được mở không xác định giá raw/adjusted, cách back-adjust, corporate actions, đơn vị giá, đơn vị Volume hay coverage thực tế cho 5 mã từ 2021.
- Vì không nhận được dữ liệu, toàn bộ kiểm tra duplicates, gaps theo lịch phiên, null, OHLC, volume và sự kiện doanh nghiệp là **chưa thực hiện được**.

**Đánh giá:** Không phù hợp với quyết định hiện tại “không mở tài khoản/chứng khoán và không dùng credentials cá nhân”. Không yêu cầu nhóm tạo TCInvest account hoặc cung cấp API Key/iOTP.

## 4. Các nguồn công khai khác

### HOSE

Trang chính thức HOSE có mục thống kê cuối ngày, nhưng bằng chứng đã khảo sát không cho thấy endpoint lịch sử tải OHLCV 5 năm tự phục vụ, không tài khoản. Biểu phí thông tin HOSE phân biệt dữ liệu hiển thị với mục đích không hiển thị; tài liệu có nhóm mục đích phân tích/risk-management và phí dịch vụ tương ứng. Do đó không coi trang hiển thị hoặc feed có điều kiện/phí là nguồn tải tự do cho nghiên cứu. Phí hiện hành, quyền với đồ án và khả năng cấp dữ liệu lịch sử cần hỏi HOSE trước khi xem xét.

Nguồn: [HOSE – thống kê cuối ngày](https://www1.hsx.vn/vi/du-lieu-giao-dich/thong-ke/du-lieu-cuoi-ngay), [biểu giá dịch vụ thông tin HOSE](https://staticfile.hsx.vn/Uploads/UploadDocuments/2404028/20240326_Bieu%20gia%20dich%20vu%20thong%20tin%20ap%20dung%20tai%20So%20GDCK%20TPHCM.pdf). Biểu giá được công bố năm 2024, nên không dùng các mức giá trong đó như báo giá hiện hành.

### Vnstock các nguồn khác và endpoint không chính thức

Trong Vnstock 6, các nguồn dữ liệu Việt Nam còn liệt kê như DNSE, SSI, TCBS, FHSC cần quyền/credentials do nhà cung cấp nguồn quy định; DNSE/SSI không đáp ứng quyết định riêng tư hiện tại. Chưa xác minh FHSC có thể cấp dữ liệu mà không đăng ký tài khoản/API key hay không. Vì vậy chưa thử gọi.

Một số mã nguồn bên thứ ba mô tả endpoint công khai/không xác thực của các website chứng khoán, nhưng đây không phải tài liệu API chính thức và không đủ bằng chứng về quyền tự động truy xuất, hạn mức hoặc giấy phép dữ liệu. Không sử dụng các endpoint này, không scraping website và không cố vượt cơ chế bảo vệ.

## 5. Bảng kết quả cho các mã thử

| Nguồn | Mã đã thử | Dữ liệu nhận được | Khoảng/ngày | Kết luận truy cập |
| --- | --- | --- | --- | --- |
| Vnstock–VCI | Không gọi | 0 dòng | Không áp dụng | Source cũ không được hỗ trợ trong V6; không gọi endpoint ngoài tài liệu |
| Vnstock–KBS | Không gọi | 0 dòng | Không áp dụng | Source cũ không được hỗ trợ trong V6; không gọi endpoint ngoài tài liệu |
| TCBS OpenAPI | FPT | 0 dòng | Không có ngày trả về | GET không credentials nhận HTTP 401 |
| FHSC/nguồn khác | Không gọi | 0 dòng | Không áp dụng | Chưa xác minh quyền truy cập ẩn danh và điều khoản |

NLG, HPG, VNM, VIC không được gửi tới nguồn nào do VCI/KBS không còn endpoint Vnstock hiện hành và TCBS đã từ chối truy cập FPT khi không xác thực. Không suy rộng phản hồi FPT thành kiểm thử các mã còn lại.

## 6. Đánh giá theo tiêu chí dữ liệu

| Tiêu chí | VCI/KBS qua Vnstock hiện hành | TCBS không xác thực | Kết luận |
| --- | --- | --- | --- |
| OHLCV ngày | Không gọi được qua source cũ trong V6 | Có schema công bố, nhưng GET thử bị 401 | Chưa có OHLCV thực |
| Lịch sử từ 2021 | Chưa xác minh | `countBack` có trong docs; độ sâu thực tế chưa rõ | Chưa đạt |
| 5 mã/FPT, NLG, HPG, VNM, VIC | Chưa xác minh | Chưa xác minh ngoài FPT request 401 | Chưa đạt |
| Ngày trùng/thiếu và quality | Không có mẫu | Không có mẫu | Không thể kiểm tra |
| Đơn vị giá/Volume | Chưa được xác minh | Endpoint docs không nêu rõ đơn vị | Chưa đạt |
| Corporate Actions/price basis | Chưa có tài liệu hiện hành đủ căn cứ | Endpoint OHLCV không xác nhận điều chỉnh | Chưa đạt |
| Quyền học thuật | Không xác minh cho adapter cũ | API Key/account terms áp dụng; chưa xác minh quyền dữ liệu học thuật | Chưa đạt |
| Không cần account/ID | Không còn source hiện hành để sử dụng | Thử ẩn danh trả 401; quy trình chuẩn dùng TCInvest/API Key/iOTP | Không đạt theo quyết định hiện tại |

## 7. Lưu trữ, tính toàn vẹn và tiến độ

- Không có OHLCV mới được tải; vì vậy không tạo CSV dữ liệu staging, không tạo bản ghi giả và không có bộ quality metrics.
- Không cài Vnstock hoặc thư viện mới; không gọi SSI; không truy vấn tiếp TCBS sau HTTP 401.
- Raw SHA-256: `1B492296E31DB393DA80A8D2579887BBECB4AFB95F4F3A9FF9CECCBFB5186043`.
- Processed SHA-256: `3574059045FBD420FC0EF473FCC6671C16C3A6BDC9F57478F02A7241598FE953`.
- Không thực hiện Feature Engineering hoặc clustering.

## 8. Khuyến nghị

1. **Không tiếp tục SSI** và không yêu cầu nhóm cung cấp SSI credentials.
2. **Không sử dụng Vnstock VCI/KBS legacy** sau ngày ngừng hỗ trợ; không gọi endpoint nội bộ/không tài liệu hóa.
3. **Không chọn TCBS** theo tiêu chí hiện tại vì test ẩn danh trả 401 và quy trình chuẩn cần TCInvest/API Key/iOTP.
4. Nếu tuyệt đối không mở tài khoản, chỉ xem xét nguồn khi nhà cung cấp công bố tải file/API miễn phí hoặc cấp phép học thuật không cần định danh; lưu email/điều khoản làm bằng chứng trước khi tải.
5. Nếu không tìm được nguồn đạt các điều kiện trên, dùng tệp CafeF nhóm đã có sau khi xác minh quyền sử dụng và cơ sở giá; nếu không thể xác minh, báo giảng viên để thống nhất phương án dữ liệu. Không đổi nguồn chính thức hoặc chạy mô hình trong giai đoạn này.

## 9. Tài liệu tham khảo

Truy cập ngày **20/11/2026**:

- [Vnstock README – phiên bản hiện hành, giới hạn và Vnstock không phải nhà cung cấp dữ liệu](https://github.com/thinh-vu/vnstock/blob/main/README.md)
- [Vnstock 6 – OHLCV Market API và danh sách nguồn](https://www.vnstocks.com/docs/vnstock/v6/thi-truong-market)
- [Vnstock 6 – nguồn Open API](https://www.vnstocks.com/docs/vnstock/v6/tham-khao/nguon-du-lieu)
- [Vnstock 6 – chuyển đổi từ thế hệ 5, nguồn VCI/KBS cũ không còn](https://www.vnstocks.com/docs/vnstock/v6/chuyen-doi/tu-the-he-5)
- [Vnstock 6 – cài đặt và yêu cầu credentials theo nguồn](https://www.vnstocks.com/docs/vnstock/v6/cai-dat)
- [TCBS – OHLCV bars dài hạn](https://developers.tcbs.com.vn/docs/v1.0.0/stock/bars-long-term/)
- [TCBS – workflow đăng ký API Key và iOTP](https://developers.tcbs.com.vn/docs/v1.0.0/workflow/)
- [TCBS Developer Portal](https://developers.tcbs.com.vn/)
- [HOSE – thống kê cuối ngày](https://www1.hsx.vn/vi/du-lieu-giao-dich/thong-ke/du-lieu-cuoi-ngay)
- [HOSE – biểu giá dịch vụ thông tin](https://staticfile.hsx.vn/Uploads/UploadDocuments/2404028/20240326_Bieu%20gia%20dich%20vu%20thong%20tin%20ap%20dung%20tai%20So%20GDCK%20TPHCM.pdf)
