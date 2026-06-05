"""Thinking Arena — Streamlit entry point."""

from __future__ import annotations

import sys
from pathlib import Path

# Đảm bảo import `src.*` khi chạy local hoặc trên Streamlit Cloud (cwd = thư mục chứa app.py).
_REPO_ROOT = Path(__file__).resolve().parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

import streamlit as st

# Phải gọi trước mọi lệnh Streamlit khác (kể cả import module dùng st.*).
st.set_page_config(
    page_title="Thinking Arena",
    page_icon="🏟️",
    layout="centered",
    initial_sidebar_state="expanded",
)

from src.ui import (
    inject_custom_css,
    render_about,
    render_home,
    render_practice,
    render_result,
    render_sidebar,
)
from src.utils import init_session_state

PAGES = {
    "Home": render_home,
    "Practice": render_practice,
    "Result": render_result,
    "About": render_about,
}


def main() -> None:
    init_session_state()
    inject_custom_css()

    with st.sidebar:
        page = render_sidebar()

    PAGES[page]()


if __name__ == "__main__":
    main()
