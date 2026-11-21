# Báo cáo khảo sát Yahoo Finance và yfinance

**Ngày rà soát:** 20/11/2026  
**Giai đoạn:** 2.13  
**Phạm vi:** 43 doanh nghiệp HOSE, dữ liệu mục tiêu 19/11/2021–18/11/2026, rủi ro biến động giá và học máy không giám sát.

## 1. Kết luận

Chưa thực hiện truy vấn Yahoo Finance. Điều khoản Yahoo hiện hành cấm truy cập hoặc thu thập dữ liệu tự động nếu không có sự cho phép rõ ràng trước đó. yfinance tự nêu đây là thư viện không liên kết hay được Yahoo chứng thực; trang PyPI hướng người dùng xem điều khoản Yahoo để biết quyền với dữ liệu tải xuống, đồng thời ghi API Yahoo Finance chỉ dành cho mục đích cá nhân. Vì vậy không gọi API/yfinance khi chưa có chấp thuận phù hợp.

Năm ticker dự kiến FPT.VN, NLG.VN, HPG.VN, VNM.VN, VIC.VN chưa được xác minh. Không có dữ liệu thật được tải, không có staging rows. Raw và Processed không bị sửa. Không tính Daily Return/Volatility, không Feature Engineering hoặc clustering.

## 2. Phiên bản và tài liệu thư viện

- Môi trường hiện tại cài yfinance **1.4.0** (đọc metadata cài đặt, không truy vấn).
- PyPI công bố yfinance **1.8.0**, phát hành 03/11/2026. Không cài/nâng cấp trong lần này.
- Tài liệu yfinance cho biết Ticker.history hỗ trợ interval hằng ngày, actions, auto_adjust, back_adjust, repair và keepna; start là ngày bao gồm, end là ngày không bao gồm. Mặc định auto_adjust=True và tùy chọn này điều chỉnh toàn bộ OHLC.
- Đây là mô tả API của thư viện, không phải bằng chứng về công thức điều chỉnh Yahoo, coverage corporate actions hoặc quyền sử dụng dữ liệu.

Nếu được phép thử nghiệm sau này, cấu hình đề xuất (chưa chạy): interval=1d, start=2021-11-19, end=2026-11-19 để bao gồm phiên 18/11/2026 do end-exclusive; auto_adjust=False, actions=True, repair=False, keepna=True. Phải ghi đầy đủ cấu hình và không diễn giải price basis nếu nhà cung cấp chưa xác nhận.

## 3. Đánh giá quyền sử dụng

| Hoạt động | Bằng chứng/đánh giá | Trạng thái |
|---|---|---|
| Truy xuất tự động | Yahoo Terms mục 4(9) yêu cầu sự cho phép rõ ràng trước khi truy cập/thu thập tự động. | Chưa được phép xác nhận; chưa truy vấn. |
| Sử dụng học thuật | yfinance được mô tả là hướng đến nghiên cứu/giáo dục, nhưng cũng yêu cầu xem Yahoo Terms về quyền dữ liệu và ghi API chỉ dành cho cá nhân. | Không thấy ngoại lệ học thuật được xác minh. |
| Lưu dữ liệu staging | Chưa tìm thấy quyền cụ thể cho phép lưu OHLCV lịch sử lấy tự động trong đồ án. | Chưa xác minh. |
| Đưa dữ liệu lên website/báo cáo | Chưa xác minh quyền tái phân phối/hiển thị. Yahoo Terms cũng hạn chế tạo nguồn dữ liệu tổng hợp cạnh tranh hoặc thay thế. | Chưa xác minh; không công khai dữ liệu Yahoo. |

Mục đích giáo dục của thư viện không tự cấp giấy phép dữ liệu. Đây là rà soát điều khoản công khai, không phải tư vấn pháp lý. Cần xin xác nhận áp dụng cụ thể cho truy cập tự động, lưu trữ, phân tích, trích dẫn, biểu đồ, chia sẻ và demo website.

## 4. Kết quả thử nghiệm năm mã

