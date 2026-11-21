from __future__ import annotations

from html import escape

import streamlit as st


def apply_dashboard_style() -> None:
    """Áp dụng kiểu hiển thị dùng chung cho các trang dashboard."""
    st.markdown(
        """
        <style>
        :root {
            --asm-navy: #10263f;
            --asm-blue: #2458a6;
            --asm-teal: #07838a;
            --asm-ink: #172b42;
            --asm-muted: #60738a;
            --asm-line: #dce5ee;
            --asm-surface: #ffffff;
            --asm-canvas: #f5f7fa;
            --asm-shadow: 0 8px 24px rgba(16, 38, 63, .055);
        }
        html, body, [class*="css"] { font-family: "Segoe UI", "Inter", sans-serif; }
        [data-testid="stAppViewContainer"] {
            background: var(--asm-canvas);
            color: var(--asm-ink);
        }
        [data-testid="stHeader"] {
            background: rgba(245, 247, 250, .92);
            border-bottom: 1px solid rgba(220, 229, 238, .7);
        }
        [data-testid="stSidebar"] {
            background: linear-gradient(180deg, #10263f 0%, #153552 100%);
            border-right: 1px solid rgba(255,255,255,.08);
        }
        [data-testid="stSidebar"] * {
            color: #edf4ff;
        }
        [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {
            color: #b9c8dc;
        }
        [data-testid="stSidebarNav"] {
            padding: .65rem .4rem 0;
        }
        [data-testid="stSidebarNav"] a[aria-current="page"] {
            background: rgba(83, 190, 196, .19);
            border: 1px solid rgba(131, 226, 223, .2);
            border-radius: .7rem;
        }
        [data-testid="stSidebarNav"] a:hover {
            background: rgba(110, 168, 255, .12);
            border-radius: .7rem;
        }
        .block-container {
            max-width: 1440px;
            padding-top: 1.8rem;
            padding-bottom: 3.5rem;
        }
        h1, h2, h3 {
            color: var(--asm-ink);
            letter-spacing: -0.025em;
        }
        h1 {
            font-weight: 740;
        }
        h2 { font-weight: 700; }
        p, li { line-height: 1.62; }
        [data-testid="stCaptionContainer"] { color: var(--asm-muted); }
        [data-testid="stMetric"] {
            background: var(--asm-surface);
            border: 1px solid var(--asm-line);
            padding: 1.05rem 1.15rem;
            border-radius: 1rem;
            box-shadow: var(--asm-shadow);
            min-height: 108px;
        }
        [data-testid="stMetricLabel"] p {
            color: var(--asm-muted);
            font-size: .84rem;
            font-weight: 620;
        }
        [data-testid="stMetricValue"] {
            color: var(--asm-ink);
            font-size: 1.55rem;
            font-weight: 720;
            letter-spacing: -.035em;
        }
        [data-testid="stVerticalBlockBorderWrapper"] {
            background: var(--asm-surface);
            border-color: var(--asm-line);
            border-radius: 1rem;
            box-shadow: 0 3px 12px rgba(16, 38, 63, .025);
        }
        [data-testid="stDataFrame"] {
            border: 1px solid var(--asm-line);
            border-radius: .75rem;
            overflow: hidden;
            background: white;
        }
        [data-testid="stAlert"] {
            border-radius: .85rem;
            border-width: 1px;
        }
        [data-testid="stTabs"] [role="tablist"] {
            gap: .35rem;
            border-bottom: 1px solid var(--asm-line);
        }
        [data-testid="stTabs"] button[role="tab"] {
            border-radius: .65rem .65rem 0 0;
            font-weight: 620;
        }
        [data-testid="stTextInput"] input, [data-testid="stSelectbox"] [data-baseweb="select"],
        [data-testid="stDateInput"] input, [data-testid="stMultiSelect"] [data-baseweb="select"] {
            border-radius: .65rem;
        }
        .stButton > button, .stDownloadButton > button {
            border-radius: .7rem;
            font-weight: 650;
            min-height: 2.7rem;
            transition: transform .15s ease, box-shadow .15s ease;
        }
        .stButton > button[kind="primary"] {
            background: linear-gradient(110deg, #176b79, #087f8c);
            border-color: #087f8c;
            box-shadow: 0 5px 12px rgba(8, 127, 140, .16);
        }
        .stButton > button:hover, .stDownloadButton > button:hover {
            transform: translateY(-1px);
            box-shadow: 0 6px 14px rgba(16, 38, 63, .1);
        }
        [data-testid="stExpander"] {
            border: 1px solid var(--asm-line);
            border-radius: .85rem;
            background: white;
        }
        .sidebar-brand {
            display: flex;
            align-items: center;
            gap: 0.7rem;
            padding: .7rem .15rem 1.05rem;
            border-bottom: 1px solid rgba(255,255,255,.12);
            margin-bottom: .8rem;
        }
        .sidebar-brand-icon {
            display: grid;
            place-items: center;
            width: 2.6rem;
            height: 2.6rem;
            border-radius: 0.8rem;
            background: rgba(111, 177, 255, 0.18);
            font-size: 1.35rem;
        }
        .sidebar-brand-title {
            color: #ffffff;
            font-size: 0.98rem;
            font-weight: 720;
        }
        .sidebar-brand-caption {
            color: #b9c8dc;
            font-size: 0.78rem;
            margin-top: 0.12rem;
        }
        .page-hero {
            position: relative;
            overflow: hidden;
            background: linear-gradient(115deg, #10263f 0%, #17456c 60%, #087f8c 120%);
            border: 1px solid rgba(255,255,255,0.12);
            border-radius: 1.15rem;
            padding: 1.55rem 1.8rem 1.65rem;
            margin: 0 0 1.35rem;
            box-shadow: 0 12px 28px rgba(16, 38, 63, .12);
        }
        .page-hero-kicker {
            color: #a5e1df;
            text-transform: uppercase;
            font-size: 0.73rem;
            font-weight: 700;
            letter-spacing: 0.12em;
            margin-bottom: 0.45rem;
        }
        .page-hero-title {
            color: #ffffff;
            font-size: clamp(1.65rem, 3vw, 2.25rem);
            line-height: 1.15;
            font-weight: 760;
            margin: 0;
        }
        .page-hero-description {
            color: #d6e3f2;
            font-size: 0.98rem;
            line-height: 1.55;
            max-width: 920px;
            margin: 0.65rem 0 0 0;
        }
        .section-kicker {
            color: var(--asm-teal);
            font-size: 0.72rem;
            text-transform: uppercase;
            letter-spacing: 0.11em;
            font-weight: 750;
            margin: .25rem 0 .3rem;
        }
        .status-line {
            display: flex;
            align-items: center;
            gap: 0.55rem;
            color: var(--asm-ink);
            font-weight: 620;
            margin: 0.2rem 0;
        }
        .status-dot {
            width: 0.55rem;
            height: 0.55rem;
            border-radius: 50%;
            background: #93a1b2;
            flex: 0 0 auto;
        }
        .status-dot.done {
            background: #15966b;
        }
        .status-dot.pending {
            background: #d39a2c;
        }
        .ticker-chip {
            display: inline-block;
            background: #edf3fb;
            color: #1c477d;
            border: 1px solid #dce7f4;
            border-radius: 0.55rem;
            padding: 0.35rem 0.65rem;
            margin: 0.18rem;
            font-size: 0.86rem;
            font-weight: 700;
        }
        .muted-copy {
            color: var(--asm-muted);
            font-size: 0.9rem;
            line-height: 1.55;
        }
        .brand-stamp {
            color: #b5eee9;
            font-size: .72rem;
            font-weight: 700;
            letter-spacing: .06em;
            text-transform: uppercase;
        }
        .quick-link-grid {
            display: grid;
            grid-template-columns: repeat(3, minmax(0, 1fr));
            gap: .8rem;
            margin: .4rem 0 1.2rem;
        }
        .quick-link {
            display: grid;
            grid-template-columns: 2.15rem 1fr;
            align-items: center;
            column-gap: .65rem;
            padding: .85rem 1rem;
            background: white;
            border: 1px solid var(--asm-line);
            border-radius: .85rem;
            color: var(--asm-ink) !important;
            text-decoration: none !important;
            box-shadow: 0 3px 12px rgba(16, 38, 63, .03);
            transition: transform .15s ease, border-color .15s ease, box-shadow .15s ease;
        }
        .quick-link:hover {
            transform: translateY(-2px);
            border-color: #80c8c9;
            box-shadow: var(--asm-shadow);
        }
        .quick-link span { grid-row: span 2; font-size: 1.35rem; }
        .quick-link strong { font-size: .94rem; }
        .quick-link small { color: var(--asm-muted); font-size: .78rem; }
        @media (max-width: 760px) {
            .block-container { padding: 1rem 1rem 2.5rem; }
            .page-hero { padding: 1.2rem 1.15rem; border-radius: .9rem; }
            [data-testid="stMetric"] { min-height: 90px; padding: .8rem; }
            .quick-link-grid { grid-template-columns: 1fr; }
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_page_header(section: str, title: str, description: str) -> None:
    st.markdown(
        f"""
        <div class="page-hero">
            <div class="page-hero-kicker">{escape(section)}</div>
            <h1 class="page-hero-title">{escape(title)}</h1>
            <p class="page-hero-description">{escape(description)}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section_heading(title: str, caption: str | None = None) -> None:
    st.markdown(f'<div class="section-kicker">{escape(title)}</div>', unsafe_allow_html=True)
    if caption:
        st.markdown(f'<div class="muted-copy">{escape(caption)}</div>', unsafe_allow_html=True)


def render_empty_panel(title: str, description: str) -> None:
    with st.container(border=True):
        st.markdown(f"**{title}**")
        st.markdown(f'<div class="muted-copy">{escape(description)}</div>', unsafe_allow_html=True)
