"""Global CSS — mobile-first, professional coaching app aesthetic."""

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

/* ── Base ────────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
    -webkit-font-smoothing: antialiased;
    font-size: 16px;
}

.main .block-container {
    max-width: 42rem;
    padding-top: 1.25rem;
    padding-bottom: 3rem;
    padding-left: 1.1rem;
    padding-right: 1.1rem;
    overflow-x: hidden;
}

section.main > div {
    overflow-x: hidden;
}

/* ── Sidebar ───────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
}
[data-testid="stSidebar"] .stRadio > label { font-size: 0 !important; }
[data-testid="stSidebar"] .stRadio > div { gap: 0.4rem; }
[data-testid="stSidebar"] .stRadio label[data-baseweb="radio"] {
    background: rgba(255,255,255,0.06);
    border-radius: 10px;
    padding: 0.7rem 0.9rem !important;
    margin: 0 !important;
    border: 1px solid transparent;
    transition: background 0.15s, border-color 0.15s;
    width: 100%;
}
[data-testid="stSidebar"] .stRadio label[data-baseweb="radio"]:has(input:checked) {
    background: rgba(99, 102, 241, 0.28);
    border-color: rgba(129, 140, 248, 0.55);
}
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.12); }
.ta-sidebar-brand {
    font-size: 1.2rem;
    font-weight: 700;
    color: #f8fafc !important;
    letter-spacing: -0.02em;
    margin: 0 0 0.2rem 0;
}
.ta-sidebar-tagline {
    font-size: 0.8rem;
    color: #94a3b8 !important;
    margin: 0;
}

/* ── Hero (Home) ───────────────────────────────────── */
.ta-hero {
    background: linear-gradient(145deg, #312e81 0%, #4f46e5 45%, #6366f1 100%);
    border-radius: 20px;
    padding: 2rem 1.5rem;
    margin-bottom: 1.5rem;
    color: #fff;
    box-shadow: 0 8px 32px rgba(49, 46, 129, 0.35);
    position: relative;
    overflow: hidden;
}
.ta-hero::after {
    content: '';
    position: absolute;
    top: -40%;
    right: -20%;
    width: 60%;
    height: 120%;
    background: radial-gradient(circle, rgba(255,255,255,0.12) 0%, transparent 70%);
    pointer-events: none;
}
.ta-hero-badge {
    display: inline-block;
    font-size: 0.68rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    background: rgba(255,255,255,0.18);
    padding: 0.3rem 0.65rem;
    border-radius: 999px;
    margin-bottom: 0.85rem;
    position: relative;
    z-index: 1;
}
.ta-hero h1 {
    font-size: 1.85rem;
    font-weight: 800;
    margin: 0 0 0.65rem 0;
    line-height: 1.15;
    letter-spacing: -0.04em;
    color: #fff !important;
    position: relative;
    z-index: 1;
}
.ta-hero p {
    font-size: 1rem;
    line-height: 1.6;
    margin: 0;
    color: #e0e7ff !important;
    position: relative;
    z-index: 1;
}
.ta-lead {
    font-size: 1.02rem;
    line-height: 1.65;
    color: #374151;
    margin: 0 0 1.25rem 0;
}

/* ── Benefit cards (Home) ──────────────────────────── */
.ta-benefits {
    display: flex;
    flex-direction: column;
    gap: 0.75rem;
    margin: 0 0 1.5rem 0;
}
.ta-benefit-card {
    background: #fff;
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    padding: 1.15rem 1.2rem;
    box-shadow: 0 2px 8px rgba(15, 23, 42, 0.05);
    display: flex;
    gap: 1rem;
    align-items: flex-start;
    transition: box-shadow 0.15s, border-color 0.15s;
}
.ta-benefit-icon {
    flex-shrink: 0;
    width: 2.5rem;
    height: 2.5rem;
    border-radius: 12px;
    background: linear-gradient(135deg, #eef2ff, #e0e7ff);
    display: flex;
    align-items: center;
    justify-content: center;
    font-size: 1.25rem;
}
.ta-benefit-title {
    font-size: 1rem;
    font-weight: 700;
    color: #111827;
    margin: 0 0 0.25rem 0;
    letter-spacing: -0.02em;
}
.ta-benefit-desc {
    font-size: 0.88rem;
    color: #6b7280;
    line-height: 1.5;
    margin: 0;
}

/* ── Cards ─────────────────────────────────────────── */
.ta-card {
    background: #ffffff;
    border: 1px solid #e8eaed;
    border-radius: 16px;
    padding: 1.15rem 1.2rem;
    margin-bottom: 1rem;
    box-shadow: 0 2px 10px rgba(15, 23, 42, 0.04);
}
.ta-card-accent {
    border-left: 4px solid #4f46e5;
    background: linear-gradient(90deg, #fafaff 0%, #ffffff 12%);
}
.ta-card-title {
    font-size: 0.92rem;
    font-weight: 700;
    color: #111827;
    margin: 0 0 0.4rem 0;
    letter-spacing: -0.01em;
}
.ta-card-body {
    font-size: 0.92rem;
    color: #4b5563;
    line-height: 1.55;
    margin: 0;
}
.ta-card-body strong { color: #1f2937; }

/* ── Practice form panel ───────────────────────────── */
.ta-form-panel {
    background: #f8fafc;
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    padding: 0.25rem 0.5rem 0.5rem;
    margin-bottom: 1.25rem;
    box-shadow: 0 1px 4px rgba(15, 23, 42, 0.04);
}

/* ── Scenario cards v2 ─────────────────────────────── */
.ta-scenario-v2 {
    background: #fff;
    border: 1px solid #e5e7eb;
    border-radius: 18px;
    padding: 0;
    margin-bottom: 1.15rem;
    box-shadow: 0 4px 14px rgba(15, 23, 42, 0.06);
    overflow: hidden;
    transition: border-color 0.2s, box-shadow 0.2s;
}
.ta-scenario-v2.ta-scenario-selected {
    border: 2px solid #4f46e5;
    box-shadow: 0 8px 24px rgba(79, 70, 229, 0.18);
}
.ta-scenario-v2-head {
    padding: 1rem 1.15rem 0.65rem;
    border-bottom: 1px solid #f3f4f6;
}
.ta-scenario-v2-top {
    display: flex;
    align-items: flex-start;
    gap: 0.65rem;
    margin-bottom: 0.55rem;
}
.ta-scenario-num {
    flex-shrink: 0;
    font-size: 0.7rem;
    font-weight: 800;
    color: #4f46e5;
    background: #eef2ff;
    padding: 0.25rem 0.5rem;
    border-radius: 8px;
    letter-spacing: 0.02em;
}
.ta-scenario-v2-title {
    font-size: 1.05rem;
    font-weight: 700;
    color: #111827;
    margin: 0;
    line-height: 1.35;
    letter-spacing: -0.02em;
}
.ta-scenario-badges {
    display: flex;
    flex-wrap: wrap;
    gap: 0.35rem;
}
.ta-badge-diff {
    font-size: 0.72rem;
    font-weight: 700;
    padding: 0.28rem 0.55rem;
    border-radius: 999px;
    letter-spacing: 0.02em;
}
.ta-badge-easy { background: #ecfdf5; color: #047857; border: 1px solid #a7f3d0; }
.ta-badge-mid { background: #fffbeb; color: #b45309; border: 1px solid #fde68a; }
.ta-badge-hard { background: #fef2f2; color: #b91c1c; border: 1px solid #fecaca; }
.ta-badge-skill {
    font-size: 0.72rem;
    font-weight: 600;
    padding: 0.28rem 0.55rem;
    border-radius: 999px;
    background: #f5f3ff;
    color: #5b21b6;
    border: 1px solid #ddd6fe;
}
.ta-scenario-v2-body {
    padding: 0.85rem 1.15rem 1rem;
    font-size: 0.9rem;
    color: #4b5563;
    line-height: 1.55;
}
.ta-scenario-v2-question {
    margin-top: 0.75rem;
    padding: 0.85rem 1rem;
    background: #f8fafc;
    border-radius: 12px;
    border-left: 3px solid #4f46e5;
    font-size: 0.92rem;
    color: #1f2937;
    font-weight: 600;
    line-height: 1.5;
}
.ta-scenario-label {
    font-size: 0.68rem;
    font-weight: 700;
    color: #9ca3af;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    margin: 0.5rem 0 0.2rem 0;
}
.ta-scenario-v2-actions {
    padding: 0 1rem 1rem;
}

/* ── Section titles ────────────────────────────────── */
.ta-section-title {
    font-size: 1.08rem;
    font-weight: 700;
    color: #111827;
    margin: 1.5rem 0 0.5rem 0;
    letter-spacing: -0.02em;
}
.ta-section-sub {
    font-size: 0.85rem;
    color: #6b7280;
    margin: -0.25rem 0 0.85rem 0;
    line-height: 1.45;
}

/* ── Page header ─────────────────────────────────────── */
.ta-page-header h2 {
    font-size: 1.4rem;
    font-weight: 800;
    color: #111827;
    margin: 0 0 0.35rem 0;
    letter-spacing: -0.03em;
}
.ta-page-header p {
    font-size: 0.92rem;
    color: #6b7280;
    margin: 0 0 1.1rem 0;
    line-height: 1.5;
}

/* ── Steps ─────────────────────────────────────────── */
.ta-steps { display: flex; flex-direction: column; gap: 0.65rem; }
.ta-step {
    display: flex;
    align-items: flex-start;
    gap: 0.75rem;
    background: #fff;
    border: 1px solid #e5e7eb;
    border-radius: 14px;
    padding: 0.9rem 1rem;
    box-shadow: 0 1px 4px rgba(15, 23, 42, 0.04);
}
.ta-step-num {
    flex-shrink: 0;
    width: 1.85rem;
    height: 1.85rem;
    background: #eef2ff;
    color: #4f46e5;
    font-weight: 800;
    font-size: 0.82rem;
    border-radius: 50%;
    display: flex;
    align-items: center;
    justify-content: center;
}
.ta-step-text { font-size: 0.9rem; color: #374151; line-height: 1.5; margin: 0.1rem 0 0 0; }
.ta-step-text strong { color: #111827; }

/* ── Chips ─────────────────────────────────────────── */
.ta-chips { display: flex; flex-wrap: wrap; gap: 0.4rem; margin: 0.5rem 0; }
.ta-chip {
    font-size: 0.75rem;
    font-weight: 600;
    padding: 0.32rem 0.62rem;
    border-radius: 999px;
    background: #f3f4f6;
    color: #374151;
    border: 1px solid #e5e7eb;
}

/* ── Score display ───────────────────────────────────── */
.ta-score-panel {
    background: linear-gradient(180deg, #fafaff 0%, #ffffff 100%);
    border: 1px solid #e0e7ff;
    border-radius: 20px;
    padding: 1.35rem 1.25rem 1.15rem;
    margin-bottom: 1.25rem;
    box-shadow: 0 4px 20px rgba(79, 70, 229, 0.08);
    text-align: center;
}
.ta-score-hero-wrap { text-align: center; margin: 0; }
.ta-score-hero {
    display: inline-flex;
    flex-direction: column;
    align-items: center;
    padding: 0.5rem 1rem;
}
.ta-score-hero-value {
    font-size: 3.25rem;
    font-weight: 800;
    line-height: 1;
    letter-spacing: -0.04em;
}
.ta-score-hero-label {
    font-size: 0.78rem;
    font-weight: 700;
    color: #6366f1;
    margin-top: 0.4rem;
    text-transform: uppercase;
    letter-spacing: 0.06em;
}
.ta-score-session-text {
    font-size: 1.05rem;
    font-weight: 700;
    color: #374151;
    margin: 0.5rem 0 0 0;
}
.ta-score-row {
    display: flex;
    flex-wrap: wrap;
    gap: 0.5rem;
    margin: 0.5rem 0;
    justify-content: center;
}
.ta-score-badge {
    display: inline-flex;
    flex-direction: column;
    align-items: center;
    min-width: 4.25rem;
    padding: 0.55rem 0.7rem;
    border-radius: 12px;
    border: 1px solid #e5e7eb;
    background: #fff;
    box-shadow: 0 1px 3px rgba(15, 23, 42, 0.04);
}
.ta-score-badge-value { font-size: 1.3rem; font-weight: 800; line-height: 1.1; }
.ta-score-badge-label { font-size: 0.65rem; color: #6b7280; margin-top: 0.2rem; text-align: center; font-weight: 600; }
.ta-score-high .ta-score-badge-value { color: #059669; }
.ta-score-mid .ta-score-badge-value { color: #d97706; }
.ta-score-low .ta-score-badge-value { color: #dc2626; }

.ta-criterion-row { margin-bottom: 0.9rem; }
.ta-criterion-head {
    display: flex;
    justify-content: space-between;
    align-items: baseline;
    margin-bottom: 0.3rem;
    gap: 0.5rem;
}
.ta-criterion-name { font-size: 0.9rem; font-weight: 600; color: #374151; }
.ta-criterion-val { font-size: 0.85rem; font-weight: 700; color: #4f46e5; flex-shrink: 0; }

/* ── Insight hero (Feedback) ─────────────────────────── */
.ta-insight-hero {
    background: linear-gradient(135deg, #fff7ed 0%, #ffedd5 50%, #fed7aa 100%);
    border: 2px solid #fb923c;
    border-radius: 18px;
    padding: 1.25rem 1.2rem;
    margin: 0 0 1.35rem 0;
    box-shadow: 0 6px 24px rgba(234, 88, 12, 0.15);
}
.ta-insight-hero-title {
    font-size: 0.75rem;
    font-weight: 800;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    color: #c2410c;
    margin: 0 0 0.65rem 0;
}
.ta-insight-hero ul {
    margin: 0;
    padding-left: 1.15rem;
    color: #9a3412;
}
.ta-insight-hero li {
    font-size: 0.95rem;
    line-height: 1.55;
    margin-bottom: 0.35rem;
    font-weight: 500;
}

/* ── Quote card (closing line) ─────────────────────── */
.ta-quote-card {
    position: relative;
    background: #fff;
    border: none;
    border-radius: 16px;
    padding: 1.5rem 1.35rem 1.35rem 1.5rem;
    margin: 0.85rem 0 1.25rem;
    box-shadow: 0 4px 16px rgba(15, 23, 42, 0.08);
    border-left: 5px solid #4f46e5;
}
.ta-quote-card::before {
    content: '"';
    position: absolute;
    top: 0.35rem;
    left: 0.75rem;
    font-size: 2.5rem;
    font-weight: 800;
    color: #c7d2fe;
    line-height: 1;
    font-family: Georgia, serif;
}
.ta-quote-text {
    font-size: 1.08rem;
    font-weight: 600;
    color: #1e293b;
    line-height: 1.55;
    margin: 0;
    padding-left: 1.25rem;
    font-style: italic;
}
.ta-quote-label {
    font-size: 0.72rem;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.06em;
    color: #6366f1;
    margin: 0 0 0.5rem 0;
    padding-left: 1.25rem;
}

/* ── Copy-friendly script blocks ───────────────────── */
.ta-copy-section-label {
    font-size: 0.88rem;
    font-weight: 700;
    color: #374151;
    margin: 0.85rem 0 0.35rem 0;
}
.ta-copy-hint {
    font-size: 0.78rem;
    color: #6b7280;
    margin: 0 0 0.75rem 0;
}

/* ── Info boxes ──────────────────────────────────────── */
.ta-info {
    border-radius: 14px;
    padding: 0.9rem 1.05rem;
    font-size: 0.9rem;
    line-height: 1.55;
    margin: 0.75rem 0;
    border: 1px solid transparent;
}
.ta-info-info { background: #eff6ff; border-color: #bfdbfe; color: #1e40af; }
.ta-info-success { background: #ecfdf5; border-color: #a7f3d0; color: #065f46; }
.ta-info-warning { background: #fffbeb; border-color: #fde68a; color: #92400e; }
.ta-info-neutral { background: #f9fafb; border-color: #e5e7eb; color: #4b5563; }

.ta-insight-highlight {
    background: linear-gradient(135deg, #fff7ed 0%, #ffedd5 100%);
    border: 1px solid #fdba74;
    border-radius: 14px;
    padding: 1rem 1.1rem;
    margin: 0.75rem 0;
    box-shadow: 0 2px 12px rgba(234, 88, 12, 0.1);
}
.ta-closing-highlight {
    background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
    border: 2px solid #6ee7b7;
    border-radius: 14px;
    padding: 1.1rem 1.15rem;
    margin: 0.75rem 0;
    font-size: 1.05rem;
    font-weight: 600;
    color: #065f46;
    line-height: 1.5;
    text-align: center;
}
.ta-counter-box {
    background: #f5f3ff;
    border: 1px solid #c4b5fd;
    border-radius: 14px;
    padding: 1rem 1.1rem;
    margin: 0.65rem 0;
}

/* ── Streamlit widgets ─────────────────────────────── */
.stButton > button {
    min-height: 3.1rem;
    border-radius: 14px !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    padding: 0.65rem 1.25rem !important;
    width: 100%;
    transition: transform 0.1s, box-shadow 0.15s;
    letter-spacing: -0.01em;
}
.stButton > button[kind="primary"] {
    box-shadow: 0 4px 14px rgba(79, 70, 229, 0.25) !important;
}
.stButton > button:active { transform: scale(0.98); }
.stTextInput > div > div > input,
.stTextArea textarea,
.stSelectbox > div > div {
    border-radius: 12px !important;
    font-size: 0.95rem !important;
    border-color: #e5e7eb !important;
}
div[data-testid="stVerticalBlock"] > div[style*="flex-direction: row"] {
    flex-wrap: wrap !important;
}
[data-testid="stCodeBlock"] {
    border-radius: 12px !important;
}

@media (max-width: 768px) {
    .main .block-container {
        padding-left: 0.85rem;
        padding-right: 0.85rem;
    }
    .ta-hero { padding: 1.65rem 1.2rem; }
    .ta-hero h1 { font-size: 1.55rem; }
    .ta-score-hero-value { font-size: 2.75rem; }
}
</style>
"""
