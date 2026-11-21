
## Cập nhật — Bản PDF và slide demo conditional (20/11/2026)

- Tạo `reports/BAO_CAO_TONG_KET_DO_AN_CONDITIONAL.pdf`, 12 trang, tổng hợp phạm vi, chất lượng dữ liệu, phương pháp conditional, thí nghiệm phân cụm, kết quả kỹ thuật, kiểm thử và giới hạn khoa học.
- Chuẩn bị bộ slide demo 12 trang trong Spaces: **ASM — Phân nhóm rủi ro HOSE**; đã rà soát bản trình chiếu và sửa slide kết luận để phản ánh đúng việc PDF conditional đã được tạo.
- Đây là đầu ra demo/trình bày có điều kiện, không phải xác nhận price basis, quyền dữ liệu, kết luận rủi ro thực tế hay phê duyệt thay đổi hướng đề tài theo PDF ASM.
- Báo cáo kỹ thuật Markdown được đồng bộ; Raw/Processed không đổi. Các kết quả clustering vẫn chỉ là thử nghiệm conditional được mô tả tại phần cập nhật bên dưới.

## Cập nhật mới nhất — Slide đã thêm vào GitHub (21/11/2026)

- Xuất bộ slide Spaces thành `reports/SLIDE_THUYET_TRINH_ASM.pptx`; kiểm tra archive PPTX hợp lệ và đủ 12 slide.
- Cập nhật README để nêu rõ PPTX được chia sẻ trong repository; PDF và dữ liệu/artifacts dẫn xuất vẫn ở ngoài Git vì điều khoản chia sẻ dữ liệu chưa được xác minh.

# PROJECT_PROGRESS

## Cập nhật mới nhất — Kiểm tra dọn dẹp và cải tiến giao diện (20/11/2026)

- Xóa ba tài liệu mô phỏng cho phạm vi Classification/ngân hàng cũ; giữ lại PDF ASM, dữ liệu, EDA, artifacts, báo cáo xác minh và lịch sử thay đổi cần thiết cho khả năng truy xuất quyết định.
- Dọn Python cache và thư mục `tmp` rỗng. Không xóa hoặc chỉnh sửa `rag_vietstock-main` vì đây là thư mục tham khảo được giữ nguyên theo ràng buộc dự án.
- Làm mới giao diện chung và cải thiện Tổng quan, bộ lọc biểu đồ EDA, trạng thái thiếu artifact, cùng cách xem ma trận/kết quả phân cụm.
- Kiểm tra sau chỉnh sửa: compileall đạt; **34/34 unittest đạt**; AppTest sáu trang và `app.py` đều không có exception; sáu URL trang và health endpoint trả HTTP 200.
- Rà soát giao diện thực tế tại trang Tổng quan: số liệu lấy từ Processed/artifact, danh sách 43 mã, cảnh báo điều kiện và các lối tắt hiển thị đúng.
- Không đổi Raw/Processed, cấu trúc module dữ liệu, API hay phạm vi nghiên cứu.

## Cập nhật mới nhất — Hoàn thiện ứng dụng và pipeline thăm dò có điều kiện

**Giai đoạn hiện tại:** hoàn thiện kỹ thuật conditional Feature Engineering + clustering; đây không phải xác minh dữ liệu hay phê duyệt kết quả rủi ro chính thức.

