# Báo cáo chất lượng dữ liệu chứng khoán 43 mã

**Ngày xử lý:** 20/11/2026  
**Nguồn đầu vào:** `DU_LIEU_CHUNG_KHOAN.zip`; tên file và sheet cho biết dữ liệu lịch sử CafeF, HOSE.  
**SHA-256 gói đầu vào:** `680ca176811129eba6bf9a0b02c3bc827af5ba04e13fed47e0030daa55744729`  
**Phạm vi:** 43 mã HOSE, dữ liệu từ 19/11/2021 đến 18/11/2026.

## 1. Kết quả đọc file

- Số file Excel trong ZIP: **215** (215 `.xlsx`, 0 `.xls`).
- Đọc thành công: **215**. Lỗi đọc/schema: **0**. File rỗng: **0**.
- Mỗi mã có **5 file**, tổng số mã: **43**.
- Tổng dòng nguồn trước xử lý: **53,471**.
- Tổng dòng Processed sau bỏ bản ghi trùng hoàn toàn: **53,385**.
- Dải ngày quan sát được: **2021-11-19 – 2026-11-18**.
- Ngày giao dịch duy nhất trong hợp các mã: **1,242**. Đây là lịch ngày suy ra từ dữ liệu, không phải lịch giao dịch HOSE độc lập.

## 2. Ánh xạ và chuẩn hóa

| Trường đích | Cột nguồn | Cách xử lý |
|---|---|---|
| Date | Ngày | Ngày dd/mm/yyyy → YYYY-MM-DD |
| Ticker | Mã | chuỗi mã viết hoa |
| Open | Giá mở cửa | số thực |
| High | Giá cao nhất | số thực |
| Low | Giá thấp nhất | số thực |
| Close | Giá đóng cửa | số thực |
| Adjusted Close | Giá điều chỉnh | số thực |
| Matched Volume | Khối lượng khớp lệnh | số nguyên |
| Matched Value | Giá trị khớp lệnh | số thực |
| Negotiated Volume | Khối lượng thỏa thuận | số nguyên |
| Negotiated Value | Giá trị thỏa thuận | số thực |
| Volume | Không có cột riêng | **Tính từ Matched Volume + Negotiated Volume**; cả hai thành phần được giữ riêng. |

Các file có thêm cột `Thay đổi`; cột này được giữ nguyên dạng chuỗi ở `Source_Change` trong Raw để tra cứu, không đưa vào schema phân tích chuẩn. Cả Raw và Processed giữ `Source_File`, `Source_Sheet`, `Source_Row`. Không ghi thay đổi vào ZIP gốc.

## 3. Trùng lặp và dữ liệu thiếu

- Thiếu ở 12 trường chuẩn trong Raw: **0 dòng**. Không có giá trị thiếu ở các cột dữ liệu nguồn bắt buộc; `Volume` được tính đủ từ hai cột khối lượng.
- Trùng khóa `Ticker + Date`: **86 nhóm**, có **86 dòng dư**.
- Cả **86 dòng dư** đều trùng hoàn toàn trên 12 trường chuẩn; **0** nhóm có giá trị OHLCV/Adjusted Close/giá trị giao dịch xung đột.
- Raw giữ đủ các dòng trùng. Processed giữ bản ghi đầu tiên theo thứ tự tên file/số dòng nguồn sau khi chứng minh các trường dữ liệu trùng nhau. Không loại dòng vì bất thường OHLC.

## 4. Kiểm tra OHLC

- `High < Low`: **0**.
- `High < Open`: **0**; `High < Close`: **8**.
- `Low > Open`: **1**; `Low > Close`: **7**.
- `Close` ngoài `[Low, High]`: **15** dòng.
- Bất nhất OHLC theo các quy tắc High phải ≥ Open/Close và Low phải ≤ Open/Close: **16 dòng**. Không có `High < Low`, giá thiếu, giá không dương.
- 16 trường hợp được giữ nguyên trong Raw và Processed, gắn cờ `Data_Quality_Flag`; chưa tự sửa giá.

