# CHANGELOG

## 2026-11-20 — Giai đoạn 2.18: tổng kết phương án dữ liệu
- Đọc/đối chiếu báo cáo chất lượng, xác minh CafeF/cơ sở giá, khảo sát SSI/DNSE, Vnstock/TCBS, Yahoo, FiinQuant/DataCedar và thử nghiệm F-Fin cùng tài liệu tiến độ liên quan.
- Tạo `reports/BAO_CAO_TONG_KET_PHUONG_AN_DU_LIEU.md` với ma trận 8 nguồn, phân biệt dữ liệu thực tải, tài liệu API, truy vấn bị từ chối và quyền chưa xác minh.
- Kết luận chưa nguồn nào đạt đồng thời coverage 43 mã × gần 5 năm, price basis/corporate actions/units và quyền sử dụng; CafeF giữ làm bộ gốc/EDA mô tả có cảnh báo, F-Fin không đủ độ phủ.
- Cập nhật PROJECT_PROGRESS sang tổng kết Giai đoạn 2.18; lựa chọn nguồn vẫn chờ nhóm/giảng viên. Không liên hệ nhà cung cấp, đăng ký, thanh toán, tải dữ liệu mới hoặc sửa Raw/Processed.
- Không tính Return/Volatility, Feature Engineering hoặc Clustering.

## 2026-11-20 — Giai đoạn 2.17: kiểm tra nguồn dữ liệu F-Fin
- Truy cập trang tải công khai F-Fin và tải XLSX nến D1 cho đúng 5 mã FPT, NLG, HPG, VNM, VIC; không đăng nhập, không cung cấp credentials.
- Lưu bản tải nguyên trạng và manifest nguồn/thời điểm/hash trong `data/staging/f_fin/`; không chạm Raw hoặc Processed.
- Kiểm tra 520 dòng (104/mã), trường OHLCV, khoảng ngày 2026-06-12–2026-11-09, null, duplicate, OHLC invariant, Volume và cờ Q3+3×IQR; đối chiếu read-only cùng ngày với CafeF.
- Ghi nhận khác biệt OHLC ở FPT/VNM, khác biệt Volume và thiếu Adjusted Close/Corporate Actions trong workbook nến; không suy luận nguyên nhân hay price basis.
- Tạo `reports/BAO_CAO_THU_NGHIEM_F_FIN.md`: phân biệt dữ liệu tải thực tế với tuyên bố F-Fin về EOD Adjusted Close/cổ tức và CC BY 4.0; kết luận chưa đủ coverage/bằng chứng để thay thế CafeF 5 năm.
- Chỉ tải XLSX; CSV/ZIP mới xác nhận là tùy chọn giao diện, chưa tải thử. Chưa tính return/volatility, Feature Engineering hay clustering.

## 2026-11-20 — Giai đoạn 2.16: chuẩn bị thư xác nhận nhà cung cấp
- Đọc lại báo cáo `reports/BAO_CAO_XAC_MINH_FIINQUANT_DATACEDAR.md` và dùng các điểm còn mở để soạn thư riêng cho FiinQuant và DataCedar.
- Tạo `reports/EMAIL_XAC_NHAN_FIINQUANT.md` và `reports/EMAIL_XAC_NHAN_DATACEDAR.md`, hỏi coverage/lịch sử, giá basis, Corporate Actions, Volume, quyền lưu trữ/học thuật/demo, chi phí và quota.
- Ghi rõ đây là bản nháp; chưa gửi thư, chưa có xác nhận nhà cung cấp. Không đăng ký, thanh toán, gọi API hoặc tải dữ liệu.
- Không sửa Raw/Processed hoặc mã nguồn; chưa Feature Engineering hay clustering.