- Đồng bộ PROJECT_CONTEXT/README theo đề tài hiện tại: 43 doanh nghiệp HOSE, phân nhóm rủi ro biến động giá.
- Đã tạo pipeline chỉ đọc CafeF Processed: simple/log return và thống kê rủi ro từ Close; không dùng Adjusted Close/OHLC; return qua ngày mã vắng bị bỏ qua; drawdown/rolling reset theo gap.
- Độ nhạy loại khỏi bản tóm tắt các return chạm 16 cờ OHLC hoặc |return| ≥10%; đây là đánh dấu/phép thử, không sửa hay xóa bản ghi nguồn.
- Đã chạy hai feature sets (giá cốt lõi; giá + CV Volume độ nhạy), StandardScaler/RobustScaler, K-Means k=2–6, Agglomerative Ward k=2–6, DBSCAN eps=0.5–2.5/min_samples=3–5; đánh giá Silhouette, Davies–Bouldin, Calinski–Harabasz, noise ratio và K-Means stability.
- Kết quả có điều kiện: 43 dòng feature; 124 cấu hình; 5.332 nhãn cấu hình; không có cấu hình nào được tự chọn thành mức rủi ro. Một cấu hình DBSCAN có Silhouette cao nhưng 79,1% noise, do đó không coi là nghiệm tốt nhất.
- Kết quả riêng tại `data/analysis/`, `artifacts/clustering/`; báo cáo `reports/BAO_CAO_THU_NGHIEM_PHAN_CUM_CO_DIEU_KIEN.md`. Metadata ghi source SHA-256, thời điểm chạy, scikit-learn version và cảnh báo.
- Sáu trang Streamlit được AppTest; trang feature/model và hồ sơ cụm đã tương tác thử. Raw/Processed giữ nguyên hash.
- Kiểm thử cuối: compileall đạt; unittest **34/34**; AppTest 6/6 trang và `app.py` không exception; tương tác chạy model/tra hồ sơ đạt; Streamlit root và health endpoint HTTP 200.
- Hash sau pipeline không đổi: Raw `1B492296E31DB393DA80A8D2579887BBECB4AFB95F4F3A9FF9CECCBFB5186043`; Processed `3574059045FBD420FC0EF473FCC6671C16C3A6BDC9F57478F02A7241598FE953`.
- Data-basis, corporate actions, quyền dùng, units Volume và phân loại ngày thiếu vẫn chưa giải quyết; conditional metrics không phải kết quả rủi ro đã xác minh.

**Chưa được xác nhận:** tính hợp lệ khoa học của return/volatility/drawdown trên CafeF; quyền lưu/hiển thị; diễn giải cụm thành mức rủi ro. Những đầu ra này chỉ để kiểm tra pipeline và trình bày rõ điều kiện, không thay thế kết luận nghiên cứu được duyệt.

## Phạm vi hiện hành

Đề tài: **Ứng dụng các thuật toán học máy không giám sát trong phân nhóm và đánh giá mức độ rủi ro của các doanh nghiệp niêm yết trên thị trường chứng khoán Việt Nam.** Phạm vi: 43 doanh nghiệp HOSE, dữ liệu CafeF gần 5 năm; rủi ro nghiên cứu là biến động giá cổ phiếu.

## Trạng thái hiện tại

**Lịch sử Giai đoạn 2.18 — tổng kết và chốt phương án dữ liệu** (hoàn thành tổng hợp bằng chứng; tại thời điểm đó chưa chọn nguồn thay thế). Báo cáo: `reports/BAO_CAO_TONG_KET_PHUONG_AN_DU_LIEU.md`. Giai đoạn này được tiếp nối bằng pipeline thăm dò có điều kiện nêu ở đầu file, theo MASTER PROMPT mới nhất.

- Đối chiếu các báo cáo chất lượng/cơ sở giá và các khảo sát, thử nghiệm CafeF, SSI, Vnstock/VCI/KBS, TCBS, Yahoo Finance, FiinQuant, DataCedar và F-Fin.
- Chỉ CafeF (43 mã, 53.385 dòng Processed, gần 5 năm) và F-Fin (5 mã, 520 dòng, khoảng 5 tháng) có dữ liệu thực tế trong hồ sơ. F-Fin không thay thế được coverage OHLCV 5 năm.
- CafeF còn 16 cờ OHLC chưa được xác minh với feed độc lập; ngày thiếu MCH (14) và 7 mã ngày 14/08/2025 chưa phân loại per-ticker; Adjusted Close/corporate actions/price basis chưa có methodology; units/semantics và quyền dùng chưa đủ bằng chứng.
- Các nguồn còn lại là tài liệu, code/fixture, request không xác thực bị 401, hoặc chưa truy vấn do quyền/credentials chưa được xác nhận; không coi schema là dữ liệu thực nghiệm.
- Phương án đã chốt tại 2.18: giữ CafeF Raw/Processed nguyên trạng làm hồ sơ/EDA mô tả có cảnh báo; không ghép F-Fin. FiinQuant/DataCedar chưa là nguồn chính thức. Hiện chỉ có conditional feature experiment riêng, không được hiểu là mở khóa khoa học cho nghiên cứu.
- Cần nhóm/giảng viên quyết định: tiếp tục xác minh CafeF; cho phép gửi email hỏi FiinQuant/DataCedar; có cho phép thử riêng bộ EOD Giá ngày/Cổ tức F-Fin cho 5 mã không. Email hiện chỉ là nháp, chưa gửi.
- Tại Giai đoạn 2.18 `PROJECT_CONTEXT.md` còn nêu 50 mã; đã được đồng bộ về phạm vi 43 HOSE trong cập nhật hoàn thiện mới nhất ở đầu file.
- Raw/Processed không bị sửa. Kể từ cập nhật mới nhất, Daily Return/Volatility/Feature Engineering/clustering chỉ được tính trong pipeline thăm dò có điều kiện và gắn cảnh báo như quy định ở đầu file.

