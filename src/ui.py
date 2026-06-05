"""Streamlit UI helpers and page renderers — mobile-first."""

from __future__ import annotations

import html
import json
from typing import Any, Literal

import streamlit as st
import streamlit.components.v1 as components

from src.demo_data import (
    get_demo_counter_feedback,
    get_demo_feedback,
    get_demo_scenarios,
)
from src.gemini_client import (
    GeminiConfigError,
    GeminiResponseError,
    get_client,
    has_api_key,
)
from src.prompts import (
    APP_NAME,
    VALID_CATEGORIES,
    VALID_DIFFICULTIES,
    VALID_MODES,
)
from src.styles import CUSTOM_CSS
from src.utils import generate_markdown_summary, reset_session

InfoVariant = Literal["info", "success", "warning", "neutral"]

SKILLS = [
    "Giải quyết vấn đề",
    "Ra quyết định",
    "Phản biện",
    "Nói rõ trọng tâm",
    "Thuyết phục",
    "Ứng biến",
]

MENU_ITEMS = ["Home", "Practice", "Result", "About"]

TARGET_DURATIONS = ["30 giây", "60 giây", "90 giây", "Không giới hạn"]
MIN_ANSWER_LENGTH = 20

SCORE_CRITERIA: list[tuple[str, str]] = [
    ("focus", "Đúng trọng tâm"),
    ("clarity", "Rõ ràng"),
    ("logic", "Logic lập luận"),
    ("decision_quality", "Chất lượng quyết định"),
    ("counter_argument", "Khả năng phản biện"),
    ("persuasiveness", "Tính thuyết phục"),
    ("concision", "Độ ngắn gọn"),
    ("practicality", "Tính thực tế"),
]

HOME_BENEFITS: list[tuple[str, str, str]] = [
    ("🧠", "Nghĩ rõ hơn", "Tình huống có trade-off thật — buộc bạn chọn phương án, không né."),
    ("🎯", "Nói trúng hơn", "Biết điều bạn muốn nói vs. điều bạn thực sự nói — và cách sửa."),
    ("⚡", "Phản biện sắc hơn", "Luyện đối đáp khi bị xoáy — logic, bình tĩnh, chốt hành động."),
]


# ── Global styles ─────────────────────────────────────────


def inject_custom_css() -> None:
    """Inject app-wide CSS once per run."""
    st.html(CUSTOM_CSS.strip())


# ── UI helpers ────────────────────────────────────────────


def render_html(fragment: str) -> None:
    """
    Render block HTML qua st.html.

    Tránh st.markdown hiển thị raw HTML khi chuỗi có thụt dòng (CommonMark coi là code block).
    """
    st.html(fragment.strip())


def render_header(
    title: str,
    subtitle: str | None = None,
    *,
    hero: bool = False,
    badge: str | None = None,
) -> None:
    """Page header — use hero=True for the Home landing block."""
    safe_title = html.escape(title)
    safe_sub = html.escape(subtitle) if subtitle else ""

    if hero:
        badge_html = (
            f'<span class="ta-hero-badge">{html.escape(badge)}</span>'
            if badge
            else '<span class="ta-hero-badge">Phòng gym tư duy</span>'
        )
        render_html(
            f'<div class="ta-hero">{badge_html}'
            f"<h1>{safe_title}</h1><p>{safe_sub}</p></div>"
        )
        return

    sub_html = f"<p>{safe_sub}</p>" if subtitle else ""
    render_html(
        f'<div class="ta-page-header"><h2>{safe_title}</h2>{sub_html}</div>'
    )


def render_section_title(title: str, subtitle: str | None = None) -> None:
    """Section heading within a page."""
    safe_title = html.escape(title)
    sub_html = (
        f'<p class="ta-section-sub">{html.escape(subtitle)}</p>'
        if subtitle
        else ""
    )
    render_html(f'<p class="ta-section-title">{safe_title}</p>{sub_html}')


def render_card(
    body: str,
    title: str | None = None,
    *,
    accent: bool = False,
) -> None:
    """Rounded content card (HTML). Body supports simple <strong> tags."""
    accent_class = " ta-card-accent" if accent else ""
    title_html = (
        f'<p class="ta-card-title">{html.escape(title)}</p>' if title else ""
    )
    render_html(
        f'<div class="ta-card{accent_class}">{title_html}'
        f'<div class="ta-card-body">{body}</div></div>'
    )


def render_score_badge(
    score: int,
    label: str,
    *,
    max_score: int = 100,
) -> None:
    """Single score pill — color follows score band."""
    ratio = score / max_score if max_score else 0
    if ratio >= 0.75:
        band = "ta-score-high"
    elif ratio >= 0.5:
        band = "ta-score-mid"
    else:
        band = "ta-score-low"

    render_html(
        f'<div class="ta-score-badge {band}">'
        f'<span class="ta-score-badge-value">{score}</span>'
        f'<span class="ta-score-badge-label">{html.escape(label)}</span></div>'
    )


def render_score_row(badges: list[tuple[int, str]]) -> None:
    """Row of score badges (wraps on narrow screens)."""
    parts: list[str] = []
    for score, label in badges:
        ratio = score / 100
        band = (
            "ta-score-high"
            if ratio >= 0.75
            else "ta-score-mid"
            if ratio >= 0.5
            else "ta-score-low"
        )
        parts.append(
            f'<div class="ta-score-badge {band}">'
            f'<span class="ta-score-badge-value">{score}</span>'
            f'<span class="ta-score-badge-label">{html.escape(label)}</span></div>'
        )
    render_html(f'<div class="ta-score-row">{"".join(parts)}</div>')


