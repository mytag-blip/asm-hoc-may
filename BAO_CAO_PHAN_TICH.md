# Báo cáo phân tích ASM Machine Learning

**Ngày cập nhật:** 17/11/2026  
**Phạm vi:** Hoàn tất phân tích nguồn và đề xuất kiến trúc; chưa triển khai ứng dụng.  
**Thư mục dự án:** D:/ASM_Hoc_May

## 1. Nguồn đã đọc và phạm vi kiểm tra

### Đề ASM
Đã mở và trích xuất đủ toàn bộ 5 trang của HỌC MÁY CƠ BẢN (2).pdf bằng pypdf.

### Dự án tham khảo
Repository nằm tại rag_vietstock-main/rag_vietstock-main. Đã liệt kê toàn bộ cây tệp dưới src/, scripts/, config/, tests/, docs/; đã mở README, cấu hình/dependencies, các module crawler, API/UI và tests liên quan.

Các file đã mở:
- Gốc/cấu hình: README.md, pyproject.toml, config/settings.py, .env.example.
- Crawler: src/crawler/vietstock_client.py, ticker_universe.py, downloader.py, pipeline.py, batch_crawler.py, ingestion_worker.py, cli.py.
- API/UI: src/api/app.py, routes_ingest.py, routes_batch.py, schemas.py; src/ui/app_streamlit.py, api_client.py, app_pages/market_sync.py, app_pages/rag_chat.py.
- Scripts/docs/tests: scripts/demo_pipeline.py, create_sample_pdf.py, run_pdf_benchmark.py; docs/PLAN-vietstock-rag.md; tests/test_crawler.py, test_ticker_universe.py, test_batch_crawler.py, test_batch_api.py.

Các tệp còn lại trong src/scripts/config/tests/docs được nhận diện trong cây thư mục, nhưng không mở từng tệp không liên quan trực tiếp. Không chạy test, không gọi crawler ra Vietstock và không xác minh endpoint trực tuyến trong lần phân tích này. Endpoint dưới đây được mô tả theo source đã mở, không phải khẳng định còn hoạt động trên website.

## 2. Yêu cầu trích từ PDF ASM

### Bối cảnh và hai hướng bài toán
Đề đặt bối cảnh nhóm 3–5 sinh viên đóng vai chuyên viên phân tích dữ liệu định lượng tại công ty chứng khoán, thu thập dữ liệu thực tế từ Vietstock và làm theo hai giai đoạn ứng với Lab 1–8.

PDF nêu hai hướng chính:
1. Regression: dự báo giá đóng cửa hoặc tỷ suất sinh lời phiên kế tiếp từ OHLCV và chỉ báo kỹ thuật.
2. Classification: dự đoán xu hướng tăng/giảm phiên kế tiếp hoặc phân loại sức khỏe tài chính doanh nghiệp.

Phạm vi hiện tại là Classification dự đoán tăng so với giảm/đứng giá của phiên kế tiếp. Không chuyển sang Regression hay nhánh sức khỏe tài chính.

### Thu thập dữ liệu
Giai đoạn 1 yêu cầu trích xuất từ Vietstock dữ liệu giao dịch lịch sử (kết quả khớp lệnh theo ngày) hoặc báo cáo tài chính, dạng CSV/XLSX. Ví dụ Classification tại trang 4 dùng lịch sử giá hằng ngày 2–3 năm cho 1 mã đầu ngành (HPG/FPT/VCB chẳng hạn) hoặc VN-Index. Đề tổng quan cho phép VN30 hoặc 5–10 mã cùng ngành.

Danh sách ngân hàng ACB, BID, CTG, MBB, TCB, VCB, VPB, STB, HDB, SHB là lựa chọn do người dùng cung cấp; PDF cho phép chọn 5–10 mã cùng ngành nhưng không bắt buộc đúng các mã này. PDF không yêu cầu API hay crawler tự động; yêu cầu file dữ liệu là .csv hoặc .xlsx.

### Mô tả dữ liệu, EDA, tiền xử lý
Phải lập bảng mô tả số dòng, số cột, ý nghĩa kinh tế từng biến đầu vào X và biến mục tiêu y. EDA yêu cầu biểu đồ giá/khối lượng/phân phối bằng line chart, histogram, boxplot và heatmap tương quan. Tiền xử lý phải xử lý missing (ví dụ ngày nghỉ/lễ hoặc mã tạm ngừng giao dịch), duplicates và outliers; chuẩn hóa/normalization; chia Train/Test theo thứ tự thời gian để tránh rò rỉ tương lai.