| Mã | Ngày | Open | High | Low | Close | Cờ | File nguồn | Dòng Excel |
|---|---|---:|---:|---:|---:|---|---|---:|
| CMG | 2023-12-18 | 39 | 39.05 | 38.6 | 39.1 | HIGH_LT_CLOSE | CafeF_LichSuGia_HOSE_CMG_20231119-20241119.xlsx | 231 |
| DHG | 2022-12-08 | 84.5 | 86.6 | 84.7 | 85.9 | LOW_GT_OPEN | CafeF_LichSuGia_HOSE_DHG_20221119-20231119.xlsx | 237 |
| DHG | 2025-05-08 | 104 | 106.7 | 103.5 | 106.9 | HIGH_LT_CLOSE | CafeF_LichSuGia_HOSE_DHG_20241119-20251119.xlsx | 139 |
| DPM | 2025-05-06 | 34.1 | 34.4 | 33.55 | 33.5 | LOW_GT_CLOSE | CafeF_LichSuGia_HOSE_DPM_20241119-20251119.xlsx | 141 |
| FRT | 2025-05-07 | 171.4 | 173 | 170 | 173.2 | HIGH_LT_CLOSE | CafeF_LichSuGia_HOSE_FRT_20241119-20251119.xlsx | 140 |
| FRT | 2025-05-08 | 173.2 | 173.2 | 170.9 | 170.5 | LOW_GT_CLOSE | CafeF_LichSuGia_HOSE_FRT_20241119-20251119.xlsx | 139 |
| GMD | 2025-05-07 | 53.3 | 53.6 | 52.5 | 52 | LOW_GT_CLOSE | CafeF_LichSuGia_HOSE_GMD_20241119-20251119.xlsx | 140 |
| HAH | 2025-05-07 | 63.5 | 66.3 | 62.8 | 66.5 | HIGH_LT_CLOSE | CafeF_LichSuGia_HOSE_HAH_20241119-20251119.xlsx | 140 |
| HDG | 2025-05-07 | 23.9 | 24.45 | 23.9 | 24.5 | HIGH_LT_CLOSE | CafeF_LichSuGia_HOSE_HDG_20241119-20251119.xlsx | 140 |
| MCH | 2022-10-05 | 90.3 | 90.3 | 90.3 | 89.5 | LOW_GT_CLOSE | CafeF_LichSuGia_HOSE_MCH_20211119-20221119.xlsx | 34 |
| MWG | 2025-05-08 | 60.1 | 60.2 | 58.9 | 60.3 | HIGH_LT_CLOSE | CafeF_LichSuGia_HOSE_MWG_20241119-20251119.xlsx | 139 |
| NLG | 2025-05-06 | 29.05 | 29.3 | 28.8 | 28.7 | LOW_GT_CLOSE | CafeF_LichSuGia_HOSE_NLG_20241119-20251119.xlsx | 141 |
| PNJ | 2025-05-06 | 70.9 | 73.3 | 70.9 | 73.6 | HIGH_LT_CLOSE | CafeF_LichSuGia_HOSE_PNJ_20241119-20251119.xlsx | 141 |
| REE | 2025-05-06 | 70.9 | 70.9 | 69.9 | 69.7 | LOW_GT_CLOSE | CafeF_LichSuGia_HOSE_REE_20241119-20251119.xlsx | 141 |
| REE | 2025-05-07 | 69.7 | 71.1 | 69.6 | 69.5 | LOW_GT_CLOSE | CafeF_LichSuGia_HOSE_REE_20241119-20251119.xlsx | 140 |
| VGC | 2025-05-13 | 45 | 46.2 | 44.75 | 46.4 | HIGH_LT_CLOSE | CafeF_LichSuGia_HOSE_VGC_20241119-20251119.xlsx | 135 |

## 5. Khối lượng giao dịch

- `Matched Volume`: không âm; dòng âm **0**, số 0 **0**.
- `Negotiated Volume`: không âm; dòng âm **0**, số 0 **36,794**. Giá trị 0 có nghĩa là trường nguồn không ghi khối lượng thỏa thuận, không được coi là thiếu.
- `Volume` là tổng khớp lệnh + thỏa thuận. Min/median/P99/max: **26 / 2,177,500 / 32,746,647 / 216,259,100** cổ phiếu.
- Cờ xem xét khối lượng lớn dùng hàng rào riêng từng mã `Q3 + 3 × IQR`: **1,008 dòng**. Đây là dấu hiệu rà soát phân phối, không phải lỗi đã xác nhận và không có dòng nào bị loại.

## 6. Close và Adjusted Close