def render_info_box(message: str, variant: InfoVariant = "info") -> None:
    """Styled alert — info, success, warning, or neutral."""
    render_html(f'<div class="ta-info ta-info-{variant}">{message}</div>')


def _difficulty_badge_class(difficulty: str) -> str:
    d = (difficulty or "").lower()
    if "rất" in d or d.strip() == "khó":
        return "ta-badge-diff ta-badge-hard"
    if "dễ" in d:
        return "ta-badge-diff ta-badge-easy"
    return "ta-badge-diff ta-badge-mid"


def _render_benefit_cards() -> None:
    cards = []
    for icon, title, desc in HOME_BENEFITS:
        cards.append(
            f'<div class="ta-benefit-card">'
            f'<div class="ta-benefit-icon">{icon}</div><div>'
            f'<p class="ta-benefit-title">{html.escape(title)}</p>'
            f'<p class="ta-benefit-desc">{html.escape(desc)}</p>'
            f"</div></div>"
        )
    render_html(f'<div class="ta-benefits">{"".join(cards)}</div>')


def _render_quote_card(text: str, label: str = "Câu chốt sắc bén") -> None:
    render_html(
        f'<div class="ta-quote-card">'
        f'<p class="ta-quote-label">{html.escape(label)}</p>'
        f'<p class="ta-quote-text">{html.escape(text)}</p></div>'
    )


def _render_insight_hero(items: list[str]) -> None:
    render_html(
        f'<div class="ta-insight-hero">'
        f'<p class="ta-insight-hero-title">⚠️ Vì sao người nghe dễ phớt lờ</p>'
        f"{_bullets_html(items)}</div>"
    )


def _render_copyable_script(text: str, label: str, key_suffix: str) -> None:
    """Hiển thị script dễ copy (Streamlit code block có nút copy)."""
    render_html(f'<p class="ta-copy-section-label">{html.escape(label)}</p>')
    if text.strip():
        st.code(text.strip(), language=None)
    else:
        st.caption("Chưa có nội dung.")


def _render_steps(steps: list[tuple[int, str, str]]) -> None:
    """Vertical step list for Home."""
    items = []
    for num, title, desc in steps:
        items.append(
            f'<div class="ta-step"><span class="ta-step-num">{num}</span>'
            f'<p class="ta-step-text"><strong>{html.escape(title)}</strong><br/>'
            f"{html.escape(desc)}</p></div>"
        )
    render_html(f'<div class="ta-steps">{"".join(items)}</div>')


def _render_skill_chips() -> None:
    chips = "".join(
        f'<span class="ta-chip">{html.escape(s)}</span>' for s in SKILLS
    )
    render_html(f'<div class="ta-chips">{chips}</div>')


def navigate_to(page: str) -> None:
    """Switch page and rerun (dùng session_state.page, không ghi đè widget key)."""
    if page not in MENU_ITEMS:
        return
    st.session_state.page = page
    st.rerun()


# ── Sidebar ───────────────────────────────────────────────


def render_sidebar() -> str:
    """Sidebar brand + menu. Returns selected page name."""
    render_html(
        '<p class="ta-sidebar-brand">🏟️ Thinking Arena</p>'
        '<p class="ta-sidebar-tagline">Luyện tư duy & giao tiếp</p>'
    )
    st.divider()

    icons = {
        "Home": "🏠 Home",
        "Practice": "🎯 Practice",
        "Result": "📊 Result",
        "About": "ℹ️ About",
    }
    current = st.session_state.get("page", "Home")
    if current not in MENU_ITEMS:
        current = "Home"
        st.session_state.page = current
    index = MENU_ITEMS.index(current)

    page = st.radio(
        "Menu",
        options=MENU_ITEMS,
        index=index,
        format_func=lambda p: icons.get(p, p),
        label_visibility="collapsed",
    )
    if page != st.session_state.get("page"):
        st.session_state.page = page

    if not has_api_key():
        st.caption("⚠️ Chưa có API key — chế độ demo")

    st.divider()
    if st.button("Reset phiên", use_container_width=True, help="Xóa tình huống, câu trả lời và feedback"):
        reset_session(keep_page=True)
        st.rerun()

    return page


# ── Pages ───────────────────────────────────────────────────


def render_home() -> None:
    render_header(
        APP_NAME,
        "Phòng gym tư duy — luyện mỗi ngày để nói rõ, quyết định nhanh "
        "và phản biện trong tình huống thật.",
        hero=True,
        badge="Luyện kỹ năng thật",
    )

    render_html(
        '<p class="ta-lead">Nhiều người nghĩ được ý trong đầu nhưng khi nói ra bị '
        "<strong>cụt</strong>, <strong>thiếu trọng tâm</strong> — người nghe dễ phớt lờ. "
        "Thinking Arena cho bạn tình huống thật, feedback thẳng, và bài luyện ngắn.</p>"
    )

    render_section_title("Bạn sẽ luyện được gì")
    _render_benefit_cards()

    render_section_title("Một phiên luyện", "Khoảng 10–15 phút")
    _render_steps(
        [
            (1, "Chọn chủ đề", "Chọn lĩnh vực gần công việc của bạn."),
            (2, "Trả lời tình huống", "Viết như đang nói trong cuộc họp."),
            (3, "Nhận feedback", "Chấm điểm, insight, rồi luyện phản biện."),
        ]
    )

    render_html("<div style='height:0.75rem'></div>")
    if st.button("Bắt đầu luyện hôm nay", type="primary", use_container_width=True):
        navigate_to("Practice")

    if has_api_key():
        render_info_box(
            "✅ Gemini API đã cấu hình — bạn có thể tạo tình huống và chấm điểm bằng AI.",
            variant="success",
        )
    else:
        _render_missing_api_key_notice(compact=True)