PDF không quy định tỷ lệ chia, nội suy cụ thể hay ngưỡng loại outlier. Không tạo phiên giao dịch giả để bù ngày nghỉ.

### Feature Engineering và mục tiêu
Cần tạo tối thiểu 3 đặc trưng mới có ý nghĩa kỹ thuật/tài chính. Ví dụ trang 2: High−Low, lợi suất ngày, MA5/MA20, lag_1/lag_2. Ví dụ Classification trang 4 nêu OHLCV của 1–3 phiên trước, mua/bán ròng khối ngoại và MA5/MA20.

Nhãn: 1 nếu giá đóng cửa ngày mai tăng so với hôm nay; 0 nếu giảm hoặc đứng giá. Logistic Regression có thể được diễn giải qua trọng số để nói về yếu tố liên quan xác suất tăng.

### Mô hình, chỉ số và tối ưu
- Giai đoạn 1 baseline Classification: Logistic Regression.
- Giai đoạn 2: thêm tối thiểu 02–03 mô hình để so sánh; đề liệt kê KNN, Decision Tree, Random Forest. Đề xuất triển khai đủ ba mô hình này.
- K-Means là phần mở rộng khuyến khích, không bắt buộc cho phạm vi Classification dự đoán xu hướng.
- Giai đoạn 1 Classification: Accuracy và Confusion Matrix.
- Giai đoạn 2 Classification: Precision, Recall, F1-Score, ROC-AUC; lập bảng so sánh trên tập kiểm thử.
- MAE, RMSE, R² trong PDF áp dụng cho Regression, không phải chỉ số chính của nhánh Classification.
- Phân tích Overfitting/Underfitting qua chênh lệch điểm Train và Test.
- Tinh chỉnh hyperparameter; ví dụ n_estimators, max_depth, n_neighbors (RF/Tree/KNN). Dùng validation theo thời gian bên trong vùng train để chọn tham số.
- Trích xuất Feature Importance từ Random Forest và giải thích các yếu tố đầu vào.

### Kiểm thử dữ liệu mới
Lấy dữ liệu thật của 20 phiên giao dịch gần nhất từ Vietstock, chưa xuất hiện trong quá trình huấn luyện, để dự báo thử. Phân tích mô hình theo pha thị trường tăng/giảm/đi ngang và nêu rủi ro thực tế như tin vĩ mô, cổ tức, biến động bất thường. Để giữ đúng ý “chưa xuất hiện”, 20 phiên này không được dùng để tune/chọn mô hình; đây là cách diễn giải kỹ thuật, không phải tỷ lệ Train/Test quy định bởi PDF.

### Sản phẩm bàn giao
Giai đoạn 1:
- CSV dữ liệu thô và dữ liệu làm sạch.
- Notebook .ipynb có đầy đủ bước; PDF gợi ý Pandas, NumPy, Matplotlib/Seaborn, Scikit-learn.
- Báo cáo tiến độ PDF 5–7 trang.

Giai đoạn 2:
- Notebook/mã nguồn hoàn chỉnh giai đoạn 1–2, chạy không lỗi.
- Báo cáo tổng kết PDF 10–15 trang.
- Slide 10–12 trang; demo trước lớp 10 phút trình bày và 5 phút hỏi đáp.

Dashboard web không phải sản phẩm bắt buộc theo PDF; đây là nhu cầu ứng dụng người dùng nêu thêm, không thay thế notebook/báo cáo/slide/demo.

### Rubric
| Hạng mục | Trọng số | Tiêu chí |
|---|---:|---|
| Giai đoạn 1: Dữ liệu & tiền xử lý | 30% | Trích xuất Vietstock chuẩn xác; xử lý lỗi/thiếu hợp lý; đặc trưng có ý nghĩa; baseline đúng kỹ thuật |
| Giai đoạn 2: Mô hình & tối ưu hóa | 35% | Triển khai/so sánh KNN, Decision Tree, Random Forest/K-Means; tuning và giải thích mức cải thiện |
| Tính ứng dụng & phân tích kinh tế | 20% | Diễn giải tài chính/đầu tư; kiểm thử dữ liệu mới thuyết phục; nêu ưu/nhược điểm |
| Báo cáo, code & thuyết trình | 15% | Code sạch, chú thích rõ; báo cáo khoa học; trình bày và phản biện tốt |

