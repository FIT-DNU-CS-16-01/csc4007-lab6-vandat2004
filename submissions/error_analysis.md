# BÁO CÁO PHÂN TÍCH LỖI – LAB 6 CINESENSE PROMPT EVALUATION

## 1. Định nghĩa bài toán

Trong bài Lab 6, mục tiêu là sử dụng mô hình ngôn ngữ lớn (LLM) để thực hiện bài toán phân tích cảm xúc (Sentiment Analysis) đối với các bài đánh giá phim.

Đầu vào của hệ thống là một đoạn review phim bằng tiếng Anh.

Đầu ra bao gồm:

* Nhãn cảm xúc (positive hoặc negative).
* Giải thích ngắn gọn cho dự đoán.
* Các cụm từ trong review làm bằng chứng (evidence phrases).

Ngoài ra, Prompt v2 và Prompt v3 CoT còn mở rộng thêm khả năng phân tích aspect, confidence và các thông tin hỗ trợ khác.

Ba phiên bản prompt được xây dựng nhằm đánh giá mức độ ảnh hưởng của thiết kế prompt đến chất lượng đầu ra của mô hình.

---

# 2. Mô tả tập dữ liệu

Nhóm sử dụng tập dữ liệu tự xây dựng gồm 30 movie reviews.

Đặc điểm của tập dữ liệu:

* 25 review mang cảm xúc tích cực (positive).
* 5 review mang cảm xúc tiêu cực (negative).
* Bao gồm nhiều dạng review:

  * Easy review.
  * Mixed review.
  * Ambiguous review.
  * Keyword trap.
  * Long review.

Toàn bộ ba prompt đều được đánh giá trên cùng một tập dữ liệu nhằm đảm bảo tính công bằng khi so sánh.

---

# 3. Prompt v1

Prompt v1 là phiên bản cơ bản.

Đặc điểm:

* Chỉ yêu cầu mô hình xác định sentiment.
* Trả về JSON đơn giản.
* Có giải thích ngắn và evidence phrases.

Ưu điểm:

* Prompt ngắn gọn.
* Dễ hiểu.
* JSON ổn định.
* Ít lỗi định dạng.

Nhược điểm:

* Chưa phân tích aspect.
* Chưa đánh giá confidence.
* Chưa có cơ chế kiểm tra reasoning.

---

# 4. Prompt v2

Prompt v2 mở rộng từ Prompt v1.

Các cải tiến:

* Bổ sung aspect extraction.
* Thêm polarity cho từng aspect.
* Thêm confidence.
* Quy định JSON nghiêm ngặt hơn.
* Nhấn mạnh việc chỉ sử dụng evidence có trong review.

Ưu điểm:

* Đầu ra giàu thông tin hơn.
* Có thể phục vụ các tác vụ phân tích chi tiết.

Nhược điểm:

* JSON phức tạp hơn.
* Dễ phát sinh lỗi định dạng hơn Prompt v1.
* Đôi khi mô hình bỏ sót một số aspect.

---

# 5. Prompt v3 (CoT-inspired)

Prompt v3 áp dụng ý tưởng Chain-of-Thought (CoT).

Mô hình được yêu cầu:

1. Xác định các dấu hiệu tích cực.
2. Xác định các dấu hiệu tiêu cực.
3. Cân nhắc toàn bộ review.
4. Sau đó mới xuất JSON cuối cùng.

Lưu ý rằng mô hình chỉ trả về JSON, không xuất reasoning dài.

Ưu điểm:

* Đầu ra rõ ràng hơn.
* Evidence đầy đủ hơn.
* Hạn chế suy diễn ngoài review.
* Khả năng xử lý mixed review tốt hơn.

Nhược điểm:

* Prompt dài hơn.
* Chi phí token cao hơn.
* Thời gian xử lý lâu hơn.

---

# 6. So sánh định lượng

Dựa trên kết quả đánh giá thu được, ba prompt đều đạt độ chính xác cao trên tập dữ liệu thử nghiệm.

| Metric             | Prompt v1 | Prompt v2 | Prompt v3 CoT |
| ------------------ | --------- | --------- | ------------- |
| Accuracy           | 100%      | 100%      | 100%          |
| Valid JSON Rate    | 100%      | 100%      | 100%          |
| Evidence Exactness | 100%      | 100%      | 100%          |
| Hallucination      | 0         | 0         | 0             |
| Outside Knowledge  | 0         | 0         | 0             |

