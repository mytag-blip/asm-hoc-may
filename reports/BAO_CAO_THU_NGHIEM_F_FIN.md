# Báo cáo thử nghiệm nguồn dữ liệu F-Fin

**Giai đoạn:** 2.17 – Kiểm tra nguồn dữ liệu F-Fin  
**Ngày truy cập và tải tệp:** 20/11/2026 (Asia/Bangkok)  
**Trang thử nghiệm:** [F-Fin – Tải Database](https://data.thebulltrust.com/download)  
**Phạm vi nghiên cứu dự án:** 43 doanh nghiệp HOSE, 19/11/2021–18/11/2026.  
**Phạm vi mẫu của lần thử:** FPT, NLG, HPG, VNM, VIC.

## 1. Kết luận điều hành

**F-Fin chưa đủ điều kiện thay thế bộ dữ liệu CafeF cho yêu cầu OHLCV 5 năm.** Lần tải thực tế qua chức năng công khai “Nến” thành công mà không đăng ký/đăng nhập: tệp XLSX chứa đủ 5 sheet, mỗi mã có 104 bản ghi D1, tổng 520 dòng. Tuy nhiên, tệp chỉ phủ **12/06/2026–09/11/2026**, không phủ từ 19/11/2021 và cũng kết thúc trước ngày mục tiêu 18/11/2026.

Tệp có `Ngày/Giờ, Open, High, Low, Close, Volume`; không có `Ticker` thành cột (ticker được biểu diễn bằng tên sheet), `Adjusted Close` hoặc Corporate Actions. Bản thân website có mô tả một tập dữ liệu EOD riêng gồm Adjusted Close và lịch sử cổ tức tiền mặt/cổ phiếu tại ngày GDKHQ, nhưng lần tải OHLCV này không chứa các trường đó. Không thể coi hai bộ dữ liệu là cùng một chuỗi hay khẳng định các nến được điều chỉnh theo Corporate Actions.

Trong 104 ngày/mã, dữ liệu không có null, trùng ngày hoặc vi phạm các bất biến OHLC cơ bản. Nhưng so sánh theo cùng ngày với Processed CafeF cho thấy chênh lệch lớn ở FPT và VNM; việc khớp tuyệt đối ở HPG, NLG, VIC trong khoảng mẫu ngắn không chứng minh được basis hoặc độ tin cậy lịch sử 5 năm. Vì vậy, F-Fin hiện chỉ phù hợp làm **nguồn đối chiếu thử nghiệm có điều kiện**, không phải nguồn thay thế đã được xác nhận.

## 2. Phương pháp và phạm vi thử

- Mở trang tải công khai F-Fin và dùng bộ dữ liệu “Nến”, khung `D1 (1 Ngày)`.
- Chọn đúng năm mã FPT, HPG, NLG, VIC, VNM; chọn chức năng xuất XLSX và tải tệp bằng nút trên trang. Không gọi API riêng, không dùng credentials, không đăng nhập, không vượt giới hạn truy cập.
- Lưu nguyên tệp tải vào khu vực staging riêng. Không sửa tệp, Raw hoặc Processed.
- Đọc năm sheet bằng pandas; chuẩn hóa ngày chỉ trong bộ nhớ để kiểm tra, không ghi ngược vào tệp.
- Đối chiếu theo `Ticker + Date` với bản Processed CafeF hiện có, chỉ trên các ngày giao nhau. Không dùng kết quả này để xác nhận nguồn nào đúng tuyệt đối.
- “Ngày thiếu” được đánh giá bằng so sánh với tập ngày CafeF trên đúng khoảng 12/06/2026–09/11/2026. Không tự tạo lịch HOSE; khoảng cách ngày lịch lớn nhất là 6 ngày, phù hợp với việc ngày nghỉ/cuối tuần có thể xen kẽ nhưng không dùng làm kiểm chứng lịch chính thức.
- Cờ Volume lớn dùng quy tắc mô tả `Q3 + 3×IQR` riêng từng mã; đây chỉ là cờ thống kê, không phải lỗi dữ liệu.

## 3. Kết quả tải dữ liệu thực tế

| Mã | Sheet | Số dòng | Ngày đầu | Ngày cuối | Null OHLCV | Trùng Date | OHLC bất biến sai | Volume âm | Cờ Volume > Q3+3×IQR |
|---|---:|---:|---|---|---:|---:|---:|---:|---:|
| FPT | FPT | 104 | 12/06/2026 | 09/11/2026 | 0 | 0 | 0 | 0 | 1 |
| HPG | HPG | 104 | 12/06/2026 | 09/11/2026 | 0 | 0 | 0 | 0 | 0 |
| NLG | NLG | 104 | 12/06/2026 | 09/11/2026 | 0 | 0 | 0 | 0 | 2 |
| VIC | VIC | 104 | 12/06/2026 | 09/11/2026 | 0 | 0 | 0 | 0 | 1 |
| VNM | VNM | 104 | 12/06/2026 | 09/11/2026 | 0 | 0 | 0 | 0 | 4 |
| **Tổng** | **5 sheet** | **520** | **12/06/2026** | **09/11/2026** | **0** | **0** | **0** | **0** | **8** |

“OHLC bất biến sai” kiểm tra `High >= max(Open, Close)`, `Low <= min(Open, Close)` và `High >= Low`. Kết quả không phát hiện vi phạm trong tệp này. Điều đó không chứng minh rằng mỗi quan sát trùng với giao dịch/sổ lệnh chính thức.

### Độ phủ thời gian

Tệp thử nghiệm chứa 104 ngày/mã, chỉ khoảng 8,4% số quan sát mỗi mã trong khoảng gần 5 năm của CafeF hiện có (CafeF: FPT/HPG/NLG 1.242 dòng; VIC/VNM 1.241 dòng). Đây là so sánh quy mô và coverage, không phải so sánh chất lượng nguồn. Khoảng thời gian 2021–11/06/2026 không có trong tệp nến đã tải; ngày 10/11–18/11/2026 cũng không có. Vì vậy không thể xác minh khả năng xuất OHLCV 5 năm từ lần tải này.

Trong đoạn 12/06–09/11/2026, tập ngày của từng mã F-Fin khớp đúng với các ngày quan sát CafeF của cùng mã: 104/104 ngày; không có ngày F-Fin ngoài tập CafeF và không thiếu ngày CafeF trong đoạn này. Đây chỉ là so sánh với CafeF, không phân biệt được ngày nghỉ giao dịch với dữ liệu bị thiếu theo lịch HOSE độc lập.

## 4. Trường dữ liệu, định dạng và đơn vị

| Trường yêu cầu | Có trong tệp nến đã tải? | Quan sát |
|---|---|---|
| Ticker | Không thành cột | Mã được dùng làm tên sheet; khi nhập vào hệ thống phải ghi rõ nguồn mapping ticker từ tên sheet. |
| Date | Có, cột `Ngày/Giờ` | Giá trị dạng `YYYY-MM-DD`, không có giờ trong 104 dòng đã kiểm tra. |
| Open, High, Low, Close | Có | Numeric float; không có cột Adjusted Close riêng. |
| Adjusted Close | Không | Không có cột hay cờ price basis trong tệp nến. |
| Volume | Có | Integer, không âm; không có mô tả đơn vị trong header của sheet nến. |
| Corporate Actions | Không | Không có trường/action sheet trong tệp nến đã tải. |

Trang tải cho phép chọn Excel, CSV, TSV, JSON và có nút tải ZIP; trong lượt này đã **thực sự tải và kiểm tra XLSX**. Giao diện thể hiện CSV/ZIP là định dạng/chức năng sẵn có, nhưng chưa tải kiểm chứng các định dạng đó. Không thấy yêu cầu đăng ký hoặc đăng nhập khi tải tệp thử.

Website hiển thị đơn vị `VND` cho cột Close của bảng “Giá lịch sử” và `CP` cho Volume; các nhãn đó không được gắn trực tiếp cho các cột bare-name `Open/High/Low/Close/Volume` của workbook Nến. Thực nghiệm cho thấy giá của các nến HPG, NLG, VIC cùng thang số với CafeF OHLC; giá của CafeF trong tệp hiện có có thang khoảng nghìn đồng/cổ phiếu. Đây là dấu hiệu thực nghiệm, **không phải xác nhận chính thức đơn vị của F-Fin candles**. Volume có cùng bậc số với CafeF Volume (số cổ phiếu) nhưng không luôn bằng nhau; chưa có định nghĩa provider cho trường Volume trong tệp nến. Chưa xác minh Volume có bao gồm giao dịch thỏa thuận hay chỉ khớp lệnh.

## 5. Kiểm tra OHLCV và đối chiếu CafeF

Tất cả 104 ngày cho cả năm mã đều khớp ngày với CafeF trong cùng khoảng mẫu. Kết quả so sánh trực tiếp các giá trị OHLC (cùng thang số thể hiện trong tệp):

| Mã | Ngày OHLC khớp CafeF (trên 104) | Quan sát Close / cơ sở giá | Volume trùng tuyệt đối | Tỷ lệ Volume F-Fin/CafeF trung vị |
|---|---:|---|---:|---:|
| FPT | 36/104 cho từng trường O/H/L/C | Từ 12/06 có Close F-Fin 66,84 so với CafeF Close 73,50 và CafeF Adjusted Close 66,82. Trong 104 ngày, 88 Close F-Fin nằm trong 0,02 đơn vị của Adjusted Close; đây không phải bằng chứng xác nhận công thức/basis. | 13/104 | 0,884 |
| HPG | 104/104 | OHLC khớp tuyệt đối với CafeF trong toàn cửa sổ mẫu; Close và Adjusted Close CafeF cũng trùng ở cửa sổ này. | 21/104 | 0,972 |
| NLG | 104/104 | OHLC khớp tuyệt đối; không suy ra basis lịch sử ngoài cửa sổ. | 64/104 | 1,000 |
| VIC | 104/104 | OHLC khớp tuyệt đối; không suy ra basis lịch sử ngoài cửa sổ. | 72/104 | 1,000 |
| VNM | 94/104 cho từng trường O/H/L/C | 94 ngày đầu khớp; 10 ngày còn lại có chênh lệch. Tại 12/06: Close F-Fin 57,18, CafeF Close 59,00, CafeF Adjusted Close 54,66. Không rõ nguồn gốc chênh lệch. | 82/104 | 1,000 |

Tỷ lệ trung vị Volume bằng 1 không đồng nghĩa toàn bộ giá trị khớp; các count cho thấy chỉ 13–82 quan sát/mã giống tuyệt đối. Mọi chênh lệch cần giữ nguyên và được làm rõ về nguồn ghi nhận, phạm vi giao dịch, độ trễ, basis hoặc sửa dữ liệu. Không suy ra rằng các ngày mismatch là do Corporate Actions.

## 6. Corporate Actions và cơ sở giá

### Bằng chứng từ trang F-Fin

- Trang F-Fin mô tả một bộ dữ liệu riêng “Lịch sử Giá & Sự kiện Quyền Cổ tức Cuối ngày (EOD)” có **Adjusted Close** và lịch sử cổ tức tiền mặt/cổ phiếu thưởng tại ngày GDKHQ; trang ghi dữ liệu giá/quyền từ VCI và KBS.
- Trang không cung cấp trong phần đã đọc công thức điều chỉnh, danh sách đầy đủ loại sự kiện (ví dụ quyền mua/chia tách), quy tắc back-adjust, cờ điều chỉnh từng bản ghi, hay xác nhận OHLC của bộ nến được điều chỉnh cùng basis với Adjusted Close.
- Workbook nến thực tải không có Adjusted Close, action fields, nguồn con theo từng dòng hoặc metadata điều chỉnh. Do đó, không thể gắn cơ chế mô tả cho EOD Adjusted Close sang tệp nến OHLCV.

### Đánh giá

- **Close:** có thể dùng để đối chiếu mô tả trong phạm vi 104 ngày, nhưng chưa đủ cơ sở để dùng tính lợi suất/rủi ro vì price basis không được ghi và có khác biệt ở FPT/VNM.
- **Adjusted Close:** website nói có ở bộ EOD khác; chưa tải/xác minh bộ đó trong lần thử này, không có công thức/metadata. Chưa đủ bằng chứng để dùng.
- **Open/High/Low:** có trong workbook, qua kiểm tra nội bộ và khớp CafeF ở 3/5 mã trong cửa sổ ngắn; chưa xác nhận raw/adjusted hay OHLC cùng basis với Adjusted Close.
- **Corporate Actions:** website công bố lịch sử cổ tức tiền mặt và cổ phiếu thưởng trong bộ EOD; không có bằng chứng từ tệp nến rằng các sự kiện này được gắn hoặc phản ánh đồng nhất vào OHLC. Quyền mua và chia tách chưa được xác minh ở tài liệu đã kiểm tra.
- **Volume:** có trong tệp, không âm; định nghĩa đơn vị và phạm vi ghi nhận chưa được tài liệu hóa cho nến. Chênh lệch đáng kể so với CafeF cần giải thích.

Không tính Daily Return, Volatility, Maximum Drawdown, ATR hay Feature Engineering trong bước này.

## 7. CC BY 4.0, học thuật, lưu trữ và website demo

Trang F-Fin tuyên bố dữ liệu miễn phí, không cần tài khoản, chia sẻ theo CC BY 4.0, và cho phép tải/trích dẫn miễn phí cho khóa luận/bài báo; trang gợi ý ghi nguồn: **“Cổng dữ liệu Tài chính & Vĩ mô mở – CLB Tài chính F-Fin, Trường Đại học FPT Cần Thơ”**. Đây là tuyên bố của F-Fin, không phải xác minh độc lập phạm vi quyền mà F-Fin nắm đối với dữ liệu upstream VCI/KBS.

Theo [Creative Commons CC BY 4.0](https://creativecommons.org/licenses/by/4.0/), điều kiện cốt lõi khi chia sẻ gồm ghi công phù hợp, dẫn liên kết giấy phép và chỉ rõ thay đổi; trang Creative Commons cũng lưu ý license chỉ cấp những quyền mà bên cấp phép có thẩm quyền cấp và có thể còn quyền khác liên quan. Vì vậy:

- **Tải về và lưu bản thử phục vụ đồ án:** F-Fin công khai cho tải trực tiếp và tuyên bố CC BY/academic use; phù hợp để lưu staging trong phạm vi nghiên cứu theo tuyên bố đó.
- **Dùng trong đồ án/báo cáo:** được F-Fin tuyên bố cho phép với ghi nguồn; nếu biến đổi dữ liệu cần nêu rõ đã xử lý/chuyển đổi.
- **Hiển thị biểu đồ trên website demo:** CC BY cho phép chia sẻ theo điều kiện attribution nếu bộ dữ liệu thực sự thuộc phạm vi license; nên ghi nguồn, link giấy phép, ngày tải và mô tả xử lý ngay trên trang demo.
- **Điểm chưa được xác minh:** F-Fin có quyền cấp lại tất cả quyền database/data của VCI/KBS cho từng bản ghi hay không; có hạn chế downstream riêng/điều khoản khác ở tệp hoặc từng nguồn con hay không. Do đó, tuyên bố trên đủ để đánh giá sơ bộ, nhưng không phải bảo đảm pháp lý độc lập cho việc tái phân phối toàn bộ dataset nguyên bản lên website công khai.

## 8. Hạn chế và vấn đề chưa xác minh

1. Không lấy được OHLCV từ 19/11/2021 trong lần xuất; dữ liệu chỉ có 104 phiên/mã, tới 09/11/2026.
2. Chưa xác minh xem giao diện có một tùy chọn lịch sử dài hơn riêng cho nến hay không; lần thử đã xuất theo cấu hình D1 hiện hành và kiểm tra chính tệp xuất.
3. Không có Adjusted Close hoặc Corporate Actions trong workbook nến; chưa thử xuất riêng bộ “Giá ngày/Cổ tức”.
4. Chưa xác minh cách điều chỉnh Corporate Actions, raw/adjusted basis, back-adjust và sự nhất quán giữa OHLC.
5. Đơn vị chính thức của giá/Volume trong sheet nến chưa được công bố trong tệp; Volume có chênh lệch với CafeF.
6. Không đối chiếu với nguồn giao dịch chính thức HOSE/VSDC hoặc xác minh từng ngày Corporate Actions.
7. CC BY là tuyên bố của F-Fin; quyền cấp lại dữ liệu nguồn VCI/KBS chưa được xác minh độc lập.
8. CSV/ZIP được cung cấp như lựa chọn trên giao diện nhưng lượt thử này chỉ tải XLSX; chưa kiểm tra mọi định dạng xuất.

## 9. Quyết định sử dụng đề xuất

| Mục đích | Đánh giá |
|---|---|
| Thử nghiệm kỹ thuật/tương thích schema trên 5 mã | **Đạt có giới hạn**: đã tải workbook thật và xác nhận cột OHLCV, 5 sheet, 520 dòng. |
| EDA mô tả trên 104 phiên trong staging | **Có thể cân nhắc có điều kiện**, ghi rõ nguồn, cửa sổ ngắn và đơn vị/basis chưa xác minh; không thay dữ liệu nghiên cứu chính. |
| Đối chiếu với CafeF | **Có ích nhưng chưa giải thích được mismatch**, nhất là FPT/VNM và Volume. |
| Thay thế CafeF cho toàn giai đoạn OHLCV 2021–2026 | **Không đạt** từ bằng chứng thử nghiệm hiện có: thiếu phần lớn lịch sử và chưa rõ basis/đơn vị. |
| Tính Daily Return/Volatility/MDD/ATR hoặc clustering rủi ro | **Chưa đủ điều kiện** do coverage và price basis chưa rõ. |

### Bước tiếp theo được đề xuất

1. Chỉ khi nhóm cho phép, thử xuất riêng “Giá ngày” và “Cổ tức” cho cùng 5 mã; lưu tách khỏi dữ liệu CafeF và kiểm tra xem EOD history có thực sự phủ 2021–2026, Adjusted Close có đầy đủ và có metadata/units hay không.
2. Hỏi F-Fin bằng văn bản về độ sâu riêng của nến D1, đơn vị OHLC/Volume, raw/adjusted, công thức và corporate actions, chênh lệch FPT/VNM/Volume, và quyền của F-Fin đối với dữ liệu VCI/KBS khi hiển thị trên website demo.
3. Chỉ xem xét mở rộng sau khi coverage đủ, price basis/units có bằng chứng, mismatch được giải thích và quyền sử dụng downstream được làm rõ.

## 10. Tệp thử nghiệm và bảo toàn dữ liệu dự án

- Tệp thử nghiệm nguyên trạng: `data/staging/f_fin/F_FIN_CANDLES_MERGED_D1.xlsx` (120.294 bytes; 5 sheet; 520 dòng dữ liệu).
- SHA-256 staging: `93B2E82C1549F47E677A9AC93E5F0E2D6914513C4726684E93E3BAAB39C89340`.
- Raw SHA-256: `1B492296E31DB393DA80A8D2579887BBECB4AFB95F4F3A9FF9CECCBFB5186043`.
- Processed SHA-256: `3574059045FBD420FC0EF473FCC6671C16C3A6BDC9F57478F02A7241598FE953`.
- Raw và Processed không bị sửa hoặc ghi đè. Không thực hiện Feature Engineering hay clustering.

## 11. Nguồn tham khảo

1. F-Fin, [Trình tải database và lựa chọn xuất dữ liệu](https://data.thebulltrust.com/download), truy cập 20/11/2026. Bằng chứng tại giao diện công khai: định dạng xuất Excel/CSV/TSV/JSON, khu vực nến có D1 và các trường OHLCV; đã tải XLSX trực tiếp cho 5 mã.
2. F-Fin, [Nguyên tắc sử dụng, nguồn dữ liệu giá/cổ tức và tuyên bố CC BY 4.0](https://data.thebulltrust.com/download), truy cập 20/11/2026. Trang nói dữ liệu giá EOD Adjusted Close và lịch sử cổ tức tiền/cổ phiếu từ VCI/KBS; không mô tả công thức điều chỉnh hoặc OHLC basis của workbook nến.
3. Creative Commons, [Attribution 4.0 International deed](https://creativecommons.org/licenses/by/4.0/), truy cập 20/11/2026.
4. Creative Commons, [Attribution 4.0 International legal code](https://creativecommons.org/licenses/by/4.0/legalcode), truy cập 20/11/2026; license chỉ cấp quyền trong phạm vi licensor có thẩm quyền.