## 2026-11-20 — Giai đoạn 2.15: xác minh FiinQuant và DataCedar
- Đọc tài liệu chính thức về API lịch sử, giá, điều khoản và quyền dữ liệu của hai nhà cung cấp trong phạm vi; không khảo sát thêm nguồn mới.
- Tạo `reports/BAO_CAO_XAC_MINH_FIINQUANT_DATACEDAR.md` với bảng đối chiếu 10 câu hỏi bắt buộc, dẫn nguồn/ngày truy cập, rủi ro quyền sử dụng, mốc chi phí và danh sách câu hỏi cần gửi.
- Đề xuất FiinQuant là nguồn ưu tiên để xin xác nhận/quote và DataCedar là dự phòng có điều kiện; chưa phê duyệt/chọn nguồn chính thức.
- Ghi rõ các khác biệt trong công bố lịch sử/giá, quyền local storage, academic use, nộp cho giảng viên và website demo còn chưa được xác minh.
- Không liên hệ, đăng ký, thanh toán, gọi API, tải dữ liệu hoặc tạo adapter. Không sửa Raw/Processed; chưa Feature Engineering hoặc clustering.

## 2026-11-20 — Giai đoạn 2.14: khảo sát nhà cung cấp dữ liệu có quyền rõ ràng
- Đọc các file tiến độ/bối cảnh và báo cáo Giai đoạn 2.12–2.13; giữ nguyên phạm vi 43 mã theo yêu cầu hiện tại, ghi nhận PROJECT_CONTEXT còn mâu thuẫn 50 mã.
- Khảo sát tài liệu chính thức FiinQuant/FiinGroup, DataCedar và HOSE. Không gọi API, không tạo key, không liên hệ nhà cung cấp, không tải dữ liệu OHLCV.
- Shortlist hai ứng viên: FiinQuant (tài liệu OHLCV Python, điều khoản có quyền tạo sản phẩm phái sinh kèm attribution; báo giá giáo dục tham khảo 87.080.832 VND/năm) và DataCedar (Quant 29 USD/tháng; source rights và quyền dùng dữ liệu chưa rõ).
- Tạo `reports/BAO_CAO_KHAO_SAT_NHA_CUNG_CAP_DU_LIEU.md` nêu coverage/price/rights theo mức tài liệu công bố, điểm chưa xác minh và câu hỏi cần gửi.
- Không sửa Raw/Processed, không tạo adapter/staging, không tính returns/volatility, Feature Engineering hoặc clustering.

## 2026-11-20 — Giai đoạn 2.13: rà soát Yahoo Finance/yfinance
- Kiểm tra điều khoản Yahoo hiện hành và tài liệu PyPI/yfinance trước khi truy vấn; điều khoản yêu cầu cho phép rõ ràng trước với truy cập/thu thập tự động.
- Do chưa có chấp thuận áp dụng cho đồ án, không gọi API/yfinance; không xác minh ticker .VN hoặc dữ liệu 5 mã, không tạo staging và không tuyên bố có kết quả tải.
- Xác nhận yfinance cài tại chỗ là 1.4.0; PyPI công bố 1.8.0. Không cài/nâng cấp.
- Tạo `reports/BAO_CAO_THU_NGHIEM_YAHOO_FINANCE.md`, ghi rõ quyền truy cập, học thuật, lưu trữ và website còn chưa xác minh; đề xuất điều kiện để thử 5 mã nếu được cho phép.
- Raw/Processed không đổi; SHA-256 được ghi trong báo cáo. Không Feature Engineering, Daily Return/Volatility hoặc clustering.

## 2026-11-20 — Giai đoạn 2.12: khảo sát nguồn OHLCV không cần tài khoản SSI
- Ghi nhận quyết định nhóm dừng SSI; không yêu cầu SSI credentials. Phạm vi thử chỉ gồm FPT, NLG, HPG, VNM, VIC từ 19/11/2021 đến 18/11/2026, không đổi universe dự án.
- Đọc tài liệu Vnstock hiện hành: thế hệ 6.0.1; VCI/KBS là nguồn cũ không còn được hỗ trợ trong V6. Không cài thư viện, không gọi endpoint legacy.
- Thử một GET đọc không credentials tới TCBS bars-long-term cho FPT; HTTP 401, không có response data. Không thử tiếp và không dùng account/token.
- Đánh giá trang dữ liệu HOSE và biểu phí chính thức; chưa thấy phương án tải miễn phí 5 năm phù hợp với quyền truy cập không định danh.
- Tạo `reports/BAO_CAO_THU_NGHIEM_NGUON_DU_LIEU_CONG_KHAI.md`; không có OHLCV mới nên không tạo staging rows, không sửa Raw/Processed, không Feature Engineering/clustering.
- Ghi nhận mâu thuẫn chưa giải quyết giữa PROJECT_CONTEXT (50 doanh nghiệp) và PROJECT_PROGRESS (43 doanh nghiệp); không đổi phạm vi trong lần khảo sát này.