- Không thiếu/không dương: **0 / 0**.
- `Adjusted Close` khác `Close`: **46,296/53,385** dòng.
- Tỷ lệ `Adjusted Close / Close` có min **0.2988**, median **0.8148**, max **1.0000**.
- Hai cột giá rõ ràng không đồng nhất về giá trị. Tệp không kèm mô tả công thức điều chỉnh hoặc phạm vi corporate actions. Không thể xác nhận chính xác Open/High/Low có được điều chỉnh hay không chỉ từ bảng tính.
- Có thể tính daily return trên Adjusted Close nếu CafeF xác nhận chuỗi này đã điều chỉnh nhất quán qua corporate actions. Với bằng chứng hiện có, chưa nên coi đây là chuỗi lợi suất đã xác minh. Không trộn Adjusted Close với Open/High/Low trong cùng công thức hoặc đặc trưng. Giữ `Close` và `Adjusted Close` riêng cho đến khi chốt cơ sở giá.
- Tệp không ghi rõ đơn vị giá/giá trị giao dịch. Giữ nguyên quy mô số nguồn, không tự gắn đơn vị chưa xác minh. Volume là số cổ phiếu theo tên trường nguồn.

## 7. Độ phủ theo mã

| Mã | File | Dòng Raw | Dòng Processed | Phiên/ngày duy nhất | Ngày đầu | Ngày cuối | Dòng thiếu | Nhóm trùng khóa | Dòng bỏ trùng | OHLC bất nhất | Dòng khối lượng âm | Cờ KL cao | Ngày thiếu so với ngày chung | Khoảng ngày thiếu |
|---|---:|---:|---:|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---|
| ANV | 5 | 1244 | 1242 | 1242 | 2021-11-19 | 2026-11-18 | 0 | 2 | 2 | 0 | 0 | 26 | 0 | Không có theo lịch ngày chung trong dữ liệu |
| BCM | 5 | 1244 | 1242 | 1242 | 2021-11-19 | 2026-11-18 | 0 | 2 | 2 | 0 | 0 | 25 | 0 | Không có theo lịch ngày chung trong dữ liệu |
| CMG | 5 | 1244 | 1242 | 1242 | 2021-11-19 | 2026-11-18 | 0 | 2 | 2 | 1 | 0 | 49 | 0 | Không có theo lịch ngày chung trong dữ liệu |
| DBC | 5 | 1244 | 1242 | 1242 | 2021-11-19 | 2026-11-18 | 0 | 2 | 2 | 0 | 0 | 4 | 0 | Không có theo lịch ngày chung trong dữ liệu |
| DCM | 5 | 1244 | 1242 | 1242 | 2021-11-19 | 2026-11-18 | 0 | 2 | 2 | 0 | 0 | 7 | 0 | Không có theo lịch ngày chung trong dữ liệu |
| DGC | 5 | 1244 | 1242 | 1242 | 2021-11-19 | 2026-11-18 | 0 | 2 | 2 | 0 | 0 | 17 | 0 | Không có theo lịch ngày chung trong dữ liệu |
| DGW | 5 | 1244 | 1242 | 1242 | 2021-11-19 | 2026-11-18 | 0 | 2 | 2 | 0 | 0 | 21 | 0 | Không có theo lịch ngày chung trong dữ liệu |
| DHG | 5 | 1244 | 1242 | 1242 | 2021-11-19 | 2026-11-18 | 0 | 2 | 2 | 2 | 0 | 42 | 0 | Không có theo lịch ngày chung trong dữ liệu |
| DPM | 5 | 1244 | 1242 | 1242 | 2021-11-19 | 2026-11-18 | 0 | 2 | 2 | 1 | 0 | 19 | 0 | Không có theo lịch ngày chung trong dữ liệu |
| DXG | 5 | 1244 | 1242 | 1242 | 2021-11-19 | 2026-11-18 | 0 | 2 | 2 | 0 | 0 | 7 | 0 | Không có theo lịch ngày chung trong dữ liệu |
| FPT | 5 | 1244 | 1242 | 1242 | 2021-11-19 | 2026-11-18 | 0 | 2 | 2 | 0 | 0 | 9 | 0 | Không có theo lịch ngày chung trong dữ liệu |
| FRT | 5 | 1244 | 1242 | 1242 | 2021-11-19 | 2026-11-18 | 0 | 2 | 2 | 2 | 0 | 8 | 0 | Không có theo lịch ngày chung trong dữ liệu |
| GAS | 5 | 1244 | 1242 | 1242 | 2021-11-19 | 2026-11-18 | 0 | 2 | 2 | 0 | 0 | 48 | 0 | Không có theo lịch ngày chung trong dữ liệu |
| GEX | 5 | 1244 | 1242 | 1242 | 2021-11-19 | 2026-11-18 | 0 | 2 | 2 | 0 | 0 | 6 | 0 | Không có theo lịch ngày chung trong dữ liệu |
| GMD | 5 | 1244 | 1242 | 1242 | 2021-11-19 | 2026-11-18 | 0 | 2 | 2 | 1 | 0 | 13 | 0 | Không có theo lịch ngày chung trong dữ liệu |
| GVR | 5 | 1244 | 1242 | 1242 | 2021-11-19 | 2026-11-18 | 0 | 2 | 2 | 0 | 0 | 16 | 0 | Không có theo lịch ngày chung trong dữ liệu |
| HAH | 5 | 1244 | 1242 | 1242 | 2021-11-19 | 2026-11-18 | 0 | 2 | 2 | 1 | 0 | 17 | 0 | Không có theo lịch ngày chung trong dữ liệu |
| HDG | 5 | 1244 | 1242 | 1242 | 2021-11-19 | 2026-11-18 | 0 | 2 | 2 | 1 | 0 | 30 | 0 | Không có theo lịch ngày chung trong dữ liệu |
| HPG | 5 | 1244 | 1242 | 1242 | 2021-11-19 | 2026-11-18 | 0 | 2 | 2 | 0 | 0 | 36 | 0 | Không có theo lịch ngày chung trong dữ liệu |
| HSG | 5 | 1244 | 1242 | 1242 | 2021-11-19 | 2026-11-18 | 0 | 2 | 2 | 0 | 0 | 1 | 0 | Không có theo lịch ngày chung trong dữ liệu |
| HT1 | 5 | 1244 | 1242 | 1242 | 2021-11-19 | 2026-11-18 | 0 | 2 | 2 | 0 | 0 | 34 | 0 | Không có theo lịch ngày chung trong dữ liệu |
| HVN | 5 | 1244 | 1242 | 1242 | 2021-11-19 | 2026-11-18 | 0 | 2 | 2 | 0 | 0 | 23 | 0 | Không có theo lịch ngày chung trong dữ liệu |
| KBC | 5 | 1244 | 1242 | 1242 | 2021-11-19 | 2026-11-18 | 0 | 2 | 2 | 0 | 0 | 12 | 0 | Không có theo lịch ngày chung trong dữ liệu |
| KDH | 5 | 1244 | 1242 | 1242 | 2021-11-19 | 2026-11-18 | 0 | 2 | 2 | 0 | 0 | 18 | 0 | Không có theo lịch ngày chung trong dữ liệu |
| MCH | 5 | 1230 | 1228 | 1228 | 2021-11-19 | 2026-11-18 | 0 | 2 | 2 | 1 | 0 | 57 | 14 | 2022-04-15 đến 2022-04-15; 2023-08-01 đến 2023-08-02; 2024-12-02 đến 2024-12-06; 2025-03-17 đến 2025-03-17; 2025-12-18 đến 2025-12-24 |
| MSN | 5 | 1244 | 1242 | 1242 | 2021-11-19 | 2026-11-18 | 0 | 2 | 2 | 0 | 0 | 14 | 0 | Không có theo lịch ngày chung trong dữ liệu |
| MWG | 5 | 1244 | 1242 | 1242 | 2021-11-19 | 2026-11-18 | 0 | 2 | 2 | 1 | 0 | 2 | 0 | Không có theo lịch ngày chung trong dữ liệu |
| NKG | 5 | 1244 | 1242 | 1242 | 2021-11-19 | 2026-11-18 | 0 | 2 | 2 | 0 | 0 | 9 | 0 | Không có theo lịch ngày chung trong dữ liệu |
| NLG | 5 | 1244 | 1242 | 1242 | 2021-11-19 | 2026-11-18 | 0 | 2 | 2 | 1 | 0 | 12 | 0 | Không có theo lịch ngày chung trong dữ liệu |
| PDR | 5 | 1244 | 1242 | 1242 | 2021-11-19 | 2026-11-18 | 0 | 2 | 2 | 0 | 0 | 20 | 0 | Không có theo lịch ngày chung trong dữ liệu |
| PLX | 5 | 1244 | 1242 | 1242 | 2021-11-19 | 2026-11-18 | 0 | 2 | 2 | 0 | 0 | 57 | 0 | Không có theo lịch ngày chung trong dữ liệu |
| PNJ | 5 | 1244 | 1242 | 1242 | 2021-11-19 | 2026-11-18 | 0 | 2 | 2 | 1 | 0 | 77 | 0 | Không có theo lịch ngày chung trong dữ liệu |
| POW | 5 | 1244 | 1242 | 1242 | 2021-11-19 | 2026-11-18 | 0 | 2 | 2 | 0 | 0 | 17 | 0 | Không có theo lịch ngày chung trong dữ liệu |
| PVD | 5 | 1244 | 1242 | 1242 | 2021-11-19 | 2026-11-18 | 0 | 2 | 2 | 0 | 0 | 12 | 0 | Không có theo lịch ngày chung trong dữ liệu |
| REE | 5 | 1244 | 1242 | 1242 | 2021-11-19 | 2026-11-18 | 0 | 2 | 2 | 2 | 0 | 16 | 0 | Không có theo lịch ngày chung trong dữ liệu |
| SAB | 5 | 1244 | 1242 | 1242 | 2021-11-19 | 2026-11-18 | 0 | 2 | 2 | 0 | 0 | 26 | 0 | Không có theo lịch ngày chung trong dữ liệu |
| VGC | 5 | 1243 | 1241 | 1241 | 2021-11-19 | 2026-11-18 | 0 | 2 | 2 | 1 | 0 | 13 | 1 | 2025-08-14 đến 2025-08-14 |
| VHC | 5 | 1243 | 1241 | 1241 | 2021-11-19 | 2026-11-18 | 0 | 2 | 2 | 0 | 0 | 13 | 1 | 2025-08-14 đến 2025-08-14 |
| VHM | 5 | 1243 | 1241 | 1241 | 2021-11-19 | 2026-11-18 | 0 | 2 | 2 | 0 | 0 | 25 | 1 | 2025-08-14 đến 2025-08-14 |
| VIC | 5 | 1243 | 1241 | 1241 | 2021-11-19 | 2026-11-18 | 0 | 2 | 2 | 0 | 0 | 58 | 1 | 2025-08-14 đến 2025-08-14 |
| VJC | 5 | 1243 | 1241 | 1241 | 2021-11-19 | 2026-11-18 | 0 | 2 | 2 | 0 | 0 | 50 | 1 | 2025-08-14 đến 2025-08-14 |
| VNM | 5 | 1243 | 1241 | 1241 | 2021-11-19 | 2026-11-18 | 0 | 2 | 2 | 0 | 0 | 30 | 1 | 2025-08-14 đến 2025-08-14 |
| VRE | 5 | 1243 | 1241 | 1241 | 2021-11-19 | 2026-11-18 | 0 | 2 | 2 | 0 | 0 | 12 | 1 | 2025-08-14 đến 2025-08-14 |

