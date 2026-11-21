# Nghiên cứu khả năng thu thập dữ liệu giá lịch sử Vietstock

Ngày kiểm tra: 17/11/2026

## 1. Phạm vi và kết luận

Đã kiểm tra tài liệu hướng dẫn VietstockFinance chính thức năm 2024, trang API chính thức và thử truy cập trang hồ sơ ACB theo URL công khai thường được dùng. Tài liệu xác nhận VietstockFinance có chức năng thống kê giao dịch cổ phiếu theo bộ lọc mã và khoảng ngày. Tuy nhiên, trong lần nghiên cứu này chưa xác minh được chức năng xuất Excel cho bảng lịch sử cổ phiếu, quyền tải không cần đăng nhập, điều khoản/lưu lượng API, hoặc một giao diện công khai hiện hoạt để tải OHLCV lịch sử. Thử nghiệm ACB không thu được dữ liệu, do đó không có file test được lưu.

Kết luận hiện tại: chưa đủ căn cứ để viết crawler tự động hoặc gọi endpoint. Giữ phương án tải CSV/XLSX thủ công từ Vietstock làm đường nhập chính; chỉ nghiên cứu tích hợp tự động tiếp nếu Vietstock xác nhận endpoint/API, quyền truy cập và điều kiện sử dụng.

## 2. Phương thức đã kiểm tra và bằng chứng

| Phương thức | Kết quả thực tế | Ý nghĩa/giới hạn |
|---|---|---|
| Hướng dẫn VietstockFinance 2024 | Mục 2.4.2 mô tả “Cổ phiếu → Thống kê giao dịch”, bộ lọc sàn, mã/index, từ ngày/đến ngày và các tab “Thống kê giá”, “Thống kê đặt lệnh”, “GD khớp lệnh”. | Xác minh được sản phẩm có tra cứu thống kê theo thời gian. Bản hướng dẫn không đủ để khẳng định bảng này cung cấp OHLCV từng phiên, có nút Excel cho cổ phiếu, hoặc quyền xuất miễn phí. |
| Trang hồ sơ ACB `https://finance.vietstock.vn/ACB.htm` | GET công khai trả HTTP 404 trong môi trường kiểm tra. | Đường dẫn này không dùng được tại thời điểm kiểm tra. Không dò hoặc đoán URL/endpoint thay thế. HTTP 404 không chứng minh Vietstock không có dữ liệu ở giao diện khác. |
| Trang API chính thức `https://api.vietstock.vn/` | Trang giới thiệu cung cấp dữ liệu giao dịch chứng khoán real-time, dữ liệu doanh nghiệp/tài chính và truy xuất một số dữ liệu qua Excel/nền web. | Không tìm thấy trong thông tin đã kiểm tra tài liệu endpoint, dữ liệu lịch sử OHLCV, cơ chế xác thực, giá, giới hạn gọi hoặc quyền sử dụng cụ thể. Không thể xem đây là API lịch sử sẵn dùng cho ASM. |
| Endpoint lịch sử giá | Không thử endpoint không được tài liệu chính thức xác nhận. | Không sử dụng các endpoint suy đoán hoặc chỉ được nêu trong mã nguồn bên thứ ba. |
| Xuất CSV/XLSX trên giao diện | Chưa thể xác minh nút xuất trong chính trang thống kê cổ phiếu ACB do trang công khai cũ trả 404 và tài liệu hướng dẫn không nêu rõ nút Excel ở mục này. | Người dùng có thể kiểm tra trực tiếp giao diện Vietstock đã đăng nhập hợp lệ và tải file nếu tính năng được cung cấp cho tài khoản. Không tự động hóa đăng nhập hoặc vượt cơ chế bảo vệ. |

## 3. Thử nghiệm thực tế ACB

- Mã: ACB.
- Phạm vi: không có phạm vi ngày nào được tải thành công.
- Dữ liệu trả về: không có nội dung bảng/CSV/XLSX để kiểm tra.
- Số dòng: 0 dòng dữ liệu nhận được; đây là kết quả không thành công, không phải tập dữ liệu hợp lệ rỗng.
- Các cột: không có cột nào nhận được; chưa thể xác nhận Date, Open, High, Low, Close, Volume, Ticker.
- Xác minh ngày giao dịch, giá, khối lượng: chưa thực hiện được vì không nhận được dữ liệu.
- Lưu trữ: không tạo `data/raw/test/` và không lưu file giả hay phản hồi HTML lỗi.
- Đăng nhập/CAPTCHA: không thử đăng nhập, không gửi thông tin xác thực và không gặp/giải CAPTCHA. Yêu cầu tới URL kiểm tra kết thúc ở 404.

