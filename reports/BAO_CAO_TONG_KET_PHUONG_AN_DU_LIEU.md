# Báo cáo tổng kết và chốt phương án dữ liệu nghiên cứu

**Giai đoạn:** 2.18 – Tổng kết và chốt phương án dữ liệu  
**Ngày tổng hợp:** 20/11/2026  
**Phạm vi được áp dụng trong báo cáo:** 43 doanh nghiệp HOSE; OHLCV; 19/11/2021–18/11/2026; phân tích rủi ro biến động giá bằng học máy không giám sát.

**Lưu ý đồng bộ hồ sơ:** `PROJECT_CONTEXT.md` vẫn còn câu chữ cũ về 50 doanh nghiệp; `PROJECT_PROGRESS.md` và phạm vi công việc hiện tại ghi 43 doanh nghiệp HOSE. Báo cáo này tuân thủ phạm vi 43 theo yêu cầu mới nhất và không tự mở rộng/đổi universe. Nên đồng bộ PROJECT_CONTEXT trong một lượt tài liệu được nhóm duyệt.

## 1. Kết luận điều hành

**Chưa có nguồn nào đồng thời được xác minh đủ về coverage, cơ sở giá/corporate actions, units và quyền sử dụng để đưa vào Feature Engineering rủi ro.**

- **CafeF** là bộ dữ liệu duy nhất hiện có trong dự án với coverage thực tế toàn bộ 43 mã và gần 5 năm. Tuy vậy, 16 cờ OHLC chưa được đối chiếu với nguồn giao dịch độc lập; ngày thiếu chưa phân loại theo lịch HOSE/tình trạng từng mã; Adjusted Close chưa có methodology; đơn vị và một số semantics chưa được xác nhận; quyền sử dụng/lưu trữ/hiển thị cũng chưa có bằng chứng đủ trong hồ sơ. Hiện chỉ được giữ làm bộ dữ liệu nghiên cứu gốc/EDA mô tả có cảnh báo, không dùng để tính đặc trưng rủi ro.
- **F-Fin** đã thực sự tải được workbook D1 cho năm mã, nhưng chỉ có 520 dòng/104 phiên mỗi mã trong khoảng 12/06/2026–09/11/2026. Có mismatch OHLC ở FPT/VNM và chênh Volume; workbook không có Adjusted Close hay Corporate Actions. Không thay thế được CafeF cho kỳ 5 năm.
- **SSI, Vnstock/VCI/KBS, TCBS, Yahoo Finance, FiinQuant và DataCedar** chưa cung cấp bộ OHLCV thực tế được chấp thuận để dùng cho nghiên cứu. Trạng thái bằng chứng khác nhau theo nguồn, nêu tại bảng Mục 3; không xem schema hoặc tuyên bố trên trang nhà cung cấp như kết quả response.

### Phương án khả thi nhất hiện tại

1. **Giữ nguyên CafeF Raw/Processed làm hồ sơ nguồn gốc và tập EDA mô tả đã có; chưa thay nguồn, chưa sửa và chưa tính risk features.** Đây là phương án khả thi về continuity/coverage, không phải xác nhận rằng dữ liệu đã đủ điều kiện nghiên cứu rủi ro.
2. Nhóm/giảng viên cần quyết định có yêu cầu xác nhận bằng văn bản từ CafeF và có chấp nhận tiếp tục dùng nguồn này nếu các câu hỏi về methodology, units và quyền được trả lời hay không.
3. Nếu CafeF không thể đáp ứng, **FiinQuant là ứng viên cần hỏi báo giá/điều khoản trước** về kỹ thuật và dữ liệu; DataCedar là phương án dự phòng có chi phí công bố thấp hơn nhưng cổng source-rights là điểm chặn. Không đăng ký/mua/tải trước khi có xác nhận bằng văn bản về đúng phạm vi và quyền.
4. F-Fin có thể được khảo sát tiếp trong chính website đã thử (bộ EOD “Giá ngày/Cổ tức”), nếu nhóm cho phép; nhưng phải coi đây là một bộ khác với workbook nến D1, và nó chưa giải quyết nhu cầu OHLC đầy đủ hoặc quyền upstream.

Không có phương án thay bằng dữ liệu mô phỏng, đổi sang rủi ro tài chính doanh nghiệp, giảm universe hoặc đổi đề tài được đề xuất trong báo cáo này.

## 2. Cơ sở tổng hợp và quy tắc đánh giá bằng chứng