def _render_missing_api_key_notice(*, compact: bool = False) -> None:
    """Thông báo thân thiện khi chưa có GEMINI_API_KEY (local hoặc Cloud)."""
    render_info_box(
        "🔑 <strong>Chưa có Gemini API key</strong> — app đang ở <strong>chế độ demo</strong>. "
        "Tình huống và feedback là dữ liệu mẫu, không phân tích câu trả lời của bạn.",
        variant="warning",
    )
    if compact:
        return
    render_info_box(
        "<strong>Chạy trên máy:</strong> copy "
        "<code>.streamlit/secrets.toml.example</code> → "
        "<code>.streamlit/secrets.toml</code>, điền key, tắt app (Ctrl+C) và chạy lại "
        "<code>streamlit run app.py</code>.",
        variant="neutral",
    )
    render_info_box(
        "<strong>Streamlit Cloud:</strong> "
        "<a href='https://share.streamlit.io' target='_blank'>share.streamlit.io</a> → "
        "chọn app → ⚙️ <strong>Settings</strong> → <strong>Secrets</strong> → thêm "
        "<code>GEMINI_API_KEY</code> và <code>GEMINI_MODEL</code> → <strong>Save</strong> → "
        "<strong>Reboot app</strong>.",
        variant="neutral",
    )


def _render_demo_mode_notice() -> None:
    _render_missing_api_key_notice(compact=False)


def _render_demo_content_banner() -> None:
    render_info_box(
        "⚠️ <strong>Dữ liệu DEMO</strong> — minh họa flow, "
        "<em>không phải</em> phân tích AI từ câu trả lời của bạn.",
        variant="warning",
    )


def _load_demo_scenarios() -> None:
    """Nạp 3 tình huống cố định, bật demo_mode."""
    st.session_state.scenarios = get_demo_scenarios()
    st.session_state.demo_mode = True
    st.session_state.selected_scenario = None
    st.session_state.practice_step = "setup"
    st.session_state.user_answer = None
    st.session_state.feedback = None
    st.session_state.counter_feedback = None
    st.session_state.first_score = None
    st.session_state.counter_argument = None
    st.toast("Đã tải 3 tình huống demo", icon="📋")


def _persist_practice_form(
    category: str,
    keyword: str,
    difficulty: str,
    mode: str,
) -> None:
    st.session_state.category = category
    st.session_state.topic = category
    st.session_state.keyword = keyword.strip() or None
    st.session_state.difficulty = difficulty
    st.session_state.mode = mode


def _generate_scenarios(
    category: str,
    keyword: str,
    difficulty: str,
    mode: str,
) -> None:
    _persist_practice_form(category, keyword, difficulty, mode)

    if not has_api_key():
        st.warning(
            "Chưa có GEMINI_API_KEY — không thể tạo tình huống bằng AI. "
            "Bấm「Dùng tình huống demo」bên dưới hoặc cấu hình key (xem hướng dẫn trên Practice)."
        )
        return

    with st.spinner("Đang tạo 3 tình huống… (15–30 giây)"):
        try:
            client = get_client()
            result = client.generate_scenarios(
                category=category,
                keyword=keyword,
                difficulty=difficulty,
                mode=mode,
            )
            st.session_state.scenarios = [
                s.model_dump() for s in result.scenarios
            ]
            st.session_state.demo_mode = False
            st.session_state.selected_scenario = None
            st.session_state.practice_step = "setup"
            st.session_state.user_answer = None
            st.session_state.feedback = None
            st.session_state.first_score = None
        except GeminiConfigError as exc:
            st.error(str(exc))
        except GeminiResponseError as exc:
            st.error(
                f"AI trả về dữ liệu không hợp lệ. Thử bấm tạo lại. Chi tiết: {exc}"
            )
        except Exception:
            st.error(
                "Không tạo được tình huống lúc này. Kiểm tra mạng/API key và thử lại."
            )


def _scenario_skill_badges_html(scenario: dict[str, Any]) -> str:
    diff = scenario.get("difficulty", "Trung bình")
    parts = [
        f'<span class="{_difficulty_badge_class(diff)}">{html.escape(diff)}</span>',
    ]
    for skill in scenario.get("skill_focus", [])[:4]:
        parts.append(f'<span class="ta-badge-skill">{html.escape(skill)}</span>')
    cat = scenario.get("category", "")
    if cat:
        parts.append(f'<span class="ta-chip">{html.escape(cat)}</span>')
    return f'<div class="ta-scenario-badges">{"".join(parts)}</div>'


def _render_scenario_card(scenario: dict[str, Any], index: int) -> None:
    selected = st.session_state.get("selected_scenario")
    is_selected = (
        selected is not None
        and selected.get("title") == scenario.get("title")
        and selected.get("question") == scenario.get("question")
    )
    sel_class = " ta-scenario-selected" if is_selected else ""
    num = f"{index + 1:02d}"
    title = html.escape(scenario.get("title", "Tình huống"))
    context = html.escape(scenario.get("context", ""))
    conflict = html.escape(scenario.get("core_conflict", ""))
    question = html.escape(scenario.get("question", ""))

    render_html(
        f'<div class="ta-scenario-v2{sel_class}">'
        f'<div class="ta-scenario-v2-head"><div class="ta-scenario-v2-top">'
        f'<span class="ta-scenario-num">#{num}</span>'
        f'<p class="ta-scenario-v2-title">{title}</p></div>'
        f"{_scenario_skill_badges_html(scenario)}</div>"
        f'<div class="ta-scenario-v2-body">'
        f'<p class="ta-scenario-label">Bối cảnh</p><p>{context}</p>'
        f'<p class="ta-scenario-label">Mâu thuẫn</p><p>{conflict}</p>'
        f'<div class="ta-scenario-v2-question">{question}</div></div></div>'
    )
    if st.button(
        "✓ Chọn tình huống này",
        key=f"select_scenario_{index}",
        type="primary",
        use_container_width=True,
    ):
        st.session_state.selected_scenario = scenario
        st.session_state.practice_step = "answer"
        st.session_state.feedback = None
        st.session_state.first_score = None
        st.session_state.counter_argument = None
        st.rerun()


