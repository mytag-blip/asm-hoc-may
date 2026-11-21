# ASM Học Máy Cơ Bản — phân nhóm rủi ro biến động giá

Dashboard Streamlit cho đề tài phân nhóm 43 doanh nghiệp niêm yết HOSE bằng các thuật toán học máy không giám sát.

## Trạng thái kết quả

> Dữ liệu giá hiện có từ CafeF chưa được xác minh đầy đủ về cơ sở điều chỉnh, Corporate Actions, đơn vị và quyền sử dụng. Ứng dụng có pipeline **thăm dò có điều kiện** trên Close và Volume để kiểm tra kỹ thuật; các return, volatility, drawdown và cụm đầu ra **không phải kết luận rủi ro thực tế đã xác minh**. Không sử dụng Adjusted Close, không nội suy, không thay đổi Raw/Processed. Đọc `reports/BAO_CAO_THU_NGHIEM_PHAN_CUM_CO_DIEU_KIEN.md` trước khi xem kết quả.

## Chức năng

- Tổng quan dự án, universe 43 mã và trạng thái dữ liệu.
- Nhập CSV/XLSX, kiểm tra schema và lưu file upload riêng; trình duyệt Processed chỉ đọc có lọc mã/ngày.
- Trang chất lượng hiển thị missing/duplicate, 16 cờ OHLC và cờ Volume lớn theo từng mã.
- EDA hiển thị biểu đồ/report đã lưu, bảng đặc trưng khám phá và heatmap Pearson có điều kiện.
- Thử nghiệm K-Means, Agglomerative Ward và DBSCAN với nhiều cấu hình, StandardScaler/RobustScaler, Silhouette, Davies–Bouldin, Calinski–Harabasz, số noise và độ ổn định K-Means.
- Tra cứu hồ sơ cụm, danh sách mã, PCA 2D để trực quan hóa. Cluster ID không được tự diễn giải thành nhãn rủi ro.
- Dashboard dùng giao diện tiếng Việt đồng nhất, lối tắt từ trang Tổng quan, bộ lọc biểu đồ EDA và các tab/bộ lọc để đọc kết quả phân cụm.

## Cài đặt

```powershell
Set-Location D:\ASM_Hoc_May
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
```

## Chạy ứng dụng

```powershell
streamlit run app.py
```

Trong trang **Machine Learning**, xem ma trận feature và cảnh báo rồi bấm **Chạy đánh giá cấu hình phân cụm**. Hoặc chạy trực tiếp:

```powershell
python scripts/run_conditional_clustering.py
```

Output nằm trong `data/analysis/`, `artifacts/clustering/`, `reports/`. Metadata lưu thời điểm chạy, hash SHA-256 của Processed, version scikit-learn và cảnh báo price basis. Các tệp Raw/Processed không bị ghi đè.

## Cách tính khám phá

- Simple return và log return từ `Close`, riêng theo mã, chỉ khi ngày kề nhau trong hợp ngày quan sát Processed; gap bị bỏ qua, không lấp ngày.
- Độ lệch chuẩn rolling 20 return (ddof=1), reset ở gap; drawdown Close-based cũng reset ở gap.
- Feature set cốt lõi: độ lệch chuẩn return, median/P95 rolling volatility và maximum drawdown. Bảng mô tả lưu thêm Volume CV và median |Volume Change|; feature set độ nhạy thêm CV Volume, không gọi đây là thanh khoản vì unit/semantics chưa đủ bằng chứng.
- Độ nhạy đánh dấu/loại khỏi bản tóm tắt các return chạm cờ OHLC đã có hoặc |return|≥10%; đây không phải sửa dữ liệu hay quy kết corporate action.
- 2 feature sets × 2 scalers × K-Means k=2–6, Agglomerative Ward k=2–6 và DBSCAN eps=0.5–2.5/min_samples=3–5. DBSCAN noise giữ riêng.
- Metric nội bộ chỉ so sánh cấu hình, không có nhãn chuẩn và không xác nhận cụm là cấp rủi ro.

## Kiểm thử

```powershell
python -m compileall -q app.py src pages tests scripts
python -m unittest discover -s tests -v
```

Test dùng fixture tổng hợp nhỏ chỉ để kiểm tra logic phần mềm, không phải dữ liệu thị trường. Đầu ra nghiên cứu conditional lấy từ Processed CafeF đang có.

## Nguồn và giới hạn

- Phạm vi: 43 ticker theo `src/data/universe.py`, 19/11/2021–18/11/2026.
- CafeF Processed: 53.385 dòng. 16 cờ OHLC, ngày vắng, Adjusted Close/corporate actions, unit và quyền lưu/hiển thị còn các hạn chế đã ghi trong `reports/BAO_CAO_TONG_KET_PHUONG_AN_DU_LIEU.md` và `reports/BAO_CAO_XAC_MINH_CO_SO_GIA.md`.
- Không ghép bộ F-Fin ngắn hạn; không gọi SSI API; không tự tạo hay yêu cầu credentials.
- Không đưa kết quả conditional lên website công khai nếu quyền hiển thị dữ liệu chưa được xác minh.
- Repository không chứa Raw/Processed, staging F-Fin, bảng/biểu đồ artifact dẫn xuất, PDF đề gốc hoặc dự án RAG tham khảo. Các tệp này bị loại khỏi Git vì điều khoản dữ liệu và quyền phân phối chưa được làm rõ. Sau khi clone, cần có bộ dữ liệu được phép sử dụng tại `data/processed/stock_data_processed.csv` mới xem được đầy đủ EDA và demo phân cụm.

## Tài liệu

- `PROJECT_CONTEXT.md`: phạm vi và nguyên tắc hiện hành.
- `PROJECT_PROGRESS.md`: tiến độ, giới hạn và công việc còn lại.
- `reports/BAO_CAO_HOAN_THIEN_DO_AN.md`: tổng kết vòng hoàn thiện hiện tại.
- `reports/SLIDE_THUYET_TRINH_ASM.pptx`: slide demo 12 trang; kết quả clustering được ghi rõ là conditional.
- PDF báo cáo conditional và các dữ liệu/artifacts dẫn xuất được giữ ngoài GitHub cho đến khi quyền chia sẻ dữ liệu được xác minh.
- `reports/BAO_CAO_THU_NGHIEM_PHAN_CUM_CO_DIEU_KIEN.md`: kết quả feature/model cụ thể.

