# BÁO CÁO XÁC MINH CƠ SỞ GIÁ CỔ PHIẾU

**Ngày truy cập nguồn:** 20/11/2026  
**Phạm vi đối chiếu:** Processed CafeF, 43 mã HOSE, 19/11/2021–18/11/2026. Đây là nghiên cứu tài liệu và đối chiếu giá hiển thị; không tính lợi suất/volatility và không hiệu chỉnh dữ liệu.

## 1. Tóm tắt kết luận

| Trường | Kết luận hiện tại | Phạm vi |
|---|---|---|
| Close | **Chỉ sử dụng có điều kiện** | Có thể mô tả giá đóng cửa theo từng mã. Chưa đủ căn cứ dùng làm chuỗi lợi suất/rủi ro qua corporate actions khi chưa xác nhận cách điều chỉnh và độ đầy đủ sự kiện. |
| Adjusted Close | **Chưa đủ bằng chứng để sử dụng** | CafeF hiển thị cột “Điều chỉnh”, và mẫu quanh một số sự kiện có diễn biến phù hợp với một chuỗi điều chỉnh. CafeF chưa công khai công thức, phạm vi sự kiện, thời điểm back-adjust hay quy tắc sửa dữ liệu lịch sử. |
| Open | **Chỉ sử dụng có điều kiện** | Dùng cho mô tả giá nguồn theo phiên; chưa được xác nhận điều chỉnh cùng basis với Adjusted Close. Không dùng tính ATR/range cho tới khi giải quyết basis và cờ OHLC. |
| High | **Chỉ sử dụng có điều kiện** | Như Open; còn có 8 trường hợp High < Close trong 16 cờ OHLC. Chưa dùng ATR. |
| Low | **Chỉ sử dụng có điều kiện** | Như Open; có 8 trường hợp Low > Open/Close (1 Low > Open, 7 Low > Close). Chưa dùng ATR. |

**Kết luận chính:** bằng chứng công khai đã tìm được không xác nhận công thức Adjusted Close của CafeF, các loại sự kiện được áp dụng đầy đủ, hoặc việc OHLC được điều chỉnh cùng cơ sở. Các quan sát quanh sự kiện FPT/NLG không thay thế tài liệu phương pháp. Do đó, chưa có chuỗi giá nào được xác nhận đủ để tính đặc trưng rủi ro xuyên corporate actions. Không tự suy ra hoặc áp dụng công thức điều chỉnh.

## 2. Nguồn CafeF đã kiểm tra

### 2.1 Trang lịch sử giao dịch và hướng dẫn

Trang lịch sử CafeF cho thấy các cột **Đóng cửa**, **Điều chỉnh**, **Mở cửa**, **Cao nhất**, **Thấp nhất**, dữ liệu khớp lệnh/thỏa thuận và chức năng xuất Excel. Trang cũng ghi dữ liệu có tính tham khảo và CafeF không chịu trách nhiệm về rủi ro sử dụng. Hướng dẫn CafeF mô tả dữ liệu lịch sử về giá/khối lượng, nhưng các trang đã tra cứu không đưa ra thuật toán tính “Điều chỉnh”.