**Giai đoạn 2.17:** thử tải OHLCV F-Fin thật cho 5 mã thành công ở mức tệp staging; coverage/date range và price basis không đạt điều kiện thay thế. Chi tiết: `reports/BAO_CAO_THU_NGHIEM_F_FIN.md`.

- Tải trực tiếp qua giao diện công khai một workbook D1 XLSX cho FPT, NLG, HPG, VNM, VIC; không đăng ký, không đăng nhập, không dùng credentials.
- Tệp có 5 sheet × 104 dòng = 520 dòng, từ 12/06/2026 đến 09/11/2026; không đáp ứng giai đoạn 19/11/2021–18/11/2026.
- Có OHLCV, ticker nằm ở tên sheet; không có Adjusted Close hoặc Corporate Actions trong tệp nến. Không có null, duplicate, OHLC invariant violation hoặc Volume âm; 8 cờ Volume theo Q3+3×IQR chỉ là outlier thống kê.
- Đối chiếu read-only CafeF trong cửa sổ mẫu: ngày khớp toàn bộ; OHLC khớp 104/104 ở HPG/NLG/VIC, 36/104 ở FPT và 94/104 ở VNM; Volume có chênh lệch. Chưa giải thích được price basis/đơn vị hoặc nguyên nhân chênh lệch.
- F-Fin tuyên bố CC BY 4.0, miễn phí/không cần tài khoản và cho phép dùng học thuật; quyền upstream VCI/KBS và phạm vi tái hiển thị nguyên bản lên website chưa được xác minh độc lập.
- Tệp thử được giữ riêng tại `data/staging/f_fin/`; Raw/Processed không đổi (hash được ghi trong báo cáo). Chưa Feature Engineering, Daily Return/Volatility hoặc clustering.
- Kết luận: F-Fin **chưa đủ điều kiện thay thế** nguồn cho bộ OHLCV 5 năm. Bước tiếp theo nếu nhóm đồng ý là kiểm tra riêng bộ EOD Giá ngày/Cổ tức và xin xác nhận bằng văn bản về OHLCV depth, basis, units, Corporate Actions và quyền dữ liệu upstream.

**Giai đoạn 2.16 (hoàn thành phần chuẩn bị):** email xác nhận FiinQuant/DataCedar được soạn nhưng chưa gửi. F-Fin là khảo sát mới ở Giai đoạn 2.17; chưa liên hệ nhà cung cấp.

- Tạo hai thư nháp: `reports/EMAIL_XAC_NHAN_FIINQUANT.md` và `reports/EMAIL_XAC_NHAN_DATACEDAR.md`.
- Nội dung hỏi phạm vi 43 mã HOSE, lịch sử 19/11/2021–18/11/2026, adjusted/raw, Corporate Actions, Volume/đơn vị, quyền truy cập/lưu trữ, học thuật, website demo, chi phí và quota.
- Đây chỉ là chuẩn bị nội dung liên hệ. Chưa gửi email, chưa nhận xác nhận; không đăng ký, thanh toán, gọi API hoặc tải dữ liệu.
- Giai đoạn 2.15 đã xác định FiinQuant là ưu tiên để xin xác nhận và DataCedar là dự phòng có điều kiện; chưa chọn nguồn chính thức.
- Raw/Processed không đổi. Chưa Feature Engineering, tính Daily Return/Volatility hoặc clustering.

**Giai đoạn 2.15 (hoàn thành phần rà soát tài liệu; chưa chọn nguồn):** `reports/BAO_CAO_XAC_MINH_FIINQUANT_DATACEDAR.md`.

