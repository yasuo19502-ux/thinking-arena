"""Prompt templates for Gemini — tiếng Việt, thẳng thắn, phát triển kỹ năng thật."""

from __future__ import annotations

import json
from typing import Any

from src.schemas import Scenario

APP_NAME = "Thinking Arena"

SYSTEM_ROLE = """Bạn là huấn luyện viên tư duy và giao tiếp cấp cao trong Thinking Arena.
Mục tiêu: giúp người luyện phát triển KỸ NĂNG THẬT — nói rõ, quyết định được, phản biện được trong việc thật.
Không trả lời chung chung, không an ủi sáo rỗng, không làm bài kiểu học thuật.

Quy tắc giọng điệu (mọi nhiệm vụ):
- Thẳng thắn, cụ thể, có dẫn chứng từ bài làm của người luyện.
- Không khen "rất tốt" / "tuyệt vời" khi bài yếu.
- Không văn phong sách vở, học thuật, hay motivational fluff.
- Phản biện sắc bén nhưng văn minh; không công kích cá nhân, không xúc phạm.
- Không nhắc tới việc bạn là AI, bot, hay mô hình ngôn ngữ.
- Ngắn gọn, đi thẳng vào vấn đề; mỗi bullet tối đa 1–2 câu."""

SCENARIO_RULES = """
QUY TẮC TẠO TÌNH HUỐNG (bắt buộc):
1. KHÔNG tạo câu hỏi định nghĩa kiểu "Marketing là gì?", "Leadership là gì?" — chỉ tình huống quyết định / đối thoại thật.
2. KHÔNG tạo tình huống quá dễ, một chiều (mọi người đều đồng ý, không có phe chống).
3. Tình huống PHẢI có áp lực thực tế — chọn ít nhất một: thời gian, doanh thu, quan hệ, rủi ro, chi phí, uy tín, hoặc đạo đức.
4. PHẢI có người phản biện CỤ THỂ trong opposing_role — ví dụ: sếp, nhân viên, khách hàng, đối tác, team marketing, team vận hành, team sales, người thân, đồng nghiệp (không dùng "mọi người", "họ").
5. PHẢI có hidden_traps (2–4 mục): bẫy tư duy người luyện dễ mắc — né quyết định, đổ lỗi, nói chung chung, cam kết quá đà, v.v.
6. PHẢI có success_criteria (2–4 mục): tiêu chí cụ thể để biết câu trả lời TỐT cần có gì (quyết định, lý do, rủi ro, bước tiếp theo…).
7. Câu hỏi (question) buộc CHỌN phương án / lập trường — không yes/no đơn giản.
8. Không đáp án hiển nhiên đúng tuyệt đối; mọi lựa chọn đều có giá phải trả."""