Đã đọc/đối chiếu các báo cáo về chất lượng, cơ sở giá, provider và thử nghiệm trong `reports/`, gồm:

- `BAO_CAO_CHAT_LUONG_DU_LIEU.md`, `BAO_CAO_XAC_MINH_DU_LIEU.md`, `BAO_CAO_XAC_MINH_CO_SO_GIA.md`, `BAO_CAO_TONG_HOP_XAC_MINH_DU_LIEU.md`.
- `BAO_CAO_KHAO_SAT_NGUON_DU_LIEU_GIA.md`, `BAO_CAO_DANH_GIA_NGUON_DU_LIEU_THAY_THE.md`, `BAO_CAO_THU_NGHIEM_NGUON_DU_LIEU_CONG_KHAI.md`, `BAO_CAO_THU_NGHIEM_YAHOO_FINANCE.md`.
- `BAO_CAO_KHAO_SAT_NHA_CUNG_CAP_DU_LIEU.md`, `BAO_CAO_XAC_MINH_FIINQUANT_DATACEDAR.md`, `BAO_CAO_THU_NGHIEM_F_FIN.md`.
- `BAO_CAO_CHUAN_BI_THU_NGHIEM_SSI.md`, `BAO_CAO_KIEM_TRA_BAO_MAT_SSI.md`, cùng `KE_HOACH_XAC_MINH_NHA_CUNG_CAP.md` và hai bản nháp email FiinQuant/DataCedar.
- `PROJECT_CONTEXT.md`, `PROJECT_PROGRESS.md`, `CHANGELOG.md`, `VIETSTOCK_DATA_RESEARCH.md` và `SSI_INTEGRATION_PLAN.md` để phân biệt lịch sử quyết định với trạng thái hiện tại.

Phân loại trong báo cáo:

- **Dữ liệu thực tế:** tệp được tải/nhận và kiểm tra trực tiếp; không đồng nghĩa đã xác nhận chính xác với sàn hoặc có quyền tái phân phối.
- **Chỉ có tài liệu:** API/schema/pricing/terms được đọc, chưa có response dữ liệu thành công.
- **Truy vấn bị từ chối:** có request đọc thực tế nhưng không nhận được dữ liệu; không suy rộng thành đánh giá chất lượng.
- **Quyền chưa xác minh:** chưa tìm thấy bằng chứng áp dụng cụ thể cho việc lưu, dùng trong đồ án, nộp cho giảng viên hoặc hiển thị demo.

## 3. Bảng so sánh các nguồn

