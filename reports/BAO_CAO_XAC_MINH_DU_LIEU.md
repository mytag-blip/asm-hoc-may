# BÁO CÁO XÁC MINH DỮ LIỆU

**Ngày:** 20/11/2026  
**Nguồn đối chiếu:** `DU_LIEU_CHUNG_KHOAN.zip` (CafeF), SHA-256 `680ca176811129eba6bf9a0b02c3bc827af5ba04e13fed47e0030daa55744729`; CSV Processed và báo cáo chất lượng Giai đoạn 1.

## 1. Phương pháp

- Đọc báo cáo chất lượng, workbook thống kê, CSV Processed và tài liệu trạng thái dự án.
- Với từng OHLC bị gắn cờ, mở đúng workbook, sheet `LichSuGia`, đối chiếu mã, ngày, Open/High/Low/Close và số dòng Excel theo provenance.
- Tính tỷ lệ Adjusted Close/Close theo mã và theo thời gian; các thay đổi lớn chỉ dùng làm điểm cần rà soát, không suy luận corporate action.
- Kiểm tra phép cộng hai trường khối lượng trên toàn Processed.
- Rà ngày thiếu bằng tập ngày có trong ít nhất một mã. Không có lịch HOSE độc lập trong bộ tài liệu hiện tại.

## 2. Xác minh 16 bản ghi OHLC

Cả **16/16 dòng** khớp nguyên giá trị với đúng dòng trong workbook nguồn CafeF. Bất nhất không phát sinh do hợp nhất hoặc chuẩn hóa. Đối chiếu này chỉ xác nhận nội dung file đã cung cấp, không xác nhận giá đúng với giao dịch thực tế.

| Quy tắc | Số dòng |
|---|---:|
| High < Open | 0 |
| High < Close | 8 |
| Low > Open | 1 |
| Low > Close | 7 |
| High < Low | 0 |
| Close ngoài [Low, High] | 15 |

Có 12/16 dòng tập trung vào 06–08/05/2025: 4 dòng ngày 06/05, 5 dòng ngày 07/05 và 3 dòng ngày 08/05. Bốn dòng còn lại là CMG 18/12/2023, DHG 08/12/2022, MCH 05/10/2022 và VGC 13/05/2025. DHG, FRT, REE có 2 dòng mỗi mã; 10 mã khác có 1 dòng mỗi mã. Danh sách giá trị và dòng nguồn có trong `BAO_CAO_CHAT_LUONG_DU_LIEU.md` và sheet `OHLC rà soát`.

**Kết luận:** giá trong Excel nguồn khớp với Processed. Chưa thể kết luận đó là lỗi nguồn, quy ước giá hay sai lệch so với giao dịch vì không có nguồn độc lập. Giữ nguyên, không tự sửa.

## 3. Adjusted Close

- Adjusted Close khác Close ở 46.296/53.385 dòng. Tỷ lệ chung min 0,2988; median 0,8148; max 1,0000.
- Median tỷ lệ theo mã dao động khoảng 0,451 (ANV) đến 1,000 (KBC, MSN). Mọi mã đều có max 1,000.
- Có 104 quan sát mà tỷ lệ thay đổi trên 5% so với phiên trước cùng mã. Đây chỉ là điểm cần điều tra, không xác định corporate action.
- File không mô tả công thức, sự kiện điều chỉnh hay xác nhận Open/High/Low cùng cơ sở với Adjusted Close.

**Kết luận:** chưa đủ bằng chứng dùng Adjusted Close như chuỗi đã điều chỉnh nhất quán. Không tính return trên cơ sở này và không trộn Adjusted Close với OHLC.

## 4. Volume và giá trị giao dịch

- `Volume = Matched Volume + Negotiated Volume` đúng trên toàn bộ Processed.
- Matched Volume không âm; Negotiated Volume không âm, gồm 36.794 giá trị bằng 0. Giá trị 0 được giữ nguyên, không coi là thiếu.
- Có 1.008 dòng bị gắn cờ volume lớn theo hàng rào Q3 + 3×IQR riêng từng mã. Đây là cờ rà soát, không xác nhận sai; không dòng nào bị xóa.
- Chưa có tài liệu xác nhận đơn vị của giá, Matched Value hoặc Negotiated Value; không tự gán đơn vị.

## 5. Rà soát ngày thiếu

So sánh với ngày xuất hiện ở ít nhất một mã, không phải lịch HOSE xác minh.

- **MCH:** 14 ngày: 15/04/2022; 01–02/08/2023; 02–06/12/2024; 17/03/2025; 18–24/12/2025. Không có bản ghi trong dữ liệu nguồn tương ứng. Chưa phân biệt được ngày nghỉ riêng/không giao dịch với thiếu dữ liệu.
- **VGC, VHC, VHM, VIC, VJC, VNM, VRE:** đều không có bản ghi ngày 14/08/2025 trong file nguồn tương ứng. Việc cùng thiếu ngày gợi ý cần rà xuất dữ liệu hoặc lịch thị trường, nhưng không đủ kết luận đó là ngày nghỉ hay thiếu dữ liệu.

Không nội suy hoặc tạo bản ghi cho các ngày này. Cần đối chiếu lịch HOSE và tình trạng giao dịch của mã từ nguồn có thể kiểm chứng.

## 6. Quyết định sử dụng theo trường

| Trường | Đánh giá | Điều kiện |
|---|---|---|
| Close | Có thể sử dụng sau khi xử lý | 15 dòng Close ngoài biên OHLC cần quyết định giữ/loại khỏi phép tính liên quan; xác minh đơn vị và ngoại lệ. Raw giữ nguyên. |
| Adjusted Close | Chưa đủ bằng chứng để sử dụng | Cần xác nhận công thức và cơ sở điều chỉnh từ CafeF; không ghép với OHLC hiện tại. |
| Open, High, Low | Có thể sử dụng sau khi xử lý | Rà 16 dòng vi phạm quan hệ OHLC; chưa xác nhận cơ sở điều chỉnh. |
| Volume | Có thể sử dụng | Công thức tổng đã xác nhận; rà cờ volume cao và xác minh quy ước đơn vị trước diễn giải. |
| Matched Value | Chưa đủ bằng chứng để sử dụng | Chưa xác minh đơn vị/thang số và định nghĩa. |
| Negotiated Value | Chưa đủ bằng chứng để sử dụng | Chưa xác minh đơn vị/thang số và định nghĩa. |

## 7. Vấn đề chưa thể xác minh

1. Tính đúng của 16 OHLC so với nguồn giao dịch độc lập.
2. Phương pháp Adjusted Close, corporate actions được áp dụng và việc OHLC có cùng basis hay không.
3. Đơn vị của giá và các trường giá trị giao dịch.
4. Lịch HOSE chính thức và lý do từng mã không có dữ liệu ở các ngày thiếu.
5. Ý nghĩa của các điểm volume cao; ngưỡng thống kê không xác nhận lỗi.

## 8. Bước tiếp theo đề xuất

Xin CafeF/người cung cấp xác nhận phương pháp Adjusted Close và đơn vị; nhóm quyết định cách xử lý từng ngoại lệ OHLC mà không sửa Raw; đối chiếu ngày thiếu với lịch HOSE và tình trạng giao dịch có dẫn nguồn. Chỉ sau khi chốt các vấn đề này mới thiết kế tập dữ liệu phân tích. Giai đoạn này chưa làm Feature Engineering hoặc Machine Learning.
