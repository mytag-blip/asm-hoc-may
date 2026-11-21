# Báo cáo hoàn thiện vòng triển khai đồ án

**Ngày:** 20/11/2026  
**Đề tài:** Ứng dụng các thuật toán học máy không giám sát trong phân nhóm và đánh giá rủi ro biến động giá cổ phiếu của 43 doanh nghiệp HOSE.

> Đây là báo cáo kết quả triển khai kỹ thuật có điều kiện. CafeF chưa được xác minh đầy đủ về price basis, corporate actions và quyền sử dụng dữ liệu. Vì vậy các đặc trưng và cụm bên dưới là thử nghiệm trên bộ Processed hiện có, không phải kết luận mức rủi ro thị trường đã xác minh.

## 1. Phạm vi dữ liệu

- Đọc `data/processed/stock_data_processed.csv`: 53.385 bản ghi, 43 mã, ngày quan sát 19/11/2021–18/11/2026; hợp ngày quan sát có 1.242 ngày.
- Số quan sát mỗi mã: 35 mã có 1.242; 7 mã có 1.241; MCH có 1.228. Tổng cộng 21 thiếu mã-ngày so với phép tích 43 × 1.242. Đây không khẳng định từng ngày là phiên giao dịch HOSE.
- Không dùng Adjusted Close, Open, High hoặc Low trong pipeline return/risk; không tính ATR do cơ sở OHLC và 16 cờ chưa giải quyết.
- Volume được đưa vào bảng mô tả và một feature set độ nhạy; không gọi là thanh khoản do unit/phạm vi chưa xác minh.
- Không dùng F-Fin để vá dữ liệu CafeF, không tải dữ liệu mới, không gọi SSI, không tạo dữ liệu giả.

## 2. Quy trình Feature Engineering

Module `src/features/risk_features.py` tạo một dòng/mã, không sửa frame đầu vào:

- Simple Return và Log Return từ Close chỉ cho cặp ngày kề nhau trong hợp ngày quan sát của bộ dữ liệu. Không tính return bắc qua ngày vắng của mã.
- Rolling volatility: độ lệch chuẩn mẫu (`ddof=1`) trên 20 return liên tục; cửa sổ không đi qua gap.
- Maximum Drawdown Close-based tính trong đoạn liên tục và reset tại gap.
- Volume summaries: mean, CV và median độ biến động tương đối theo các phiên kề có Volume trước đó dương; chỉ là hoạt động khối lượng mô tả.
- Bản sensitivity loại khỏi thống kê những return chạm một trong 16 dòng `Data_Quality_Flag` ở một trong hai đầu mút, hoặc có |return| ≥10%. Đây là ngưỡng cảnh báo khám phá, không xác định dữ liệu lỗi hay corporate action. Không dòng nguồn nào bị xóa.

Không đưa Average Return, Volume, ticker hay nhãn tự tạo vào feature set giá cốt lõi. Feature set độ nhạy thêm `Volume_CV_Descriptive` để kiểm tra độ nhạy kết quả với biến hoạt động giao dịch; kết quả tách MCH thành nhóm riêng trong một cấu hình, cho thấy nguy cơ phụ thuộc trường Volume chưa rõ semantics.

## 3. Thuật toán và đánh giá

Đã chạy hai feature set, StandardScaler và RobustScaler:

- K-Means: k=2–6, `random_state=42`, `n_init=20`.
- Agglomerative Ward: k=2–6.
- DBSCAN: eps=0.5, 0.75, 1.0, 1.25, 1.5, 2.0, 2.5; `min_samples`=3, 4, 5.
- Tổng 124 cấu hình; 5.332 dòng gán cluster qua các cấu hình.
- Đánh giá Silhouette, Davies–Bouldin, Calinski–Harabasz; DBSCAN báo riêng tỷ lệ noise. Không tính metric nếu còn ít hơn hai cụm/không đủ mẫu sau khi bỏ noise.
- K-Means độ ổn định so seed 42 với seed 7, 21, 99 bằng Adjusted Rand Index.

Cấu hình cao nhất theo Silhouette trong từng feature set/thuật toán:

| Feature set | Thuật toán | Scaler | Cụm | Noise | Silhouette | Davies–Bouldin | Calinski–Harabasz |
|---|---|---|---:|---:|---:|---:|---:|
| Giá cốt lõi | K-Means | StandardScaler | 2 | 0 | 0,40910 | 0,86400 | 46,26927 |
| Giá cốt lõi | Agglomerative | RobustScaler | 2 | 0 | 0,39713 | 0,89065 | 42,94161 |
| Giá cốt lõi | DBSCAN | StandardScaler | 2 | 33 (76,7%) | 0,58292 | 0,54796 | 24,95228 |
| Giá + CV Volume (độ nhạy) | K-Means | RobustScaler | 2 | 0 | 0,77421 | 0,14026 | 36,86290 |
| Giá + CV Volume (độ nhạy) | Agglomerative | RobustScaler | 2 | 0 | 0,77421 | 0,14026 | 36,86290 |
| Giá + CV Volume (độ nhạy) | DBSCAN | StandardScaler | 2 | 34 (79,1%) | 0,76929 | 0,28909 | 76,48670 |

> Đây là metric nội bộ trên 43 dòng tổng hợp cross-sectional, không có nhãn chuẩn. Silhouette DBSCAN cao được tính trên phần không-noise nhưng phần lớn doanh nghiệp bị gán noise. CV Volume làm K-Means/Agglomerative tách MCH thành cụm một mã ở cấu hình k=2. Không có cơ sở chọn các cấu hình này làm mô hình nghiên cứu hay đặt nhãn “rủi ro thấp/trung bình/cao”.