- FiinQuant được đề xuất ưu tiên để xin xác nhận/quote; DataCedar là dự phòng có điều kiện. Đây chưa phải quyết định chọn nguồn dữ liệu chính thức.
- Xác minh từ tài liệu: FiinQuant có API lịch sử OHLCV, cờ adjusted/unadjusted và định nghĩa Volume là khối lượng khớp lệnh; DataCedar công bố OHLCV, các mode raw/split/dividend/all, Volume theo shares và actions cho cash dividends/splits.
- Chưa xác minh: coverage API thực tế cho đủ 43 mã và khoảng thời gian; semantics đầy đủ của Corporate Actions; đơn vị/phạm vi giao dịch của Volume FiinQuant; quyền lưu raw/staging, nộp dữ liệu cho giảng viên, dùng học thuật và hiển thị website demo.
- Tài liệu giá có điểm chưa nhất quán: FiinQuant có bảng độ sâu lịch sử khác nhau; DataCedar Pricing tổng quát ghi 30 ngày cho Quant trong khi tài liệu lịch sử chuyên biệt ghi daily back-to-listing. Cần nhà cung cấp xác nhận gói áp dụng.
- Mốc chi phí tham khảo: FiinQuant 87.080.832 VND/12 tháng là báo giá giáo dục cho gói rộng, không phải quote riêng OHLCV và không ràng buộc; DataCedar Quant niêm yết $29/tháng, nhưng entitlement HOSE và thuế/quyền sử dụng còn mở.
- Chưa liên hệ, đăng ký, thanh toán, gọi API hoặc tải dữ liệu. Raw/Processed không đổi. Chưa Feature Engineering, tính Daily Return/Volatility hoặc clustering.

- Giai đoạn 2.14 (lịch sử): shortlist FiinQuant/DataCedar được lập từ khảo sát tài liệu; Stage 2.15 đã rà soát chi tiết hơn và kết luận chưa chọn nguồn chính thức.
- Chưa liên hệ nhà cung cấp; chưa gọi API, tạo key, tải dữ liệu hoặc tạo staging. Không có xác minh runtime về response, coverage đủ 43 mã, chất lượng hay đối chiếu CafeF.
- PROJECT_CONTEXT vẫn còn phạm vi 50 trong khi tiến độ/nhiệm vụ hiện ghi 43; chưa tự sửa phạm vi.

Giai đoạn 2.13 Yahoo Finance được ghi trong CHANGELOG và `reports/BAO_CAO_THU_NGHIEM_YAHOO_FINANCE.md`; do điều khoản yêu cầu cho phép truy cập tự động trước, không truy vấn Yahoo. Các ghi chú chi tiết của Giai đoạn 2.14 nằm trong CHANGELOG và `reports/BAO_CAO_KHAO_SAT_NHA_CUNG_CAP_DU_LIEU.md`.

- Vnstock 6.0.1 hiện hành không còn hỗ trợ nguồn VCI/KBS cũ; không thử gọi adapter/API legacy.
- Một truy vấn GET không xác thực tới TCBS bars-long-term cho FPT trả HTTP 401, 0 dòng. Không gửi credentials.
- Chưa có nguồn nào trong phạm vi khảo sát đáp ứng đồng thời OHLCV 5 năm, quyền truy cập hợp lệ và tiêu chí không mở tài khoản/không cung cấp định danh. Không có dữ liệu staging mới.
- 5 mã kiểm tra không làm thay đổi universe nghiên cứu. Chưa Feature Engineering hoặc clustering.
- Ghi nhận tài liệu hiện có mâu thuẫn phạm vi tổng thể (PROJECT_CONTEXT nêu 50, PROJECT_PROGRESS nêu 43); nhiệm vụ này không tự quyết định lại phạm vi.

**Giai đoạn 2.12A — chuẩn bị SSI probe** được ghi trong lịch sử dưới đây; quyết định mới thay thế hướng kết nối SSI và không tiếp tục yêu cầu credentials.

**Giai đoạn 2.11 — đánh giá nguồn thay thế và triển khai adapter/staging hoàn tất ở mức fixture.** Báo cáo: `reports/BAO_CAO_DANH_GIA_NGUON_DU_LIEU_THAY_THE.md`. Quy trình SSI đã được chuẩn bị nhưng quyết định Giai đoạn 2.12 mới dừng hướng này; không yêu cầu credentials và không tiếp tục kết nối SSI.

**Giai đoạn 2.9 — tổng hợp xác minh dữ liệu hoàn tất.** Báo cáo: `reports/BAO_CAO_TONG_HOP_XAC_MINH_DU_LIEU.md`; bộ CafeF chưa đủ điều kiện Feature Engineering/Clustering trên dữ liệu nghiên cứu.

**Giai đoạn 2.8 — chuẩn bị xác minh nhà cung cấp hoàn tất phần tài liệu.** Kế hoạch: `reports/KE_HOACH_XAC_MINH_NHA_CUNG_CAP.md`. Các câu hỏi vẫn chưa được liên hệ; chưa có API response hoặc credentials.

**Giai đoạn 2.7 — khảo sát tài liệu SSI FastConnect và DNSE OpenAPI hoàn tất.** Báo cáo: `reports/BAO_CAO_KHAO_SAT_NGUON_DU_LIEU_GIA.md`. Chưa xác minh response thực tế, quyền sử dụng, coverage 43 mã hoặc price basis.