| Nguồn | Loại bằng chứng hiện có | Coverage 43 mã / 5 năm | Giá basis, corporate actions, units | Quyền sử dụng | Đánh giá cho ASM |
|---|---|---|---|---|---|
| **CafeF** | **Có dữ liệu thực tế:** 215 XLSX nguồn; Raw/Processed hiện có. | 43 mã; Processed 53.385 dòng; dải 19/11/2021–18/11/2026; 1.242 ngày quan sát chung trong dữ liệu. | Adjusted Close chưa có công thức; OHLC cùng basis chưa xác minh; corporate actions mới đối chiếu một số case, chưa có event ledger; phép cộng Volume thành phần đúng nhưng units/semantics giao dịch cần xác nhận. | Chưa có văn bản đủ rõ về quyền dùng/lưu/chia sẻ/demo trong hồ sơ. | **Tạm giữ làm nguồn lưu trữ/EDA mô tả. Chưa đủ điều kiện tạo risk features.** |
| **SSI FastConnect** | Tài liệu API; adapter/staging code được test bằng fixture. Không có SSI response thật. | Tài liệu nói daily từ ngày mã bắt đầu giao dịch; chưa xác minh mã/ngày trong account. | Docs có OHLCV và endpoint Corporate Actions, không xác nhận OHLC raw/adjusted hoặc đơn vị Volume cụ thể. | Cần tài khoản/quyền; terms học thuật/lưu/hiển thị chưa xác minh. Nhóm đã quyết định không tiếp tục vì quy trình thông tin cá nhân; không yêu cầu credentials. | **Không theo đuổi ở quyết định hiện tại; fixture không phải dữ liệu SSI.** |
| **Vnstock (VCI/KBS)** | Thư viện client và tài liệu; không có dữ liệu thật. Vnstock không phải nhà cung cấp. | VCI/KBS legacy không còn được Vnstock 6.0.1 hiện hành hỗ trợ theo tài liệu; không gọi endpoint ngoài tài liệu. | Không có response basis/actions/units để đánh giá. | Quyền phụ thuộc upstream, chưa xác minh. | **Không dùng VCI/KBS legacy; không coi Vnstock là nguồn thay thế.** |
| **TCBS OpenAPI** | Tài liệu endpoint và một GET ẩn danh thật với FPT. Kết quả HTTP 401, 0 dòng. | Coverage/lịch sử chưa kiểm tra; request từ chối trước khi có dữ liệu. | Docs không xác nhận adjusted/raw, corporate actions hoặc units. | Quy trình chính thức cần TCInvest/API Key/iOTP; không phù hợp lựa chọn không dùng credentials cá nhân. | **Không có OHLCV thực; không đủ điều kiện.** |
| **Yahoo Finance / yfinance** | Đọc Terms/docs; **không gọi API** vì quyền truy cập tự động chưa được xác nhận. | Năm mã .VN chưa được xác minh; 0 dòng thử nghiệm. | Không có response OHLC/actions/basis/units. Tham số thư viện không chứng minh dữ liệu hay công thức Yahoo. | Yahoo Terms yêu cầu cho phép rõ trước khi tự động truy cập; quyền academic/storage/demo chưa được xác minh. | **Không truy vấn/không dùng trong trạng thái hiện tại.** |
| **FiinQuant** | Tài liệu Python, pricing/terms và quotation được rà soát; không đăng ký/gọi API. | Docs và các bảng lịch sử không nhất quán; chưa có response xác nhận 43 mã/đúng 5 năm. | Có cờ `adjusted`; công thức/event handling chưa rõ; Volume được mô tả là khối lượng khớp, unit/phạm vi cần hỏi. | Quyền raw local, nộp file, academic/demo chưa rõ; terms có hạn chế chuyển giao. | **Ứng viên cần hỏi trước; không phải nguồn đã chọn.** |
| **DataCedar** | Tài liệu API/pricing/Data Rights; không tạo account/key hoặc gọi API. | Trang HOSE claims coverage; tài liệu riêng có history back-to-listing nhưng pricing tổng quát không nhất quán; chưa audit 43 mã. | Có mode raw/split/dividend/all theo docs; event coverage đầy đủ và semantics OHLC cần xác minh. Trang mô tả giá VND/Volume shares; loại giao dịch vẫn cần hỏi. | Data Rights nói API access không tự cấp quyền; Terms/upstream rights và academic/storage/demo chưa được xác nhận. | **Dự phòng về giá/khả năng kỹ thuật, nhưng quyền là điểm chặn.** |
| **F-Fin** | **Có dữ liệu thực tế:** workbook XLSX nến D1 tải công khai cho 5 mã. | 520 dòng; 104/mã; chỉ 12/06/2026–09/11/2026, không đủ 5 năm. | Workbook OHLCV không có Adjusted Close/actions; mismatch tại FPT/VNM và Volume; đơn vị/basis nến chưa có bằng chứng chính thức. | F-Fin tuyên bố CC BY 4.0 và cho phép academic use; quyền upstream VCI/KBS độc lập chưa xác minh. | **Không thay được CafeF cho kỳ nghiên cứu; chỉ đối chiếu/EDA staging có điều kiện.** |

## 4. Đánh giá bộ dữ liệu CafeF hiện tại

### 4.1 Coverage và cấu trúc đã kiểm tra

- 215/215 XLSX đọc được, 43 mã; 53.471 dòng Raw, 53.385 dòng Processed sau khi bỏ 86 dòng trùng hoàn toàn.
- Khoảng ngày quan sát 19/11/2021–18/11/2026; hợp lịch 1.242 ngày là lịch suy ra từ các tệp, không phải lịch HOSE độc lập.
- Schema hiện có Date, Ticker, Open, High, Low, Close, Adjusted Close, Volume, Matched Volume/Value, Negotiated Volume/Value và provenance.
- Dữ liệu đã chuẩn hóa cấu trúc, không có thiếu giá trị ở 12 trường chuẩn; điều này không xác minh độ đúng kinh tế của từng giá trị.

### 4.2 16 cờ OHLC

16/16 dòng trong Processed trùng với đúng dòng Excel nguồn. Bất biến bị vi phạm gồm 8 trường hợp High < Close, 1 Low > Open, 7 Low > Close; 15 Close ngoài [Low, High]. 12/16 dòng tập trung trong các ngày 06–08/05/2025. Đối chiếu nguồn gốc chỉ chứng minh quá trình hợp nhất đã đọc đúng file, **không** xác nhận giá nguồn đúng với giao dịch. Không được tự sửa/xóa.