Tổng: 100%.

## 3. Cấu trúc và chức năng source tham khảo đã kiểm tra

### Nhận diện
README xác định đây là Vietstock PDF RAG Engine: thu thập tài liệu cổ đông, parse/OCR/bảng PDF, lưu PostgreSQL/pgvector, hybrid search, reranker và Qwen. pyproject.toml khai báo FastAPI, SQLAlchemy async/PostgreSQL, httpx, BeautifulSoup, tenacity, parser/OCR, embedding và Streamlit; không khai báo scikit-learn, Matplotlib hay Seaborn.

Cây source chính gồm crawler, parser, rag, llm, db, api, ui; ngoài ra scripts, config, tests, docs, docker và fixtures PDF.

### Crawler, request và loại dữ liệu
- src/crawler/vietstock_client.py: base URL finance.vietstock.vn. GET /{ticker}/tai-tai-lieu.htm lấy cookie phiên và __RequestVerificationToken; sau đó POST /data/getdocument với ticker/page/token và tùy chọn loại/năm. Chuẩn hóa title, URL file, extension, năm/kỳ/ngày công bố/loại tài liệu; có fallback parse link HTML. fetch_all_documents_by_ticker duyệt phân trang metadata tài liệu, có limit/dedupe.
- Client dùng httpx.AsyncClient, timeout, raise_for_status, delay cấu hình 1.5–3 giây và log lỗi. Một số lỗi trả danh sách rỗng nên caller có thể thấy kết quả rỗng thay cho lỗi có cấu trúc.
- src/crawler/ticker_universe.py: GET /search-stock phân trang với query/page/pageSize/skip/languageId; chuẩn hóa mã, tên, sàn, ngành và upsert Company. Đây là metadata doanh nghiệp, không phải giá lịch sử.
- src/crawler/downloader.py: GET file URL theo redirect; retry tối đa 3 lần exponential backoff; SHA-256, kích thước, lưu theo data/pdfs/{TICKER}/{YEAR}/{filename}. Không kiểm tra MIME, magic bytes %PDF- hay schema nội dung trước khi lưu.
- src/crawler/pipeline.py: đảm bảo Company, lấy document types/URL đã biết, lấy metadata, bỏ non-PDF/trùng URL, tải file, dedupe hash, lưu ShareholderDocument trạng thái DOWNLOADED.
- Kết luận chính xác: “toàn bộ lịch sử” trong crawler là toàn bộ lịch sử tài liệu công bố của ticker. Trong các module crawler đã mở không thấy endpoint hay parser lấy OHLCV/close/volume/foreign flow theo từng phiên giao dịch. Crawler này không cung cấp sẵn dữ liệu giá ASM; hai loại dữ liệu không tương đương.

### Batch, xử lý, logging
- src/crawler/batch_crawler.py: tạo CrawlJob, asyncio queue/worker (mặc định concurrency 2), delay giữa ticker, checkpoint số mã thành công/thất bại, số tài liệu, current ticker và error summary trong PostgreSQL; hỗ trợ hủy job. Batch theo ticker để tải tài liệu.
- src/crawler/ingestion_worker.py: trạng thái DOWNLOADED → parse PDF/bảng → PARSED → chunk/embed → EMBEDDED hoặc ERROR. Đây là ingestion tài liệu RAG.
- src/crawler/cli.py: sync-companies, crawl-ticker, crawl-market, status; cấu hình logging cơ bản trên console. Các module dùng logger theo module; job lưu trạng thái và error summary DB. Các file đã mở không cho thấy handler ghi log crawler riêng ra file.
- src/api/app.py, routes_ingest.py, routes_batch.py: FastAPI mount các endpoint crawl tài liệu, parse/batch, danh sách tài liệu, đồng bộ danh mục và theo dõi/hủy job; không phải API giá/ML.
- src/ui/app_streamlit.py, api_client.py và app_pages/market_sync.py: Streamlit tiếng Việt cho chọn mã, “Quét PDF”, quản lý trạng thái file, đồng bộ ticker, khởi chạy job, hiển thị tiến độ/hủy job; api_client gọi FastAPI bằng HTTPX và cache ngắn. rag_chat.py gọi endpoint query Q&A. Đây là mẫu cấu trúc UI/API, không phải dashboard ML.
- Scripts: demo_pipeline.py chạy parse → chunk → embedding → rerank → Qwen. create_sample_pdf.py sinh PDF tài chính tổng hợp để kiểm thử. run_pdf_benchmark.py đánh giá extraction/OCR/bảng PDF, không benchmark giá hoặc model classification.
- Tests: test_crawler.py kiểm tra normalize metadata, pagination mock, lọc extension/URL duplicate/hash; test_ticker_universe.py kiểm tra normalize/filter; test_batch_crawler.py và test_batch_api.py kiểm tra một phần job/API. Payload là mock/fake; không chứng minh truy xuất giá live.
- docs/PLAN-vietstock-rag.md mô tả mục tiêu RAG; kết luận thực tế ở báo cáo dựa trên source đã mở, không dựa duy nhất vào kế hoạch.