Khoảng ngày thiếu ở bảng trên là các ngày có mặt trong ít nhất một mã khác nhưng mã này không có bản ghi. Đây chỉ là so sánh với lịch suy ra từ 43 mã, không kết luận ngày đó là phiên HOSE bị thiếu hay ngày mã bị đình chỉ. MCH thiếu 14 ngày trong hợp lịch; 7 mã VGC, VHC, VHM, VIC, VJC, VNM, VRE thiếu cùng ngày 14/08/2025. Cần đối chiếu với lịch sàn/sự kiện mã trước khi điền hoặc loại quan sát.

## 8. Đầu ra và đánh giá

- `data/raw/stock_data_raw.csv`: 53,471 dòng, giữ bản ghi trùng, giá bất nhất, cột thay đổi nguyên dạng và thông tin nguồn.
- `data/processed/stock_data_processed.csv`: 53,385 dòng; chuẩn hóa kiểu/tên, loại 86 dòng trùng hoàn toàn, giữ 16 OHLC bất nhất và gắn cờ.
- `reports/THONG_KE_43_CO_PHIEU.xlsx`: thống kê theo mã, danh sách bất nhất OHLC, ánh xạ trường và phương pháp xử lý.
- `reports/BAO_CAO_CHAT_LUONG_DU_LIEU.md`: báo cáo kiểm tra và quyết định xử lý.

**Đánh giá:** bộ dữ liệu đã hợp nhất và chuẩn hóa cấu trúc, nhưng **chưa đủ điều kiện dùng trực tiếp cho Feature Engineering**. Cần nhóm quyết định cách xử lý 16 bất nhất OHLC, xác minh đơn vị và phương pháp Adjusted Close, đồng thời rà soát 14 ngày thiếu của MCH và ngày 14/08/2025. Không nội suy hoặc sửa giá ở bước này.
