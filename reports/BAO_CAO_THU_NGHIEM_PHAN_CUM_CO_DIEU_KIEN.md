# Báo cáo Feature Engineering và phân cụm thăm dò có điều kiện

**Trạng thái:** kết quả thực nghiệm phần mềm trên Processed CafeF hiện có; *không phải mức rủi ro cổ phiếu đã xác minh*.

## 1. Phạm vi và cảnh báo dữ liệu

- Sử dụng Close và Volume từ `data/processed/stock_data_processed.csv`; không dùng Adjusted Close.
- CafeF chưa công bố công thức Adjusted Close, cơ sở giá qua corporate actions và quyền lưu/hiển thị dữ liệu vẫn chưa được xác minh.
- Do đó return, rolling volatility và drawdown dưới đây chỉ là đặc trưng khám phá có điều kiện. Không gọi kết quả là rủi ro thực tế.
- Không sửa Raw/Processed, không nội suy, không xóa quan sát nguồn. Các kết quả được lưu riêng trong `data/analysis/`.
- Lịch kề tính toán là hợp ngày quan sát trong Processed, không phải lịch HOSE độc lập; return qua ngày vắng của mã bị bỏ qua.

## 2. Quy trình đặc trưng

Tạo một dòng cho mỗi mã gồm độ lệch chuẩn return Close, median và P95 của rolling standard deviation 20 quan sát kề, cùng Maximum Drawdown dựa trên Close. Mean/log return và các thống kê Volume (mean, CV, median biến động tương đối) lưu để tham khảo; Volume không được gọi là thanh khoản vì đơn vị/phạm vi ghi nhận chưa được xác minh. Không dùng OHLC/ATR do basis OHLC và 16 cờ chưa giải quyết.

Phân tích độ nhạy loại khỏi phép tóm tắt những return chạm bản ghi có `Data_Quality_Flag` hoặc có độ lớn tuyệt đối từ 10% trở lên. Đây là phép lọc trong bản nhạy cảm, không sửa dữ liệu và ngưỡng 10% không xác định lỗi/corporate action. Chi tiết trong CSV độ nhạy; độ lệch tuyệt đối tương đối trung bình của độ lệch chuẩn return: 5.9%.

## 3. Quy mô và kiểm tra

- Số dòng nguồn: 53,385; số mã: 43; hợp ngày quan sát: 1242.
- Return kề được tính: 53,330; cặp bị bỏ qua do mã vắng ngày trong hợp lịch: 12.
- Cờ OHLC nguồn đã truyền sang sensitivity: 16; return jump nghi vấn (cờ cảnh báo, không khẳng định lỗi): 72.
- Ma trận đặc trưng phân cụm: 43 mã; đặc trưng giá cốt lõi được scale riêng từng lần chạy.

## 4. Mô hình và đánh giá

Đã khảo sát hai bộ: (a) bốn đặc trưng giá cốt lõi; (b) cùng bộ giá cộng hệ số biến thiên Volume (CV) như độ nhạy hoạt động giao dịch, không gọi đây là thanh khoản. Mỗi bộ thử K-Means (k=2–6, random_state=42, n_init=20), Agglomerative Ward (k=2–6) và DBSCAN (eps=0.5–2.5, min_samples=3–5), với StandardScaler và RobustScaler. DBSCAN noise không bị ép thành cụm; các metric chỉ tính trên phần tử không-noise nếu còn ít nhất hai cụm.

Các cấu hình đứng đầu theo Silhouette trong từng thuật toán và feature set (chỉ số nội bộ, không xác định tính đúng kinh tế):

| Feature_Set | Algorithm | Scaler | Parameters | N_Clusters | Noise_Count | Noise_Fraction | Silhouette | Davies_Bouldin | Calinski_Harabasz |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Giá (cốt lõi) | KMeans | StandardScaler | {"n_clusters": 2, "n_init": 20, "random_state": 42} | 2 | 0 | 0.00000 | 0.40910 | 0.86400 | 46.26927 |
| Giá (cốt lõi) | Agglomerative | RobustScaler | {"linkage": "ward", "n_clusters": 2} | 2 | 0 | 0.00000 | 0.39713 | 0.89065 | 42.94161 |
| Giá (cốt lõi) | DBSCAN | StandardScaler | {"eps": 0.75, "metric": "euclidean", "min_samples": 5} | 2 | 33 | 0.76744 | 0.58292 | 0.54796 | 24.95228 |
| Giá + CV Volume (độ nhạy) | KMeans | RobustScaler | {"n_clusters": 2, "n_init": 20, "random_state": 42} | 2 | 0 | 0.00000 | 0.77421 | 0.14026 | 36.86290 |
| Giá + CV Volume (độ nhạy) | Agglomerative | RobustScaler | {"linkage": "ward", "n_clusters": 2} | 2 | 0 | 0.00000 | 0.77421 | 0.14026 | 36.86290 |
| Giá + CV Volume (độ nhạy) | DBSCAN | StandardScaler | {"eps": 0.75, "metric": "euclidean", "min_samples": 4} | 2 | 34 | 0.79070 | 0.76929 | 0.28909 | 76.48670 |

Silhouette/DB/CH không có nhãn chuẩn và không chứng minh các cụm là cấp rủi ro thật. DBSCAN với Silhouette cao vẫn có thể bao phủ ít doanh nghiệp; cần đọc Noise_Fraction cùng metric. CV Volume có thể tách riêng mã MCH vì hệ số biến thiên lớn, đây là bằng chứng độ nhạy của phép gom cụm đối với trường Volume chưa rõ unit/semantics, không phải kết luận rủi ro. Kiểm tra độ ổn định K-Means bằng Adjusted Rand Index giữa seed 42 và 7/21/99; xem `artifacts/clustering/kmeans_stability.csv`.

## 5. Giới hạn

- Cơ sở giá, corporate actions và quyền dữ liệu chưa xác minh; biến động sự kiện có thể bị ghi nhận sai.
- Các mã chỉ 43 quan sát tổng hợp cross-section; phân cụm nhạy với feature set, scaler, tham số và ngoại lệ.
- Ngày thiếu không được nội suy; hợp ngày là đại diện quan sát, không phải lịch sàn.
- Volume summaries chỉ mô tả mức/độ biến thiên trường Volume; không đo thanh khoản đã xác nhận.
- Không đặt nhãn “rủi ro thấp/trung bình/cao” theo Cluster ID. Cần xác minh cơ sở giá và được nhóm/giảng viên chấp nhận trước khi dùng kết quả nghiên cứu.

## 6. Tệp đầu ra

- `data/analysis/features_conditional.csv`
- `data/analysis/features_sensitivity.csv`
- `artifacts/clustering/clustering_metrics.csv`
- `artifacts/clustering/clustering_labels.csv`
- `artifacts/clustering/cluster_profiles.csv`
- `artifacts/clustering/kmeans_stability.csv`
- `artifacts/clustering/metadata.json`
- `reports/BI_DO_SILHOUETTE_CAU_HINH.png`

Nguồn và giới hạn: `reports/BAO_CAO_TONG_KET_PHUONG_AN_DU_LIEU.md`, `reports/BAO_CAO_XAC_MINH_CO_SO_GIA.md`, `reports/DE_XUAT_FEATURE_ENGINEERING_RUI_RO.md`.