### 4.3 Ngày thiếu

- MCH có 14 ngày vắng trong hợp ngày quan sát các mã.
- VGC, VHC, VHM, VIC, VJC, VNM và VRE đều thiếu ngày 14/08/2025. Hồ sơ có bằng chứng ngày đó thị trường có giao dịch toàn thị trường, nhưng chưa giải thích trạng thái giao dịch hoặc lý do thiếu của từng mã.
- Không nội suy hoặc coi hợp ngày 43 mã là lịch HOSE chính thức. Cần lịch sàn và trạng thái từng mã/ngày.

### 4.4 Close, Adjusted Close và corporate actions

- Adjusted Close khác Close ở 46.296/53.385 dòng; tỷ lệ Adjusted Close/Close có median 0,8148 và có 104 thay đổi trên 5% giữa các phiên.
- CafeF chưa công bố công thức, danh sách đầy đủ sự kiện điều chỉnh, quy tắc back-adjust/revision hoặc việc OHLC có cùng basis với Adjusted Close.
- Tài liệu HOSE/VSDC và trang doanh nghiệp xác nhận một số case cổ tức tiền, phát hành cổ phiếu từ vốn chủ, quyền mua của FPT/NLG. Các cột giá quanh sự kiện chỉ là dấu hiệu; không chứng minh thuật toán CafeF. Chưa lập ledger cho đủ 43 mã và chưa xác minh đầy đủ split/reverse split.
- **Chưa có trường giá nào được xác nhận để tính Daily Return/Volatility/MDD** trên toàn kỳ. Open/High/Low cũng chưa đủ điều kiện ATR/True Range.

### 4.5 Volume, giá trị và units

- Công thức `Volume = Matched Volume + Negotiated Volume` đúng trên Processed; cả hai thành phần không âm.
- 1.008 dòng cờ Q3 + 3×IQR là cờ thống kê, không phải lỗi; giữ nguyên.
- Có thể mô tả Volume và hai thành phần trong EDA theo quy tắc đã duyệt; không kết luận thanh khoản khi chưa xác minh unit/định nghĩa, ý nghĩa các số 0 và phạm vi giao dịch được ghi nhận.
- Matched Value và Negotiated Value chưa đủ bằng chứng về đơn vị/thang số để diễn giải hoặc dùng làm feature.

**Quyết định hiện hành:** giữ bộ CafeF làm nguồn gốc và tập EDA mô tả đã lưu; không dùng nó như risk-ready data. Raw và Processed không bị thay đổi trong Giai đoạn 2.18.

## 5. Đánh giá riêng F-Fin

- Tải thật một XLSX nến D1 qua giao diện không đăng nhập: 5 sheet (FPT, HPG, NLG, VIC, VNM), 104 dòng/mã, tổng 520; khoảng ngày 12/06/2026–09/11/2026.
- Không có null, duplicate Date, OHLC invariant violation hoặc Volume âm; có 8 cờ Volume lớn Q3+3×IQR. Các cờ này không xác nhận lỗi.
- Ngày trong đoạn mẫu khớp tập ngày CafeF. OHLC khớp 104/104 ở HPG/NLG/VIC; 36/104 ở FPT và 94/104 ở VNM. Volume trùng tuyệt đối 13–82 dòng/mã. Chênh lệch chưa được giải thích; không quy nguyên nhân cho Corporate Actions.
- File có ngày và OHLCV, nhưng ticker nằm ở tên sheet; không có Adjusted Close hay Corporate Actions. Tài liệu F-Fin nói có một bộ EOD riêng chứa Adjusted Close và lịch sử cổ tức từ VCI/KBS, nhưng chưa xuất bộ đó trong thử nghiệm và không áp đặc tính ấy sang workbook nến.
- F-Fin tuyên bố miễn phí/không tài khoản/CC BY 4.0 và cho phép dùng học thuật. Cần giữ attribution. Tuy nhiên quyền upstream VCI/KBS và quyền tái phân phối tệp nguyên bản trên website demo chưa được xác minh độc lập.

**Kết luận:** đạt về tải thử và schema OHLCV ngắn hạn; không đạt làm nguồn thay thế cho 43 mã/5 năm. Không nhập staging F-Fin vào Raw/Processed.

## 6. Phương án dữ liệu đề xuất và giới hạn

### A. Tình trạng ngay hiện tại — chưa chọn nguồn chính thức

