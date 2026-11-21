# PROJECT_CONTEXT

## Phạm vi hiện hành

**Đề tài:** Ứng dụng các thuật toán học máy không giám sát trong phân nhóm và đánh giá mức độ rủi ro biến động giá cổ phiếu của 43 doanh nghiệp niêm yết HOSE.

- Universe đúng theo `src/data/universe.py` (43 mã), không tự mở rộng.
- Bộ dữ liệu nghiên cứu có trong workspace là CafeF Processed, OHLCV/Volume và các trường provenance, 19/11/2021–18/11/2026.
- Mục tiêu là phân nhóm cross-sectional theo một hàng đặc trưng/mã, không phải Classification hay dự báo giá.
- Thuật toán: K-Means, Agglomerative/Hierarchical và DBSCAN.
- F-Fin chỉ là staging thử ngắn hạn; không ghép với CafeF. SSI adapter là mã chuẩn bị, chưa kết nối thật và không tiếp tục yêu cầu credentials.

## Trạng thái phương pháp và dữ liệu

- 53.471 dòng Raw; 53.385 dòng Processed; 43 mã. Raw và Processed phải được giữ nguyên.
- 16 cờ OHLC đã đối chiếu với workbook CafeF gốc, chưa xác minh với feed độc lập. MCH có 14 ngày thiếu theo hợp ngày quan sát; 7 mã thiếu ngày 14/08/2025 chưa được phân loại theo trạng thái từng mã.
- CafeF chưa công bố công thức Adjusted Close, cơ sở điều chỉnh OHLC hoặc đầy đủ phương pháp Corporate Actions. Quyền lưu trữ/hiển thị trên demo cũng chưa xác minh.
- Volume có quan hệ tổng đã kiểm tra và 1.008 cờ Q3+3×IQR; đơn vị/phạm vi dữ liệu chưa xác minh. Không gọi Volume là thanh khoản đã được xác nhận.
- Giai đoạn hoàn thiện hiện có pipeline **thăm dò có điều kiện**: Close (không Adjusted Close), chỉ return giữa ngày liền kề trong hợp lịch quan sát, rolling std 20 phiên, drawdown reset tại gap, cùng độ nhạy cờ OHLC/|return|≥10%. Không nội suy hoặc sửa nguồn.
- Kết quả conditional không phải ước lượng rủi ro thực tế đã xác minh; không đưa vào kết luận học thuật như ground truth. Chưa được nhóm/giảng viên xác nhận sử dụng như kết quả nghiên cứu chính thức.

## Kiến trúc hiện có

- Python, Streamlit, Pandas, NumPy, scikit-learn, Matplotlib, Seaborn, OpenPyXL.
- `src/data/`: importer, universe, quality, staging, provider SSI (fixture-tested only), read-only research loader.
- `src/features/risk_features.py`: tạo feature cấp ticker và bản độ nhạy có điều kiện.
- `src/models/clustering.py`: hai feature set, StandardScaler/RobustScaler, K-Means, Agglomerative, DBSCAN; metric nội bộ và độ ổn định K-Means.
- `src/reporting/experiment_report.py`: báo cáo Markdown và biểu đồ metric.
- `pages/`: 6 trang Streamlit; trang ML chạy thử nghiệm, trang cuối tra cứu hồ sơ/cấu hình.
- Output thử nghiệm nằm riêng trong `data/analysis/`, `artifacts/clustering/` và `reports/`; không ghi Raw/Processed.

## Quy tắc không được vi phạm

1. Không đổi đề tài, universe 43 HOSE hoặc nguồn dữ liệu chính thức khi chưa được nhóm/giảng viên chấp thuận.
2. Không tuyên bố basis CafeF/Adjusted Close/Corporate Actions/units đã xác minh.
3. Không sử dụng Adjusted Close trong return; không ghép Adjusted Close với OHLC.
4. Không nội suy ngày vắng, sửa/xóa cờ OHLC hay Volume lớn trong dữ liệu gốc.
5. Không gán Cluster ID thành mức rủi ro; chỉ diễn giải hồ sơ khi có bằng chứng và phê duyệt.
6. Không coi fixture tests là dữ liệu thị trường; không dùng nguồn/endpoint trái điều khoản.
7. Không đưa credentials vào mã nguồn, README, Git, log hoặc chat.
8. Không chỉnh sửa thư mục `rag_vietstock-main`.

## Chạy và kiểm tra

```powershell
Set-Location D:\ASM_Hoc_May
python -m pip install -r requirements.txt
python -m compileall -q app.py src pages tests scripts
python -m unittest discover -s tests -v
streamlit run app.py
```

Chạy pipeline conditional từ terminal: `python scripts/run_conditional_clustering.py`. Chỉ chạy khi đã hiểu cảnh báo dữ liệu; đầu ra có provenance/hash nguồn trong `artifacts/clustering/metadata.json`.

## Còn cần xác minh/duyệt

- Bằng chứng chính thức về CafeF price basis, adjusted methodology, Corporate Actions, units và quyền sử dụng/storing/demo.
- Phân loại chính thức ngày thiếu và độc lập kiểm tra 16 cờ OHLC.
- Quyết định nhóm/giảng viên có chấp nhận bản conditional để minh họa kỹ thuật hay yêu cầu có nguồn giá đã xác minh trước khi trình bày kết quả cụm.
- Yêu cầu sản phẩm cuối cùng của ASM áp dụng cho đề tài đã điều chỉnh (báo cáo, slide, demo); PDF gốc phải tiếp tục là nguồn rubric cao nhất.