**Giai đoạn 2.6 — xác minh cơ sở giá:** nghiên cứu và đối chiếu mẫu hoàn tất; kết luận chưa thay đổi. CafeF chưa công bố phương pháp Adjusted Close hoặc xác nhận OHLC cùng basis. Không tính Daily Return/Volatility, chưa Feature Engineering hoặc Machine Learning.

## Giai đoạn 1 — hợp nhất dữ liệu (hoàn thành)

- 215/215 file Excel đọc thành công; 43 mã, 5 file mỗi mã.
- Raw: 53.471 dòng; Processed: 53.385 dòng sau khi bỏ 86 dòng trùng hoàn toàn; Raw giữ provenance và bản ghi gốc.
- Chuẩn hóa Date, Ticker, OHLC, Adjusted Close, volume/value; Volume = Matched Volume + Negotiated Volume.

## Giai đoạn 1.5 — xác minh chất lượng (hoàn thành, có giới hạn)

- 16/16 OHLC flags khớp file nguồn; chưa xác minh độc lập tính đúng giao dịch.
- Adjusted Close khác Close ở 46.296/53.385 dòng; công thức chưa được công bố trong tài liệu truy cập.
- Phép cộng Volume xác nhận; 1.008 cờ lớn không được coi là lỗi.
- Rà ngày thiếu MCH và 7 mã ngày 14/08/2025; lý do theo từng mã chưa rõ.

## Giai đoạn 2 — EDA mô tả (hoàn thành)

- Báo cáo `reports/BAO_CAO_EDA.md`, 89 biểu đồ ở `reports/eda/`.
- EDA dùng Close/Volume và thành phần khối lượng theo mã với cảnh báo; không tính return/volatility.

## Giai đoạn 2.5 — nghiên cứu đặc trưng (hoàn thành)

- Đề xuất đặc trưng và điều kiện dữ liệu tại `reports/DE_XUAT_FEATURE_ENGINEERING_RUI_RO.md`.
- Chưa tính hoặc chọn chính thức bộ đặc trưng.

## Giai đoạn 2.6 — xác minh cơ sở giá

- CafeF công khai cột Đóng cửa/Điều chỉnh và Open/High/Low nhưng không tìm thấy công thức Adjusted Close, lịch back-adjustment hoặc xác nhận OHLC cùng basis.
- Đối chiếu các ngày sự kiện FPT (cổ tức tiền, phát hành tăng vốn từ vốn chủ sở hữu) và NLG (quyền mua) với các dòng Processed. Adjusted Close quanh một số sự kiện thay đổi khác Close theo hướng tương thích với có điều chỉnh, nhưng đây không phải bằng chứng công thức.
- Chưa xác minh được trường hợp chia tách thuần túy trong mẫu; không kết luận không có trong toàn universe.
- Kết luận: Close/Open/High/Low chỉ dùng có điều kiện cho mô tả theo mã; Adjusted Close chưa đủ bằng chứng để dùng tính lợi suất. Chưa có chuỗi giá được xác nhận đủ cho risk features.
- Không thay đổi Raw/Processed, không tính return/volatility.

## Vấn đề còn mở trước Feature Engineering

1. Xin CafeF data dictionary/methodology về Adjusted Close, corporate actions, OHLC basis và quy tắc cập nhật lịch sử.
2. Đối chiếu raw price với nguồn giá độc lập có điều khoản rõ; HOSE/VSDC xác minh event details nhưng chưa tìm thấy chuỗi adjusted OHLC 5 năm trong nguồn công khai đã tra.
3. Hoàn thiện event ledger cho 43 mã, đặc biệt chia tách thuần và sự kiện quyền mua/cổ tức trùng ngày.
4. Nhóm/giảng viên quyết định có chấp thuận dùng Close thô với giới hạn được công khai hay yêu cầu nguồn adjusted khác.
5. Chốt cách xử lý 16 OHLC bất thường và các ngày thiếu.

Giai đoạn 2.6 đã được khảo sát; kết luận và các vướng mắc vẫn được theo dõi ở trên. Trạng thái mới nhất là Giai đoạn 2.7, chờ nhóm đánh giá báo cáo trước khi quyết định thử nghiệm dữ liệu.

## Giai đoạn 2.7 — khảo sát nguồn dữ liệu giá (hoàn thành, chờ nhóm đánh giá)