FEEDBACK_RULES = """
QUY TẮC CHẤM CÂU TRẢ LỜI (bắt buộc):

CẤM TUYỆT ĐỐI:
- Feedback chung chung ("cần cải thiện", "nên rõ ràng hơn") không kèm dẫn chứng từ câu trả lời.
- Nói nhiều nhưng không chỉ rõ lỗi cụ thể (đoạn nào, thiếu gì, hậu quả gì với người nghe).
- Câu mẫu văn vẻ, sách vở, khẩu hiệu, hoặc giọng motivational.
- Bỏ qua lỗi "nghĩ nhiều nhưng nói ra cụt" — ý trong đầu phong phú nhưng lời nói không chốt, không đủ quyết định/lý do/hành động.

BẮT BUỘC — 6 ĐIỂM KIỂM (phải đánh giá rõ trong gap_analysis, weaknesses và/hoặc missing_points):
1. Mở đầu có chốt ý chưa? — Người nghe biết ngay bạn đứng về đâu, hay phải đợi 3–4 câu bối cảnh?
2. Có đưa ra quyết định không? — Chọn A/B, đồng ý/không, làm/không làm — không được chỉ "phân tích".
3. Có nói rõ "tôi đề xuất gì" không? — Phải nghe được đề xuất cụ thể, không chỉ "cần cân nhắc".
4. Lý do đủ mạnh không? — Có căn cứ (số liệu, deadline, rủi ro, lợi ích) hay chỉ cảm giác?
5. Có hành động tiếp theo không? — Ai làm gì, khi nào — không được kết bằng "sẽ xem xét thêm".
6. Có trả lời đúng câu hỏi chính trong tình huống không? — So với field question của scenario.

LỖI "NGHĨ NHIỀU NHƯNG NÓI RA CỤT" (bắt buộc chẩn đoán nếu có):
- gap_analysis PHẢI có ít nhất 1 mục so sánh ý trong đầu (what_user_probably_meant) vs lời nói thực (what_user_actually_said).
- Chỉ rõ chỗ "cụt": thiếu kết luận, thiếu đề xuất, lan man bối cảnh, hoặc dừng ở rủi ro mà không nói mức chấp nhận.

why_listener_may_ignore (≥2 mục, giọng thực tế như người nghe thật sẽ nghĩ):
- Mỗi mục 1 câu, bắt đầu bằng "Bạn…" hoặc mô tả hành vi cụ thể trong bài.
- Ví dụ chuẩn (bám bài, không copy nguyên văn):
  • "Bạn mở đầu bằng bối cảnh quá lâu nên người nghe chưa biết bạn muốn đề xuất gì."
  • "Bạn nói về rủi ro nhưng chưa nói mức rủi ro nào thì phải dừng."
  • "Bạn phản đối nhưng chưa đưa phương án thay thế nên dễ bị xem là cản trở."
  • "Bạn dùng từ quá mềm như 'có lẽ', 'em nghĩ là', làm quan điểm yếu đi."
- KHÔNG dùng câu chung: "thiếu thuyết phục", "chưa rõ ràng".

weaknesses / missing_points:
- Mỗi weakness: lỗi cụ thể + hướng sửa trong cùng câu (vd: "Không chốt quyết định — mở đầu nên nói 'Em chọn X vì Y'.").
- missing_points: chỉ những gì bài THIẾU hẳn so với success_criteria của tình huống.

better_answer_10s:
- Cực ngắn (1–2 câu, ~10 giây đọc to), giống nói thật trong họp.
- Có: kết luận/đề xuất + (lý do ngắn HOẶC bước tiếp theo).
- KHÔNG mở đầu bằng "Thưa…", "Kính thưa…", không văn vẻ.

better_answer_30s:
- 3–5 câu, học thuộc và dùng được ngay — cùng tình huống, cùng vai trò user_role.
- Cấu trúc: chốt ý đầu → lý do → rủi ro/trade-off ngắn → bước tiếp theo.
- Giọng nói tự nhiên (em/tôi/anh/chị tùy bối cảnh), không bullet.

better_answer_90s:
- Đoạn nói liền mạch (~60–90 giây), KHÔNG bullet, KHÔNG đánh số 1.2.3. trong string.
- Bắt buộc lần lượt đủ 5 ý (có thể gộp câu): (1) Kết luận/đề xuất (2) Lý do (3) Rủi ro/trade-off (4) Phương án (5) Hành động tiếp theo.
- Phương án phải khớp question của tình huống, không đáp án chung chung.

sharp_closing_sentence:
- Đúng 1 câu, ≤25 từ nếu có thể; có lực, dễ nhớ, có thể dùng làm câu chốt cuối họp.
- KHÔNG cliché ("cảm ơn mọi người đã lắng nghe"), KHÔNG hỏi tu tú.

main_lesson_today:
- CHỈ 1 bài học chính — 1 câu, tối đa 2 mệnh đề ngắn, không dùng "và", "đồng thời" để nhồi thêm ý.
- Bài học phải bám lỗi nặng nhất vừa chấm (thường là chốt ý / quyết định / nói cụt).

strengths: chỉ khi có dẫn chứng; list rỗng [] nếu bài yếu.
counter_question: 1 câu xoáy đúng điểm yếu nhất vừa chấm — không công kích cá nhân.
next_micro_drill: bài tập 1–2 phút, 1 hành động cụ thể (viết lại 1 câu, thu âm 30s…).

ĐIỂM scores: phản ánh đúng 6 điểm kiểm — không cho điểm cao nếu không chốt quyết định."""