| Mã HOSE | Ticker dự kiến | Có dữ liệu thật? | Số dòng/khoảng ngày | Chất lượng và CafeF |
|---|---|---|---|---|
| FPT | FPT.VN | Chưa kiểm tra — không truy vấn | Chưa có | Chưa kiểm tra/đối chiếu |
| NLG | NLG.VN | Chưa kiểm tra — không truy vấn | Chưa có | Chưa kiểm tra/đối chiếu |
| HPG | HPG.VN | Chưa kiểm tra — không truy vấn | Chưa có | Chưa kiểm tra/đối chiếu |
| VNM | VNM.VN | Chưa kiểm tra — không truy vấn | Chưa có | Chưa kiểm tra/đối chiếu |
| VIC | VIC.VN | Chưa kiểm tra — không truy vấn | Chưa có | Chưa kiểm tra/đối chiếu |

Do không có response, không thể báo số dòng, ngày đầu/cuối, ngày trùng/thiếu, null, OHLC bất thường, Volume/đơn vị, corporate actions hoặc khả năng phủ đủ 5 năm. Không kết luận ticker .VN nào tồn tại hay được hỗ trợ.

## 5. Cơ sở giá và corporate actions

- PyPI cho biết giá mặc định được điều chỉnh theo cổ tức; tài liệu API mô tả auto_adjust điều chỉnh OHLC và actions có thể yêu cầu các trường sự kiện.
- Điều này không chứng minh công thức Adjusted Close, cách back-adjust, cách xử lý quyền mua/cổ phiếu thưởng/chia tách, tính đầy đủ của actions, hoặc OHLC và Adjusted Close của mã Việt Nam cùng cơ sở.
- Chưa quan sát được Close, Adj Close, OHLC, Volume, Dividends hay Stock Splits của năm mã.
- Chưa đủ điều kiện dùng Yahoo hoặc CafeF để tính lợi suất/rủi ro trong giai đoạn này.

## 6. Bảo toàn dữ liệu

Không tải dữ liệu; không tạo thư mục staging Yahoo trong lượt này. SHA-256 sau rà soát:

- Raw: 1B492296E31DB393DA80A8D2579887BBECB4AFB95F4F3A9FF9CECCBFB5186043
- Processed: 3574059045FBD420FC0EF473FCC6671C16C3A6BDC9F57478F02A7241598FE953

Dự án D:\ASM_Hoc_May không phải Git working tree; không khởi tạo hoặc thay đổi repository.

## 7. Kết luận theo yêu cầu

1. **Mã lấy được dữ liệu thật:** Chưa mã nào được truy vấn; chưa xác minh ticker.
2. **Đủ lịch sử 5 năm:** Chưa xác minh.
3. **Cơ sở giá rõ ràng:** Chưa đủ bằng chứng cho chuỗi mã Việt Nam và phương pháp corporate actions.
4. **Corporate Actions kiểm chứng được:** Chưa xác minh coverage/độ tin cậy thực tế; có tham số actions không đồng nghĩa dữ liệu đầy đủ.
5. **Đủ điều kiện dùng cho đồ án:** Chưa. Quyền truy cập tự động, lưu trữ/hiển thị, chất lượng và price basis đều còn mở.
6. **Mở rộng lên 43 mã:** Chưa nên. Chỉ xem xét sau khi có chấp thuận bằng văn bản, nhóm duyệt thử 5 mã, và thử nghiệm xác nhận được quyền, coverage, đơn vị, cơ sở giá và corporate actions.

## 8. Điều kiện tiếp tục

Cần có xác nhận bằng văn bản từ Yahoo hoặc nhà cung cấp được ủy quyền rằng cách truy cập tự động cụ thể được cho phép; xác nhận riêng phạm vi học thuật, mã và thời gian, lưu staging, chia sẻ kết quả, website demo và thời hạn lưu. Sau đó cần nhóm đồng ý chạy thử 5 mã. Nếu không có quyền đó, không sử dụng yfinance để tải tự động.

## 9. Nguồn tham khảo

Ngày truy cập: **20/11/2026**.

1. [Yahoo Terms of Service](https://legal.yahoo.com/us/en/yahoo/terms/otos/index.html) — mục 4(9) về thu thập tự động cần cho phép trước; mục 4(10) về tạo nguồn dữ liệu cạnh tranh/thay thế.
2. [yfinance trên PyPI](https://pypi.org/project/yfinance/) — tình trạng không liên kết Yahoo, mục đích thư viện, lưu ý quyền dữ liệu/API cá nhân và phiên bản 1.8.0.
3. [Tài liệu yfinance PriceHistory](https://ranaroussi.github.io/yfinance/reference/yfinance.price_history.html) — history, auto_adjust, actions, repair, keepna và khoảng ngày start/end.