Giữ CafeF Raw/Processed làm bộ dữ liệu gốc hiện có và chỉ dùng cho báo cáo quality/EDA mô tả theo giới hạn đã ghi. Giữ F-Fin XLSX trong staging làm bằng chứng khảo sát. Không ghép hai bộ, không thay thế từng ticker hoặc một đoạn ngày để “vá” lịch sử: hiện chưa có bằng chứng basis/units nhất quán, và cách ghép sẽ tạo chuỗi lai khó giải thích.

### B. Điều kiện để tiến lên Feature Engineering

Phải hoàn thành các mục sau bằng văn bản/bằng chứng có nguồn và được nhóm/giảng viên chấp thuận:

1. **Source rights:** cho phép tải/lưu Raw nội bộ, dùng trong đồ án, nộp trích đoạn/bản dữ liệu cho giảng viên, lưu staging/dev, và hiển thị chart/metrics trên demo; phân biệt demo nội bộ với public.
2. **Coverage:** xác nhận từng mã trong 43 mã có daily data cho cửa sổ yêu cầu và giải quyết ngày đầu/cuối, ticker mapping, missing/session.
3. **Price basis:** data dictionary xác nhận Close/Adjusted Close và OHLC raw/adjusted, sự kiện áp dụng, công thức hoặc methodology/back-adjust/revision, units/rounding.
4. **Corporate actions:** event ledger đáng tin cậy từ provider/HOSE/VSDC/issuer cho cash dividends, stock/bonus, rights, splits/reverse splits và correction; không tự dựng factor.
5. **Ngoại lệ/missing:** đối chiếu 16 dòng OHLC với nguồn độc lập; phân loại MCH và bảy ticker ngày 14/08/2025 theo lịch/trading status; nhóm chốt quy tắc cho observations bị cờ mà không sửa Raw.
6. **Volume:** xác nhận units và giao dịch được tính (khớp/thỏa thuận/tổng), ý nghĩa zero, Value fields và giải thích mismatch; giữ riêng các thành phần nếu định nghĩa khác nhau.
7. **Pilot:** sau khi có quyền và duyệt, thử 3–5 mã, lưu nguồn/version/timestamp/params và raw response riêng; kiểm tra null/duplicate/gap/OHLC/volume/actions và so sánh CafeF. Chỉ mở rộng 43 mã khi pilot được duyệt.

Feature Engineering, Daily Return, Rolling Volatility, Maximum Drawdown, ATR và clustering vẫn đang **bị chặn** cho đến khi các mục trên đạt. Scaling/split dữ liệu không sửa được basis giá sai.

## 7. Quyết định cần nhóm/giảng viên xác nhận

1. **Có cho phép dùng CafeF làm nguồn tiếp tục không**, với điều kiện phải xác nhận bằng văn bản về methodology, units, quyền học thuật/demo và xử lý các vấn đề đã nêu? Nếu không, nguồn nào trong shortlist được phép xin quyền/quote?
2. **Có cho phép liên hệ FiinQuant và DataCedar** bằng các email nháp đã chuẩn bị để xin chính xác license/quote cho 43 mã, EOD, năm năm, lưu trữ, nộp giảng viên và demo không? Báo giá FiinQuant hiện có là gói rộng tham khảo 87.080.832 VND/12 tháng, không phải quote OHLCV; DataCedar Quant công bố $29/tháng nhưng rights/entitlement chưa rõ.
3. **Có cho phép thử bộ EOD “Giá ngày/Cổ tức” của F-Fin cho đúng 5 mã** để kiểm tra coverage/Adjusted Close/event fields không? Thử nghiệm ấy không giải quyết OHLC basis tự thân và vẫn cần xác minh upstream rights.
4. Xác nhận rằng cho tới khi source/basis/rights đạt, không được tính risk features hoặc chạy phân cụm trên dữ liệu nghiên cứu; tiếp tục các phần không phụ thuộc cơ sở giá nếu cần.

Các câu hỏi này xin quyết định phạm vi hành động kế tiếp; báo cáo không tự gửi thư, đăng ký, mua dữ liệu hay đổi nguồn.

## 8. Việc đã xong, việc bị chặn, và việc có thể làm ngay

### Đã hoàn thành

- Hợp nhất và kiểm tra cấu trúc 43 mã CafeF; giữ Raw/Processed cùng cờ/provenance.
- EDA mô tả đã lưu; không tính return/volatility.
- Tổng hợp bằng chứng/giới hạn các nguồn SSI, Vnstock, TCBS, Yahoo, FiinQuant, DataCedar và F-Fin.
- Tải thử thật F-Fin 5 mã vào staging, kiểm tra 520 dòng và so sánh ngày/OHLC/Volume với CafeF.
- Soạn câu hỏi/email liên hệ FiinQuant/DataCedar; chưa gửi.