- Đọc tài liệu chính thức SSI FastConnect và DNSE OpenAPI; chỉ nghiên cứu tài liệu, không gọi API.
- SSI công bố daily OHLCV từ ngày mã bắt đầu giao dịch, có phân trang và rate-limit headers; chưa xác minh coverage 43 mã bằng response thực tế. Tài liệu SSI có khác biệt về luồng đăng ký và format ngày; quota OHLC cụ thể chưa thấy.
- DNSE công bố endpoint lịch sử OHLCV với `symbol`, `type`, `resolution`, `from/to` Unix seconds và `nextTime`; chưa công bố rõ độ sâu lịch sử, giới hạn riêng endpoint OHLC hoặc semantics paging đầy đủ.
- Cả hai nguồn chưa xác nhận price basis/adjustment của OHLC. SSI có endpoint corporate actions riêng; DNSE có lịch sử quyền theo tài khoản, không xác nhận adjusted OHLC.
- SSI là ứng viên ưu tiên cho thử nghiệm đối chiếu vì tài liệu history/pagination rõ hơn; DNSE là phương án tiềm năng dự phòng. Không tự chọn nguồn thay thế CafeF.
- Phí dịch vụ FastConnect được FAQ SSI mô tả hiện không thu, nhưng quyền dùng/redistribution dữ liệu chưa xác minh. Phí và quyền học thuật DNSE cũng chưa xác minh.
- Chưa tải dữ liệu, chưa sửa Raw/Processed, chưa tính return/volatility hoặc thực hiện Feature Engineering/Machine Learning.
- Còn cần hỏi hai nhà cung cấp về cơ sở giá, coverage từ 2021 cho 43 mã, giới hạn OHLC, đơn vị Volume, phí và quyền sử dụng trong đồ án.

Những nội dung khảo sát 2.7 tiếp tục là căn cứ cho kế hoạch 2.8; chờ nhóm xem xét trước khi liên hệ nhà cung cấp hoặc cho phép thử nghiệm nhỏ.

## Giai đoạn 2.8 — chuẩn bị xác minh nhà cung cấp (hoàn thành phần tài liệu)

- Đọc PROJECT_CONTEXT.md, PROJECT_PROGRESS.md, CHANGELOG.md, báo cáo khảo sát nguồn giá và báo cáo xác minh cơ sở giá.
- Tạo `reports/KE_HOACH_XAC_MINH_NHA_CUNG_CAP.md` với câu hỏi riêng cho CafeF, SSI và DNSE, cùng bảng theo dõi bắt đầu ở trạng thái `Chưa liên hệ`.
- Ghi các điều kiện cần đáp ứng trước khi thử nghiệm API: quyền truy cập hợp lệ, hiểu điều khoản, làm rõ/định hướng xác minh cơ sở giá, giới hạn và sự đồng ý của nhóm.
- Chỉ hoàn thành khâu chuẩn bị. Chưa liên hệ nhà cung cấp, chưa gọi API, chưa có câu trả lời/bằng chứng mới, chưa tạo/sử dụng credentials và chưa tải dữ liệu.
- Raw/Processed/CSV không bị chỉnh sửa; chưa tính Daily Return/Volatility, Feature Engineering hoặc phân cụm.

Chờ nhóm kiểm tra kế hoạch và tự quyết định việc liên hệ nhà cung cấp; chưa chuyển sang thử nghiệm dữ liệu.

## Giai đoạn 2.10 — đồng bộ phạm vi và xác nhận cuối (hoàn thành phần được kiểm tra)