## 4. Bảng đối chiếu và khả năng kế thừa

| Thành phần | Dự án tham khảo | Yêu cầu ASM | Khả năng kế thừa |
|---|---|---|---|
| Dữ liệu | Danh mục công ty, metadata và file PDF cổ đông | OHLCV hằng ngày, 2–3 năm, nhãn xu hướng | Không dùng crawler PDF làm nguồn giá; nhập Vietstock CSV/XLSX hoặc xây client lịch sử giá riêng sau khi xác minh |
| HTTP | httpx async, timeout/status, retry/delay | Lấy dữ liệu giá nếu truy cập hợp lệ | Kế thừa phân lớp client, timeout, xử lý lỗi; không mặc định endpoint tài liệu là endpoint lịch sử giá |
| Extraction | JSON/HTML metadata và file PDF | Bảng ngày có giá, volume, trường bổ sung nếu có | Cần parser CSV/XLSX hoặc parser lịch sử giao dịch riêng |
| Validation | Chuẩn hóa metadata, lọc title/URL/extension, dedupe URL/hash | Schema, kiểu ngày/giá, duplicate mã-ngày, missing, outlier, dữ liệu thực | Kế thừa kiểm tra schema và chống trùng về ý tưởng; viết validation tài chính riêng |
| Lưu trữ | PDF phân cấp theo mã/năm, PostgreSQL | CSV thô/sạch và kết quả notebook | Kế thừa raw/processed/provenance; database không bắt buộc ban đầu |
| Pipeline | Crawl metadata → download → DB → parse/OCR → vector | Import → kiểm tra → EDA → features → time split → ML/evaluate | Kế thừa các stage, trạng thái, lỗi; thiết kế pipeline ML riêng |
| Batch/log | Worker queue, checkpoint DB, progress/cancel, logger | Xử lý nhiều mã và quan sát tiến trình | Kế thừa progress/logging mức nhẹ; không cần PostgreSQL job queue lúc đầu |
| FastAPI | API cho crawler, RAG query, batch | Dashboard ASM | Chưa cần; chỉ thêm nếu cần backend độc lập/multiple clients |
| Streamlit | Quản lý PDF, RAG/OCR và job | Dashboard tiếng Việt cho EDA/ML/dự báo | Kế thừa giao diện/navigation/trạng thái; thay toàn bộ nghiệp vụ PDF |
| ML/RAG | Không có pipeline classification; nhiều thành phần RAG | LR, KNN, Tree, RF và chỉ số classification | Xây riêng bằng Scikit-learn; bỏ Qwen, BGE, vector DB, OCR, hybrid search, reranker |

## 5. Kiến trúc ASM đề xuất

Đề xuất một ứng dụng Streamlit đơn khối với package Python dùng chung; không tách FastAPI vì đề không yêu cầu API độc lập. Notebook giai đoạn 1 và 2 là đầu ra học thuật bắt buộc và dùng chung logic xử lý với dashboard, không bị dashboard thay thế.

Luồng đề xuất:
Vietstock CSV/XLSX → lưu raw → kiểm tra → làm sạch → mô tả/EDA → tạo nhãn/đặc trưng → chia thời gian → Logistic Regression baseline → KNN/Decision Tree/Random Forest và tuning → đánh giá/so sánh/feature importance → dự báo 20 phiên mới → xuất CSV, hình, báo cáo.