## 2026-11-20 — Giai đoạn 2.12: chuẩn bị SSI probe trước credentials
- Tạo `scripts/ssi_probe.py`, giới hạn mỗi lần chạy đúng một trong FPT, NLG, HPG, VNM, VIC; mặc định khoảng 19/11/2021–18/11/2026.
- Probe ghi dữ liệu vào `data/staging/ssi/` và ghi trạng thái/lỗi/thời điểm/nguồn vào manifest; không ghi Raw/Processed và không có lệnh giao dịch.
- Cập nhật README hướng dẫn nhập credentials ẩn bằng PowerShell; `.gitignore` chặn `.env`, `.env.*` và SSI staging (ngoại trừ `.env.example`). Không ghi credentials vào logs hoặc thông báo lỗi.
- Làm thông báo transport an toàn hơn; sửa encoding CLI UTF-8 trên Windows. Tạm giới hạn pageSize 10 và tối đa 500 trang cho đến khi SSI xác nhận quota.
- Bổ sung fixture tests cho allowlist, staging, kết quả rỗng, log lỗi không lộ secret, giới hạn paging, trang phân trang lặp và trạng thái ngày thiếu chưa đánh giá khi không có lịch. `compileall` đạt, 27/27 unittest đạt; `--help` hoạt động, ticker ngoài allowlist bị từ chối trước kết nối.
- Không có credentials trong environment, không gọi API thật, không tải dữ liệu. Chưa xác minh price basis, đơn vị, corporate actions, coverage hoặc quyền sử dụng; SSI chưa được chọn làm nguồn chính thức.
- Raw/Processed không đổi; chưa Feature Engineering hoặc clustering.
- Thư mục dự án không phải Git working tree nên chưa thể kiểm tra tracked/index; `.gitignore` chặn `.env` và dữ liệu staging.
- Kiểm tra bảo mật cuối SSI: bổ sung allowlist ở hàm `run()` để không thể vượt giới hạn bằng cách gọi Python trực tiếp; xác nhận HTTP 401/log không lộ secret, staging tách biệt, không có lệnh giao dịch.
- Phát hiện `.env.example` trong dự án tham khảo RAG chứa thông tin đăng nhập phát triển mẫu cho PostgreSQL; không phải SSI credential, chưa xác minh là secret thật. Không sửa thư mục tham khảo. Cả dự án chính và thư mục tham khảo đều không phải Git working tree nên không thể xác minh file tracked.
- Chạy lại `compileall` và **28/28 unittest** đạt; không gọi API thật.

## 2026-11-17

### Giai đoạn phân tích
- Đọc PDF ASM gốc và ghi nhận yêu cầu, hai hướng bài toán, rubric, sản phẩm bàn giao; xác định phạm vi hiện tại là Classification xu hướng giá.
- Phân tích README, cấu trúc và mã nguồn liên quan của rag_vietstock-main.
- Xác minh crawler mẫu lấy danh mục doanh nghiệp và tài liệu cổ đông/PDF, không phải lịch sử OHLCV theo ngày.
- Cập nhật BAO_CAO_PHAN_TICH.md với kết quả phân tích và kiến trúc đề xuất.
- Tạo PROJECT_CONTEXT.md và PROJECT_PROGRESS.md để lưu quyết định, ràng buộc và trạng thái dự án.