def _scenario_compact_body(scenario: dict[str, Any]) -> str:
    """Card gọn cho phần Answer — chỉ các field cốt lõi."""
    return (
        f'<p class="ta-scenario-label">Bối cảnh</p>'
        f"<p>{html.escape(scenario.get('context', ''))}</p>"
        f'<p class="ta-scenario-label">Mâu thuẫn</p>'
        f"<p>{html.escape(scenario.get('core_conflict', ''))}</p>"
        f'<p class="ta-scenario-label">Câu hỏi cần trả lời</p>'
        f"<p><strong>{html.escape(scenario.get('question', ''))}</strong></p>"
    )


def _bullets_html(items: list[str]) -> str:
    if not items:
        return "<p><em>Không có.</em></p>"
    lis = "".join(f"<li>{html.escape(item)}</li>" for item in items)
    return f"<ul style='margin:0;padding-left:1.1rem'>{lis}</ul>"


def render_score_badge_large(score: int, label: str = "Tổng điểm") -> None:
    """Badge điểm lớn cho tổng điểm phiên."""
    ratio = score / 100
    if ratio >= 0.75:
        color = "#059669"
    elif ratio >= 0.5:
        color = "#d97706"
    else:
        color = "#dc2626"

    render_html(
        f'<div class="ta-score-hero-wrap"><div class="ta-score-hero">'
        f'<span class="ta-score-hero-value" style="color:{color}">{score}</span>'
        f'<span class="ta-score-hero-label">{html.escape(label)}</span>'
        f"</div></div>"
    )


def _render_total_score_block(total: int) -> None:
    ratio = total / 100
    if ratio >= 0.75:
        color = "#059669"
    elif ratio >= 0.5:
        color = "#d97706"
    else:
        color = "#dc2626"

    render_html(
        f'<div class="ta-score-panel"><div class="ta-score-hero-wrap">'
        f'<div class="ta-score-hero">'
        f'<span class="ta-score-hero-value" style="color:{color}">{total}</span>'
        f'<span class="ta-score-hero-label">Điểm tổng</span></div></div>'
        f'<p class="ta-score-session-text">Điểm phiên trả lời: {total}/100</p></div>'
    )
    st.progress(min(max(total / 100, 0.0), 1.0))


def _render_score_breakdown_bars(scores: dict[str, Any]) -> None:
    for key, label in SCORE_CRITERIA:
        value = int(scores.get(key, 0) or 0)
        render_html(
            f'<div class="ta-criterion-row"><div class="ta-criterion-head">'
            f'<span class="ta-criterion-name">{html.escape(label)}</span>'
            f'<span class="ta-criterion-val">{value}/100</span></div></div>'
        )
        st.progress(min(max(value / 100, 0.0), 1.0))


def _evaluate_user_answer(
    scenario: dict[str, Any],
    answer: str,
    mode: str,
    target_duration: str,
) -> None:
    if len(answer.strip()) < MIN_ANSWER_LENGTH:
        st.warning(
            f"Câu trả lời quá ngắn (cần ít nhất {MIN_ANSWER_LENGTH} ký tự). "
            "Hãy nói rõ quyết định, lý do, rủi ro và bước tiếp theo."
        )
        return

    st.session_state.user_answer = answer.strip()
    st.session_state.target_duration = target_duration

    if not has_api_key():
        st.session_state.demo_mode = True
        fb = get_demo_feedback()
        st.session_state.feedback = fb
        st.session_state.first_score = fb["total_score"]
        st.session_state.counter_argument = fb["counter_question"]
        st.session_state.counter_feedback = None
        _render_demo_content_banner()
        return

    with st.spinner("AI đang phân tích câu trả lời của bạn…"):
        try:
            client = get_client()
            result = client.evaluate_answer(
                scenario=scenario,
                user_answer=answer.strip(),
                mode=mode,
                target_duration=target_duration,
            )
            st.session_state.feedback = result.model_dump()
            st.session_state.first_score = result.total_score
            st.session_state.counter_argument = result.counter_question
            st.session_state.counter_feedback = None
            st.session_state.demo_mode = False
        except GeminiConfigError as exc:
            st.error(str(exc))
        except GeminiResponseError as exc:
            st.error(
                f"Không đọc được kết quả chấm điểm. Thử lại. Chi tiết: {exc}"
            )
        except Exception:
            st.error(
                "Chấm điểm thất bại. Kiểm tra mạng/API key và thử lại."
            )


