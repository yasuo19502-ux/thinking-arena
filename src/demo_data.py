"""Dữ liệu demo cố định khi chưa có GEMINI_API_KEY."""

from __future__ import annotations

from src.schemas import CounterFeedback, Feedback, Scenario, ScenarioList, ScoreBreakdown


def get_demo_scenarios() -> list[dict]:
    """3 tình huống demo — validate qua Pydantic rồi trả dict."""
    data = ScenarioList(
        scenarios=[
            Scenario(
                title="Claim quảng cáo: mạnh hay an toàn?",
                category="Marketing",
                context=(
                    "Bạn là Marketing Manager. Team muốn chạy campaign với claim "
                    "'bán chạy nhất category' dựa trên số liệu nội bộ 2 tuần. "
                    "Legal và Brand lo claim vượt mức công bố so với đối thủ."
                ),
                core_conflict=(
                    "Tăng conversion trước mùa sale vs. rủi ro khiếu nại, phạt "
                    "nền tảng quảng cáo và mất uy tín thương hiệu."
                ),
                user_role="Marketing Manager",
                opposing_role="Trưởng phòng Legal / Brand",
                question=(
                    "Trong cuộc họp chiều nay, bạn chọn phương án nào và nói với "
                    "Legal thế nào để vừa không chậm campaign vừa giảm rủi ro?"
                ),
                skill_focus=["Ra quyết định", "Thuyết phục", "Quản lý rủi ro"],
                difficulty="Trung bình",
                hidden_traps=[
                    "Cam kết số liệu không kiểm chứng được",
                    "Đổ lỗi cho Legal làm chậm tiến độ",
                    "Nói chung chung 'team sẽ cẩn thận' không chốt phương án",
                ],
                success_criteria=[
                    "Chốt 1 phương án (claim đầy đủ / làm mềm / hoãn)",
                    "Nêu lý do và trade-off rõ",
                    "Đề xuất bước kiểm duyệt cụ thể với Legal",
                ],
            ),
            Scenario(
                title="Nhân viên giỏi nhưng trễ deadline",
                category="Nhân sự",
                context=(
                    "Bạn là team lead. Một senior làm output tốt nhưng 3 sprint liên "
                    "tiếp trễ deadline, ảnh hưởng release. HR nhắc cần xử lý công bằng."
                ),
                core_conflict=(
                    "Giữ người giỏi vs. gửi thông điệp sai cho cả team về kỷ luật "
                    "deadline và uy tín quản lý."
                ),
                user_role="Team lead",
                opposing_role="HR Business Partner",
                question=(
                    "Bạn sẽ nói gì với nhân viên đó trong 1-1 tuần này, và báo cáo "
                    "ngắn với HR như thế nào?"
                ),
                skill_focus=["Giao tiếp nơi làm việc", "Ra quyết định", "Quản lý con người"],
                difficulty="Trung bình",
                hidden_traps=[
                    "Chỉ nhắc thành tích, né hậu quả trễ hạn",
                    "Đe dọa sa thải ngay không có căn cứ quy trình",
                    "Hứa linh tinh không cam kết hành động theo dõi",
                ],
                success_criteria=[
                    "Chốt kỳ vọng deadline và hậu quả nếu lặp lại",
                    "Thể hiện công bằng, không cá nhân hóa",
                    "Có bước theo dõi tuần tới",
                ],
            ),
            Scenario(
                title="Traffic sàn sụt trước ngày sale",
                category="Vận hành sàn TMĐT",
                context=(
                    "Bạn phụ trách vận hành shop trên sàn. Traffic organic giảm ~40% "
                    "trong 5 ngày, còn 3 ngày tới mega sale. Ads đang hết ngân sách test."
                ),
                core_conflict=(
                    "Đốt ngân sách ads gấp vs. tối ưu listing/flash sale; team sales "
                    "ép cam kết doanh thu, sàn cảnh báo vi phạm nếu spike bất thường."
                ),
                user_role="Shop Operations Lead",
                opposing_role="Trưởng team Sales",
                question=(
                    "Họp khẩn sáng mai: bạn đề xuất kế hoạch 72 giờ nào và nói với "
                    "Sales thế nào để họ chốt mục tiêu thực tế?"
                ),
                skill_focus=["Ứng biến", "Ra quyết định", "Phối hợp liên phòng ban"],
                difficulty="Khó",
                hidden_traps=[
                    "Hứa doanh thu không có số liệu giả định",
                    "Đổ hết cho thuật toán sàn",
                    "Bỏ qua rủi ro vi phạm khi tăng ads đột ngột",
                ],
                success_criteria=[
                    "Chốt ưu tiên 72h (ads / listing / giá / kho)",
                    "Nêu rủi ro và điều kiện thành công",
                    "Thỏa thuận KPI với Sales có căn cứ",
                ],
            ),
        ]
    )
    return [s.model_dump() for s in data.scenarios]


