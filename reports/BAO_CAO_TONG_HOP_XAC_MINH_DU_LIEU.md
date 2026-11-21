# BÁO CÁO TỔNG HỢP XÁC MINH DỮ LIỆU

**Giai đoạn:** 2.9 – rà soát bằng chứng nguồn dữ liệu  
**Ngày tổng hợp:** 20/11/2026  
**Phạm vi:** 43 doanh nghiệp HOSE; CafeF; OHLCV, 19/11/2021–18/11/2026.

## 1. Mục tiêu và nguồn tài liệu

Đánh giá liệu bộ Processed hiện tại có đủ căn cứ để xây dựng risk features và phân cụm. Đây là tổng hợp hồ sơ đã có, không phải xác minh mới từ CafeF/HOSE/SSI/DNSE; không gọi API, không tải dữ liệu, không sửa CSV và không tính đặc trưng.

Đã đối chiếu các tài liệu: `reports/BAO_CAO_CHAT_LUONG_DU_LIEU.md`, `reports/BAO_CAO_XAC_MINH_DU_LIEU.md`, `reports/BAO_CAO_XAC_MINH_CO_SO_GIA.md`, `reports/BAO_CAO_KHAO_SAT_NGUON_DU_LIEU_GIA.md`, `reports/KE_HOACH_XAC_MINH_NHA_CUNG_CAP.md`, `PHUONG_PHAP_XU_LY_DU_LIEU.md` và `PROJECT_PROGRESS.md`.

## 2. Tóm tắt bộ dữ liệu đã xác minh

- 215/215 workbook nguồn đọc được; 43 mã HOSE; Raw 53.471 dòng, Processed 53.385 dòng sau khi loại 86 bản ghi trùng hoàn toàn.
- Khoảng ngày trong dữ liệu: 19/11/2021–18/11/2026. Có 1.242 ngày trong hợp lịch quan sát của các mã; đây không phải lịch HOSE độc lập.
- Processed chuẩn hóa `Date`, `Ticker`, OHLC, `Adjusted Close`, các thành phần Volume/Value và tổng `Volume`; provenance của Raw được giữ.
- Tất cả 16 cờ bất nhất OHLC trong Processed khớp chính xác workbook nguồn; điều này xác minh thao tác hợp nhất, không xác minh giá có đúng với giao dịch.
- Không có câu trả lời mới của nhà cung cấp trong bảng theo dõi Giai đoạn 2.8: trạng thái câu hỏi vẫn là `Chưa liên hệ`. SSI/DNSE chỉ là khảo sát tài liệu; không có response API thực tế.

## 3. Bảng tổng hợp vấn đề và quyết định sử dụng