def render_feedback_section(feedback: dict[str, Any] | None = None) -> None:
    """
    Hiển thị Feedback học tập — đọc từ tham số hoặc session_state['feedback'].
    """
    data = feedback if feedback is not None else st.session_state.get("feedback")
    if not data:
        return

    if st.session_state.get("demo_mode"):
        _render_demo_content_banner()

    render_section_title("Kết quả chấm điểm")

    # 1. Điểm tổng
    total = int(data.get("total_score", 0) or 0)
    _render_total_score_block(total)

    # 2. Insight nổi bật — ngay sau điểm tổng
    _render_insight_hero(data.get("why_listener_may_ignore", []))

    # 3. Bản đồ điểm — thu gọn
    scores = data.get("scores") or {}
    with st.expander("📊 Xem chi tiết 8 tiêu chí", expanded=False):
        _render_score_breakdown_bars(scores)

    st.divider()

    # 4. Bạn đang muốn nói gì?
    render_section_title("Bạn đang muốn nói gì?")
    render_card(
        html.escape(data.get("user_intent_summary", "")),
        accent=True,
    )

    # 4. Khoảng cách ý trong đầu ↔ lời nói thực tế
    render_section_title(
        "Khoảng cách giữa ý trong đầu và lời nói thực tế",
        "Ba góc nhìn — so sánh trực diện",
    )
    render_card(
        _bullets_html(data.get("what_user_probably_meant", [])),
        title="Có thể bạn muốn nói",
    )
    render_card(
        _bullets_html(data.get("what_user_actually_said", [])),
        title="Nhưng câu trả lời thực tế thể hiện",
    )
    render_card(
        _bullets_html(data.get("gap_analysis", [])),
        title="Khoảng cách cần sửa",
        accent=True,
    )

    # 5. Điểm tốt cần giữ
    render_section_title("Điểm tốt cần giữ")
    strengths = data.get("strengths") or []
    if strengths:
        render_card(_bullets_html(strengths))
    else:
        render_info_box("Chưa có điểm mạnh rõ — tập trung sửa phần dưới.", variant="neutral")

    # 6. Điểm cần sửa ngay
    render_section_title("Điểm cần sửa ngay")
    weaknesses = data.get("weaknesses") or []
    missing = data.get("missing_points") or []
    if weaknesses:
        render_card(_bullets_html(weaknesses), title="Điểm yếu")
    if missing:
        render_card(_bullets_html(missing), title="Còn thiếu trong câu trả lời")
    if not weaknesses and not missing:
        render_info_box("Không ghi nhận điểm yếu cụ thể.", variant="neutral")

    # 7. Nói lại tốt hơn — dễ copy
    render_section_title("Nói lại tốt hơn")
    render_html(
        '<p class="ta-copy-hint">Bấm icon copy góc phải mỗi khối để dán vào ghi chú hoặc luyện đọc to.</p>'
    )
    _render_copyable_script(data.get("better_answer_10s", ""), "⏱ Bản ~10 giây", "10s")
    _render_copyable_script(data.get("better_answer_30s", ""), "⏱ Bản ~30 giây", "30s")
    _render_copyable_script(data.get("better_answer_90s", ""), "⏱ Bản ~90 giây", "90s")

    # 8. Câu chốt — quote card
    render_section_title("Câu chốt sắc bén")
    _render_quote_card(data.get("sharp_closing_sentence", ""))

    # 9. AI phản biện bạn
    render_section_title("AI phản biện bạn")
    counter_q = data.get("counter_question", "")
    render_html(
        f'<div class="ta-counter-box"><p style="margin:0">{html.escape(counter_q)}</p></div>'
    )
    if (
        st.session_state.get("practice_step") != "counter"
        and not st.session_state.get("counter_feedback")
    ):
        if st.button(
            "Trả lời phản biện này",
            type="primary",
            use_container_width=True,
            key="btn_start_counter",
        ):
            st.session_state.practice_step = "counter"
            st.session_state.counter_argument = counter_q
            st.rerun()

    # 10. Bài tập nhỏ tiếp theo
    render_section_title("Bài tập nhỏ tiếp theo")
    render_card(html.escape(data.get("next_micro_drill", "")))

    # 11. Bài học quan trọng nhất hôm nay
    render_section_title("Bài học quan trọng nhất hôm nay")
    render_info_box(
        html.escape(data.get("main_lesson_today", "")),
        variant="success",
    )


def _reset_for_new_scenario() -> None:
    """Bắt đầu phiên tình huống mới — giữ thiết lập chủ đề/độ khó."""
    st.session_state.scenarios = None
    st.session_state.selected_scenario = None
    st.session_state.feedback = None
    st.session_state.counter_feedback = None
    st.session_state.user_answer = None
    st.session_state.rebuttal_answer = None
    st.session_state.first_score = None
    st.session_state.final_lesson = None
    st.session_state.counter_argument = None
    st.session_state.demo_mode = False
    st.session_state.practice_step = "setup"
    for key in ("practice_user_answer", "practice_rebuttal"):
        if key in st.session_state:
            del st.session_state[key]


def _evaluate_counter_response(
    scenario: dict[str, Any],
    counter_question: str,
    rebuttal: str,
) -> None:
    if len(rebuttal.strip()) < MIN_ANSWER_LENGTH:
        st.warning(
            f"Câu phản biện quá ngắn (cần ít nhất {MIN_ANSWER_LENGTH} ký tự). "
            "Hãy bảo vệ quan điểm bằng lý do cụ thể."
        )
        return

    st.session_state.rebuttal_answer = rebuttal.strip()

    if not has_api_key():
        st.session_state.demo_mode = True
        st.session_state.counter_feedback = get_demo_counter_feedback()
        st.session_state.final_lesson = st.session_state.counter_feedback["final_advice"]
        _render_demo_content_banner()
        return

    with st.spinner("AI đang kiểm tra khả năng phản biện của bạn…"):
        try:
            client = get_client()
            result = client.evaluate_counter_response(
                scenario=scenario,
                counter_question=counter_question,
                user_response=rebuttal.strip(),
            )
            st.session_state.counter_feedback = result.model_dump()
            st.session_state.final_lesson = result.final_advice
            st.session_state.demo_mode = False
        except GeminiConfigError as exc:
            st.error(str(exc))
        except GeminiResponseError as exc:
            st.error(
                f"Không đọc được kết quả phản biện. Thử lại. Chi tiết: {exc}"
            )
        except Exception:
            st.error(
                "Chấm phản biện thất bại. Kiểm tra mạng/API key và thử lại."
            )