## 4. Giao diện

- Tổng quan lấy số dòng/ngày từ Processed và số cấu hình đã đánh giá từ artifact; universe đọc từ `src/data/universe.py`.
- Quản lý dữ liệu giữ nguyên luồng nhập CSV/XLSX hiện có và bổ sung bộ lọc đọc-only cho Processed.
- Chất lượng dữ liệu hiển thị thiếu, trùng, 16 cờ OHLC và cờ Volume lớn; không tự sửa.
- Phân tích dữ liệu giữ biểu đồ EDA/report đã lưu, bảng feature conditional và heatmap Pearson của bốn đặc trưng giá tổng hợp có cảnh báo.
- Machine Learning hiển thị feature matrix, bản sensitivity, nút chạy các cấu hình và bảng/biểu đồ metric.
- Điều hướng trang cuối đổi từ “Dự báo” sang “Đánh giá rủi ro”; hiển thị cấu hình, cluster profiles, danh sách mã và PCA 2D để trực quan hóa. PCA không phải trục rủi ro.

## 5. Tệp đầu ra

- `data/analysis/features_conditional.csv`
- `data/analysis/features_sensitivity.csv`
- `artifacts/clustering/clustering_metrics.csv`
- `artifacts/clustering/clustering_labels.csv`
- `artifacts/clustering/cluster_profiles.csv`
- `artifacts/clustering/kmeans_stability.csv`
- `artifacts/clustering/metadata.json`
- `reports/BAO_CAO_THU_NGHIEM_PHAN_CUM_CO_DIEU_KIEN.md`
- `reports/BI_DO_SILHOUETTE_CAU_HINH.png`

Metadata ghi thời điểm UTC, SHA-256 của Processed, phiên bản scikit-learn, seed, scaler/feature sets và cảnh báo price basis. Output chỉ nằm ngoài Raw/Processed.

## 6. Kiểm thử và vận hành

- `python -m compileall -q app.py src pages tests scripts`: đạt.
- `python -m unittest discover -s tests -v`: **34/34 đạt**. Có 6 test mới cho feature/gap/flag/clustering; fixture tổng hợp chỉ kiểm thử logic, không phải dữ liệu thị trường. Một test argparse in usage/error khi cố tình truyền ticker ngoài allowlist rồi xác nhận bị từ chối; test vẫn đạt.
- Streamlit `AppTest`: 6/6 trang không exception; `app.py` không exception. Đã click chạy thí nghiệm trong trang ML và mở trang hồ sơ sau khi có artifacts, đều không exception.
- Server Streamlit thực: `/` HTTP 200; `/_stcore/health` HTTP 200, body `ok`.
- AppTest có các hộp cảnh báo có chủ đích về price basis chưa xác minh; log kiểm thử bare mode có thông báo thiếu ScriptRunContext, không phải lỗi khi chạy server.
- Dependencies không thay đổi.

## 7. Tính toàn vẹn và trạng thái repository

Raw/Processed giữ đúng SHA-256 đã có trước đó:

- Raw: `1B492296E31DB393DA80A8D2579887BBECB4AFB95F4F3A9FF9CECCBFB5186043`.
- Processed: `3574059045FBD420FC0EF473FCC6671C16C3A6BDC9F57478F02A7241598FE953`.
- F-Fin staging không được sửa; hash: `93B2E82C1549F47E677A9AC93E5F0E2D6914513C4726684E93E3BAAB39C89340`.

`D:\ASM_Hoc_May` hiện không nằm trong Git work tree (`git rev-parse --is-inside-work-tree` thất bại). Không khởi tạo hoặc thay đổi repository.

## 8. Hạn chế và việc còn lại

- Chưa xác minh CafeF Close qua corporate actions; vì vậy return, volatility và drawdown có thể chứa biến động kỹ thuật do điều chỉnh quyền/cổ tức.
- Chưa phân loại lịch phiên thiếu theo từng mã; hợp ngày quan sát không phải lịch HOSE chính thức.
- Chưa có feed độc lập cho 16 cờ OHLC; unit/semantics Volume và quyền lưu trữ/hiển thị CafeF chưa xác minh.
- 43 doanh nghiệp là cỡ mẫu nhỏ cho đánh giá clustering; metric nội bộ không chứng minh cụm có ý nghĩa kinh tế.
- Chưa có nguồn đã được nhóm/giảng viên chấp thuận làm nguồn chính thức; chưa đủ điều kiện kết luận mức độ rủi ro thực tế.
- Đã chuẩn bị báo cáo PDF conditional 12 trang tại `reports/BAO_CAO_TONG_KET_DO_AN_CONDITIONAL.pdf` và bộ slide demo 12 trang trong Spaces. Đây là tài liệu trình bày thử nghiệm có điều kiện, chưa phải báo cáo nghiên cứu đã xác minh hoặc xác nhận đáp ứng đầy đủ rubric của PDF ASM. Cần cập nhật sau khi làm rõ cơ sở dữ liệu và yêu cầu giảng viên.

## 9. Kết luận

Ứng dụng và pipeline phân cụm có thể chạy; các trang chính và kiểm thử đạt. Kết quả hiện đáp ứng mục tiêu hoàn thiện kỹ thuật/demo có cảnh báo, nhưng **chưa đủ điều kiện khoa học để công bố mức rủi ro thực tế**. Bước tiếp theo phù hợp là trình bày rõ đây là thử nghiệm conditional, đồng thời xin/thu thập bằng chứng về price basis, Corporate Actions, units, quyền sử dụng và xử lý ngày thiếu trước khi phê duyệt kết quả nghiên cứu cuối.