## 4. Cấu trúc dữ liệu và độ phủ thời gian

Schema mục tiêu của ASM là Date, Open, High, Low, Close, Volume, Ticker. Chưa có file dữ liệu giao dịch cổ phiếu thực từ Vietstock trong workspace để xác nhận tên cột, đơn vị giá/khối lượng, định dạng ngày, điều chỉnh giá hay độ phủ.

Tài liệu 2024 có minh họa bộ lọc khoảng thời gian cho thống kê giao dịch, nhưng chưa xác minh việc chọn được 2–3 năm và xuất đủ từng phiên. Vì vậy chưa thể khẳng định độ phủ 2–3 năm cho ACB hoặc khả năng tải đồng nhất cho 10 mã.

## 5. Khả năng mở rộng tới 10 mã

Chưa được kiểm chứng thực nghiệm. Nếu Vietstock cung cấp một chức năng được phép xuất cho mỗi mã và mỗi phạm vi ngày, 10 mã có thể được xử lý theo lô ở phía ứng dụng ASM sau khi biết giới hạn và điều khoản. Trước khi tự động hóa cần xác minh:

1. API/export chính thức có trả dữ liệu lịch sử OHLCV theo ngày hay không.
2. Tài khoản/giấy phép cần thiết và mục đích sử dụng được cho phép.
3. Giới hạn phạm vi ngày, kích thước file, tốc độ và số yêu cầu.
4. Có thể xuất lần lượt 10 mã với cùng schema và đơn vị hay không.
5. Chính sách lưu trữ và tái sử dụng dữ liệu tải xuống.

Không chạy batch 10 mã trong giai đoạn này.

## 6. Phương án đề xuất

1. Dùng giao diện Vietstock theo cách truy cập hợp lệ để tải ACB dạng CSV/XLSX; nếu chức năng yêu cầu tài khoản, người dùng đăng nhập/tải trực tiếp. Nhập file vào module quản lý dữ liệu hiện có, giữ nguyên raw và xác minh nội dung trước khi xác nhận.
2. Kiểm tra mẫu thật để chốt alias cột, ngày, đơn vị giá/khối lượng, giá điều chỉnh hay chưa, trùng lặp và phạm vi thời gian. Không giả định schema trước khi thấy file.
3. Chỉ bổ sung crawler/API sau khi có endpoint hoặc tài liệu chính thức, quyền sử dụng rõ ràng và thử nghiệm ACB nhỏ thành công. Không dùng endpoint suy đoán, không tự động hóa đăng nhập, không vượt CAPTCHA/bảo vệ.
4. Sau khi kiểm chứng ACB và giới hạn dịch vụ, mới cân nhắc mở rộng tuần tự tới các mã ngân hàng khác; ghi log từng mã, kiểm tra dữ liệu thực nhận, không coi HTTP 200 là thành công.

## 7. Nguồn đã mở

- [Hướng dẫn sử dụng VietstockFinance 2024 (PDF)](https://static1.vietstock.vn/vietstock/2024/VSTF-Huong-dan-su-dung-2024.pdf), mục 2.4.2 “Thống kê giao dịch” (trang 21 trong tài liệu).
- [Trang giới thiệu Vietstock API](https://api.vietstock.vn/).
- Trang ACB đã thử: `https://finance.vietstock.vn/ACB.htm` (GET trả 404 ngày 17/11/2026).

## 8. Những điểm còn chưa xác minh

- Giao diện hiện hành cụ thể để mở thống kê giá lịch sử riêng cho ACB.
- Có nút tải CSV/XLSX cho bảng cổ phiếu hay không và điều kiện tài khoản.
- API chính thức có lịch sử OHLCV theo ngày hay chỉ dữ liệu realtime/dịch vụ khác.
- Cột thực tế, đơn vị, điều chỉnh giá, thời gian dữ liệu tối đa, giới hạn và quyền sử dụng.
- Khả năng thu thập tự động hợp lệ cho một mã và mở rộng mười mã.
