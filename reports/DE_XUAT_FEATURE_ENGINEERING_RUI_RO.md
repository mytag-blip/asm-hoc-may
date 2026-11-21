# Đề xuất phương pháp xây dựng đặc trưng rủi ro

**Giai đoạn:** 2.5 — nghiên cứu phương pháp, chưa triển khai Feature Engineering.  
**Đề tài:** Ứng dụng các thuật toán học máy không giám sát trong phân nhóm và đánh giá mức độ rủi ro của các doanh nghiệp niêm yết trên thị trường chứng khoán Việt Nam.  
**Phạm vi:** 43 doanh nghiệp HOSE; CafeF gần 5 năm; rủi ro biến động giá cổ phiếu.

## 1. Trạng thái và nguyên tắc

- **Đã thông qua:** bảo toàn Raw/Processed; không tự sửa 16 dòng OHLC, không nội suy ngày thiếu, không xóa 1.008 cờ Volume lớn; chưa dùng Adjusted Close tính lợi suất; chưa tính Volatility khi cơ sở giá và corporate actions chưa rõ.
- **Đề xuất trong tài liệu này:** các công thức và bộ đặc trưng để nhóm xem xét. Chưa có công thức nào được phê duyệt làm pipeline chính thức.
- **Chờ bằng chứng nguồn:** cách tính Adjusted Close, cơ sở điều chỉnh của OHLC, đơn vị và trạng thái giao dịch ở ngày thiếu.
- **Chưa thực hiện:** không tính đặc trưng, không sửa dữ liệu, không huấn luyện hay phân cụm.

Nguồn EDA ghi nhận 53.385 dòng, 43 mã, 19/11/2021–18/11/2026; 16 OHLC flags; 1.008 cờ volume cao; MCH vắng 14 ngày và 7 mã vắng dữ liệu ngày 14/08/2025. Close chưa xác minh điều chỉnh corporate actions. Các trường giá trị giao dịch chưa xác minh đơn vị. Đây là các giới hạn trực tiếp đối với nghiên cứu đặc trưng.

## 2. Cơ sở giá: Close và Adjusted Close

Trong file nguồn có cả `Close` và `Adjusted Close`; hai trường khác nhau ở 46.296/53.385 dòng. Tỷ lệ có 104 thay đổi trên 5% theo cách rà của báo cáo xác minh. Các mức này tự thân không cho biết công thức hoặc xác định sự kiện chia tách/cổ tức.