Chỉ xây tự động hóa Vietstock historical-price sau khi xác minh phương thức hợp lệ và kiểm tra nội dung dữ liệu thực nhận. Nếu không khả thi, nhập file người dùng tải từ Vietstock. Không tạo dữ liệu giả.

### Cấu trúc thư mục đề xuất
D:/ASM_Hoc_May/
- app.py; pages/ cho tổng quan, dữ liệu, EDA, mô hình, dự báo.
- notebooks/giai_doan_1_baseline.ipynb; notebooks/giai_doan_2_mo_hinh_va_danh_gia.ipynb.
- src/data/ cho loaders, validation và client lịch sử giá (chỉ nếu truy cập hợp lệ).
- src/preprocessing/, src/features/, src/models/, src/visualization/, src/reporting/.
- data/raw/, data/processed/, artifacts/, reports/, slides/, requirements.txt.

### Trách nhiệm chính
- Loader/validator: đọc CSV/XLSX Vietstock, báo cột thiếu/sai kiểu, missing, duplicates theo ticker-ngày, và lỗi nội dung.
- Preprocessing/EDA: biểu đồ theo PDF, thống kê thiếu/outlier; giữ dữ liệu thô; không nội suy ngày nghỉ thành phiên giao dịch.
- Features: ít nhất ba biến mới; tạo target theo từng mã, căn close(t+1) với X tại t để không rò rỉ tương lai.
- Model/evaluation: Logistic Regression baseline; KNN, Decision Tree, Random Forest; đúng metric classification; tuning theo thời gian; RF feature importance.
- Dashboard và notebooks dùng chung xử lý. Scaler/imputer fit trên train, không shuffle; giữ 20 phiên cuối mới tách biệt nếu dữ liệu thực cho phép.
- Export các CSV, notebook, PDF report và slide đúng yêu cầu.

## 6. Vấn đề chưa thể xác minh và rủi ro
1. Chưa có dữ liệu giao dịch thực tế trong source/workspace để xác minh tên cột, chất lượng, độ phủ 2–3 năm, adjustment, đơn vị volume hoặc có foreign flow không.
2. Chưa xác minh endpoint lịch sử giá hay quyền/điều kiện truy cập Vietstock hiện tại; source mẫu chỉ cho thấy endpoint danh mục và tài liệu.
3. Tỷ lệ Train/Test, validation/tuning cụ thể không được PDF nêu; cần ghi rõ lựa chọn khi triển khai và không dùng 20 phiên mới để tune.
4. 10 mã ngân hàng là lựa chọn của người dùng, không danh sách bắt buộc của PDF.
5. Phân loại pha thị trường tăng/giảm/đi ngang cần tiêu chí minh bạch; PDF không định nghĩa phương pháp.
6. Foreign net flow nằm trong ví dụ đặc trưng nhưng chưa xác minh có trong file tải. Không đưa biến vào nếu nguồn không có.
7. Reference downloader không xác minh nội dung/magic bytes trước khi ghi file; status HTTP không đủ để xác nhận PDF hợp lệ.
8. Test/demo dự án mẫu là mock hoặc PDF fixture; không được dùng thay dữ liệu giá thật.

## 7. Kết luận
PDF yêu cầu baseline Logistic Regression ở giai đoạn 1; giai đoạn 2 so sánh thêm KNN, Decision Tree, Random Forest; EDA, tiền xử lý, tối thiểu ba feature mới, chia thời gian, metric classification, tuning, train-test gap, RF feature importance, kiểm thử 20 phiên Vietstock chưa thấy trong train, phân tích ứng dụng/rủi ro và bàn giao notebook, CSV, báo cáo, slide, demo theo rubric 30/35/20/15.

Dự án tham khảo có thể cung cấp ý tưởng kỹ thuật về HTTP client, timeout/retry/delay, chống trùng, pipeline nhiều bước, batch progress, logging và giao diện Streamlit/FastAPI. Nhưng crawler của nó thu thập danh mục mã và tài liệu PDF cổ đông, không phải dữ liệu giao dịch lịch sử theo ngày. Đề xuất dùng CSV/XLSX Vietstock làm luồng dữ liệu ban đầu và chỉ bổ sung crawler lịch sử giá sau khi xác minh truy cập hợp lệ.

**Phân tích đã hoàn tất; chưa viết code triển khai và chưa chuyển sang giai đoạn tiếp theo.**