| Vấn đề/trường | Bằng chứng hiện có | Trạng thái | Sử dụng được hiện nay | Bằng chứng/hành động còn thiếu |
|---|---|---|---|---|
| Close | Có trong toàn bộ dữ liệu chuẩn; 15 giá trị nằm ngoài `[Low, High]` thuộc 16 dòng bất nhất OHLC. Không có nguồn giao dịch độc lập xác nhận. | **Có thể sử dụng có điều kiện** | EDA mô tả theo mã; không suy diễn risk/return qua corporate actions. Chưa đủ điều kiện tính Daily Return, Rolling Volatility hoặc Maximum Drawdown. | CafeF xác nhận basis, đơn vị, cách cập nhật corporate actions; đối chiếu 16 dòng và quy tắc được nhóm duyệt cho các quan sát đó. |
| Adjusted Close | Khác Close ở 46.296/53.385 dòng; tỷ lệ min 0,2988, median 0,8148; có 104 lần thay đổi tỷ lệ trên 5%. CafeF chưa công bố công thức/loại sự kiện/back-adjust. | **Chưa xác minh; không đủ điều kiện sử dụng cho risk features** | Có thể mô tả riêng trong báo cáo chất lượng, không gọi đây là total-return/adjusted series đã xác nhận. | Data dictionary/methodology chính thức, corporate-action scope, cách làm tròn và hồi tố, ví dụ tính; xác nhận nhất quán theo thời gian. |
| Open/High/Low | Có dữ liệu; 16 dòng vi phạm quan hệ OHLC; chưa xác nhận cùng basis với Adjusted Close hoặc Close đã điều chỉnh hay raw. | **Không đủ điều kiện cho đặc trưng dùng OHLC; EDA mô tả có điều kiện** | Chưa dùng ATR, True Range, intraday range hoặc kết hợp OHLC với Adjusted Close. | CafeF xác nhận giá basis từng trường; đối chiếu độc lập các dòng ngoại lệ và thống nhất xử lý từng cờ. |
| Corporate actions | Đã rà một số ví dụ FPT/NLG quanh cổ tức tiền, phát hành từ vốn chủ và quyền mua; quan sát tương thích với khả năng có điều chỉnh nhưng không chứng minh công thức. Chưa lập ledger đầy đủ cho 43 mã. | **Chưa xác minh đầy đủ** | Không tự điều chỉnh giá; không tính biến động xuyên sự kiện như chuỗi nhất quán. | Event ledger theo ticker/ngày/loại/tỷ lệ từ HOSE/VSDC/issuer; methodology giá từ CafeF/provider. Bao gồm cash dividend, stock dividend/bonus, rights issue, split/reverse split và sự kiện khác. |
| 16 dòng OHLC bất thường | 16/16 khớp workbook; 12 dòng tập trung 06–08/05/2025; chưa xác nhận độc lập với giao dịch. | **Đã xác minh nguồn gốc nội bộ; tính đúng giao dịch chưa xác minh** | Giữ nguyên; loại khỏi phép tính cụ thể chỉ sau khi có quy tắc được duyệt và ghi nhận. Không sửa/xóa Raw. | Feed độc lập hoặc xác nhận nguồn; quyết định nhóm về từng công thức/quan sát. |
| Ngày thiếu MCH (14 ngày) | Ngày vắng trong dữ liệu nguồn; so sánh với hợp ngày quan sát 43 mã, không phải lịch HOSE. | **Chưa phân loại** | Giữ thiếu; không fill/interpolate và không tự loại mã. | Lịch phiên chính thức cộng trạng thái/niêm yết/đình chỉ theo từng ngày và mã. |
| Ngày 14/08/2025 ở 7 mã | CafeF thiếu bản ghi cho VGC, VHC, VHM, VIC, VJC, VNM, VRE. Hồ sơ phương pháp dẫn báo cáo HOSE tổng hợp giao dịch ngày này với dữ liệu toàn thị trường. Điều đó hỗ trợ kết luận thị trường có giao dịch; không xác định nguyên nhân mỗi mã thiếu bản ghi. | **Ngày thị trường có giao dịch: có bằng chứng; nguyên nhân thiếu theo mã: chưa xác minh** | Không tự tạo phiên/giá; ghi nhận là missing theo mã. | Đối chiếu dữ liệu trading status và response CafeF/nguồn độc lập cho từng ticker/ngày; không quy nguyên nhân cho cả bảy mã từ bằng chứng aggregate. |
| Volume / Matched Volume / Negotiated Volume | Phép cộng `Volume = Matched Volume + Negotiated Volume` đúng toàn bộ Processed; không âm. Negotiated Volume có 36.794 số 0. 1.008 dòng bị cờ Q3+3×IQR riêng mã. | **Công thức tổng đã xác minh trong file; semantics/đơn vị chỉ có điều kiện** | EDA mô tả theo mã và thành phần, giữ cờ 1.008; không gọi outlier thống kê là lỗi hay kết luận thanh khoản. Chưa dùng làm đặc trưng rủi ro chính thức. | CafeF xác nhận đơn vị, phạm vi giao dịch (khớp/thỏa thuận), ý nghĩa 0 và đơn vị/định nghĩa từng thành phần. |
| Matched Value / Negotiated Value | Có trường nguồn nhưng đơn vị/thang số/định nghĩa chưa được chứng minh. | **Không đủ điều kiện diễn giải/đưa vào features** | Chỉ giữ truy vết và rà nguồn; không gọi là VND hay suy ra giá trị thanh khoản. | Data dictionary và đơn vị xác nhận của CafeF. |
| Date / Ticker | Ngày và mã chuẩn hóa; 43 mã được đối chiếu với workbook và danh sách Processed. Hợp ngày không phải lịch giao dịch độc lập. | **Có thể dùng làm khóa/trục, có điều kiện về missing** | Dùng groupby/index, mô tả độ phủ; không coi ngày giữa hai quan sát là phiên liên tục nếu chưa xác minh calendar. | Lịch HOSE chính thức và mapping ticker/lịch sử mã nếu phân tích panel qua niêm yết/đổi mã. |