def render_counter_feedback_section(
    counter_feedback: dict[str, Any] | None = None,
) -> None:
    """Hiển thị CounterFeedback — gọn, tập trung học tập."""
    data = (
        counter_feedback
        if counter_feedback is not None
        else st.session_state.get("counter_feedback")
    )
    if not data:
        return

    if st.session_state.get("demo_mode"):
        _render_demo_content_banner()

    render_section_title("Kết quả phản biện", "Ngắn gọn — điểm mạnh/yếu và bản nói lại")

    score = int(data.get("score", 0) or 0)
    render_score_badge_large(score, "Điểm phản biện")
    st.progress(min(max(score / 100, 0.0), 1.0))
    render_html(f'<p class="ta-score-session-text">Điểm phản biện: {score}/100</p>')

    strong = data.get("strong_points") or []
    weak = data.get("weak_points") or []

    if strong:
        render_card(_bullets_html(strong), title="Điểm mạnh")
    if weak:
        render_card(_bullets_html(weak), title="Điểm yếu")

    with st.expander("Phiên bản trả lời phản biện tốt hơn", expanded=True):
        st.markdown(data.get("better_counter_response", ""))

    render_info_box(
        html.escape(data.get("final_advice", "")),
        variant="success",
    )


def _render_counter_practice_actions() -> None:
    """Nút sau khi hoàn thành phản biện — xếp dọc cho mobile."""
    if st.button(
        "Xem tổng kết phiên luyện",
        type="primary",
        use_container_width=True,
        key="btn_go_result",
    ):
        navigate_to("Result")

    if st.button(
        "Luyện tình huống mới",
        use_container_width=True,
        key="btn_new_scenario",
    ):
        _reset_for_new_scenario()
        st.rerun()


def _render_counter_reply_section() -> None:
    """Counter Practice — trả lời và chấm câu phản biện."""
    feedback = st.session_state.get("feedback")
    if not feedback:
        render_info_box(
            "Chưa có feedback câu trả lời chính. Hãy chấm câu trả lời trước.",
            variant="warning",
        )
        if st.button("← Quay lại trả lời", use_container_width=True):
            st.session_state.practice_step = "answer"
            st.rerun()
        return

    scenario = st.session_state.get("selected_scenario")
    if not scenario:
        render_info_box("Chưa có tình huống được chọn.", variant="warning")
        return

    counter_q = (
        feedback.get("counter_question")
        or st.session_state.get("counter_argument")
        or ""
    )
    if not counter_q:
        render_info_box(
            "Chưa có câu phản biện từ AI. Chấm lại câu trả lời chính để nhận câu xoáy.",
            variant="warning",
        )
        return

    st.session_state.counter_argument = counter_q

    render_section_title("Counter Practice", "Đối đáp chuyên nghiệp, không né câu hỏi")

    render_card(
        html.escape(counter_q),
        title="AI phản biện bạn",
        accent=True,
    )

    counter_fb = st.session_state.get("counter_feedback")

    if not counter_fb:
        if "practice_rebuttal" not in st.session_state:
            st.session_state.practice_rebuttal = (
                st.session_state.get("rebuttal_answer") or ""
            )

        rebuttal = st.text_area(
            "Câu trả lời phản biện",
            placeholder=(
                "Trả lời như trong một cuộc họp thật. "
                "Hãy bảo vệ quan điểm nhưng vẫn chuyên nghiệp…"
            ),
            height=160,
            key="practice_rebuttal",
        )
        st.session_state.rebuttal_answer = rebuttal

        if st.button(
            "Chấm câu trả lời phản biện",
            type="primary",
            use_container_width=True,
        ):
            _evaluate_counter_response(scenario, counter_q, rebuttal)

        if st.button("← Quay lại xem feedback", use_container_width=True):
            st.session_state.practice_step = "answer"
            st.rerun()
    else:
        render_counter_feedback_section(counter_fb)
        _render_counter_practice_actions()

        with st.expander("Sửa và chấm lại phản biện", expanded=False):
            rebuttal = st.text_area(
                "Câu trả lời phản biện",
                key="practice_rebuttal_retry",
                height=120,
            )
            if st.button("Chấm lại", use_container_width=True):
                _evaluate_counter_response(scenario, counter_q, rebuttal)