### Trạng thái triển khai
- Chưa có code ứng dụng, dữ liệu thực, mô hình, dashboard hoặc artifacts được tạo.
- Giai đoạn phân tích hoàn tất; chờ xác nhận trước khi triển khai.

## 2026-11-17 — Khởi tạo cấu trúc ứng dụng
- Tạo cấu trúc thư mục ASM, package Python và các file cơ bản.
- Khởi tạo trang chủ tiếng Việt bằng Streamlit.
- Khai báo các dependency phân tích dữ liệu/học máy; không thêm gói RAG, LLM, OCR hoặc PostgreSQL.
- Kiểm tra chạy Streamlit trên môi trường hiện tại: server khởi động và trang trả HTTP 200.
- Chưa thêm dữ liệu, mô hình hoặc chức năng ngoài khung/trang chủ.

## 2026-11-17 — Xây dựng giao diện Dashboard
- Thêm điều hướng và sáu trang tiếng Việt: Tổng quan, Quản lý dữ liệu, Chất lượng dữ liệu, Phân tích dữ liệu, Machine Learning, Dự báo.
- Tạo kiểu giao diện dùng chung; chỉ hiển thị trạng thái chưa có dữ liệu/kết quả, không tạo số liệu minh họa.
- Bổ sung khung trang chủ với danh sách 10 mã dự kiến và trạng thái các giai đoạn.
- Kiểm tra import/cú pháp; sáu trang chạy qua Streamlit AppTest không exception.
- Khởi chạy Streamlit thành công và nhận HTTP 200.
- Chưa xử lý dữ liệu, thu thập dữ liệu hoặc huấn luyện mô hình.

## 2026-11-17 — Nhập và quản lý dữ liệu cổ phiếu
- Thêm src/data/stock_data.py cho đọc CSV/XLSX, gợi ý ánh xạ alias chính xác, kiểm tra kiểu/ngày/missing/duplicate/OHLC và lưu file.
- Tích hợp upload, ánh xạ cột, thông báo chất lượng, xem trước và xác nhận bản CSV chuẩn hóa vào trang Quản lý dữ liệu.
- Hỗ trợ file một hoặc nhiều mã nếu có cột Ticker. File gốc được lưu nguyên byte bằng tên duy nhất; không tự xóa dòng và không ghi đè. File lỗi không được xác nhận vào data/processed.
- Thêm tests/test_stock_data.py với fixture tổng hợp chỉ dùng trong test; không tạo dữ liệu giả trong data/raw hoặc data/processed.
- 12 kiểm thử unittest đạt; compileall, Streamlit AppTest sáu trang và khởi chạy HTTP 200 đạt.
- Cài openpyxl 3.1.5 trong môi trường hiện tại để kiểm tra XLSX; dependency đã có trong requirements.txt.
- Không xây crawler, EDA, feature engineering hoặc Machine Learning.

## 2026-11-17 — Nghiên cứu dữ liệu lịch sử Vietstock
- Đọc PROJECT_CONTEXT.md và PROJECT_PROGRESS.md để theo đúng phạm vi, không đọc lại toàn bộ mã nguồn dự án tham khảo.
- Đọc hướng dẫn VietstockFinance chính thức 2024: xác nhận trang Cổ phiếu > Thống kê giao dịch có lọc mã và khoảng ngày; chưa xác minh xuất OHLCV/Excel cho cổ phiếu.
- Kiểm tra trang giới thiệu API Vietstock; thông tin công khai chưa xác nhận endpoint lịch sử OHLCV, xác thực, giới hạn hoặc điều khoản cụ thể.
- Thử GET trang ACB công khai đã biết; phản hồi 404. Không dò endpoint thay thế, không gọi API không tài liệu, không đăng nhập hoặc vượt cơ chế bảo vệ.
- Không nhận dữ liệu giao dịch nên không lưu file thử; ghi rõ schema, số dòng và thời gian chưa thể xác minh trong VIETSTOCK_DATA_RESEARCH.md.
- Đề xuất tiếp tục bằng CSV/XLSX người dùng tải hợp lệ từ Vietstock; chỉ nghiên cứu tự động hóa khi xác minh được quyền và giao diện/API chính thức.