def get_demo_feedback() -> dict:
    """Feedback mẫu — không phân tích câu trả lời thật của user."""
    return Feedback(
        total_score=62,
        scores=ScoreBreakdown(
            focus=65,
            clarity=60,
            logic=58,
            decision_quality=55,
            counter_argument=50,
            persuasiveness=58,
            concision=70,
            practicality=52,
        ),
        user_intent_summary=(
            "Bạn có vẻ muốn thuyết phục và giữ quan hệ, nhưng câu trả lời demo "
            "chưa thể hiện rõ điều đó vì đây là dữ liệu mẫu cố định."
        ),
        what_user_probably_meant=[
            "Muốn được nghe và có giải pháp khả thi",
            "Muốn tránh xung đột leo thang",
        ],
        what_user_actually_said=[
            "(Demo) Hệ thống không phân tích câu bạn vừa nhập — đây là khung mẫu",
            "Cần API key để AI đọc và chấm câu trả lời thật",
        ],
        gap_analysis=[
            "Ý định có vẻ là chọn phương án an toàn, nhưng bài demo không chốt 'em chọn X' — nghe như đang phân tích.",
            "Mở đầu thiếu đề xuất: người nghe phải đợi mới biết bạn muốn làm gì.",
            "Có nhắc rủi ro nhưng chưa nói mức rủi ro nào thì chấp nhận dừng campaign.",
        ],
        strengths=[],
        weaknesses=[
            "Không chốt quyết định — mở đầu nên nói 'Em chọn làm mềm claim vì rủi ro pháp lý'.",
            "Thiếu hành động tiếp theo — nên nói ai họp Legal, deadline T+2.",
        ],
        why_listener_may_ignore=[
            "Bạn mở đầu bằng bối cảnh quá lâu nên sếp chưa biết bạn muốn đề xuất gì.",
            "Bạn nói về rủi ro nhưng chưa nói mức rủi ro nào thì phải dừng quảng cáo.",
            "Bạn dùng từ mềm như 'có lẽ', 'em nghĩ là' — quan điểm nghe yếu, dễ bị gạt sang 'xem thêm'.",
        ],
        missing_points=[
            "Cam kết thời gian và người chịu trách nhiệm",
            "Phương án B nếu phương án A không được duyệt",
        ],
        better_answer_10s=(
            "Em chọn làm mềm claim, chấp nhận giảm CTR nhẹ — tuần này chốt với Legal."
        ),
        better_answer_30s=(
            "Em chọn làm mềm claim và giữ timeline campaign. Lý do: rủi ro pháp lý "
            "cao hơn lợi conversion thêm. Tuần này em làm việc Legal để duyệt bản "
            "công bố, đồng thời A/B headline an toàn hơn. Nếu chưa duyệt trước T+2, "
            "em hoãn push ads và báo lại số impact."
        ),
        better_answer_90s=(
            "Tóm lại em chọn phương án làm mềm claim vì rủi ro khiếu nại và phạt "
            "nền tảng lớn hơn benefit conversion ngắn hạn. Trade-off là có thể giảm "
            "CTR 5–10% nhưng giữ uy tín brand. Rủi ro nếu không làm: campaign dừng "
            "gấp giữa chừng. Bước tiếp: (1) họp Legal 24h tới chốt wording, "
            "(2) chuẩn bị 2 bản ads backup, (3) báo cáo Sales con số kỳ vọng thực tế. "
            "Em nhận trách nhiệm follow-up và update vào thứ Sáu."
        ),
        sharp_closing_sentence=(
            "Em chốt phương án an toàn, và T+2 em báo lại kết quả duyệt — không để "
            "campaign chạy mù rủi ro."
        ),
        counter_question=(
            "Nếu sếp bạn bảo 'cứ chạy claim mạnh, có sao đâu', bạn trả lời thế nào "
            "mà không làm mất uy tín với Legal?"
        ),
        next_micro_drill=(
            "Viết lại câu trả lời của bạn trong 4 câu: Quyết định — Lý do — Rủi ro — "
            "Bước tiếp theo."
        ),
        main_lesson_today="Mở đầu phải chốt đề xuất — đừng để người nghe đoán ý bạn.",
    ).model_dump()


def get_demo_counter_feedback() -> dict:
    return CounterFeedback(
        score=58,
        strong_points=["Giữ giọng chuyên nghiệp (giả định khi luyện tập)"],
        weak_points=[
            "Chưa trả lời thẳng câu xoáy — nên lặp lại ý 'tôi không chấp nhận rủi ro X'",
            "Thiếu chốt hành động sau phản biện",
        ],
        better_counter_response=(
            "Em hiểu áp lực doanh số, nhưng em không chấp nhận chạy claim chưa duyệt "
            "vì rủi ro phạt và dừng campaign là mất lớn hơn. Em đề xuất: duyệt bản "
            "an toàn trong 48h, song song chạy creative không claim tuyệt đối. "
            "Thứ Sáu em báo số thực tế — em chịu trách nhiệm phần vận hành."
        ),
        final_advice=(
            "Phản biện tốt = không né câu hỏi + giữ lập trường bằng logic + một "
            "bước hành động. Cấu hình API key để được chấm đúng câu bạn viết."
        ),
    ).model_dump()