def _render_practice_answer_section() -> None:
    scenario = st.session_state.get("selected_scenario")

    if not scenario:
        render_section_title("Trả lời tình huống")
        render_info_box(
            "Bạn chưa chọn tình huống. Hãy tạo và chọn một tình huống trước.",
            variant="warning",
        )
        if st.button("Quay lại chọn tình huống", use_container_width=True):
            st.session_state.practice_step = "setup"
            st.rerun()
        return

    step = st.session_state.get("practice_step", "answer")

    if step == "answer":
        render_section_title("Trả lời tình huống", "Viết như bạn sẽ nói trong tình huống thật")

        render_card(
            _scenario_compact_body(scenario),
            title=scenario.get("title", "Tình huống"),
            accent=True,
        )

        render_info_box(
            "Hãy trả lời như đang nói trong một cuộc họp thật. Đừng cố viết hay. Hãy nói rõ:<br/>"
            "• <strong>Tôi chọn gì?</strong><br/>"
            "• <strong>Vì sao?</strong><br/>"
            "• <strong>Rủi ro là gì?</strong><br/>"
            "• <strong>Hành động tiếp theo là gì?</strong>",
            variant="info",
        )

        default_duration = st.session_state.get("target_duration") or TARGET_DURATIONS[1]
        duration_index = (
            TARGET_DURATIONS.index(default_duration)
            if default_duration in TARGET_DURATIONS
            else 1
        )
        target_duration = st.selectbox(
            "Thời lượng mục tiêu",
            options=TARGET_DURATIONS,
            index=duration_index,
            key="practice_target_duration",
        )
        st.session_state.target_duration = target_duration

        if "practice_user_answer" not in st.session_state:
            st.session_state.practice_user_answer = (
                st.session_state.get("user_answer") or ""
            )

        answer = st.text_area(
            "Câu trả lời của bạn",
            placeholder="Viết câu trả lời của bạn ở đây…",
            height=200,
            key="practice_user_answer",
        )
        st.session_state.user_answer = answer

        mode = st.session_state.get("mode") or VALID_MODES[-1]

        if st.button(
            "Chấm câu trả lời",
            type="primary",
            use_container_width=True,
        ):
            _evaluate_user_answer(scenario, answer, mode, target_duration)

        if st.button("← Chọn tình huống khác", use_container_width=True):
            st.session_state.practice_step = "setup"
            st.session_state.selected_scenario = None
            st.session_state.feedback = None
            st.rerun()

    elif step == "counter":
        render_section_title("Phản biện", "Đọc lại feedback rồi trả lời câu xoáy bên dưới")
        with st.expander("Câu trả lời đã nộp", expanded=False):
            st.markdown(st.session_state.get("user_answer") or "_Chưa có_")

    feedback = st.session_state.get("feedback")
    if feedback:
        st.divider()
        if step == "counter":
            with st.expander("Feedback câu trả lời chính", expanded=False):
                render_feedback_section(feedback)
        else:
            render_feedback_section(feedback)

    if step == "counter":
        st.divider()
        _render_counter_reply_section()


def render_practice() -> None:
    render_header(
        "Bắt đầu phiên luyện hôm nay",
        "Chọn chủ đề → nhận 3 tình huống → chọn một → viết câu trả lời.",
    )

    if not has_api_key():
        _render_demo_mode_notice()
        if st.button("Dùng tình huống demo", type="primary", use_container_width=True):
            _load_demo_scenarios()
            st.rerun()

    has_scenarios = bool(st.session_state.get("scenarios"))

    st.markdown('<div class="ta-form-panel">', unsafe_allow_html=True)
    with st.expander("⚙️ Thiết lập phiên luyện", expanded=not has_scenarios):
        default_category = st.session_state.get("category") or VALID_CATEGORIES[0]
        category_index = (
            VALID_CATEGORIES.index(default_category)
            if default_category in VALID_CATEGORIES
            else 0
        )
        category = st.selectbox(
            "Nhóm chủ đề",
            options=VALID_CATEGORIES,
            index=category_index,
            key="practice_category_select",
        )
        keyword = st.text_input(
            "Keyword (tuỳ chọn)",
            value=st.session_state.get("keyword") or "",
            placeholder="VD: TikTok Shop, trễ deadline, claim quảng cáo…",
            key="practice_keyword_input",
        )
        default_difficulty = st.session_state.get("difficulty") or VALID_DIFFICULTIES[1]
        difficulty = st.selectbox(
            "Độ khó",
            options=VALID_DIFFICULTIES,
            index=VALID_DIFFICULTIES.index(default_difficulty)
            if default_difficulty in VALID_DIFFICULTIES
            else 1,
            key="practice_difficulty_select",
        )
        default_mode = st.session_state.get("mode") or VALID_MODES[-1]
        mode = st.selectbox(
            "Chế độ luyện",
            options=VALID_MODES,
            index=VALID_MODES.index(default_mode)
            if default_mode in VALID_MODES
            else len(VALID_MODES) - 1,
            key="practice_mode_select",
        )
        _persist_practice_form(category, keyword, difficulty, mode)

        if has_api_key():
            if st.button("Tạo 3 tình huống", type="primary", use_container_width=True):
                _generate_scenarios(category, keyword, difficulty, mode)
            if has_scenarios and st.button("Tạo lại tình huống khác", use_container_width=True):
                _generate_scenarios(category, keyword, difficulty, mode)
        elif has_scenarios and st.session_state.get("demo_mode"):
            if st.button("Tải lại tình huống demo", use_container_width=True):
                _load_demo_scenarios()
                st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    scenarios: list[dict[str, Any]] | None = st.session_state.get("scenarios")
    if scenarios:
        render_section_title(
            "Chọn tình huống",
            f"{len(scenarios)} tình huống — đọc và bấm「Chọn tình huống này」",
        )
        for idx, scenario_data in enumerate(scenarios):
            _render_scenario_card(scenario_data, idx)

    if st.session_state.get("selected_scenario") and st.session_state.get(
        "practice_step"
    ) in ("answer", "counter"):
        st.divider()
        _render_practice_answer_section()


def _result_session_payload() -> dict[str, Any]:
    """Gom dữ liệu phiên hiện tại cho Result & Markdown."""
    return {
        "scenario": st.session_state.get("selected_scenario"),
        "category": st.session_state.get("category"),
        "keyword": st.session_state.get("keyword"),
        "mode": st.session_state.get("mode"),
        "difficulty": st.session_state.get("difficulty"),
        "target_duration": st.session_state.get("target_duration"),
        "feedback": st.session_state.get("feedback"),
        "user_answer": st.session_state.get("user_answer"),
        "counter_feedback": st.session_state.get("counter_feedback"),
        "rebuttal_answer": st.session_state.get("rebuttal_answer"),
    }