## 2026-11-20 — Giai đoạn 1: hợp nhất và kiểm tra dữ liệu CafeF
- Kiểm tra archive `DU_LIEU_CHUNG_KHOAN.zip`: đọc thành công 215/215 file Excel, gồm 43 mã HOSE và 5 file mỗi mã; không sửa/ghi đè file nguồn.
- Tạo `data/raw/stock_data_raw.csv` với 53.471 dòng, giữ các bản ghi trùng/bất thường cùng provenance; tạo `data/processed/stock_data_processed.csv` với 53.385 dòng sau khi bỏ đúng 86 dòng trùng hoàn toàn.
- Chuẩn hóa schema Date, Ticker, OHLC, Adjusted Close, Volume, Matched Volume/Value và Negotiated Volume/Value. Volume là tổng hai thành phần khối lượng trong file nguồn.
- Phát hiện 16 bản ghi OHLC bất nhất; giữ nguyên trong cả hai bộ dữ liệu và gắn cờ để nhóm xem xét. Không có trường chuẩn bị thiếu hoặc volume âm.
- Lập báo cáo chất lượng và workbook thống kê per-ticker, khoảng ngày thiếu tương đối, các cờ khối lượng lớn và chi tiết 16 ngoại lệ OHLC.
- Ghi nhận Adjusted Close khác Close ở một số quan sát nhưng file không mô tả phương pháp điều chỉnh/cơ sở điều chỉnh của OHLC; chưa tính return hay trộn hai cơ sở giá.
- Giai đoạn 1 hoàn tất về mặt kỹ thuật; cần nhóm xem xét ngoại lệ, đơn vị và quy tắc điều chỉnh trước Feature Engineering. Chưa triển khai mô hình.

## 2026-11-20 — Giai đoạn 1.5: xác minh chất lượng dữ liệu
- Đối chiếu 16/16 bản ghi OHLC với workbook, sheet và dòng nguồn; các giá trị khớp dữ liệu Processed. Không kết luận được độ đúng giao dịch nếu thiếu nguồn độc lập; không sửa/xóa.
- Ghi nhận 12/16 OHLC bất nhất tập trung trong các ngày 06–08/05/2025.
- Kiểm tra Adjusted Close/Close theo mã và thời gian; 46.296/53.385 giá trị khác Close, 104 thay đổi tỷ lệ trên 5%; chưa xác minh được công thức điều chỉnh hay basis OHLC.
- Xác nhận Volume = Matched Volume + Negotiated Volume trên toàn Processed; lưu 1.008 cờ volume cao để rà soát, không xóa.
- Rà ngày thiếu MCH và ngày 14/08/2025 của 7 mã so với tập ngày quan sát; chưa đối chiếu được lịch HOSE độc lập.
- Lập `reports/BAO_CAO_XAC_MINH_DU_LIEU.md`; dữ liệu không bị thay đổi.
- Các mục đề tài Classification/10 ngân hàng phía trên là lịch sử của phạm vi đề tài trước đây; phạm vi hiện hành được ghi trong PROJECT_PROGRESS.md.

## 2026-11-20 — Giai đoạn 2: EDA mô tả
- Thống kê Processed: 53.385 dòng, 43 mã, khoảng 2021-11-19–2026-11-18; không thiếu giá trị trong 12 trường chuẩn, không trùng Ticker + Date.
- Mô tả độ phủ, Close, Volume, Matched Volume và Negotiated Volume theo mã; không gán đơn vị hoặc kết luận thanh khoản.
- Tính cờ Q3 + 3×IQR riêng từng mã trong bộ nhớ: 1.008, khớp báo cáo chất lượng. Không ghi vào CSV, không xóa/clip/winsorize.
- Hiển thị 16 OHLC flags trong báo cáo và đánh dấu trên biểu đồ Close; không sửa dữ liệu.
- Tạo `reports/BAO_CAO_EDA.md` và 89 biểu đồ PNG trong `reports/eda/`.
- Hash SHA-256 Raw/Processed trước và sau giống nhau. Không tính Daily Return/Volatility, không Feature Engineering, không Machine Learning.

