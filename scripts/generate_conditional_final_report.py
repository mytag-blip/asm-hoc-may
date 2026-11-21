"""Create a 10–15 page Vietnamese conditional project report from saved evidence."""
from __future__ import annotations

from pathlib import Path
import json
import pandas as pd
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import mm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, PageBreak,
                                Table, TableStyle, Image, KeepTogether)


ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "reports" / "BAO_CAO_TONG_KET_DO_AN_CONDITIONAL.pdf"
FONT_DIR = Path("C:/Windows/Fonts")


def register_fonts() -> tuple[str, str]:
    regular = FONT_DIR / "arial.ttf"
    bold = FONT_DIR / "arialbd.ttf"
    if regular.exists() and bold.exists():
        pdfmetrics.registerFont(TTFont("ArialASM", str(regular)))
        pdfmetrics.registerFont(TTFont("ArialASM-Bold", str(bold)))
        return "ArialASM", "ArialASM-Bold"
    return "Helvetica", "Helvetica-Bold"


def build() -> Path:
    regular, bold = register_fonts()
    output_dir = OUTPUT.parent
    output_dir.mkdir(parents=True, exist_ok=True)
    styles = getSampleStyleSheet()
    styles.add(ParagraphStyle(name="TitleVN", parent=styles["Title"], fontName=bold, fontSize=25, leading=33, textColor=colors.HexColor("#10233F"), alignment=TA_LEFT, spaceAfter=14))
    styles.add(ParagraphStyle(name="SubVN", parent=styles["Normal"], fontName=regular, fontSize=13, leading=20, textColor=colors.HexColor("#52657C"), spaceAfter=8))
    styles.add(ParagraphStyle(name="H1VN", parent=styles["Heading1"], fontName=bold, fontSize=17, leading=23, textColor=colors.HexColor("#10233F"), spaceBefore=2, spaceAfter=10))
    styles.add(ParagraphStyle(name="H2VN", parent=styles["Heading2"], fontName=bold, fontSize=12, leading=17, textColor=colors.HexColor("#087F8C"), spaceBefore=8, spaceAfter=5))
    styles.add(ParagraphStyle(name="BodyVN", parent=styles["BodyText"], fontName=regular, fontSize=9.4, leading=14.2, textColor=colors.HexColor("#202C3C"), spaceAfter=6))
    styles.add(ParagraphStyle(name="SmallVN", parent=styles["BodyText"], fontName=regular, fontSize=7.3, leading=10, textColor=colors.HexColor("#566579"), spaceAfter=3))
    styles.add(ParagraphStyle(name="CalloutVN", parent=styles["BodyText"], fontName=bold, fontSize=10, leading=15, textColor=colors.HexColor("#7B3F00"), backColor=colors.HexColor("#FFF3D6"), borderColor=colors.HexColor("#F1C56B"), borderWidth=.6, borderPadding=8, spaceBefore=6, spaceAfter=10))

    def P(text: str, style: str = "BodyVN") -> Paragraph:
        return Paragraph(text, styles[style])

    def bullet(text: str) -> Paragraph:
        return Paragraph("• " + text, styles["BodyVN"])

    def table(rows, widths=None, font=7.4):
        converted = [[P(str(cell), "SmallVN") for cell in row] for row in rows]
        tbl = Table(converted, colWidths=widths, repeatRows=1, hAlign="LEFT")
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#173D6D")),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("FONTNAME", (0, 0), (-1, 0), bold),
            ("GRID", (0, 0), (-1, -1), .35, colors.HexColor("#CBD5E1")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F1F5F9")]),
            ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
            ("LEFTPADDING", (0, 0), (-1, -1), 6), ("RIGHTPADDING", (0, 0), (-1, -1), 6),
            ("TOPPADDING", (0, 0), (-1, -1), 5), ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
        ]))
        return tbl

    story = []
    # 1. Cover
    story += [Spacer(1, 36*mm), P("BÁO CÁO TỔNG KẾT ĐỒ ÁN", "TitleVN"),
              P("Phân nhóm rủi ro biến động giá cổ phiếu của 43 doanh nghiệp HOSE bằng học máy không giám sát", "SubVN"),
              Spacer(1, 9*mm), P("BẢN DEMO NGHIÊN CỨU CÓ ĐIỀU KIỆN", "H1VN"),
              P("Các đặc trưng lợi suất và cụm được tính từ CafeF Processed để kiểm tra pipeline. Cơ sở giá, Corporate Actions, đơn vị Volume và quyền sử dụng dữ liệu chưa được xác minh đầy đủ; không xem các kết quả là mức rủi ro thực tế.", "CalloutVN"),
              Spacer(1, 45*mm), P("Đồ án Học Máy Cơ Bản · Ngày 20/11/2026", "SubVN"),
              PageBreak()]

    # 2. Executive summary
    story += [P("Tóm tắt điều hành", "H1VN"),
              P("Đồ án xây dựng ứng dụng Streamlit phục vụ phân nhóm 43 doanh nghiệp niêm yết HOSE theo đặc trưng biến động giá. Pipeline conditional đọc CafeF Processed, tạo feature cấp mã, scale và khảo sát K-Means, Agglomerative Ward, DBSCAN. Ứng dụng không thay đổi Raw/Processed và không ghép dữ liệu F-Fin vào chuỗi CafeF."),
              P("Kết quả kỹ thuật", "H2VN"), bullet("43 dòng đặc trưng; hai feature sets; hai scaler; 124 cấu hình phân cụm; 5.332 dòng gán cluster."),
              bullet("34/34 unit tests đạt; sáu trang AppTest không exception; Streamlit root và health endpoint trả HTTP 200."),
              bullet("Hash Raw và Processed giữ nguyên sau pipeline."),
              P("Kết luận nghiên cứu", "H2VN"),
              P("Chưa đủ căn cứ để kết luận cấp rủi ro. CafeF chưa công khai methodology Adjusted Close, cơ sở giá OHLC hoặc event ledger Corporate Actions; một số ngày thiếu và cờ OHLC chưa được xác minh độc lập. Metric clustering là chỉ số nội bộ không có nhãn chuẩn. Mọi kết quả trong báo cáo này phải được ghi là thăm dò có điều kiện."),
              P("Cách đọc báo cáo", "H2VN"),
              P("Các phần dữ liệu/mô hình mô tả kết quả runtime thực tế trên file Processed hiện có. Những nội dung về nguồn, đơn vị, quyền sử dụng chưa được kiểm chứng được ghi rõ là hạn chế, không nội suy hoặc suy đoán."), PageBreak()]

    # 3. Objective
    story += [P("1. Bài toán và phạm vi", "H1VN"),
              P("Tên đề tài hiện hành: Ứng dụng các thuật toán học máy không giám sát trong phân nhóm và đánh giá mức độ rủi ro của các doanh nghiệp niêm yết trên thị trường chứng khoán Việt Nam. Nhóm đã chốt 43 doanh nghiệp HOSE; rủi ro nghiên cứu là biến động giá, không phải rủi ro tài chính doanh nghiệp."),
              P("Đơn vị quan sát", "H2VN"),
              P("Mỗi mã cổ phiếu được tóm tắt thành một hàng feature trên toàn giai đoạn. Ticker là khóa tra cứu, không là biến đầu vào. Vì mục tiêu là phân cụm cross-sectional, không có nhãn mục tiêu và không dùng split train/test phân loại. Độ ổn định được khảo sát qua seed K-Means và thay đổi feature set/scaler; các metric không thay cho validation kinh tế."),
              P("Liên hệ với PDF ASM", "H2VN"),
              P("PDF yêu cầu quy trình dữ liệu, EDA, ít nhất ba đặc trưng, scaling, baseline và mô hình mở rộng; gợi ý K-Means nằm trong hướng phân cụm kết hợp supervised. Đề tài hiện hành tập trung unsupervised K-Means/Agglomerative/DBSCAN theo phạm vi nhóm; việc sai khác so với ví dụ K-Means + Random Forest/KNN cần được giảng viên xác nhận. Các sản phẩm PDF và slide phải bám rubric gốc."),
              PageBreak()]

    # 4. Data
    story += [P("2. Dữ liệu và nguồn", "H1VN"),
              P("Nguồn dùng trong pipeline: data/processed/stock_data_processed.csv, bộ CafeF đã hợp nhất từ 215 workbook. File gồm 53.385 dòng sau khi loại 86 dòng trùng hoàn toàn khỏi Processed; Raw còn 53.471 dòng."),
              table([["Thuộc tính", "Giá trị đã kiểm tra"],
                     ["Số mã", "43"], ["Khoảng quan sát", "19/11/2021–18/11/2026"],
                     ["Số ngày trong hợp ngày", "1.242"], ["Schema", "Date, Ticker, OHLC, Adjusted Close, Volume và provenance"],
                     ["Adjusted Close", "Có trong file; methodology chưa xác minh"]], [42*mm, 104*mm]),
              Spacer(1, 5*mm), P("Các nguồn khác", "H2VN"),
              P("F-Fin có dữ liệu tải thử thật cho năm mã nhưng chỉ 520 dòng/104 ngày/mã trong khoảng tháng 6 đến tháng 11/2026; không đủ thay thế 5 năm. SSI chưa có credentials/response thật; Vnstock/TCBS/Yahoo/FiinQuant/DataCedar chưa đạt điều kiện truy cập, coverage và quyền dùng. Không có nguồn nào được chọn chính thức thay CafeF."),
              P("Quyền dữ liệu", "H2VN"), P("Quyền lưu bản thô, sử dụng học thuật và hiển thị website đối với CafeF vẫn chưa có bằng chứng đủ trong hồ sơ. Dashboard chỉ là demo nội bộ; không nên phát hành công khai dữ liệu hoặc biểu đồ cho tới khi quyền được xác nhận."), PageBreak()]

    # 5. Quality
    story += [P("3. Chất lượng và giới hạn dữ liệu", "H1VN"),
              table([["Vấn đề", "Kết quả", "Tác động"],
                     ["Cờ OHLC", "16 dòng; khớp workbook CafeF gốc", "Chưa có feed độc lập; không dùng ATR/True Range"],
                     ["Ngày thiếu", "MCH thiếu 14 ngày theo hợp ngày; 7 mã thiếu 14/08/2025", "Không nội suy; chưa phân loại ngày nghỉ hay thiếu theo mã"],
                     ["Adjusted Close", "Khác Close ở 46.296/53.385 dòng theo báo cáo xác minh", "Không dùng tính return; công thức/back-adjust chưa biết"],
                     ["Corporate Actions", "Chưa có ledger đầy đủ 43 mã", "Return/Drawdown có thể chứa discontinuity kỹ thuật"],
                     ["Volume", "1.008 cờ Q3+3×IQR; tổng Matched + Negotiated khớp", "Unit/phạm vi giao dịch chưa rõ; không gọi là thanh khoản"],
                     ["Quyền dùng", "Chưa đủ bằng chứng lưu/hiển thị", "Hạn chế chia sẻ dữ liệu/demo công khai"]], [30*mm, 54*mm, 62*mm]),
              Spacer(1, 4*mm), P("Các cờ ngoại lai là tín hiệu kiểm tra thống kê, không tự chứng minh lỗi. 16 bản ghi OHLC vẫn được giữ nguyên. Các cột giá trị giao dịch cũng chưa được gán đơn vị vì thiếu tài liệu xác nhận."),
              PageBreak()]

    # 6. Feature engineering
    story += [P("4. Feature Engineering có điều kiện", "H1VN"),
              P("Chỉ Close được dùng làm cơ sở thử nghiệm; Adjusted Close không được ghép với OHLC. Trong từng ticker, dữ liệu được sắp theo Date. Return chỉ tính giữa hai ngày liên tiếp trong hợp ngày quan sát của dataset, không phải lịch HOSE chính thức."),
              table([["Feature", "Định nghĩa triển khai", "Giới hạn"],
                     ["Simple Return", "Close(t) / Close(t-1) − 1", "Conditional; không qua gap"],
                     ["Log Return", "ln(Close(t) / Close(t-1))", "Cùng giới hạn cơ sở giá"],
                     ["Rolling Volatility", "Std mẫu 20 return liên tục; ddof=1", "Reset ở gap; chưa xác minh Corporate Actions"],
                     ["Maximum Drawdown", "Tỷ lệ giảm từ đỉnh trên chuỗi tích lũy Close return", "Reset ở gap; toàn kỳ có thể lệch do sự kiện doanh nghiệp"],
                     ["Volume summaries", "Mean, CV, median biến động tương đối", "Mô tả activity; không kết luận thanh khoản"]], [34*mm, 65*mm, 47*mm]),
              Spacer(1, 4*mm), P("Không dùng Open/High/Low hoặc ATR vì basis OHLC chưa rõ và có 16 cờ quan hệ giá. Feature set giá cốt lõi gồm độ lệch chuẩn return, median/P95 rolling volatility và drawdown. Feature set sensitivity bổ sung CV Volume để kiểm tra mức phụ thuộc hoạt động khối lượng."), PageBreak()]

    # 7. Sensitivity
    story += [P("5. Phân tích độ nhạy", "H1VN"),
              P("Bản sensitivity không thay đổi dữ liệu nguồn. Một return bị loại khỏi bản tóm tắt độ nhạy nếu một trong hai đầu mút có Data_Quality_Flag hoặc độ lớn tuyệt đối return đạt ít nhất 10%. Mức 10% chỉ là ngưỡng rà soát; không gán nguyên nhân cho dữ liệu lỗi hay Corporate Action."),
              table([["Chỉ số", "Giá trị"], ["Cờ OHLC được đọc từ Processed", "16"], ["Return có |r| ≥ 10%", "72"], ["Return bị loại trong sensitivity (cộng cả cờ hai đầu mút)", "173"], ["Thay đổi tương đối tuyệt đối trung bình của std return", "5,9%"]], [105*mm, 41*mm]),
              Spacer(1, 6*mm), P("Diễn giải", "H2VN"),
              P("Việc feature thống kê thay đổi trung bình 5,9% cho thấy lựa chọn xử lý các quan sát nghi vấn có ảnh hưởng. Con số này không cho biết phương án nào đúng về mặt kinh tế; cần methodology nguồn và event ledger để phân loại."),
              PageBreak()]

    # 8. Algorithms
    story += [P("6. Thuật toán và đánh giá", "H1VN"),
              table([["Thuật toán", "Không gian tham số"],
                     ["K-Means", "k = 2–6; random_state=42; n_init=20"],
                     ["Agglomerative Ward", "k = 2–6; linkage=ward"],
                     ["DBSCAN", "eps ∈ {0,5; 0,75; 1; 1,25; 1,5; 2; 2,5}; min_samples ∈ {3,4,5}"]], [42*mm, 104*mm]),
              Spacer(1, 5*mm), P("Mỗi cấu hình thử StandardScaler và RobustScaler trên hai feature sets. Báo cáo Silhouette, Davies–Bouldin, Calinski–Harabasz, số cụm, tỷ lệ noise; chỉ tính metric khi còn ít nhất hai cụm và đủ mẫu sau khi bỏ noise. K-Means so seed 42 với 7, 21, 99 bằng Adjusted Rand Index."),
              P("Không chọn cấu hình theo một metric duy nhất. DBSCAN có thể đánh dấu nhiều điểm là noise; tỷ lệ coverage phải được đọc cùng Silhouette."), PageBreak()]

    # 9. Results
    metrics = pd.read_csv(ROOT / "artifacts" / "clustering" / "clustering_metrics.csv")
    eligible = metrics.dropna(subset=["Silhouette"])
    idx = eligible.groupby(["Feature_Set", "Algorithm"])['Silhouette'].idxmax()
    best = eligible.loc[idx]
    rows = [["Feature set", "Thuật toán", "Scaler", "Cụm", "Noise", "Silhouette", "DB", "CH"]]
    for row in best.itertuples(index=False):
        rows.append([row.Feature_Set, row.Algorithm, row.Scaler, str(row.N_Clusters), f"{row.Noise_Count} ({row.Noise_Fraction:.1%})", f"{row.Silhouette:.3f}", f"{row.Davies_Bouldin:.3f}", f"{row.Calinski_Harabasz:.2f}"])
    story += [P("7. Kết quả phân cụm thăm dò", "H1VN"),
              P("Tóm tắt cấu hình có Silhouette cao nhất trong từng thuật toán và feature set. Đây là lựa chọn để so sánh, không phải lựa chọn mô hình cuối."),
              table(rows, [28*mm, 24*mm, 21*mm, 10*mm, 20*mm, 17*mm, 13*mm, 14*mm]),
              Spacer(1, 5*mm),
              P("DBSCAN core: 33/43 mã là noise ở cấu hình đứng đầu; DBSCAN sensitivity: 34/43 noise. Silhouette được tính trên phần dữ liệu không-noise, do đó không đại diện cho toàn bộ mã. K-Means/Agglomerative trên feature giá + CV Volume tách MCH thành cluster một mã, thể hiện độ nhạy với Volume."),
              PageBreak()]

    # 10. Interpretation
    story += [P("8. Diễn giải cụm và kiểm soát kết luận", "H1VN"),
              P("Cluster IDs phụ thuộc thuật toán/tham số và có thể hoán vị giữa các lần chạy. Chúng không phải nhãn rủi ro. Chưa gán “thấp/trung bình/cao” vì: (1) cơ sở giá và Corporate Actions chưa rõ; (2) Volume unit/semantics chưa rõ; (3) DBSCAN có tỷ lệ noise lớn; (4) feature set Volume làm MCH tách singleton; (5) 43 doanh nghiệp là cỡ mẫu cross-sectional nhỏ."),
              P("Metric nội bộ đánh giá độ tách hình học trong feature space; không kiểm tra khả năng dự đoán, tính nhân quả, hiệu quả danh mục hay rủi ro đầu tư. Không có nhãn chuẩn để tính accuracy/F1/ROC-AUC."),
              P("PCA 2D trên trang web chỉ là cách chiếu dữ liệu đã scale để quan sát; PC1/PC2 không phải trục rủi ro."),
              P("Trước khi kết luận cần xác minh nguồn, chạy các feature trên basis được duyệt, kiểm tra ổn định theo thời kỳ và nhận phê duyệt của nhóm/giảng viên."), PageBreak()]

    # 11. App/test
    story += [P("9. Ứng dụng và kiểm thử", "H1VN"),
              table([["Trang", "Chức năng"],
                     ["Tổng quan", "Phạm vi, dữ liệu và trạng thái thử nghiệm"],
                     ["Quản lý dữ liệu", "Upload CSV/XLSX và trình duyệt Processed chỉ đọc có lọc"],
                     ["Chất lượng dữ liệu", "Missing/duplicate, OHLC flags, Volume flags"],
                     ["Phân tích dữ liệu", "EDA đã lưu, feature table và heatmap Pearson conditional"],
                     ["Machine Learning", "Feature matrix, sensitivity, 124 cấu hình và metric"],
                     ["Đánh giá rủi ro", "Tra cứu cluster profile, danh sách mã và PCA 2D"]], [37*mm, 109*mm]),
              Spacer(1, 5*mm),
              bullet("Compileall: đạt; 34/34 unittest đạt."), bullet("AppTest sáu trang và app.py không exception; đã tương tác chạy mô hình/tra hồ sơ."),
              bullet("Streamlit root và health endpoint trả HTTP 200."),
              bullet("Raw SHA-256: 1B492296E31DB393DA80A8D2579887BBECB4AFB95F4F3A9FF9CECCBFB5186043."),
              bullet("Processed SHA-256: 3574059045FBD420FC0EF473FCC6671C16C3A6BDC9F57478F02A7241598FE953."),
              PageBreak()]

    # 12. Conclusion
    story += [P("10. Hạn chế và bước tiếp theo", "H1VN"),
              P("Hạn chế chính", "H2VN"),
              bullet("Không có xác nhận chính thức phương pháp Adjusted Close, raw/adjusted OHLC, cách back-adjust và độ đầy đủ Corporate Actions."),
              bullet("Chưa phân loại các ngày thiếu theo phiên HOSE và tình trạng từng mã; 16 cờ OHLC chưa được đối chiếu với feed độc lập."),
              bullet("Đơn vị Volume/giá trị giao dịch và quyền lưu/chia sẻ/hiển thị dữ liệu chưa được xác minh."),
              bullet("Kết quả conditional không đủ để công bố mức rủi ro thực tế; phân cụm 43 mã có metric nội bộ nhưng chưa có validation kinh tế."),
              P("Bước tiếp theo", "H2VN"),
              P("Thu thập bằng chứng về price basis, corporate actions, units, ngày vắng và quyền sử dụng; xin quyết định nhóm/giảng viên. Sau khi được chấp thuận, cập nhật policy, chạy lại pipeline, so độ nhạy theo kỳ và chỉ diễn giải cụm khi hồ sơ đặc trưng hỗ trợ. Không thay đổi universe hoặc tự chọn nguồn dữ liệu."),
              P("Tài liệu tham khảo trong dự án", "H2VN"),
              P("[1] HỌC MÁY CƠ BẢN (2).pdf — đề ASM gốc và rubric. [2] reports/BAO_CAO_TONG_KET_PHUONG_AN_DU_LIEU.md. [3] reports/BAO_CAO_XAC_MINH_CO_SO_GIA.md. [4] reports/DE_XUAT_FEATURE_ENGINEERING_RUI_RO.md. [5] reports/BAO_CAO_THU_NGHIEM_PHAN_CUM_CO_DIEU_KIEN.md. [6] PROJECT_CONTEXT.md và PROJECT_PROGRESS.md.", "SmallVN"),
              P("Trạng thái bản báo cáo: kết quả conditional để demo kỹ thuật; chưa thay thế báo cáo kết luận khoa học sau xác minh dữ liệu.", "CalloutVN")]

    def page(canvas, doc):
        canvas.saveState()
        if doc.page > 1:
            canvas.setStrokeColor(colors.HexColor("#D5DEE9"))
            canvas.line(22*mm, 16*mm, 188*mm, 16*mm)
            canvas.setFont(regular, 8)
            canvas.setFillColor(colors.HexColor("#65758B"))
            canvas.drawString(22*mm, 10*mm, "ASM Học Máy Cơ Bản · Conditional research report")
            canvas.drawRightString(188*mm, 10*mm, f"Trang {doc.page}")
        canvas.restoreState()

    doc = SimpleDocTemplate(str(OUTPUT), pagesize=A4, rightMargin=22*mm, leftMargin=22*mm,
                            topMargin=19*mm, bottomMargin=23*mm, title="Báo cáo tổng kết đồ án conditional")
    doc.build(story, onFirstPage=page, onLaterPages=page)
    return OUTPUT


if __name__ == "__main__":
    print(build())