Kết quả cho thấy cả ba prompt đều hoạt động tốt trên bộ dữ liệu đã xây dựng.

Prompt v2 và Prompt v3 tạo ra đầu ra giàu thông tin hơn Prompt v1, trong khi vẫn duy trì độ chính xác cao.

---

# 7. Phân tích Error Bucket

Trong quá trình đánh giá, không phát hiện lỗi nghiêm trọng trên tập dữ liệu hiện tại.

| Error Bucket           | Count v1 | Count v2 | Count v3 |
| ---------------------- | -------- | -------- | -------- |
| wrong_sentiment        | 0        | 0        | 0        |
| invalid_json           | 0        | 0        | 0        |
| hallucinated_evidence  | 0        | 0        | 0        |
| outside_knowledge      | 0        | 0        | 0        |
| missed_positive_aspect | 0        | 0        | 0        |
| missed_negative_aspect | 0        | 0        | 0        |
| wrong_aspect_polarity  | 0        | 0        | 0        |
| keyword_trap           | 0        | 0        | 0        |
| mixed_review_failure   | 0        | 0        | 0        |
| overconfident          | 0        | 0        | 0        |
| cot_not_helpful        | 0        | 0        | 0        |

Điều này cho thấy prompt được thiết kế tương đối phù hợp với tập dữ liệu sử dụng.

---

# 8. Ba ví dụ tiêu biểu

## Ví dụ 1

**Review ID:** R004

Review:

> The plot is predictable, yet the warm characters and sharp dialogue kept me engaged.

Đây là một mixed review.

Mặc dù review có ý chê phần cốt truyện ("predictable"), mô hình vẫn xác định đúng cảm xúc tổng thể là **positive**, đồng thời chỉ ra các evidence phù hợp.

---

## Ví dụ 2

**Review ID:** R017

Review:

> Although the middle section drags, the film recovers with a satisfying final act.

Review vừa có điểm tích cực vừa có điểm tiêu cực.

Prompt v3 CoT đã xác định riêng positive clues và negative clues trước khi đưa ra kết luận cuối cùng, giúp giải thích rõ hơn so với Prompt v1.

---

## Ví dụ 3

**Review ID:** R028

Đây là một review mang cảm xúc tiêu cực.

Cả ba prompt đều dự đoán đúng nhãn negative và không bổ sung bất kỳ thông tin nào ngoài nội dung review.

Điều này cho thấy mô hình không xảy ra hiện tượng hallucination.

---

# 9. Đánh giá tác động của CoT

Chain-of-Thought không làm thay đổi Accuracy trên bộ dữ liệu hiện tại vì cả ba prompt đều đạt kết quả chính xác.

Tuy nhiên, Prompt v3 CoT tạo ra quá trình phân tích rõ ràng hơn.

Các ưu điểm quan sát được:

* Tách positive clues và negative clues.
* Giải thích quyết định tốt hơn.
* Evidence đầy đủ hơn.
* Hạn chế suy diễn ngoài review.

Do đó, mặc dù Accuracy không tăng, Prompt v3 vẫn có giá trị trong việc nâng cao khả năng giải thích (Explainability) của hệ thống.

---

# 10. Kết luận

Qua quá trình xây dựng và đánh giá ba phiên bản prompt, có thể thấy thiết kế prompt ảnh hưởng đáng kể đến chất lượng đầu ra của mô hình.

Prompt v1 đơn giản, ổn định và phù hợp với các bài toán sentiment cơ bản.

Prompt v2 mở rộng khả năng phân tích aspect và confidence, giúp đầu ra giàu thông tin hơn.

Prompt v3 CoT mang lại khả năng giải thích tốt nhất, trình bày quá trình suy luận rõ ràng hơn và vẫn duy trì độ chính xác cao.

Trong phạm vi bộ dữ liệu của bài thực hành, Prompt v3 CoT được xem là lựa chọn phù hợp nhất nhờ cân bằng giữa độ chính xác, tính đầy đủ của thông tin và khả năng giải thích kết quả.
