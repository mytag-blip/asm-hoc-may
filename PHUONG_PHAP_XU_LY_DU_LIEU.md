# PHƯƠNG PHÁP XỬ LÝ DỮ LIỆU

**Trạng thái:** Giai đoạn 1.6 — hoàn thiện bảng quyết định và quy tắc bảo thủ. Đây là tài liệu phương pháp; chưa áp dụng lên CSV.  
**Phạm vi:** 43 doanh nghiệp HOSE, dữ liệu CafeF gần 5 năm; nghiên cứu rủi ro biến động giá cổ phiếu bằng học máy không giám sát.

### Ý nghĩa trạng thái

- **Đã chốt nguyên tắc:** người dùng đã yêu cầu rõ ràng trong phạm vi hiện tại; được áp dụng làm ràng buộc cho các bước sau, không đồng nghĩa đã xử lý dữ liệu.
- **Chờ nhóm xác nhận:** cần quyết định phương pháp luận cụ thể trước khi dùng trường/dòng cho phân tích có ảnh hưởng đến kết quả.
- **Chờ bằng chứng nguồn:** cần tài liệu hoặc dữ liệu kiểm chứng từ CafeF/HOSE/nguồn độc lập; không thể giải quyết bằng giả định.

## 1. Bảng quyết định xử lý dữ liệu