- Đồng bộ README và các trang Tổng quan, Quản lý dữ liệu, Chất lượng dữ liệu, Phân tích dữ liệu, Machine Learning, Tra cứu nhóm với đề tài clustering của 43 mã HOSE.
- Tách danh sách 43 ticker hiện có từ Processed vào `src/data/universe.py`; giữ `PLANNED_TICKERS` như alias tương thích, không chặn import mã ngoài danh sách mà cảnh báo.
- Trang Phân tích dữ liệu truy cập biểu đồ EDA đã lưu và báo cáo Markdown; trang Chất lượng dữ liệu đọc thống kê thiếu từ Processed. Không tính return/volatility.
- Cập nhật API Streamlit `width="stretch"` để tránh cảnh báo `use_container_width`.
- Universe có 43 ticker duy nhất, đúng danh sách mã trong Processed; importer dùng cùng universe cho gợi ý/ cảnh báo mã ngoài phạm vi.
- Quét README/app/pages/src không còn mô tả Classification 10 ngân hàng; mã ACB/BID trong test còn lại là fixture nhập liệu tổng hợp, không phải phạm vi nghiên cứu.
- Vòng xác nhận cuối: compileall đạt; 15/15 unittest đạt (bổ sung 3 test về universe/importer); sáu trang AppTest chạy không exception; route trang Phân tích có một ảnh EDA; Streamlit trả HTTP 200.
- Đối chiếu Processed cho đúng 43 mã và thứ tự/số lượng khớp hằng số universe. Quét app.py/pages/src/README không còn nội dung Classification 10 ngân hàng; fixtures ACB/BID trong tests chỉ là dữ liệu kiểm thử importer.
- SHA-256 tại vòng xác nhận: Raw `1B492296E31DB393DA80A8D2579887BBECB4AFB95F4F3A9FF9CECCBFB5186043`; Processed `3574059045FBD420FC0EF473FCC6671C16C3A6BDC9F57478F02A7241598FE953`. Không ghi vào hoặc sửa hai file dữ liệu.
- EDA trong giao diện mới chỉ liên kết tới 89 biểu đồ và báo cáo lưu sẵn; chưa có bộ lọc/biểu đồ tương tác động. Chất lượng dữ liệu trong trang là kiểm tra cấu trúc cơ bản, không thay báo cáo xác minh đầy đủ.
- Chưa chạy phân cụm/feature engineering trên dữ liệu nghiên cứu vì cơ sở giá và corporate actions chưa xác minh.

## Vấn đề còn tồn tại

- CafeF chưa xác nhận phương pháp Adjusted Close, cơ sở OHLC và cách back-adjust corporate actions; không tính Daily Return/Volatility.
- 16 cờ OHLC và ngày thiếu vẫn chờ quyết định/bằng chứng; không tự sửa hoặc nội suy.
- Feature Engineering và K-Means/Hierarchical/DBSCAN chưa triển khai/chạy trên dữ liệu nghiên cứu.

## Giai đoạn 2.9 — tổng hợp xác minh nguồn dữ liệu (hoàn thành phần rà soát hồ sơ)

- Đọc và đối chiếu báo cáo chất lượng, xác minh dữ liệu, xác minh cơ sở giá, khảo sát SSI/DNSE, kế hoạch hỏi nhà cung cấp và phương pháp xử lý dữ liệu.
- Không thấy câu trả lời mới từ CafeF/SSI/DNSE. Bằng chứng HOSE aggregate cho 14/08/2025 chỉ xác nhận ngày có giao dịch toàn thị trường, không giải thích 7 mã thiếu record.
- Tổng hợp trạng thái Close/Adjusted Close/OHLC, corporate actions, 16 cờ OHLC, ngày thiếu, Volume/Value và định danh Date/Ticker trong `reports/BAO_CAO_TONG_HOP_XAC_MINH_DU_LIEU.md`.
- Kết luận: chưa đủ điều kiện tính Daily Return, Rolling Volatility, Maximum Drawdown, ATR hoặc chạy phân cụm trên dữ liệu nghiên cứu. Close/Volume chỉ dùng EDA mô tả có cảnh báo; Value chưa đủ căn cứ diễn giải.
- Không sửa Raw/Processed, không tải dữ liệu, không tính Feature Engineering hoặc chạy mô hình.
- Tiếp theo: nhận trả lời bằng văn bản về giá basis/units/rights, xác minh nguồn từng lỗi và ngày thiếu, xin quyết định nhóm/giảng viên trước khi thử nghiệm nguồn thay thế.

## Giai đoạn 2.11 — đánh giá nguồn dữ liệu thay thế

- Ghi nhận xác nhận giảng viên cho phép dùng nguồn ngoài CafeF; universe 43 mã, khoảng thời gian và đề tài không đổi.
- Đọc lại báo cáo tổng hợp xác minh, khảo sát SSI/DNSE, kế hoạch xác minh và các quyết định trước.
- Đọc tài liệu chính thức SSI trước, sau đó DNSE. SSI docs mô tả daily OHLCV history từ listing, pagination và corporate-action endpoint; DNSE docs mô tả OHLCV daily nhưng history depth/paging details còn mở. Không provider nào trong tài liệu này xác nhận adjusted OHLC/corporate-action price basis.
- Chọn tạm 5 mã cho thiết kế test: FPT, NLG, HPG, VNM, VIC; chỉ FPT/NLG có event cases đã nêu trong báo cáo cũ, event windows khác cần xác minh trước khi chạy.
- Kiểm tra sự hiện diện của biến môi trường SSI_API_KEY/SSI_API_SECRET/SSI_ACCESS_TOKEN mà không đọc giá trị: cả ba không có; không có `.env`. Vì vậy không gọi API, không có kết quả runtime và không tải dữ liệu.
- Triển khai `src/data/providers/ssi.py`, `src/data/staging.py`, `src/data/quality.py` và test fixture `tests/test_ssi_adapter.py`; không gọi API từ Streamlit.
- Kiểm thử: compileall đạt; 20/20 unittest; AppTest 6 trang không exception; Streamlit HTTP 200. Chưa có test API thật.
- Raw/Processed SHA-256 giữ nguyên: `1B492296E31DB393DA80A8D2579887BBECB4AFB95F4F3A9FF9CECCBFB5186043` và `3574059045FBD420FC0EF473FCC6671C16C3A6BDC9F57478F02A7241598FE953`.
- Chưa chọn nguồn thay thế chính thức, chưa tải dữ liệu, chưa Feature Engineering hoặc clustering.