## 4. Bằng chứng mới hay không?

Không thấy bằng chứng mới giải quyết cơ sở giá hoặc Adjusted Close. Báo cáo 2.7 chỉ khảo sát tài liệu SSI/DNSE; chưa có quyền truy cập/response thực tế, chưa xác định price basis và bảng liên hệ 2.8 vẫn `Chưa liên hệ`.

Một cập nhật trong hồ sơ phương pháp nêu tài liệu tổng hợp giao dịch HOSE ngày 14/08/2025. Phạm vi chứng minh chỉ là ngày có giao dịch toàn thị trường. Nó **không** chứng minh bảy mã đều được giao dịch, không giải thích tại sao file CafeF của từng mã thiếu dòng và không cho phép nội suy.

Các quan sát CafeF quanh sự kiện FPT/NLG vẫn là dấu hiệu cần hỏi nhà cung cấp, không phải bằng chứng công thức. Việc 16 dòng khớp workbook xác nhận file đã được đọc đúng, không xác nhận nguồn giá chính xác.

## 5. Trường nào đủ căn cứ cho các risk features?

### Daily Return

**Chưa có trường giá đủ điều kiện hiện tại.** Chỉ có thể tính sau khi provider xác nhận chuỗi giá đóng cửa đã được điều chỉnh nhất quán qua corporate actions, hoặc nhóm/giảng viên chấp thuận một nguồn/chuỗi khác có methodology minh bạch. Không dùng Close thô/Adjusted Close hiện tại trong phép tính nghiên cứu khi chưa có quyết định. Không trộn các basis.

### Rolling Volatility

**Chưa đủ điều kiện.** Cần chuỗi return được xây từ một cơ sở giá nhất quán, ngày giao dịch được căn chỉnh đúng và chính sách cho missing/corporate actions đã chốt. Rolling window không khắc phục được sai cơ sở giá đầu vào.

### Maximum Drawdown

**Chưa đủ điều kiện.** Cần wealth/index series dựa trên returns nhất quán hoặc chuỗi total-return được provider xác nhận; Adjusted Close hiện chưa có methodology xác nhận. Không dùng giá tuyệt đối không điều chỉnh qua các corporate actions.

### ATR / True Range và đặc trưng OHLC khác

**Không đủ điều kiện hiện tại.** Cần xác nhận Open/High/Low/Close cùng basis, xử lý được 16 bất nhất, xác minh đơn vị/scale và liên hệ với previous close sau corporate actions.

### Volume và đặc trưng từ Volume

Chỉ phù hợp cho **EDA mô tả có cảnh báo**. Trước khi tạo Average Volume, volume variability hoặc đặc trưng thanh khoản/rủi ro cần xác nhận định nghĩa/đơn vị và cân nhắc thỏa thuận/khác biệt coverage. Không dùng đơn vị suy đoán và không loại 1.008 dòng bị cờ.

### Ticker/Date

Có thể dùng làm định danh/khóa và để mô tả coverage, nhưng phải xử lý missing/date alignment rõ ràng. Không coi hợp ngày quan sát là lịch HOSE chính thức.

## 6. Phương án phù hợp với phạm vi 43 doanh nghiệp HOSE

1. Giữ Raw bất biến; không sửa Processed hiện tại cho tới khi nhóm duyệt phương pháp. Mọi thử nghiệm sau này phải là bản dẫn xuất riêng có provenance.
2. Gửi câu hỏi bằng văn bản cho CafeF theo `reports/KE_HOACH_XAC_MINH_NHA_CUNG_CAP.md`: adjusted methodology, corporate actions, basis từng OHLC, units, volume semantics, lịch cập nhật/sửa hồi tố, và quyền dùng học thuật.
3. Nếu CafeF không trả lời được, nhóm có thể xin phép thử nghiệm mẫu 3–5 mã từ SSI/DNSE sau khi quyền truy cập/điều khoản hợp lệ và provider trả lời price basis/history/units. Đây là đề xuất cần nhóm phê duyệt, không phải nguồn đã được chọn.
4. Lập event ledger cho 43 mã dựa trên thông báo HOSE/VSDC/issuer; đồng thời đối chiếu từng mã/ngày bị thiếu và 16 record OHLC bằng bằng chứng độc lập.
5. Nhóm/giảng viên cần quyết định chấp nhận nguồn/methodology nào. Sau đó khóa data dictionary, đơn vị, quy tắc missing/outlier, cách loại trừ quan sát cụ thể và data-lineage.
6. Chỉ sau các bước trên mới phê duyệt riêng việc tạo bản phân tích dẫn xuất và tính risk features; tiếp đó mới đánh giá điều kiện cho phân cụm.