def _render_copy_markdown_button(markdown_text: str, *, key: str) -> None:
    """Nút copy clipboard (chạy trên trình duyệt, không lưu server)."""
    payload = json.dumps(markdown_text)
    components.html(
        f"""
        <button id="copy_{key}" style="
            width:100%; min-height:3rem; padding:0.65rem 1rem;
            border-radius:12px; border:none; background:#4f46e5;
            color:#fff; font-weight:600; font-size:0.95rem; cursor:pointer;
        ">📋 Copy nội dung tổng kết</button>
        <script>
        (function() {{
            var btn = document.getElementById("copy_{key}");
            btn.onclick = function() {{
                navigator.clipboard.writeText({payload}).then(function() {{
                    btn.innerText = "✓ Đã copy!";
                    setTimeout(function() {{
                        btn.innerText = "📋 Copy nội dung tổng kết";
                    }}, 2000);
                }}).catch(function() {{
                    btn.innerText = "Không copy được — dùng tải file .md";
                }});
            }};
        }})();
        </script>
        """,
        height=70,
    )


def render_result() -> None:
    render_header("Result", "Tổng kết phiên luyện hiện tại.")

    feedback = st.session_state.get("feedback")

    if not feedback:
        render_info_box(
            "Bạn chưa hoàn thành phiên luyện nào.",
            variant="info",
        )
        if st.button("Bắt đầu luyện ở Practice", type="primary", use_container_width=True):
            navigate_to("Practice")
        return

    payload = _result_session_payload()
    scenario = payload["scenario"] or {}
    counter_fb = payload["counter_feedback"]

    # 1. Chủ đề / tình huống
    render_section_title("Chủ đề & tình huống")
    topic_title = scenario.get("title") or payload.get("category") or "—"
    render_card(
        f"<strong>{html.escape(str(topic_title))}</strong>"
        + (
            f"<br/><span style='color:#6b7280'>"
            f"{html.escape(str(scenario.get('category') or payload.get('category') or ''))}"
            f"</span>"
            if scenario.get("category") or payload.get("category")
            else ""
        ),
        title="Đã luyện",
        accent=True,
    )

    # 2. Câu hỏi chính
    render_section_title("Câu hỏi chính")
    render_card(html.escape(scenario.get("question", "—")))

    # 3. Câu trả lời ban đầu
    render_section_title("Câu trả lời ban đầu của bạn")
    answer = (payload.get("user_answer") or "").strip()
    if answer:
        with st.expander("Xem câu trả lời", expanded=False):
            st.markdown(answer)
    else:
        st.caption("Chưa lưu câu trả lời.")

    # 4. Điểm tổng
    render_section_title("Điểm tổng")
    total = int(feedback.get("total_score", 0) or 0)
    _render_total_score_block(total)

    # 5. Vì sao bị phớt lờ
    render_section_title("Lỗi chính khiến người nghe dễ phớt lờ")
    render_html(
        f'<div class="ta-insight-highlight">{_bullets_html(feedback.get("why_listener_may_ignore", []))}</div>'
    )

    # 6. Bản nói lại 30 giây
    render_section_title("Câu nói lại tốt hơn (~30 giây)")
    render_card(html.escape(feedback.get("better_answer_30s", "")))

    render_section_title("Câu chốt sắc bén")
    _render_quote_card(feedback.get("sharp_closing_sentence", ""))

    # 8. Bài học hôm nay
    render_section_title("Bài học quan trọng nhất hôm nay")
    render_info_box(
        html.escape(feedback.get("main_lesson_today", "")),
        variant="success",
    )

    # 9. Phản biện (nếu có)
    if counter_fb:
        render_section_title("Kết quả phản biện")
        c_score = int(counter_fb.get("score", 0) or 0)
        render_score_badge_large(c_score, "Điểm phản biện")
        st.progress(min(max(c_score / 100, 0.0), 1.0))

        render_section_title("Phiên bản phản biện tốt hơn")
        with st.expander("Xem bản mẫu", expanded=True):
            st.markdown(counter_fb.get("better_counter_response", ""))

        render_section_title("Lời khuyên cuối")
        render_info_box(
            html.escape(counter_fb.get("final_advice", "")),
            variant="success",
        )

    st.divider()
    render_section_title("Xuất tổng kết", "Copy hoặc tải file Markdown")

    md_summary = generate_markdown_summary(**payload)

    _render_copy_markdown_button(md_summary, key="result_md")

    st.download_button(
        label="Tải kết quả dạng Markdown",
        data=md_summary.encode("utf-8"),
        file_name="thinking_arena_result.md",
        mime="text/markdown",
        use_container_width=True,
        type="primary",
    )

    with st.expander("Xem trước nội dung Markdown", expanded=False):
        st.markdown(md_summary)

    if st.button("Luyện tiếp ở Practice", use_container_width=True):
        navigate_to("Practice")


def render_about() -> None:
    render_header("About", f"Về {APP_NAME}")

    render_card(
        "<strong>Thinking Arena</strong> là phòng gym tư duy hằng ngày — "
        "luyện cách suy nghĩ, quyết định và truyền đạt ý trong tình huống thật.",
        title="Sứ mệnh",
        accent=True,
    )

    render_section_title("Công nghệ")
    render_card(
        "• Python + Streamlit<br/>"
        "• Google Gemini (<code>google-genai</code>)<br/>"
        "• Pydantic cho structured output<br/>"
        "• Không database, không đăng nhập",
        title="Stack",
    )

    render_section_title("Phiên bản")
    render_info_box(
        "v1.0 — Streamlit + Gemini + demo mode + export Markdown.",
        variant="success",
    )