## 2026-11-20 — Giai đoạn 2.7: khảo sát nguồn dữ liệu giá
- Đọc tài liệu chính thức SSI FastConnect Data và DNSE OpenAPI; không gọi API, không sử dụng credentials và không tải dữ liệu.
- Ghi nhận SSI daily OHLCV history từ ngày bắt đầu giao dịch theo tài liệu, phân trang và rate-limit headers; phát hiện khác biệt giữa trang đăng ký và Quick Start về luồng đăng ký/định dạng ngày, đồng thời chưa có quota OHLC cụ thể.
- Ghi nhận DNSE endpoint OHLC history, tham số symbol/type/resolution/from/to, schema timestamp arrays và nextTime; depth dữ liệu, giới hạn OHLC và semantics paging chưa được xác minh.
- So sánh coverage, cơ sở giá, corporate actions, truy cập, phí và quyền học thuật trong `reports/BAO_CAO_KHAO_SAT_NGUON_DU_LIEU_GIA.md`.
- Đề xuất SSI làm ứng viên ưu tiên cho thử nghiệm đối chiếu và DNSE làm dự phòng tiềm năng; không chọn nguồn thay CafeF và chưa xác nhận adjusted basis của nguồn nào.
- Raw/Processed/CSV không bị thay đổi; không tính Daily Return/Volatility, không Feature Engineering hoặc Machine Learning.

## 2026-11-20 — Giai đoạn 2.8: chuẩn bị xác minh nhà cung cấp
- Đọc PROJECT_CONTEXT.md, PROJECT_PROGRESS.md, CHANGELOG.md, báo cáo khảo sát nguồn giá và báo cáo xác minh cơ sở giá.
- Tạo `reports/KE_HOACH_XAC_MINH_NHA_CUNG_CAP.md` gồm câu hỏi cho CafeF, SSI và DNSE, bảng theo dõi với mọi mục ban đầu `Chưa liên hệ`, cùng tiêu chí cho phép thử nghiệm API.
- Ghi rõ đây chỉ là chuẩn bị tài liệu; chưa liên hệ, chưa gọi API, chưa tạo/sử dụng credentials, chưa tải dữ liệu và chưa có kết luận xác minh mới.
- Không sửa Raw/Processed/CSV; không tính Daily Return/Volatility, không tạo Feature Engineering hoặc chạy phân cụm.

## 2026-11-20 — Đồng bộ phạm vi UI và ticker
- Thêm `src/data/universe.py` với 43 mã đã có trong Processed; module nhập liệu không còn giới hạn universe ở 10 mã ngân hàng cũ.
- Đồng bộ trang Tổng quan, Quản lý dữ liệu, Chất lượng dữ liệu, Phân tích dữ liệu, Machine Learning và Tra cứu nhóm sang clustering rủi ro HOSE.
- Kết nối trang EDA tới artifacts hiện có; giữ nguyên báo cáo và hình ảnh EDA đã hoàn thành.
- Sửa cú pháp thụt lề trang Tổng quan và thay tham số Streamlit deprecated `use_container_width`.
- Cập nhật README và PROJECT_PROGRESS. Xác minh compileall, 12/12 unittest, AppTest sáu trang không exception và HTTP 200 từ Streamlit.
- Không sửa Raw/Processed; chưa tính risk features hoặc chạy phân cụm thực tế.