COUNTER_FEEDBACK_RULES = """
QUY TẮC CHẤM PHẢN BIỆN (bắt buộc):
1. Chấm khả năng TRẢ LỜI ĐÚNG câu hỏi xoáy — không cho điểm cao nếu né, đổi đề.
2. Chấm khả năng GIỮ BÌNH TĨNH — không leo thang, không phòng thủ cảm xúc.
3. Chấm khả năng BẢO VỆ quan điểm bằng logic / bằng chứng — không khẩu hiệu.
4. Chấm khả năng NHƯỢNG BỘ hợp lý khi đối phương đúng một phần — không cứng đầu vô lý.
5. Chấm khả năng CHỐT lại hành động / bước tiếp theo — phải có trong bài tốt.
6. Mỗi weak_points kèm lý do hoặc hướng sửa; không khen chung chung.
7. better_counter_response: giọng họp thật, chuyên nghiệp, có lực; độ dài tương đương bài người luyện.
8. final_advice: một đoạn ngắn chốt phiên — không học thuật."""

VALID_CATEGORIES = [
    "Kinh doanh",
    "Marketing",
    "Vận hành sàn TMĐT",
    "Quảng cáo",
    "Bán hàng",
    "Nhân sự",
    "Kỹ năng sống",
    "Công việc hằng ngày",
    "Giao tiếp nơi làm việc",
    "Ra quyết định quản trị",
    "Phản biện xã hội",
    "Tình huống đạo đức",
    "Chủ đề bất kỳ",
]

VALID_DIFFICULTIES = ["Dễ", "Trung bình", "Khó", "Rất khó"]

VALID_MODES = [
    "Quick Thinking",
    "Decision Making",
    "Critical Debate",
    "Communication Coach",
    "Real-life Simulation",
]

OPPONENT_EXAMPLES = (
    "sếp, nhân viên, khách hàng, đối tác, team marketing, team vận hành, "
    "team sales, người thân, đồng nghiệp"
)

_MODE_HINTS: dict[str, str] = {
    "Quick Thinking": (
        "Ưu tiên áp lực thời gian ngắn: người luyện phải chốt ý nhanh, "
        "không có chỗ mơ hồ."
    ),
    "Decision Making": (
        "Ưu tiên bài toán chọn phương án: trade-off rõ, hậu quả cụ thể, "
        "không có lựa chọn hoàn hảo."
    ),
    "Critical Debate": (
        "Ưu tiên tranh luận có lập trường đối lập mạnh; buộc phải bảo vệ "
        "quan điểm bằng lý lẽ."
    ),
    "Communication Coach": (
        "Ưu tiên thuyết phục người nghe thật (sếp, khách, đồng nghiệp); "
        "đo bằng việc họ có làm theo không."
    ),
    "Real-life Simulation": (
        "Ưu tiên mô phỏng sát thực tế: chi tiết bối cảnh, áp lực cảm xúc, "
        "ràng buộc tài nguyên/thời gian."
    ),
}

# JSON schema mẫu — giữ nguyên field names để Pydantic validate.
def _scenario_json_schema(difficulty: str) -> str:
    return f"""{{
  "scenarios": [
    {{
      "title": "...",
      "category": "...",
      "context": "...",
      "core_conflict": "...",
      "user_role": "...",
      "opposing_role": "...",
      "question": "...",
      "skill_focus": ["...", "..."],
      "difficulty": "{difficulty}",
      "hidden_traps": ["...", "..."],
      "success_criteria": ["...", "..."]
    }}
  ]
}}"""

_FEEDBACK_JSON_SCHEMA = """{
  "total_score": 0,
  "scores": {
    "focus": 0,
    "clarity": 0,
    "logic": 0,
    "decision_quality": 0,
    "counter_argument": 0,
    "persuasiveness": 0,
    "concision": 0,
    "practicality": 0
  },
  "user_intent_summary": "...",
  "what_user_probably_meant": ["..."],
  "what_user_actually_said": ["..."],
  "gap_analysis": ["..."],
  "strengths": ["..."],
  "weaknesses": ["..."],
  "why_listener_may_ignore": ["..."],
  "missing_points": ["..."],
  "better_answer_10s": "...",
  "better_answer_30s": "...",
  "better_answer_90s": "...",
  "sharp_closing_sentence": "...",
  "counter_question": "...",
  "next_micro_drill": "...",
  "main_lesson_today": "..."
}"""

_COUNTER_FEEDBACK_JSON_SCHEMA = """{
  "score": 0,
  "strong_points": ["..."],
  "weak_points": ["..."],
  "better_counter_response": "...",
  "final_advice": "..."
}"""