CafeF công khai trang lịch sử giao dịch có các cột “Đóng cửa” và “Điều chỉnh”, cùng Open/High/Low và thông tin khớp lệnh/thỏa thuận, nhưng trang được kiểm tra không mô tả công thức Adjusted Close hoặc xác nhận OHLC đã được điều chỉnh cùng basis. [Trang lịch sử giao dịch CafeF](https://cafef.vn/du-lieu/lich-su-giao-dich-aat-1.chn) (truy cập 20/11/2026). Do đó:

- Không suy diễn Adjusted Close là total-return price, giá đã điều chỉnh đầy đủ, hoặc đồng nhất giữa các mã.
- Không tính return từ Adjusted Close trong tình trạng hiện tại.
- Không kết hợp Adjusted Close với Open/High/Low.
- Close có thể mô tả riêng theo mã theo quy tắc EDA đã duyệt; điều này chưa đủ để dùng Close cho risk return.

Để chứng minh phương pháp điều chỉnh cần có: tài liệu chính thức của CafeF/người cung cấp định nghĩa trường; hành động doanh nghiệp được điều chỉnh (cổ tức tiền, cổ tức cổ phiếu, chia/tách, phát hành quyền…); thời điểm áp dụng và cách back-adjust; xác nhận OHLC/Close có cùng basis hay không; ví dụ có thể đối chiếu với một sự kiện cụ thể và dữ liệu chính thức độc lập. Nếu không có các bằng chứng này, lựa chọn giữa Close thô và Adjusted Close phải được nhóm/giảng viên quyết định cùng với giới hạn công khai.

## 3. Các đặc trưng ứng viên

Ký hiệu (P_t) là giá đóng cửa nhất quán về cơ sở điều chỉnh, (O_t,H_t,L_t,C_t) lần lượt là Open, High, Low, Close; (V_t) là Volume. Tất cả phép tính phải riêng theo mã, sắp theo ngày. Các công thức dưới đây là định nghĩa đề xuất, không phải kết quả đã tính.

| Đặc trưng | Công thức đề xuất | Ý nghĩa | Đầu vào | Ưu điểm | Hạn chế với dữ liệu hiện tại |
|---|---|---|---|---|---|
| Daily Return | Số học: (r_t=P_t/P_{t-1}-1); log: (r_t=\ln(P_t/P_{t-1})) | Thay đổi tương đối từng phiên; đầu vào cho đặc trưng rủi ro khác | Chuỗi giá đóng cửa có cơ sở nhất quán, ngày giao dịch hợp lệ | Không phụ thuộc mức giá tuyệt đối; diễn giải được | Chưa thể tính đáng tin cậy: Adjusted Close chưa giải thích; Close chưa rõ corporate action. Không được nối hai quan sát qua ngày bị thiếu như thể là hai phiên liên tiếp. |
| Rolling Volatility | Trên cửa sổ (W): (s_{t,W}=\sqrt{\sum_{i=0}^{W-1}(r_{t-i}-\bar r)^2/(W-1)}). Có thể annualize (s\sqrt{252}) nếu quy ước 252 phiên được chấp nhận | Độ phân tán lợi suất gần đây, thay đổi theo thời gian | Daily Return đã xác thực, cửa sổ phiên thống nhất | Nhận diện biến động theo chế độ thị trường; cùng đơn vị tương đối giữa mã | Phụ thuộc hoàn toàn vào cơ sở giá; cửa sổ bị đứt bởi ngày thiếu. Cần chốt W, yêu cầu đủ quan sát, ddof và annualization. Rolling standard deviation trong pandas dùng ddof=1 mặc định, khác NumPy mặc định; cần ghi rõ khi triển khai. [Pandas Rolling.std](https://pandas.pydata.org/docs/reference/api/pandas.api.typing.Rolling.std.html) |
| Average Return | ̄r = (\frac{1}{n}\sum r_t), trong cửa sổ/period đã xác định | Mức tăng/giảm trung bình, cung cấp bối cảnh lợi nhuận chứ không đo trực tiếp rủi ro | Daily Return đã xác thực | Giúp tách “rủi ro cao” khỏi “lợi nhuận cao/thấp” khi diễn giải cụm | Trung bình có thể gần 0 dù biến động lớn; nhạy với giai đoạn, dấu và outlier. Không nên là feature rủi ro cốt lõi; có thể báo cáo riêng hoặc dùng để diễn giải. |
| Maximum Drawdown | (D_t=P_t/\max_{s\le t}P_s-1); (MDD=\min_t D_t) trong kỳ. Có thể báo cáo độ lớn dưới dạng (-MDD) dương | Mức sụt giảm sâu nhất từ đỉnh trước đó đến đáy, nắm bắt rủi ro giảm giá | Chuỗi giá/wealth index nhất quán qua corporate actions và thời kỳ xác định | Diễn giải tốt về sụt giảm tích lũy; bổ sung cho độ lệch chuẩn hai phía | Không đáng tin nếu giá chưa được điều chỉnh đúng khi có corporate action; kỳ 5 năm khác nhau khi độ phủ không đều. GIPS định nghĩa drawdown theo mức giảm peak-to-trough trên giá trị/returns trong kỳ. [CFA Institute GIPS Handbook](https://www.gipsstandards.org/wp-content/uploads/2021/06/gips-standards-fmp-handbook.pdf) |
| ATR | (TR_t=\max(H_t-L_t,|H_t-C_{t-1}|,|L_t-C_{t-1}|)); ATR là trung bình làm mượt TR, thường Wilder (ATR_t=(ATR_{t-1}(n-1)+TR_t)/n). Biến thể chuẩn hóa (NATR_t=ATR_t/C_t\times100\%) | Biên độ dao động thực, gồm gap qua close phiên trước; ATR có đơn vị giá, NATR tương đối | OHLC nhất quán theo cơ sở điều chỉnh, close trước, chuỗi ngày phiên | Khai thác range trong ngày/gap mà return close-to-close bỏ qua | 16 dòng vi phạm quan hệ OHLC trực tiếp làm TR/ATR đáng ngờ; basis OHLC chưa xác minh; NATR vẫn sai nếu giá adjustment không nhất quán. TA-Lib cung cấp ATR với high/low/close và chu kỳ mặc định phổ biến 14, nhưng chu kỳ cần nhóm chốt. [TA-Lib ATR](https://ta-lib.github.io/ta-lib-python/func_groups/volatility_indicators.html) |
| Average Volume | (\bar V_W=\frac1W\sum_{i=0}^{W-1}V_{t-i}), theo cửa sổ hoặc kỳ xác định | Hoạt động khối lượng giao dịch; không đo trực tiếp rủi ro giá | Volume; nếu so sánh mã cần đơn vị/định nghĩa nhất quán | Bổ sung bối cảnh giao dịch, có thể giúp giải thích quan sát cực đoan | Không được gọi là thanh khoản khi đơn vị và cách gộp khớp lệnh/thỏa thuận chưa được xác minh. Lệch phân phối và 1.008 cờ lớn làm mean nhạy; không tự loại. Nên là biến bổ trợ, không thuộc bộ rủi ro giá lõi. |

`Rolling Volatility` thường là chuỗi theo thời gian; để phân cụm 43 doanh nghiệp thành một hàng/mã cần quy tắc tổng hợp rõ (ví dụ median hoặc phân vị cao của rolling volatility trong kỳ). Không chọn mặc định khi chưa có quyết định nhóm.

## 4. Vấn đề dữ liệu và ảnh hưởng theo đặc trưng

### 16 dòng OHLC bất thường

Giữ nguyên. Các cờ là 8 `High < Close`, 1 `Low > Open`, 7 `Low > Close`; 15 dòng có Close ngoài [Low, High]. Đã xác nhận khớp workbook CafeF nhưng chưa có nguồn giao dịch độc lập.

- Ảnh hưởng trực tiếp: ATR/True Range, do dùng High/Low/Open/Close; các dòng phải được gắn cờ, quyết định riêng trước khi tính ATR.
- Daily Return, rolling volatility, average return và drawdown dùng Close-to-Close; quan hệ OHLC bất hợp lệ không tự chứng minh Close sai, nhưng các điểm này vẫn cần cảnh báo và kiểm tra tính nhất quán với sự kiện/giá nguồn trước khi chấp nhận chuỗi Close.
- Average Volume không phụ thuộc OHLC.
- Không tự sửa hoặc xóa. Nếu nhóm cho phép loại khỏi phép tính cụ thể, chỉ loại ở phép tính đó, có provenance và báo số dòng ảnh hưởng.

### Ngày thiếu

Không có lịch HOSE hoàn chỉnh gắn vào dữ liệu; ngày thiếu so với hợp ngày quan sát không tự chứng minh mã có phiên giao dịch. Với 7 mã thiếu 14/08/2025, có bằng chứng HOSE công bố giao dịch toàn thị trường ngày đó, nhưng không rõ trạng thái từng mã. MCH vắng 14 ngày; chưa phân loại từng ngày.

- Không nội suy, forward-fill hay tính return giữa hai quan sát cách nhau qua ngày vắng như lợi suất một phiên.
- Với return/rolling volatility, MDD và ATR, cần phân biệt chuỗi phiên thực có bằng lịch HOSE với khoảng trống dữ liệu; nếu chưa xác minh, đánh dấu khoảng cách quan sát và không giả định phiên liền nhau.
- Average Volume theo số dòng có thể bị lệch khi ngày vắng là ngày giao dịch bị thiếu; không đổi ngày vắng thành volume 0.

### Corporate actions

Cổ tức cổ phiếu, chia/tách, quyền mua hoặc điều chỉnh giá có thể tạo thay đổi biểu kiến trong chuỗi giá. Không có lịch sự kiện đầy đủ/định nghĩa Adjusted Close nên chưa đánh giá được magnitude/impact cho từng mã. Đây là lý do chặn return, volatility và drawdown đáng tin cậy, không phải lý do tự hiệu chỉnh dữ liệu.

### Volume lớn và đơn vị

Volume = Matched Volume + Negotiated Volume đã được kiểm tra trên toàn Processed. 1.008 cờ Q3+3×IQR là dấu hiệu thống kê, không phải lỗi xác nhận. Average Volume có thể bị những điểm này chi phối. Đơn vị của Volume/giá trị chưa được tài liệu hóa đầy đủ trong dữ liệu dự án; không kết luận thanh khoản.

## 5. Đề xuất bộ đặc trưng

### Bộ tối thiểu — đề xuất, chưa thông qua

Chỉ sau khi nhóm xác nhận cơ sở giá, chất lượng phiên và chính sách OHLC, đề xuất bắt đầu với hai đại lượng mỗi mã trên cùng một giai đoạn so sánh:

1. **Độ lệch chuẩn Daily Return theo kỳ** (mức biến động tổng thể).
2. **Maximum Drawdown theo kỳ** (mức sụt giảm cực đại).

Hai đại lượng bổ sung góc nhìn khác nhau: độ lệch chuẩn xem biến động hai chiều; drawdown nhấn mạnh sụt giảm từ đỉnh. Dùng cùng kỳ lịch/độ dài quan sát; nếu độ phủ không cân bằng cần báo cáo số return hợp lệ và quy tắc kỳ. Rolling volatility có thể được chọn thay thế/thêm vào khi nhóm muốn mô tả biến động cục bộ, nhưng tránh đưa đồng thời nhiều đại lượng gần trùng mà không kiểm tra tương quan/redundancy.

### Bộ mở rộng — đề xuất, chưa thông qua

- Median hoặc phân vị cao của rolling volatility theo cửa sổ đã chốt để mô tả mức/cao điểm biến động.
- ATR chuẩn hóa (NATR) để bổ sung biên độ trong phiên, chỉ sau khi basis OHLC và 16 cờ được giải quyết.
- Average Return như biến bối cảnh, không gắn nhãn rủi ro.
- Average Volume/Matched/Negotiated Volume làm đặc trưng phụ chỉ khi đơn vị, định nghĩa và cách xử lý cờ volume được xác nhận; nếu không, chỉ báo cáo mô tả riêng.

Không đưa toàn bộ ứng viên vào clustering mặc định. Trước khi chọn, kiểm tra tương quan/redundancy, phân phối và cách chuẩn hóa trên ma trận 43 hàng; quyết định feature set phải có giải thích tài chính và ghi nhận được nhóm duyệt.

## 6. Khả năng triển khai từ dữ liệu hiện tại

| Ứng viên | Trạng thái hiện tại | Lý do |
|---|---|---|
| Daily Return | Chưa thể tính đáng tin cậy | Giá chưa có cơ sở corporate-action được xác nhận; ngày vắng cần xử lý theo phiên thật. |
| Rolling Volatility | Chưa thể tính đáng tin cậy | Phụ thuộc return, cửa sổ và căn chỉnh phiên; không được tính trước khi chốt giá. |
| Average Return | Chưa thể tính đáng tin cậy | Phụ thuộc return; hơn nữa không phải thước đo rủi ro thuần. |
| Maximum Drawdown | Chưa thể tính đáng tin cậy | Cần chuỗi giá/wealth nhất quán qua corporate actions và kỳ so sánh chuẩn. |
| ATR | Chưa thể tính đáng tin cậy | 16 OHLC bất thường và adjustment basis chưa giải quyết. |
| Average Volume | Có thể mô tả thống kê; dùng làm feature cần xác minh | Trường có sẵn và phép tổng đúng; 1.008 cờ cần giữ, đơn vị/định nghĩa chưa đủ để kết luận thanh khoản. |

Vì vậy, hiện chưa có feature rủi ro giá nào được xác nhận đủ để tính và đưa vào clustering. Đây là kết luận về bằng chứng và phương pháp, không phải lỗi phần mềm.

## 7. Các quyết định cần nhóm xác nhận

1. Nếu CafeF không cung cấp công thức Adjusted Close, nhóm có chấp thuận Close chưa điều chỉnh làm cơ sở nghiên cứu không, với giới hạn corporate actions được công khai?
2. Chọn phương pháp lợi suất (số học hay log), độ dài kỳ và cửa sổ volatility; có annualize hay không?
3. Chọn cách tổng hợp rolling volatility thành một giá trị mỗi doanh nghiệp.
4. Chọn quy tắc MDD (toàn kỳ hay kỳ con) và xử lý giai đoạn thiếu phiên.
5. Có đưa ATR/NATR vào bộ mở rộng sau khi xác minh OHLC không?
6. Volume chỉ là biến bổ trợ mô tả hay feature; bằng chứng đơn vị/định nghĩa nào sẽ yêu cầu từ CafeF?
7. Chốt cách xử lý 16 OHLC bất thường và yêu cầu độ phủ tối thiểu từng mã.

## 8. Nguồn phương pháp tham khảo

- CafeF, *Lịch sử giao dịch* — xác định tên trường được hiển thị; không có công thức điều chỉnh được nêu trên trang đã kiểm tra. [cafef.vn](https://cafef.vn/du-lieu/lich-su-giao-dich-aat-1.chn) (truy cập 20/11/2026).
- pandas, `Rolling.std` — định nghĩa độ lệch chuẩn cửa sổ và `ddof` mặc định bằng 1. [pandas.pydata.org](https://pandas.pydata.org/docs/reference/api/pandas.api.typing.Rolling.std.html) (truy cập 20/11/2026).
- CFA Institute, *GIPS Standards for Fiduciary Management Providers Handbook* — mô tả Maximum Drawdown là loss peak-to-trough trong kỳ và công thức (Trough − Peak)/Peak. [GIPS Handbook PDF](https://www.gipsstandards.org/wp-content/uploads/2021/06/gips-standards-fmp-handbook.pdf) (truy cập 20/11/2026).
- TA-Lib, *Volatility Indicators* — liệt kê ATR nhận High/Low/Close và NATR. [TA-Lib](https://ta-lib.github.io/ta-lib-python/func_groups/volatility_indicators.html) (truy cập 20/11/2026).

## 9. Phân định đề xuất, thông qua và chờ xác minh

- **Đã thông qua:** ràng buộc bảo toàn dữ liệu và không dùng Adjusted Close tính lợi suất/không tính Volatility trước khi cơ sở giá được thống nhất.
- **Đề xuất, chờ nhóm duyệt:** bộ tối thiểu Daily Return dispersion + Maximum Drawdown; bộ mở rộng có rolling volatility, NATR, Average Return và volume như biến phụ.
- **Chờ bằng chứng nguồn:** công thức Adjusted Close/corporate actions; điều chỉnh basis OHLC; lịch giao dịch và trạng thái từng mã ở ngày vắng; đơn vị và định nghĩa các cột volume/value.

Tài liệu này chỉ là nghiên cứu phương pháp. Chưa sửa Raw/Processed, chưa tạo dữ liệu phân tích, chưa tính đặc trưng, chưa thay đổi cấu trúc, API hoặc giao diện, và chưa huấn luyện hay phân cụm.