## 7. Phương án nghiên cứu thay thế nhưng giữ nguyên đề tài/phạm vi

Không đổi đề tài hoặc 43 doanh nghiệp. Nếu không thể xác minh CafeF, có thể đề xuất cho giảng viên một **nguồn giá thay thế có methodology và quyền sử dụng rõ**, rồi tái lập dữ liệu riêng cho cùng 43 mã/khoảng thời gian. Cần đối chiếu mẫu, coverage, corporate actions, units và điều khoản trước khi thay. SSI/DNSE hiện mới là ứng viên theo tài liệu; chưa đủ điều kiện thay thế.

Nếu chưa có nguồn hợp lệ, có thể tiếp tục công việc không phụ thuộc giá điều chỉnh (rà tài liệu, thiết kế code/tests bằng fixtures test-only, hoàn thiện dashboard/EDA mô tả) nhưng **không được tuyên bố đã đánh giá rủi ro hay phân cụm**. Nếu báo cáo clustering rủi ro là mục tiêu bắt buộc, cần chờ bằng chứng giá thay vì thay sang rủi ro tài chính hoặc dữ liệu mô phỏng.

## 8. Điều kiện còn thiếu và hành động tiếp theo

### Bằng chứng cần nhận

- CafeF/provider xác nhận công thức Adjusted Close, sự kiện được điều chỉnh, back-adjust/revision policy và basis của Open/High/Low/Close.
- Xác nhận đơn vị giá, Volume, Matched/Negotiated Value và Volume; phạm vi giao dịch thỏa thuận.
- Nguồn độc lập hoặc xác nhận giao dịch cho 16 cờ OHLC.
- Lịch HOSE và trạng thái từng mã để phân biệt ngày nghỉ, mã không giao dịch, đình chỉ hay thiếu export; đặc biệt 14 ngày MCH và bảy mã ngày 14/08/2025.
- Nếu chọn SSI/DNSE: quyền sử dụng học thuật, coverage thực 43 mã, lịch sử từ 2021, price basis, units và response kiểm thử đã được cấp phép.
- Quyết định nhóm/giảng viên về nguồn chính thức, chính sách missing/record anomaly và cho phép thử nghiệm nhỏ.

### Hành động đề xuất kế tiếp

1. Nhóm tự gửi bộ câu hỏi trong `reports/KE_HOACH_XAC_MINH_NHA_CUNG_CAP.md`, lưu trả lời/điều khoản minh chứng.
2. Cập nhật bảng theo dõi bằng câu trả lời thực, không đánh dấu xác minh từ suy luận.
3. Nhóm/giảng viên quyết định provider và quyền thử nghiệm 3–5 mã; chưa tải 43 mã trước khi test được duyệt.
4. Hoàn thành đối chiếu source/units/corporate actions và đưa ra quyết định dữ liệu bằng biên bản.
5. Khi điều kiện đầu vào đạt, phê duyệt một giai đoạn riêng cho feature engineering; báo cáo hiện tại không tự cấp phép bước đó.

## 9. Kết luận

**Dữ liệu hiện tại CHƯA đủ điều kiện triển khai Feature Engineering rủi ro hoặc phân cụm trên dữ liệu nghiên cứu.** Close chỉ dùng cho EDA mô tả theo mã với cảnh báo. Adjusted Close, Daily Return, Rolling Volatility, Maximum Drawdown và OHLC-derived ATR chưa được phép sử dụng trên chuỗi hiện tại. Volume chỉ dùng EDA mô tả có điều kiện; Value chưa đủ căn cứ diễn giải.

Kết luận này dựa trên tài liệu CafeF chưa mô tả methodology, đối chiếu 16 record chỉ với cùng workbook nguồn, ngày thiếu chưa được phân loại đầy đủ, units/semantics chưa xác nhận và không có trả lời mới từ SSI/DNSE/CafeF. Raw/Processed không bị sửa; báo cáo này không tính toán đặc trưng hay mô hình.