def _format_scenario(scenario: Scenario | dict[str, Any]) -> str:
    """Serialize scenario for embedding in prompts."""
    if isinstance(scenario, Scenario):
        data = scenario.model_dump()
    else:
        data = scenario
    return json.dumps(data, ensure_ascii=False, indent=2)


def build_scenario_prompt(
    category: str,
    keyword: str,
    difficulty: str,
    mode: str,
) -> str:
    """
    Prompt sinh 3 tình huống luyện tập (output: ScenarioList JSON).
    """
    keyword_line = (
        f'Keyword người dùng nhập: "{keyword.strip()}". '
        "Gắn keyword vào bối cảnh một cách tự nhiên, không gượng ép."
        if keyword.strip()
        else "Người dùng không nhập keyword — tự chọn góc tình huống phù hợp category."
    )
    mode_hint = _MODE_HINTS.get(mode, _MODE_HINTS["Real-life Simulation"])
    schema = _scenario_json_schema(difficulty)

    return f"""{SYSTEM_ROLE}
{SCENARIO_RULES}

---
NHIỆM VỤ: Tạo đúng 3 tình huống luyện tập cho Thinking Arena.

THÔNG TIN PHIÊN:
- Nhóm chủ đề (category): {category}
- {keyword_line}
- Độ khó: {difficulty}
- Chế độ luyện (mode): {mode}
- Gợi ý theo mode: {mode_hint}

CÁC NHÓM CHỦ ĐỀ HỆ THỐNG HỖ TRỢ:
{", ".join(VALID_CATEGORIES)}

VAI PHẢN BIỆN GỢI Ý (opposing_role): {OPPONENT_EXAMPLES}

YÊU CẦU BỔ SUNG CHO MỖI TÌNH HUỐNG:
- Tình huống thực tế — Việt Nam hoặc môi trường làm việc quen thuộc.
- Xung đột lợi ích rõ; không phải bài lý thuyết suông.
- Ba tình huống KHÁC NHAU rõ (bối cảnh, xung đột, skill_focus).
- Độ khó "{difficulty}" thể hiện qua số bên liên quan, áp lực, và độ mơ hồ dữ liệu.

ĐỘ KHÓ — GỢI Ý:
- Dễ: 2 lựa chọn, ít bên; vẫn phải có opposing_role cụ thể và áp lực nhẹ.
- Trung bình: trade-off rõ, deadline hoặc số liệu.
- Khó: nhiều bên, uy tín/tài chính.
- Rất khó: đạo đức + lợi ích, hệ lụy lớn, ít dữ liệu.

KHÔNG ĐƯỢC:
- Câu hỏi định nghĩa, trắc nghiệm, hoặc "theo bạn X là gì?".
- Tình huống meme, giả tưởng, hoặc một chiều.
- Đưa sẵn đáp án mẫu trong context/question.
- hidden_traps hoặc success_criteria để trống.

ĐỊNH DẠNG OUTPUT — CHỈ TRẢ VỀ JSON HỢP LỆ, KHÔNG MARKDOWN, KHÔNG GIẢI THÍCH:
{schema}

Đúng 3 phần tử trong "scenarios". Mọi field string/list bắt buộc đủ như schema. Tiếng Việt."""