| Trường dữ liệu | Vấn đề hiện tại | Quy tắc sử dụng | Phạm vi được phép phân tích | Điều kiện cần xác minh thêm | Trạng thái quyết định |
|---|---|---|---|---|---|
| Toàn bộ dữ liệu Raw | Bản tham chiếu gốc có provenance; không phải tất cả nội dung đã được xác minh độc lập | Không sửa, xóa, nội suy hoặc ghi đè; mọi biến đổi về sau phải là bản dẫn xuất có nhật ký | Tra cứu, đối chiếu, kiểm toán | Không có điều kiện để thay đổi Raw; cần giữ provenance khi tạo bản dẫn xuất | Đã chốt nguyên tắc |
| 16 dòng OHLC bất thường | Khớp Excel nguồn; 15 Close ngoài biên, tổng 16 dòng vi phạm quan hệ OHLC; chưa có nguồn độc lập xác nhận giá giao dịch | Không sửa hoặc xóa. Gắn cờ và loại khỏi phép tính cụ thể chỉ khi nhóm thông qua quy tắc; phải lưu số dòng và lý do | EDA mô tả các trường này chỉ với cảnh báo; không dùng 16 dòng trong phép tính đòi hỏi OHLC hợp lệ cho tới khi có quyết định | Bằng chứng giá từ nguồn độc lập; quyết định nhóm về giữ có cảnh báo hay loại khỏi từng phép tính | Không sửa/xóa: đã chốt nguyên tắc. Cách xử lý phân tích: chờ nhóm xác nhận và bằng chứng nguồn |
| Close | Có giá trong CafeF; chưa xác nhận đã điều chỉnh corporate actions; 15 dòng nằm ngoài High-Low | Chỉ dùng Close cho EDA mô tả theo từng mã, kèm cảnh báo; không so sánh giá tuyệt đối giữa mã; không tính return/volatility lúc này | EDA mô tả đơn biến và đường giá theo mã; 15 dòng cần được đánh dấu | Xác minh cơ sở giá/đơn vị và xử lý luận cứ cho 15 Close ngoài biên trước phép tính nhạy với tính hợp lệ OHLC | Chỉ EDA mô tả Close và Volume: đã chốt nguyên tắc. Dùng cho đặc trưng: chờ nhóm xác nhận |
| Adjusted Close | Khác Close ở 46.296/53.385 dòng; có 104 thay đổi tỷ lệ trên 5%; chưa rõ công thức hay basis OHLC | Không dùng tính Daily Return, Volatility hoặc ghép với Open/High/Low; có thể trình bày riêng như mô tả chất lượng, không diễn giải cơ chế | Chỉ đối chiếu mô tả riêng với Close trong rà soát chất lượng | Tài liệu CafeF về công thức, corporate actions, thời điểm điều chỉnh và xác nhận tương thích với OHLC | Không dùng tính lợi suất: đã chốt nguyên tắc. Sử dụng định lượng khác: chờ bằng chứng |
| Date và ngày thiếu | MCH vắng 14 ngày; 7 mã vắng 14/08/2025; ngày gộp không phải lịch HOSE | Không nội suy, forward-fill, tự thêm phiên hoặc tự gán ngày nghỉ; giữ quan sát vắng là vắng | Thống kê độ phủ và số bản ghi hiện có; thể hiện ngày thiếu/cảnh báo riêng | Lịch HOSE và thông báo trạng thái từng mã để phân biệt nghỉ sàn, không giao dịch và thiếu dữ liệu. Báo cáo HOSE “Tổng hợp thông tin giao dịch” ghi ngày 14/08/2025 và có số liệu tổng giao dịch toàn thị trường (khớp lệnh, thỏa thuận). Nguồn: https://staticfile.hsx.vn/Uploads/UploadDocuments/2397233/20250814%20Tong%20hop%20thong%20tin%20giao%20dich.pdf (truy cập 20/11/2026). Điều này xác nhận có giao dịch toàn thị trường trong ngày; không xác định nguyên nhân 7 mã vắng bản ghi. | Không nội suy: đã chốt nguyên tắc. Phân loại ngày thiếu: chờ bằng chứng nguồn |
| Volume | Volume tổng bằng Matched Volume + Negotiated Volume trên mọi dòng; 1.008 cờ lớn theo Q3+3×IQR; chưa xác nhận đơn vị/ý nghĩa các điểm lớn | Giữ hai thành phần và tổng; không xóa, clip hoặc winsorize 1.008 dòng; 0 giữ là 0 | EDA mô tả Volume theo mã với cờ hiển thị; không gọi cờ thống kê là lỗi xác nhận | Xác nhận định nghĩa/đơn vị nguồn và rà từng điểm nếu muốn kết luận bất thường | Không xóa cờ lớn: đã chốt nguyên tắc. Diễn giải đơn vị/outlier: chờ bằng chứng nguồn |
| Matched Volume, Negotiated Volume | Không âm; Negotiated Volume có 36.794 số 0 | Giữ nguyên từng cột, không biến số 0 thành missing | EDA mô tả thành phần volume, kèm chú thích đơn vị chưa được xác nhận | Tài liệu nguồn định nghĩa và xác nhận đơn vị | Giữ nguồn: đã chốt nguyên tắc. Diễn giải đơn vị: chờ bằng chứng |
| Matched Value, Negotiated Value | Chưa xác nhận đơn vị/thang số | Chưa dùng để kết luận quy mô giao dịch hay tạo đặc trưng | Chỉ giữ để truy vết và kiểm tra nguồn | Metadata/tài liệu CafeF xác nhận đơn vị và định nghĩa | Chờ bằng chứng nguồn |
| Ticker | Định danh mã doanh nghiệp; 43 mã trong phạm vi | Dùng để phân nhóm quan sát và phân tích từng mã; không dùng làm biến số liên tục | Nhóm/lọc trong EDA | Xác nhận danh sách universe cuối cùng nếu nhóm thay đổi phạm vi | Đã chốt phạm vi hiện tại |
| Source_File, Source_Sheet, Source_Row | Trường provenance, không phải đại lượng tài chính | Giữ trong bản kiểm toán; không đưa vào đặc trưng mô hình | Truy vết và đối chiếu nguồn | Không có | Đã chốt nguyên tắc |

## 2. Các nguyên tắc bảo thủ đã chốt cho bước tiếp theo

Theo yêu cầu hiện tại, áp dụng làm giới hạn cho công việc tiếp theo; không có nghĩa đã chạy phân tích:

1. Bảo toàn dữ liệu Raw.
2. Không tự sửa 16 dòng OHLC bất thường.
3. Không dùng Adjusted Close tính Daily Return khi chưa xác minh.
4. Không nội suy ngày thiếu.
5. Không tự loại 1.008 dòng Volume lớn.
6. Chỉ dùng Close và Volume cho EDA mô tả với cảnh báo đã ghi; Date/Ticker chỉ làm trục thời gian và phân nhóm. Trường provenance chỉ dùng kiểm toán.
7. Chưa tính Volatility hoặc tạo đặc trưng rủi ro khi chưa thống nhất cơ sở giá và tác động corporate actions.
8. Không so sánh trực tiếp giá tuyệt đối giữa các mã để đánh giá rủi ro.
9. Phân biệt EDA mô tả với Feature Engineering phục vụ mô hình.

## 3. Quy tắc đề xuất có thể áp dụng ngay

Các mục dưới đây là quy tắc bảo toàn/giới hạn phân tích đã được người dùng chấp thuận trong yêu cầu Giai đoạn 1.6:

- Raw bất biến; mọi thao tác sau này tạo bản dẫn xuất và ghi nhật ký.
- Close và Volume chỉ phục vụ EDA mô tả từng mã, có cảnh báo chất lượng; không tính lợi suất hoặc volatility.
- OHLC bất thường giữ nguyên, không sửa; ngày thiếu để trống, không nội suy; cờ volume cao giữ lại.
- Không đưa Adjusted Close vào phép tính lợi suất cho tới khi có xác minh.

Việc chạy EDA thực tế vẫn chưa được yêu cầu trong nhiệm vụ hiện tại.

## 4. Những điểm cần nhóm xác nhận

1. Sau khi có/không có bằng chứng nguồn, nhóm chọn định nghĩa cơ sở giá cho phân tích rủi ro. Nếu CafeF không xác nhận Adjusted Close, có chấp thuận nghiên cứu với Close thô kèm giới hạn corporate actions không?
2. Quy tắc dùng 16 dòng OHLC cho các phép tính cần OHLC hợp lệ: giữ có cờ hay loại khỏi đúng phép tính đó? Không sửa dữ liệu.
3. Khi thiếu lịch sử cụ thể của một mã, yêu cầu độ phủ tối thiểu nào (nếu có) để mã được đưa vào phân tích so sánh?
4. Có cần dùng Matched/Negotiated Value hay chỉ giữ lại để kiểm tra nguồn? Hiện không được diễn giải định lượng.

## 5. Bằng chứng cần có từ nguồn

- CafeF/người cung cấp: phương pháp Adjusted Close; corporate actions được áp dụng; basis của OHLC; đơn vị giá, Volume, Matched Value, Negotiated Value.
- HOSE/nguồn độc lập: lịch giao dịch và thông báo trạng thái từng mã cho ngày thiếu; đối chiếu 16 bản ghi với dữ liệu giao dịch nếu có.
- Với 1.008 cờ volume: dữ liệu nguồn/ghi chú giao dịch để kết luận trường hợp cụ thể; ngưỡng Q3 + 3×IQR một mình không đủ.

## 6. Điều kiện trước Feature Engineering

- Nhóm xác nhận basis giá và chấp thuận định nghĩa lợi suất/volatility phù hợp; không dùng Adjusted Close hoặc Close thô ngoài quyết định đó.
- Chốt chính sách phân tích cho 16 OHLC; mọi loại trừ chỉ ở phép tính cụ thể và được ghi nhận.
- Phân loại ngày thiếu khi có bằng chứng hoặc thống nhất giữ là vắng mặt; tuyệt đối không nội suy.
- Xác minh đơn vị và vai trò của Volume/giá trị giao dịch; giữ cờ volume lớn cho tới khi có quyết định dựa trên nguồn.
- Lập data dictionary, quy tắc căn chỉnh thời gian giữa mã, provenance và kiểm tra đầu ra.

## 7. Giới hạn và trạng thái triển khai

Bảng phân biệt ràng buộc đã chốt với quyết định phương pháp còn mở và bằng chứng cần bổ sung. Tài liệu này không sửa CSV, không tạo dữ liệu, không chạy EDA, không tính đặc trưng và không triển khai Machine Learning. Giai đoạn 1.6 hoàn tất phần chuẩn bị phương pháp; chờ nhóm xác nhận các quyết định còn mở trước khi bước tiếp.