## 2026-11-20 — Giai đoạn 2.9: tổng hợp xác minh dữ liệu
- Đối chiếu báo cáo chất lượng, xác minh dữ liệu/cơ sở giá, khảo sát SSI/DNSE, kế hoạch xác minh nhà cung cấp và quy tắc xử lý.
- Tạo `reports/BAO_CAO_TONG_HOP_XAC_MINH_DU_LIEU.md`, phân loại từng vấn đề và xác định rõ trường nào chưa đủ điều kiện cho Daily Return, Rolling Volatility, Maximum Drawdown, ATR và clustering.
- Ghi nhận không có bằng chứng mới từ nhà cung cấp; HOSE evidence cho ngày 14/08/2025 chỉ xác nhận thị trường có giao dịch, không giải thích missing của từng mã.
- Cập nhật PROJECT_PROGRESS.md. Raw/Processed không thay đổi; không tải dữ liệu, tính đặc trưng hoặc chạy mô hình.

## 2026-11-20 — Giai đoạn 2.11: đánh giá nguồn dữ liệu thay thế
- Ghi nhận giảng viên cho phép nguồn khác CafeF; phạm vi 43 mã HOSE, OHLCV và thời gian nghiên cứu giữ nguyên.
- Đọc lại tài liệu dự án và nghiên cứu tài liệu chính thức SSI FastConnect trước, DNSE OpenAPI sau; phân biệt schema/documentation claims với dữ liệu chưa thử runtime.
- Tạo `reports/BAO_CAO_DANH_GIA_NGUON_DU_LIEU_THAY_THE.md` với so sánh nguồn, thiết kế test 5 mã và kết quả kỹ thuật.
- Xác minh presence-only: không có SSI_API_KEY/SSI_API_SECRET/SSI_ACCESS_TOKEN hoặc `.env`; không gọi API, không tạo credentials, không tải dữ liệu.
- Triển khai SSI read-only adapter, CSV staging riêng với JSONL load manifest, quality audit không phá hủy và fixture tests.
- Kiểm thử cuối: compileall, 20/20 unittest, Streamlit AppTest sáu trang không exception và HTTP 200; Raw/Processed hashes giữ nguyên.
- Chưa chọn nguồn chính thức; chưa xác minh API thực tế, không sửa Raw/Processed và không thực hiện Feature Engineering/clustering.
# 2026-11-20 — Hoàn thiện ứng dụng và pipeline phân cụm thăm dò có điều kiện

- Đồng bộ `PROJECT_CONTEXT.md` và `README.md` với đề tài hiện hành: 43 doanh nghiệp HOSE, risk volatility và unsupervised clustering; Classification/10 ngân hàng chỉ còn là lịch sử cũ nơi có ghi.
- Bổ sung `src/data/research.py` để đọc Processed ở chế độ chỉ đọc và lấy 16 cờ OHLC trực tiếp từ `Data_Quality_Flag` (không hard-code danh sách giả định).
- Bổ sung `src/features/risk_features.py`: simple/log return, rolling volatility 20 phiên, drawdown theo đoạn liên tục, descriptive Volume và bản sensitivity; không dùng Adjusted Close, không nội suy, không chỉnh sửa dữ liệu nguồn.
- Bổ sung `src/models/clustering.py`: 2 feature sets (giá cốt lõi và giá + CV Volume độ nhạy), StandardScaler/RobustScaler, K-Means, Agglomerative Ward, DBSCAN, Silhouette/DB/CH, noise fraction và K-Means stability.
- Bổ sung script chạy thí nghiệm, metadata/provenance SHA-256, báo cáo Markdown và biểu đồ. Kết quả lưu riêng tại `data/analysis/`, `artifacts/clustering/`, `reports/`.
- Hoàn thiện trang quản lý dữ liệu với bộ lọc chỉ đọc, trang chất lượng có thống kê/cờ nguồn, trang EDA có bảng feature, trang phân cụm chạy pipeline, trang hồ sơ cụm/PCA. Điều hướng cuối đổi từ “Dự báo” sang “Đánh giá rủi ro”.
- Thêm heatmap Pearson cho bốn đặc trưng giá tổng hợp vào tab tương quan EDA, kèm cảnh báo đây là quan hệ khám phá trên dữ liệu conditional.
- Kết quả pipeline conditional trên dữ liệu CafeF hiện có: 43 mã, 124 cấu hình, 5.332 nhãn cấu hình; đây là thử nghiệm phần mềm có điều kiện, không phải kết quả rủi ro đã xác minh. DBSCAN noise được giữ nguyên và cảnh báo.
- Kiểm thử hoàn tất: compileall đạt, 34/34 unittest, AppTest sáu trang và app.py không exception; tương tác chạy mô hình/tra hồ sơ đạt; Streamlit `/` và `/_stcore/health` HTTP 200.
- SHA-256 Raw/Processed không đổi: `1B492296E31DB393DA80A8D2579887BBECB4AFB95F4F3A9FF9CECCBFB5186043` / `3574059045FBD420FC0EF473FCC6671C16C3A6BDC9F57478F02A7241598FE953`. Project folder không nằm trong Git work tree; không khởi tạo Git.
- Tạo `reports/BAO_CAO_HOAN_THIEN_DO_AN.md`; nhấn mạnh chưa đủ cơ sở khoa học/quyền sử dụng để công bố cụm như mức rủi ro thực tế.
- Raw và Processed không bị thay đổi. Test mới dùng fixture tổng hợp chỉ cho logic phần mềm.

