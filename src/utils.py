"""Shared helpers for session state and configuration."""

from __future__ import annotations

from datetime import datetime
from typing import Any

import streamlit as st

SESSION_DEFAULTS: dict[str, Any] = {
    "page": "Home",
    "practice_step": "setup",  # setup | answer | counter
    "category": None,
    "topic": None,
    "keyword": None,
    "difficulty": "Trung bình",
    "mode": "Real-life Simulation",
    "scenarios": None,
    "selected_scenario": None,
    "user_answer": None,
    "target_duration": "60 giây",
    "feedback": None,
    "first_score": None,
    "counter_argument": None,
    "rebuttal_answer": None,
    "counter_feedback": None,
    "final_lesson": None,
    "demo_mode": False,
}


def has_api_key() -> bool:
    """Có GEMINI_API_KEY hay không."""
    from src.gemini_client import has_api_key as _has

    return _has()


def init_session_state() -> None:
    """Ensure all expected session keys exist with defaults."""
    for key, default in SESSION_DEFAULTS.items():
        if key not in st.session_state:
            st.session_state[key] = default


_VALID_PAGES = frozenset({"Home", "Practice", "Result", "About"})


def reset_session(*, keep_page: bool = True) -> None:
    """
    Xóa toàn bộ session (phiên luyện + widget Streamlit).
    Dùng khi người dùng muốn bắt đầu lại từ đầu.
    """
    preserve = (
        st.session_state.get("page", "Home") if keep_page else "Home"
    )
    if preserve not in _VALID_PAGES:
        preserve = "Home"

    for key in list(st.session_state.keys()):
        del st.session_state[key]

    init_session_state()
    st.session_state.page = preserve


def get_gemini_api_key() -> str | None:
    """Read API key from Streamlit secrets or environment (never hard-coded)."""
    from src.gemini_client import get_gemini_api_key as _get_key

    return _get_key()


def get_gemini_model() -> str:
    """Read model name from secrets, env, or default."""
    from src.gemini_client import get_gemini_model as _get_model

    return _get_model()


def _md_list(items: list[str] | None, *, empty: str = "_Không có_") -> str:
    if not items:
        return empty
    return "\n".join(f"- {line.strip()}" for line in items if line.strip())


def generate_markdown_summary(
    *,
    scenario: dict[str, Any] | None = None,
    category: str | None = None,
    keyword: str | None = None,
    mode: str | None = None,
    difficulty: str | None = None,
    target_duration: str | None = None,
    feedback: dict[str, Any] | None = None,
    user_answer: str | None = None,
    counter_feedback: dict[str, Any] | None = None,
    rebuttal_answer: str | None = None,
) -> str:
    """
    Tạo nội dung Markdown tổng kết phiên luyện — dùng cho copy/tải file.
    Không đọc session_state; caller truyền dữ liệu tường minh.
    """
    if not feedback:
        return "# Thinking Arena\n\n_Chưa có dữ liệu phiên luyện._\n"

    sc = scenario or {}
    topic_line = sc.get("title") or category or "—"
    cat_line = sc.get("category") or category or "—"

    lines: list[str] = [
        "# Thinking Arena — Tổng kết phiên luyện",
        "",
        f"**Ngày:** {datetime.now().strftime('%Y-%m-%d %H:%M')}",
        "",
        "## Thiết lập phiên",
        f"- **Chủ đề / tình huống:** {topic_line}",
        f"- **Nhóm chủ đề:** {cat_line}",
    ]

    if keyword:
        lines.append(f"- **Keyword:** {keyword}")
    if mode:
        lines.append(f"- **Chế độ luyện:** {mode}")
    if difficulty:
        lines.append(f"- **Độ khó:** {difficulty}")
    if target_duration:
        lines.append(f"- **Thời lượng mục tiêu:** {target_duration}")

    lines.extend(
        [
            "",
            "## Tình huống",
            "",
            sc.get("context", "_Không có bối cảnh_"),
            "",
            f"**Mâu thuẫn:** {sc.get('core_conflict', '—')}",
            "",
            "## Câu hỏi chính",
            "",
            sc.get("question", "—"),
            "",
            "## Câu trả lời ban đầu của bạn",
            "",
            (user_answer or "_Chưa có_").strip(),
            "",
            "## Điểm tổng",
            "",
            f"**{feedback.get('total_score', 0)}/100**",
            "",
            "## Lỗi chính khiến người nghe dễ phớt lờ",
            "",
            _md_list(feedback.get("why_listener_may_ignore")),
            "",
            "## Câu nói lại tốt hơn (~30 giây)",
            "",
            feedback.get("better_answer_30s", "—"),
            "",
            "## Câu chốt sắc bén",
            "",
            f"> {feedback.get('sharp_closing_sentence', '—')}",
            "",
            "## Bài học quan trọng nhất hôm nay",
            "",
            feedback.get("main_lesson_today", "—"),
        ]
    )

    if counter_feedback:
        lines.extend(
            [
                "",
                "---",
                "",
                "## Phản biện",
                "",
                f"**Điểm phản biện:** {counter_feedback.get('score', 0)}/100",
                "",
            ]
        )
        if rebuttal_answer:
            lines.extend(
                [
                    "### Câu trả lời phản biện của bạn",
                    "",
                    rebuttal_answer.strip(),
                    "",
                ]
            )
        lines.extend(
            [
                "### Phiên bản phản biện tốt hơn",
                "",
                counter_feedback.get("better_counter_response", "—"),
                "",
                "### Lời khuyên cuối",
                "",
                counter_feedback.get("final_advice", "—"),
            ]
        )

    lines.append("")
    return "\n".join(lines)