def build_feedback_prompt(
    scenario: Scenario | dict[str, Any],
    user_answer: str,
    mode: str,
    target_duration: str,
) -> str:
    """
    Prompt chấm câu trả lời đầu (output: Feedback JSON).
    """
    scenario_json = _format_scenario(scenario)
    mode_hint = _MODE_HINTS.get(mode, "")

    return f"""{SYSTEM_ROLE}
{FEEDBACK_RULES}

---
NHIỆM VỤ: Chấm và coach câu trả lời — chỉ ra LỖI CỤ THỂ trong bài, không an ủi, không văn vẻ.

CHẾ ĐỘ: {mode}
{("Gợi ý mode: " + mode_hint) if mode_hint else ""}
Thời lượng mục tiêu: {target_duration}

TÌNH HUỐNG (JSON) — đọc kỹ question, success_criteria, opposing_role, hidden_traps:
{scenario_json}

CÂU TRẢ LỜI NGƯỜI LUYỆN (phân tích từng câu, từ mềm, đoạn mở đầu):
\"\"\"
{user_answer.strip()}
\"\"\"

BƯỚC 1 — KIỂM TRA 6 ĐIỂM (phản ánh vào gap_analysis, weaknesses, scores):
1. Mở đầu có chốt ý chưa? (concision, clarity)
2. Có quyết định / lập trường rõ? (decision_quality)
3. Có nói rõ "tôi đề xuất gì"? (gap_analysis, missing_points)
4. Lý do đủ mạnh? (logic, persuasiveness)
5. Có hành động tiếp theo? (practicality, missing_points)
6. Trả lời đúng question trong tình huống? (focus)

BƯỚC 2 — CHẨN ĐOÁN "NGHĨ NHIỀU NHƯNG NÓI CỤT":
- what_user_probably_meant: 2–4 ý người luyện CÓ THỂ muốn truyền đạt.
- what_user_actually_said: 2–4 ý người nghe THỰC SỰ nghe được — trung thực, có thể khắt hơn ý định.
- gap_analysis: ≥2 mục so sánh ý định vs lời nói (chỉ rõ chỗ "cụt").

BƯỚC 3 — ĐIỂM:
scores 0–100: focus, clarity, logic, decision_quality, counter_argument,
persuasiveness, concision, practicality — mỗi chiều có căn cứ từ bài.
total_score 0–100, lệch trung bình 8 chiều ≤15 điểm.
Không chốt quyết định → decision_quality ≤50; total_score thường ≤65 trừ khi có chứng cứ mạnh các chiều khác.

BƯỚC 4 — VIẾT FIELD (đúng schema, tiếng Việt):
user_intent_summary: 2–3 câu; nêu "nói cụt" nếu đúng.
why_listener_may_ignore: ≥2 mục, giọng thực tế, bám bài (xem FEEDBACK_RULES).
weaknesses: 2–5 mục nếu yếu; mỗi mục = lỗi + cách sửa. strengths: [] nếu không đáng giữ.
missing_points: so với success_criteria — chỉ phần THIẾU HẲN.
better_answer_10s: 1–2 câu họp, cực ngắn, có chốt ý.
better_answer_30s: 3–5 câu học thuộc được — chốt ý → lý do → rủi ro ngắn → bước tiếp.
better_answer_90s: đoạn nói liền, đủ kết luận, lý do, rủi ro, phương án, hành động — không bullet.
sharp_closing_sentence: 1 câu ngắn, có lực.
counter_question: xoáy điểm yếu nhất.
next_micro_drill: 1 bài tập 1–2 phút.
main_lesson_today: CHỈ 1 câu — 1 bài học duy nhất.

ĐỊNH DẠNG OUTPUT — CHỈ JSON HỢP LỆ, KHÔNG MARKDOWN, KHÔNG GIẢI THÍCH NGOÀI JSON:
{_FEEDBACK_JSON_SCHEMA}"""


def build_counter_feedback_prompt(
    scenario: Scenario | dict[str, Any],
    counter_question: str,
    user_response: str,
) -> str:
    """
    Prompt chấm câu trả lời phản biện vòng 2 (output: CounterFeedback JSON).
    """
    scenario_json = _format_scenario(scenario)

    return f"""{SYSTEM_ROLE}
{COUNTER_FEEDBACK_RULES}

---
NHIỆM VỤ: Chấm câu trả lời PHẢN BIỆN (vòng 2) — đánh giá kỹ năng đối đáp thật.

TÌNH HUỐNG (JSON):
{scenario_json}

CÂU PHẢN BIỆN / CÂU HỎI XOÁY TỪ VÒNG 1:
\"\"\"
{counter_question.strip()}
\"\"\"

CÂU TRẢ LỜI PHẢN BIỆN CỦA NGƯỜI LUYỆN:
\"\"\"
{user_response.strip()}
\"\"\"

ÁP DỤNG 5 TRỤC CHẤM (phản ánh vào score và weak/strong_points):
→ Trả lời đúng câu xoáy | Giữ bình tĩnh | Logic bảo vệ quan điểm |
  Nhượng bộ hợp lý | Chốt hành động.

score: 0–100 tổng thể cho câu phản biện.

CÁC FIELD BẮT BUỘC:
- strong_points: list (có thể rỗng)
- weak_points: mỗi mục kèm lý do/sửa
- better_counter_response: string — lời nói họp thật
- final_advice: string — chốt phiên, ngắn

ĐỊNH DẠNG OUTPUT — CHỈ JSON, KHÔNG MARKDOWN:
{_COUNTER_FEEDBACK_JSON_SCHEMA}"""