- [CafeF — Lịch sử giao dịch](https://cafef.vn/du-lieu/lich-su-giao-dich-%7Bcode%7D-1.chn) — truy cập 20/11/2026.
- [CafeF — Hướng dẫn sử dụng dữ liệu](https://cafef.vn/du-lieu/huong-dan-su-dung.chn) — truy cập 20/11/2026.
- Trang lịch sử nêu xuất dữ liệu theo năm, tối đa khoảng một năm mỗi lượt xuất; điều này giải thích cách tải thành nhiều giai đoạn nhưng không chứng minh basis giá.

### 2.2 Những điều CafeF chưa công khai trong nguồn đã tra cứu

Chưa tìm thấy mô tả chính thức về:

- Công thức chính xác của Adjusted Close và cách xử lý làm tròn.
- Chuỗi điều chỉnh là điều chỉnh ngược toàn bộ lịch sử hay chỉ điều chỉnh quanh ngày quyền; điều chỉnh được cập nhật hồi tố đến thời điểm nào.
- Có xử lý cổ tức tiền mặt, cổ tức/cổ phiếu thưởng, chia/tách, quyền mua, phát hành khác, hủy/đính chính giao dịch hay không.
- Open/High/Low có được điều chỉnh cùng hệ số/thời điểm với Close hay vẫn là giá khớp giao dịch của phiên.
- Có thay đổi lịch sử sau khi xảy ra corporate action mới hay không; quy tắc đối với mã có nhiều loại quyền cùng một ngày.

Vì vậy, tên cột “Điều chỉnh” không đủ để kết luận đó là adjusted close theo một chuẩn cụ thể hay total-return series.

## 3. Đối chiếu sự kiện doanh nghiệp với dữ liệu mẫu

Các dòng được đọc trực tiếp từ Processed chỉ nhằm đối chiếu giá trị đã lưu quanh ngày sự kiện. Không tính return, hệ số điều chỉnh, hoặc biến đổi chuỗi.

| Mã/sự kiện | Bằng chứng sự kiện | CafeF quanh ngày trong Processed | Nhận xét giới hạn |
|---|---|---|---|
| FPT — cổ tức tiền mặt 2024 | Thông báo HOSE: ngày không hưởng quyền 12/06/2025, 1.000 đồng/cổ phiếu. [Thông báo HOSE](https://staticfile.hsx.vn/Uploads/UploadDocuments/2379533/20250606%20-%20FPT%20-%20TB%20ve%20ngay%20DKCC%20chi%20tra%20co%20tuc%20con%20lai%20nam%202024%20bang%20tien.pdf), truy cập 20/11/2026. | 11/06: Close 117,9 / Adjusted Close 90,22; 12/06: 117,0 / 90,30; 13/06: 115,4 / 89,06. | Close không có bước giảm lớn rõ ràng trong những ngày được liệt kê; điều đó không xác nhận hoặc bác bỏ adjustment. Các giá trị không cho biết hệ số/công thức. |
| FPT — phát hành tăng vốn từ vốn chủ sở hữu 20:3 | Thông báo HOSE: ngày không hưởng quyền 21/07/2025; 20 cổ phiếu nhận 3 cổ phiếu. [Thông báo HOSE](https://file.fpts.com.vn/FileStore2/File/2025/07/16/20250715_-_FPT_-_TB_ngay_DKCC_phat_hanh_CP_de_tang_von_tu_NV_CSH.pdf), truy cập 20/11/2026. | 18/07: Close 126,0 / Adjusted Close 97,24; 21/07: 110,3 / 97,89; 22/07: 112,1 / 99,49. | Adjusted Close thay đổi ít hơn Close quanh ngày quyền, phù hợp với khả năng có điều chỉnh; nhưng một ví dụ không chứng minh công thức, xử lý cổ tức tiền hoặc sự nhất quán toàn lịch sử. |
| FPT — kết hợp cổ tức tiền và thưởng cổ phiếu 12/06/2024 | Trang sự kiện CafeF ghi ngày 12/06/2024 có thưởng cổ phiếu 15% và cổ tức tiền 10%; danh sách sự kiện CafeF là nguồn tổng hợp, không thay thế thông báo gốc. [Trang thông tin FPT CafeF](https://cafef.vn/du-lieu/fpt/thong-tin-chung.chn), truy cập 20/11/2026. | 11/06: Close 146,5 / Adjusted Close 96,14; 12/06: 132,0 / 100,31; 13/06: 130,0 / 98,79. | Biến động của hai cột rất khác nhau quanh sự kiện; đây là dấu hiệu cần giải thích bằng tài liệu phương pháp, không phải bằng chứng đủ để tái tạo adjustment. Ngày sự kiện cần đối chiếu thông báo gốc nếu dùng làm case chính thức. |
| NLG — quyền mua 100:26, giá chào bán 25.000 đồng | Thông báo có mẫu biểu HOSE được lưu trữ: ngày không hưởng quyền 17/10/2025; 100:26. [Thông báo HOSE PDF](https://static2.vietstock.vn/vietstock/2025/10/14/20251013___nlg___tb_1883_ve_ndkcc_thuc_hien_quyen_mua_cp_phat_hanh_them.pdf), truy cập 20/11/2026. Báo cáo tài chính NLG nộp HOSE sau đó ghi đợt chào bán 100.022.079 cổ phiếu hoàn tất ngày 22/12/2025. [Báo cáo thường niên/BCTC NLG](https://static2.vietstock.vn/vietstock/2026/4/3/20260403___nlg___cbtt_bao_cao_thuong_nien_2025.pdf), truy cập 20/11/2026. | 16/10: Close 42,05 / Adjusted Close 37,80; 17/10: 38,65 / 37,92; 20/10: 35,95 / 35,27. | Chuỗi Adjusted Close ít biến động hơn ngay ở ngày quyền nhưng giảm sau đó; không thể suy ra cách CafeF xử lý quyền chưa thực hiện, giá phát hành, hoặc điều chỉnh tương lai. |

### 3.1 Cổ tức tiền, cổ tức cổ phiếu và quyền mua

Các hồ sơ HOSE/VSDC cung cấp ngày không hưởng quyền, tỷ lệ và mục đích của một số sự kiện. Các ví dụ trên xác nhận trong phạm vi mẫu có cổ tức tiền, phát hành cổ phiếu từ vốn chủ sở hữu và quyền mua. Sự kiện khác nhau có thể tác động khác nhau đến giá tham chiếu và số cổ phiếu; không thể gộp thành một hệ số điều chỉnh tự suy ra.

### 3.2 Chia tách cổ phiếu

Trong đối chiếu mẫu nêu trên, **chưa xác minh được một trường hợp chia tách cổ phiếu độc lập** (tách/gộp số cổ phiếu, tách biệt với cổ tức cổ phiếu/phát hành tăng vốn). Điều này không chứng minh không có sự kiện chia tách trong toàn bộ 43 mã hoặc ngoài mẫu. Cần tra thông báo doanh nghiệp/HOSE/VSDC theo từng mã và phân loại đúng bản chất sự kiện.

## 4. Khả năng OHLC cùng basis với Adjusted Close

- CafeF hiển thị Adjusted Close cạnh các trường Open/High/Low, nhưng giao diện cùng bảng không chứng minh các trường có chung basis.
- Trong FPT ngày quyền 21/07/2025, Close/Open/High/Low thể hiện mặt bằng giá phiên sau sự kiện trong khi Adjusted Close nằm ở mặt bằng chuỗi khác; đây là quan sát tương thích với cách lưu giá giao dịch chưa điều chỉnh cùng cột Close điều chỉnh, nhưng **không đủ căn cứ để khẳng định cơ chế đó**.
- 16 dòng vi phạm quan hệ OHLC đã được xác nhận khớp file CafeF; chưa có dữ liệu sàn độc lập. Các dòng này khiến ATR/True Range rủi ro hơn nhưng không tự chứng minh Close sai.

**Kết luận:** Open/High/Low chưa được xác nhận cùng basis với Adjusted Close. Không dùng chung chúng trong ATR hay bất kỳ công thức tổng hợp OHLC/adjusted-close nào trước khi có xác nhận.

## 5. Nguồn đối chiếu độc lập và khả năng thay thế

### Nguồn sự kiện chính thức

- **HOSE:** thông báo ngày không hưởng quyền, mục đích, tỷ lệ, giá phát hành/thông tin sự kiện; phù hợp xác nhận ngày và loại event. Không phải chuỗi Adjusted Close 5 năm trong các tài liệu đã tra.
- **VSDC:** thông báo quyền, đăng ký cuối cùng, tỷ lệ và lịch thực hiện; phù hợp đối chiếu corporate actions. Không tự nó xác nhận giá lịch sử đã điều chỉnh của CafeF.
- **Doanh nghiệp/IR và báo cáo tài chính đã kiểm toán:** có thể xác nhận quyết nghị và kết quả thực hiện; cần ghép với thông báo HOSE/VSDC để xác định ngày hiệu lực.

### Nguồn giá độc lập

- **SSI iBoard/SSI FastConnect** và **DNSE OpenAPI** là các nguồn/vendor tiềm năng đã khảo sát trước trong dự án; cần kiểm tra chính xác API/package hiện hành, quyền truy cập, điều khoản, và liệu trả về raw OHLCV hay adjusted OHLCV. Chưa gọi API trong Giai đoạn 2.6 và chưa xác minh hai nguồn này có chuỗi Adjusted Close lịch sử phù hợp.
- **Vnstock** là lớp thư viện truy cập các nguồn khác nhau, không phải nguồn gốc dữ liệu độc lập tự thân. Chỉ có giá trị đối chiếu sau khi xác định provider cụ thể và điều khoản.
- Nguồn dữ liệu thương mại thứ ba có thể dùng để đối chiếu chéo, nhưng cùng provider hoặc cùng feed upstream có thể không độc lập. Phải ghi provider gốc và timestamp/điều khoản.

**Đánh giá khả năng lấy từ nguồn chính thức:** HOSE/VSDC cung cấp bằng chứng về reference price và event details ở các thông báo cụ thể. Chưa tìm được bằng chứng trong tài liệu khảo sát rằng HOSE/VSDC phân phối một chuỗi daily adjusted OHLC đầy đủ 5 năm cho 43 mã kèm hệ số điều chỉnh lịch sử. Cần hỏi nhà cung cấp dữ liệu/HOSE/VSDC hoặc sử dụng API thương mại có hợp đồng/tài liệu rõ; không tự dựng adjusted series trong phạm vi này.

## 6. Phương án nghiên cứu nếu không xác minh được Adjusted Close

1. **Ưu tiên:** yêu cầu CafeF trả lời bằng văn bản data dictionary, methodology note hoặc ví dụ điều chỉnh cụ thể; giữ nguyên file và không hiệu chỉnh thủ công.
2. **Đối chiếu mẫu:** chọn các event HOSE/VSDC của nhiều loại trên, lấy raw OHLC từ một provider thứ hai có điều khoản phù hợp; so khớp raw prices, event dates và reference price. Việc provider thứ hai khớp không tự chứng minh Adjusted Close CafeF đúng.
3. **Nếu có chuỗi adjusted chính thức từ một provider khác:** nhóm/giảng viên quyết định có thay nguồn cho phần nghiên cứu hay không, ghi provenance và phương pháp. Không tự thay dữ liệu chính thức trong dự án.
4. **Nếu không thể có chuỗi giá nhất quán:** giới hạn nghiên cứu ở EDA giá Close trong từng mã và thảo luận chất lượng; hoãn/định nghĩa lại bài toán clustering rủi ro giá cùng giảng viên. Không tính Daily Return/Volatility từ chuỗi chưa xác minh và không tạo hệ số điều chỉnh nội bộ.

## 7. Những vấn đề còn chưa xác minh

1. Công thức CafeF Adjusted Close, loại corporate action áp dụng, back-adjustment và quy tắc cập nhật lịch sử.
2. OHLC có cùng basis với Adjusted Close hay là giá giao dịch chưa điều chỉnh.
3. Danh sách đầy đủ sự kiện corporate action cho cả 43 mã trong toàn kỳ, đặc biệt trường hợp chia tách thuần túy.
4. Đối chiếu raw price với feed giao dịch độc lập; FPT/NLG chỉ là các mẫu được xem xét.
5. Cách xử lý ngày có nhiều quyền đồng thời, quyền mua không thực hiện hết và các thay đổi sau ngày GDKHQ.
6. Tính phù hợp/điều khoản hiện hành của SSI/DNSE/Vnstock và liệu có chuỗi adjusted đáng tin cậy.

## 8. Khuyến nghị

- Tạm kết luận Close/Open/High/Low **chỉ dùng có điều kiện cho mô tả phiên theo từng mã**; chưa dùng để tính đặc trưng rủi ro xuyên corporate actions.
- Tạm kết luận Adjusted Close **chưa đủ bằng chứng để sử dụng cho lợi suất**. Mẫu FPT và NLG cho thấy khác biệt quanh sự kiện nhưng không xác minh công thức.
- Thu thập từ CafeF data dictionary/methodology bằng văn bản và lập event ledger chính thức HOSE/VSDC cho mẫu trước; sau đó mới đề xuất nhóm xác nhận bộ giá đầu vào.
- Không sửa Raw/Processed; không tính Daily Return/Volatility hoặc Feature Engineering trong Giai đoạn 2.6.

## 9. Nguồn đã tra cứu

| Nguồn | Nội dung dùng | Ngày truy cập |
|---|---|---|
| [CafeF — Lịch sử giao dịch](https://cafef.vn/du-lieu/lich-su-giao-dich-%7Bcode%7D-1.chn) | Tên trường, xuất Excel, tuyên bố tham khảo | 20/11/2026 |
| [CafeF — Hướng dẫn dữ liệu](https://cafef.vn/du-lieu/huong-dan-su-dung.chn) | Phạm vi dữ liệu lịch sử được giới thiệu | 20/11/2026 |
| [CafeF — Thông tin/sự kiện FPT](https://cafef.vn/du-lieu/fpt/thong-tin-chung.chn) | Danh sách sự kiện tổng hợp để định vị mẫu; không thay nguồn event chính thức | 20/11/2026 |
| [HOSE — FPT cash dividend notice](https://staticfile.hsx.vn/Uploads/UploadDocuments/2379533/20250606%20-%20FPT%20-%20TB%20ve%20ngay%20DKCC%20chi%20tra%20co%20tuc%20con%20lai%20nam%202024%20bang%20tien.pdf) | Ngày GDKHQ/tỷ lệ cổ tức tiền | 20/11/2026 |
| [HOSE — FPT stock issuance notice](https://file.fpts.com.vn/FileStore2/File/2025/07/16/20250715_-_FPT_-_TB_ngay_DKCC_phat_hanh_CP_de_tang_von_tu_NV_CSH.pdf) | Ngày GDKHQ/tỷ lệ 20:3 | 20/11/2026 |
| [HOSE — NLG rights issue notice](https://static2.vietstock.vn/vietstock/2025/10/14/20251013___nlg___tb_1883_ve_ndkcc_thuc_hien_quyen_mua_cp_phat_hanh_them.pdf) | Ngày GDKHQ/tỷ lệ/giá chào bán quyền mua | 20/11/2026 |
| [FPT — báo cáo tài chính kiểm toán nộp HOSE](https://staticfile.hsx.vn/Uploads/UploadDocuments/2445581/20260319%20-%20FPT%20-%20BCTC%20rieng%20nam%202025%20da%20kiem%20toan.pdf) | Kết quả phát hành/corporate action sau khi thực hiện | 20/11/2026 |
| [NLG — báo cáo thường niên nộp HOSE](https://static2.vietstock.vn/vietstock/2026/4/3/20260403___nlg___cbtt_bao_cao_thuong_nien_2025.pdf) | Ghi nhận thực hiện đợt chào bán năm 2025 | 20/11/2026 |
| [HOSE — quy định giao dịch, mã sự kiện](https://staticfile.hsx.vn/Uploads/UploadDocuments/2453338/HTGD_Quy%20dinh%20can%20biet%20khi%20GDCK%20tren%20HOSE_T2.2026.pdf) | Phân biệt mã ngày không hưởng cổ tức tiền/cổ phiếu/quyền mua | 20/11/2026 |

**Trạng thái Giai đoạn 2.6:** nghiên cứu tài liệu và đối chiếu mẫu hoàn tất trong giới hạn dữ liệu công khai. Cơ sở giá CafeF chưa được xác minh đủ để cho phép tính lợi suất/volatility. Chờ nhóm xem báo cáo và quyết định có yêu cầu CafeF cung cấp methodology hoặc cho phép kiểm tra provider độc lập ở bước tiếp theo.