## 2026-11-20 — Rà soát tệp dư thừa và cải tiến UI/UX
- Loại bỏ ba tài liệu mô phỏng OHLCV thuộc phạm vi Classification/ngân hàng cũ (`SIMULATION_DESIGN.md`, `SIMULATION_PARAMETERS.md`, `FINAL_SIMULATION_SPEC.md`); không có mã nguồn nào tham chiếu các tệp này. Giữ nguyên PDF ASM, hồ sơ quyết định, dữ liệu, artifacts, báo cáo EDA và thư mục dự án tham khảo.
- Dọn cache Python và thư mục tạm rỗng trong workspace.
- Làm mới hệ thống kiểu dùng chung: phân cấp màu sắc, khoảng cách, thẻ metric, cảnh báo, bảng, tab, nút và hiển thị màn hình nhỏ.
- Cải tiến trang Tổng quan bằng số liệu đọc từ dữ liệu thực và lối tắt điều hướng; bổ sung lọc loại biểu đồ và trạng thái rỗng rõ ràng ở trang EDA; rút gọn trang Machine Learning bằng các khối mở rộng, tab kết quả và bộ lọc chỉ số.
- Không thay đổi dữ liệu Raw/Processed, API hay thuật toán. Các kết quả thăm dò vẫn có điều kiện.
- Xác minh sau sửa: compileall đạt, 34/34 unittest đạt, AppTest sáu trang và app.py không exception; sáu route và health endpoint Streamlit trả HTTP 200. Không thay requirements.

## 2026-11-21 — Xuất slide demo và cập nhật GitHub
- Xuất deck Spaces thành `reports/SLIDE_THUYET_TRINH_ASM.pptx`; kiểm tra archive và xác nhận đủ 12 slide.
- Cập nhật README/PROJECT_PROGRESS để phân biệt slide đã lưu trong repository với PDF báo cáo conditional đang được giữ ngoài GitHub do quyền chia sẻ dữ liệu chưa xác minh.

## 2026-11-20 — Bản PDF và slide demo conditional
- Tạo `reports/BAO_CAO_TONG_KET_DO_AN_CONDITIONAL.pdf` dài 12 trang; render và kiểm tra trực quan trang đại diện, kiểm tra đủ 12 trang và nội dung trích xuất.
- Chuẩn bị bộ slide demo 12 trang trong Spaces; cập nhật slide kết luận để không còn ghi rằng PDF chưa được tạo.
- Đồng bộ `reports/BAO_CAO_HOAN_THIEN_DO_AN.md` và `PROJECT_PROGRESS.md`; nhấn mạnh đây là bản conditional, chưa phải kết luận nghiên cứu hoặc xác nhận đáp ứng rubric cuối cùng.
- Không sửa dữ liệu Raw/Processed, không thay đổi mã nguồn ứng dụng trong bước hoàn thiện tài liệu này.