### Còn bị chặn

- Quyền dùng/lưu/chia sẻ/demonstrate dữ liệu CafeF và quyền cấp lại upstream của F-Fin.
- Giá basis, formula Adjusted Close, corporate-action completeness, units/Volume semantics.
- Xác minh độc lập 16 cờ OHLC và phân loại ngày thiếu theo từng ticker.
- SSI không còn là hướng được theo đuổi theo quyết định riêng tư của nhóm; các credentials không được yêu cầu.
- Không có nguồn mới nào ngoài CafeF/F-Fin có response được kiểm tra.

### Có thể triển khai ngay mà không làm sai lệch nghiên cứu

- Duy trì bảo toàn/integrity hashes, provenance và audit trail cho file đã có; sửa tài liệu trạng thái cũ nêu sai hoặc mâu thuẫn khi được phép.
- Hoàn thiện bộ câu hỏi/biên bản quyết định để nhóm tự liên hệ và lưu câu trả lời/terms có ngày hiệu lực.
- Tiếp tục các cải tiến UI, tài liệu hoặc kiểm tra cấu trúc dữ liệu không tính đặc trưng giá; mọi EDA mới phải gắn rõ nguồn, cửa sổ và cảnh báo.
- Không ghép nguồn, không sửa giá/missing và không trình bày mức độ rủi ro hoặc kết quả clustering cho đến khi được mở khóa.

## 9. Tệp dữ liệu hiện có và tính toàn vẹn

Giai đoạn tổng kết chỉ đọc các bộ dữ liệu. Theo xác minh gần nhất trong báo cáo F-Fin:

- CafeF Raw: `data/raw/stock_data_raw.csv`, SHA-256 `1B492296E31DB393DA80A8D2579887BBECB4AFB95F4F3A9FF9CECCBFB5186043`.
- CafeF Processed: `data/processed/stock_data_processed.csv`, SHA-256 `3574059045FBD420FC0EF473FCC6671C16C3A6BDC9F57478F02A7241598FE953`.
- F-Fin staging: `data/staging/f_fin/F_FIN_CANDLES_MERGED_D1.xlsx`, SHA-256 `93B2E82C1549F47E677A9AC93E5F0E2D6914513C4726684E93E3BAAB39C89340`.

Không thực hiện Return, Volatility, Feature Engineering hay Clustering.

## 10. Tài liệu nền đã dùng

- [Báo cáo chất lượng dữ liệu](BAO_CAO_CHAT_LUONG_DU_LIEU.md)
- [Xác minh dữ liệu CafeF](BAO_CAO_XAC_MINH_DU_LIEU.md)
- [Xác minh cơ sở giá](BAO_CAO_XAC_MINH_CO_SO_GIA.md)
- [Tổng hợp xác minh nguồn dữ liệu](BAO_CAO_TONG_HOP_XAC_MINH_DU_LIEU.md)
- [Khảo sát SSI/DNSE](BAO_CAO_KHAO_SAT_NGUON_DU_LIEU_GIA.md)
- [Đánh giá nguồn thay thế](BAO_CAO_DANH_GIA_NGUON_DU_LIEU_THAY_THE.md)
- [Khảo sát Vnstock/TCBS và nguồn công khai](BAO_CAO_THU_NGHIEM_NGUON_DU_LIEU_CONG_KHAI.md)
- [Yahoo Finance](BAO_CAO_THU_NGHIEM_YAHOO_FINANCE.md)
- [Khảo sát FiinQuant/DataCedar](BAO_CAO_KHAO_SAT_NHA_CUNG_CAP_DU_LIEU.md)
- [Xác minh FiinQuant/DataCedar](BAO_CAO_XAC_MINH_FIINQUANT_DATACEDAR.md)
- [Thử nghiệm F-Fin](BAO_CAO_THU_NGHIEM_F_FIN.md)
- `BAO_CAO_CHUAN_BI_THU_NGHIEM_SSI.md`, `BAO_CAO_KIEM_TRA_BAO_MAT_SSI.md`, `KE_HOACH_XAC_MINH_NHA_CUNG_CAP.md`, `EMAIL_XAC_NHAN_FIINQUANT.md`, `EMAIL_XAC_NHAN_DATACEDAR.md`.

