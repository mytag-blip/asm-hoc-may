# Thư nháp xác nhận dữ liệu và quyền sử dụng — FiinQuant

**Trạng thái:** Bản nháp để nhóm tự xem xét. Chưa gửi.  
**Người nhận dự kiến:** Bộ phận tư vấn/chăm sóc khách hàng FiinQuant  
**Kênh liên hệ công khai đã ghi trong tài liệu:** info@fiinquant.vn  
**Ngày soạn:** 20/11/2026

**Tiêu đề:** Đề nghị xác nhận dữ liệu OHLCV và quyền sử dụng cho đồ án sinh viên

Kính gửi FiinQuant,

Nhóm sinh viên chúng tôi đang thực hiện đồ án học thuật về phân nhóm và đánh giá rủi ro biến động giá cổ phiếu của 43 doanh nghiệp niêm yết trên HOSE. Nhóm đang đánh giá nguồn dữ liệu trước khi đăng ký hoặc thanh toán. Chúng tôi chưa tạo tài khoản và chưa truy cập API.

Kính nhờ FiinQuant xác nhận bằng văn bản các nội dung sau:

### 1. Phạm vi và độ sâu dữ liệu

1. FiinQuant có cung cấp OHLCV **hằng ngày** cho toàn bộ 43 mã HOSE trong danh sách nhóm hay không? Nhóm có thể gửi danh sách ticker theo yêu cầu.
2. Dữ liệu có đủ từ **19/11/2021 đến 18/11/2026** cho từng mã không? Nếu một mã không đủ, xin cho biết ngày đầu/cuối khả dụng hoặc cách kiểm tra coverage trước khi mua.
3. Gói nào đáp ứng đồng thời 43 mã, OHLCV ngày và tối thiểu 5 năm lịch sử? Trên trang Pricing nhóm thấy các bảng thể hiện độ sâu lịch sử khác nhau; xin xác nhận bảng/gói nào hiện hành và áp dụng cho thư viện Python.

### 2. Cơ sở giá và sự kiện doanh nghiệp

4. Dữ liệu OHLCV có lựa chọn giá chưa điều chỉnh và giá điều chỉnh không? Với từng chế độ, xin mô tả định nghĩa và công thức hoặc cung cấp data dictionary chính thức.
5. Khi adjusted được bật, Open, High, Low và Close có được điều chỉnh trên cùng cơ sở không? Lịch sử có được back-adjust lại khi phát sinh sự kiện doanh nghiệp hoặc khi dữ liệu được cập nhật không?
6. Những Corporate Actions nào được hỗ trợ, bao gồm cổ tức tiền mặt, cổ tức/cổ phiếu thưởng, quyền mua, chia tách và gộp cổ phiếu? Có endpoint/bảng sự kiện để đối chiếu ngày chốt quyền, ngày hiệu lực và hệ số điều chỉnh không?

### 3. Volume và đơn vị

7. Tài liệu mô tả `volume` là matching order volume. Đơn vị trả về là cổ phiếu hay lô? Trường này gồm các giao dịch khớp lệnh nào và có/không bao gồm giao dịch thỏa thuận? Có trường tổng khối lượng riêng không?
8. Đơn vị giá và cách biểu diễn timestamp/ngày giao dịch trong dữ liệu ngày là gì?

### 4. Quyền sử dụng dữ liệu cho đồ án

Nhóm dự kiến chỉ sử dụng dữ liệu cho mục đích học thuật không thương mại. Xin xác nhận rõ trong gói được đề xuất, nhóm có được:

9. Truy xuất/tải dữ liệu về máy và lưu bản OHLCV gốc trong thời gian làm đồ án không?
10. Lưu dữ liệu trong khu vực staging phục vụ phát triển, kiểm thử và tái lập kết quả; sau khi gói kết thúc có phải xóa dữ liệu không?
11. Sử dụng dữ liệu để tính các chỉ số/đặc trưng và phân cụm; nộp file dữ liệu hoặc trích đoạn cần thiết cho giảng viên chấm đồ án không?
12. Hiển thị biểu đồ và kết quả tổng hợp/dẫn xuất trên website demo tiếng Việt không? Xin phân biệt demo chỉ dùng nội bộ/lớp học, demo giới hạn truy cập và website công khai; nhóm sẽ không đăng file CSV/raw nếu không được cấp quyền.
13. Cần ghi attribution theo mẫu nào? Có giới hạn về số điểm dữ liệu, ảnh chụp biểu đồ, báo cáo, slide hoặc thời gian lưu không?

### 5. Giá, đăng ký và giới hạn

14. Xin báo giá hiện hành cho phạm vi cụ thể: **43 mã HOSE, OHLCV daily, lịch sử tối thiểu 5 năm, không yêu cầu dữ liệu realtime**. Vui lòng ghi rõ VAT, phí khởi tạo/cài đặt, thời hạn, gói tối thiểu và điều kiện gia hạn.
15. Quota áp dụng gồm số mã, request/tháng, tốc độ request, số kết nối và giới hạn lịch sử là bao nhiêu? Có cơ chế phân trang hoặc giới hạn số dòng mỗi request không?
16. Có chương trình/gói dành cho sinh viên hoặc trường đại học không? Quy trình đăng ký dùng thử/tài khoản yêu cầu thông tin gì và có yêu cầu giấy tờ định danh cá nhân hoặc tài khoản chứng khoán không?
17. Xin gửi điều khoản/giấy phép áp dụng cho quyền lưu trữ, sử dụng học thuật, chia sẻ cho giảng viên và hiển thị website demo để nhóm cùng giảng viên xem xét trước khi đăng ký.

Nhóm chưa đăng ký, thanh toán, gọi API hoặc tải dữ liệu. Chúng tôi sẽ chỉ xem xét thử nghiệm đọc dữ liệu sau khi hiểu và được phép theo điều khoản áp dụng, nhận được phản hồi về quyền sử dụng, và có xác nhận của nhóm.

Xin cảm ơn FiinQuant.

Trân trọng,

**[Họ tên đại diện nhóm]**  
**[Tên trường/lớp hoặc môn học]**  
**[Email liên hệ]**
