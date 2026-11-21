# Báo cáo kiểm tra bảo mật module SSI

**Ngày kiểm tra:** 20/11/2026  
**Phạm vi:** SSI adapter, probe, staging, environment files, ignore rules và test hiện có.  
**Kết luận:** Chưa tìm thấy SSI API key/secret/access token thật trong environment hoặc cấu hình dự án chính. Chưa gọi SSI API. Không thể xác minh Git index vì dự án chưa được khởi tạo Git.

## Kết quả kiểm tra

| Hạng mục | Kết quả |
| --- | --- |
| Hard-code SSI credentials | Không thấy giá trị SSI credentials thật trong source/config. Source chỉ đọc `SSI_API_KEY` và `SSI_API_SECRET` từ environment; các token trong tests là fixture giả. |
| File `.env` thực tế | Không tìm thấy trong `D:\ASM_Hoc_May`. Environment hiện tại không có `SSI_API_KEY`, `SSI_API_SECRET` hoặc `SSI_ACCESS_TOKEN` (chỉ kiểm tra có/không, không đọc giá trị). |
| `.env.example` | Có một file trong `rag_vietstock-main/rag_vietstock-main`. Đây là cấu hình mẫu của dự án tham khảo, không chứa SSI credentials; có giá trị đăng nhập phát triển mẫu cho PostgreSQL. Chưa xác minh giá trị mẫu có được dùng ở môi trường nào không. Không chỉnh sửa thư mục tham khảo trong lượt này. |
| `.gitignore` dự án chính | Bỏ `.env`, `.env.*` (trừ `.env.example`), `.streamlit/secrets.toml` và `data/staging/ssi/*` (trừ `.gitkeep`). |
| `.gitignore` dự án tham khảo | Bỏ `.env`, nhưng cho phép `.env.example`. |
| Git status | `D:\ASM_Hoc_May` và thư mục tham khảo đều không phải Git working tree. Không tự khởi tạo hoặc thay đổi repository. Vì vậy không thể xác minh file nào đang tracked hoặc đã commit. |
| Log và lỗi | Adapter không ghi header Authorization, access token, request body hoặc response body vào log/error; lỗi HTTP chỉ trả status, transport lỗi chỉ trả loại exception. Unit test dùng secret giả và xác nhận response body có secret không xuất hiện trong lỗi. |
| Ticker ngoài allowlist | argparse và `run()` đều giới hạn đúng một ticker trong FPT/NLG/HPG/VNM/VIC. Gọi trực tiếp `run("ACB",...)` cũng bị từ chối trước khi tạo client hoặc ghi staging. |
| Read-only | Authentication dùng POST tới token endpoint; truy vấn OHLC dùng GET. Không có endpoint hoặc hàm đặt lệnh mua/bán/giao dịch trong adapter/probe. |
| Raw/Processed | `StagingStore` chỉ ghi `data/staging/ssi/`; unit test xác nhận staging không tạo/ghi Raw hoặc Processed. SHA-256 các CSV nghiên cứu giữ nguyên. |

## Vấn đề phát hiện

1. **Không thể xác nhận Git tracking:** project chưa có Git repository, do đó các quy tắc `.gitignore` mới chỉ là cấu hình; không thể kết luận file không nằm trong index/commit cũ.
2. **File mẫu trong dự án tham khảo:** `.env.example` chứa thông tin đăng nhập phát triển mặc định cho PostgreSQL. Không có bằng chứng đó là credential đang hoạt động và không phải SSI credential; tuy nhiên, trước khi chia sẻ hoặc triển khai dự án tham khảo, nhóm nên thay các giá trị này bằng placeholder không dùng được. File không được chỉnh sửa trong đợt audit này.
3. **Staging hiện là dữ liệu local:** `.gitignore` ngăn commit mới khi repository được khởi tạo, nhưng sau khi khởi tạo Git cần chạy kiểm tra ignore/tracked-file trước khi commit.

## Kiểm thử

- `python -m compileall -q app.py src pages tests scripts`: đạt.
- `python -m unittest discover -s tests -v`: **28/28 đạt**.
- `python scripts/ssi_probe.py --help`: đạt.
- `python scripts/ssi_probe.py --ticker ACB`: bị từ chối trước client/network.
- Không gọi SSI API thật; không credentials nào được tạo hoặc yêu cầu cung cấp.
- Raw SHA-256: `1B492296E31DB393DA80A8D2579887BBECB4AFB95F4F3A9FF9CECCBFB5186043`.
- Processed SHA-256: `3574059045FBD420FC0EF473FCC6671C16C3A6BDC9F57478F02A7241598FE953`.

## Kết luận bảo mật

SSI module hiện không có SSI credential hard-code được phát hiện; credential được đọc từ environment và không ghi vào log/manifest. Probe bị khóa ở 5 mã được phép, chỉ truy vấn OHLC, và ghi dữ liệu vào staging tách biệt. Trạng thái Git chưa thể xác nhận vì chưa có repository. File `.env.example` của dự án RAG là cấu hình phát triển mẫu riêng, không phải credentials SSI; cần xử lý riêng nếu chuẩn bị phân phối dự án tham khảo.