Việc kế tiếp cần nhóm tự thiết lập access hợp lệ/điều khoản, xin xác nhận price basis/units/corporate actions và cho phép read-only test 5 mã.

## Giai đoạn 2.12 — chuẩn bị kết nối SSI (phần trước credentials hoàn thành)

- Rà soát `src/data/providers/ssi.py`, `src/data/staging.py`, `src/data/quality.py`, `.gitignore`, README và tests. Adapter chỉ lấy token rồi GET dữ liệu OHLC; không có lệnh giao dịch hoặc caller trong Streamlit.
- Bổ sung `scripts/ssi_probe.py`: chỉ nhận một ticker mỗi lần, giới hạn FPT/NLG/HPG/VNM/VIC; ngày mặc định 2021-11-19–2026-11-18; không có tùy chọn batch. Ghi OHLCV vào staging và mọi lần thử/trạng thái vào manifest.
- Tăng độ an toàn thông báo lỗi transport, cập nhật README nhập secret bằng prompt ẩn trong PowerShell và xóa biến môi trường sau probe. `.gitignore` chặn `.env`, `.env.*` (trừ `.env.example`) và dữ liệu staging SSI.
- Thêm test fixture cho allowlist/single ticker, ghi staging, kết quả rỗng, log lỗi không chứa credentials; sửa lỗi encoding UTF-8 khi CLI help chạy trên Windows.
- Quality audit đánh dấu ngày thiếu là `not assessed` khi chưa truyền lịch phiên xác minh; probe ghi rõ lý do thay vì báo một danh sách rỗng gây hiểu nhầm.
- Tạm chặn cấu hình vượt `SSI_PAGE_SIZE=10` và `SSI_MAX_PAGES=500` cho đến khi SSI xác nhận quota; đây là giới hạn an toàn nội bộ, không phải giới hạn provider công bố.
- Rà soát bảo mật SSI: không thấy SSI credentials thật trong environment hoặc file `.env`; allowlist được kiểm tra cả trong CLI và hàm `run()`; auth chỉ POST token, OHLC chỉ GET; staging tách khỏi Raw/Processed. Kết quả chi tiết tại `reports/BAO_CAO_KIEM_TRA_BAO_MAT_SSI.md`.
- Kiểm tra `compileall` đạt; 28/28 unittest đạt. CLI `--help` hoạt động; mã ngoài allowlist thoát trước khi tạo client/kết nối. Không gọi SSI API thật.
- Thư mục dự án hiện không phải Git working tree, nên chưa thể xác minh index/tracked files; `.gitignore` vẫn chặn `.env` và nội dung staging SSI.
- Không có `SSI_API_KEY`, `SSI_API_SECRET`, `SSI_ACCESS_TOKEN` trong environment hiện tại. Chưa có staging data/manifest thật. Không sửa Raw/Processed; SHA-256 giữ nguyên: Raw `1B492296E31DB393DA80A8D2579887BBECB4AFB95F4F3A9FF9CECCBFB5186043`, Processed `3574059045FBD420FC0EF473FCC6671C16C3A6BDC9F57478F02A7241598FE953`.
- Khi có response, script đã chuẩn bị đối chiếu OHLCV mô tả với Processed CafeF trên ngày trùng; hiện chưa có response nên chưa có kết quả so sánh thực tế. Còn chờ credentials hợp lệ do nhóm tự cấu hình, xác nhận điều khoản/quyền học thuật, và nhóm cho phép chạy read-only probe. Chưa xác minh API runtime, coverage, đơn vị, corporate actions hoặc price basis.
- Chưa Feature Engineering, Daily Return/Volatility, hoặc clustering.


