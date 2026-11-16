"""Global look-and-feel for the Career Plan Monitor.

A light, friendly palette — soft surfaces, rounded corners, gentle accents,
and warm highlights so the app feels approachable rather than technical.
"""

from __future__ import annotations

import streamlit as st

ACCENT = "#5B8DEF"
TEAL = "#2EC4A8"
AMBER = "#F2B134"
ROSE = "#F06A7C"
VIOLET = "#9B86F0"

PALETTE = {
    "accent": ACCENT,
    "teal": TEAL,
    "amber": AMBER,
    "rose": ROSE,
    "violet": VIOLET,
}

TONE_COLORS = {
    "accent": ACCENT,
    "teal": TEAL,
    "amber": AMBER,
    "rose": ROSE,
    "violet": VIOLET,
    "muted": "#7C8AA3",
}

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

:root {
    --cp-bg: #F4F6FB;
    --cp-surface: #FFFFFF;
    --cp-surface-2: #EEF2F9;
    --cp-border: #E2E8F3;
    --cp-border-strong: #BFD0EE;
    --cp-text: #1F2A3D;
    --cp-muted: #7C8AA3;
    --cp-accent: #5B8DEF;
    --cp-teal: #2EC4A8;
    --cp-amber: #F2B134;
    --cp-rose: #F06A7C;
    --cp-violet: #9B86F0;
    --cp-radius: 16px;
}

html, body, [class*="css"], .stApp, button, input, textarea, select {
    font-family: 'Inter', 'Segoe UI', system-ui, -apple-system, sans-serif;
}

.stApp {
    background:
        radial-gradient(1100px 620px at 12% -8%, rgba(91, 141, 239, 0.10), transparent 62%),
        radial-gradient(900px 520px at 92% 4%, rgba(46, 196, 168, 0.08), transparent 60%),
        radial-gradient(760px 520px at 60% 108%, rgba(155, 134, 240, 0.07), transparent 62%),
        var(--cp-bg);
}

header[data-testid="stHeader"] {
    background: transparent;
    height: 0;
}

#MainMenu, footer, [data-testid="stToolbar"] {
    visibility: hidden;
}

.block-container {
    padding-top: 1.4rem;
    padding-bottom: 3rem;
    max-width: 1500px;
}

::-webkit-scrollbar { width: 10px; height: 10px; }
::-webkit-scrollbar-track { background: transparent; }
::-webkit-scrollbar-thumb {
    background: rgba(124, 138, 163, 0.30);
    border-radius: 999px;
    border: 2px solid transparent;
    background-clip: content-box;
}
::-webkit-scrollbar-thumb:hover { background: rgba(124, 138, 163, 0.50); background-clip: content-box; }

::selection { background: rgba(91, 141, 239, 0.25); }

/* ---------------------------------------------------------------- sidebar */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #FFFFFF 0%, #F7F9FD 100%);
    border-right: 1px solid var(--cp-border);
}

section[data-testid="stSidebar"] > div {
    padding-top: 1.1rem;
}

section[data-testid="stSidebar"] hr {
    margin: 0.85rem 0;
    border-color: var(--cp-border);
}

section[data-testid="stSidebar"] div[role="radiogroup"] {
    gap: 0.18rem;
}

section[data-testid="stSidebar"] div[role="radiogroup"] > label {
    display: flex;
    align-items: center;
    width: 100%;
    padding: 0.52rem 0.72rem;
    margin: 0;
    border-radius: 0.7rem;
    border: 1px solid transparent;
    cursor: pointer;
    transition: background 180ms ease, border-color 180ms ease, transform 180ms ease;
}

section[data-testid="stSidebar"] div[role="radiogroup"] > label:hover {
    background: rgba(91, 141, 239, 0.08);
    border-color: rgba(91, 141, 239, 0.20);
    transform: translateX(2px);
}

section[data-testid="stSidebar"] div[role="radiogroup"] > label:has(input:checked) {
    background: linear-gradient(90deg, rgba(91, 141, 239, 0.14), rgba(91, 141, 239, 0.03));
    border-color: var(--cp-border-strong);
}

section[data-testid="stSidebar"] div[role="radiogroup"] > label > div:first-child {
    display: none;
}

section[data-testid="stSidebar"] div[role="radiogroup"] > label p {
    font-size: 0.885rem;
    font-weight: 500;
    letter-spacing: 0.01em;
    color: var(--cp-text);
}

/* ------------------------------------------------------------------ brand */
.cp-brand {
    display: flex;
    align-items: center;
    gap: 0.7rem;
    padding: 0.2rem 0.2rem 0.9rem 0.2rem;
}

.cp-brand-avatar {
    width: 42px;
    height: 42px;
    flex: 0 0 42px;
    border-radius: 13px;
    display: grid;
    place-items: center;
    font-weight: 700;
    font-size: 0.95rem;
    letter-spacing: 0.02em;
    color: #FFFFFF;
    background: linear-gradient(140deg, #5B8DEF, #2EC4A8);
    box-shadow: 0 8px 20px rgba(46, 196, 168, 0.22);
}

.cp-brand-name {
    font-weight: 650;
    font-size: 0.94rem;
    line-height: 1.15;
    color: var(--cp-text);
}

.cp-brand-sub {
    font-size: 0.74rem;
    color: var(--cp-muted);
    letter-spacing: 0.02em;
}

/* --------------------------------------------------------------- hero */
.cp-hero {
    position: relative;
    overflow: hidden;
    border-radius: 22px;
    border: 1px solid var(--cp-border);
    background:
        radial-gradient(720px 340px at 6% -30%, rgba(91, 141, 239, 0.18), transparent 60%),
        radial-gradient(600px 300px at 100% 0%, rgba(46, 196, 168, 0.14), transparent 58%),
        linear-gradient(155deg, #FFFFFF 0%, #F1F5FC 78%);
    padding: 1.6rem 1.8rem 1.5rem 1.8rem;
    margin-bottom: 1.1rem;
    animation: cpFade 320ms ease-out;
    box-shadow: 0 10px 30px rgba(31, 42, 61, 0.06);
}

.cp-hero::after {
    content: "";
    position: absolute;
    inset: 0;
    background-image:
        linear-gradient(rgba(91, 141, 239, 0.05) 1px, transparent 1px),
        linear-gradient(90deg, rgba(91, 141, 239, 0.05) 1px, transparent 1px);
    background-size: 46px 46px;
    mask-image: radial-gradient(circle at 20% 0%, black, transparent 72%);
    pointer-events: none;
}

.cp-hero-inner { position: relative; z-index: 1; }

.cp-eyebrow {
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 0.16em;
    text-transform: uppercase;
    color: var(--cp-teal);
    margin-bottom: 0.5rem;
}

.cp-hero h1 {
    font-size: 2.05rem;
    line-height: 1.12;
    font-weight: 750;
    margin: 0 0 0.45rem 0;
    background: linear-gradient(96deg, #1F2A3D 8%, #5B8DEF 52%, #2EC4A8 96%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
    color: transparent;
}

.cp-hero p {
    color: #5A6780;
    font-size: 0.95rem;
    max-width: 78ch;
    margin: 0 0 0.9rem 0;
    line-height: 1.55;
}

.cp-chip-row { display: flex; flex-wrap: wrap; gap: 0.45rem; }

.cp-chip {
    display: inline-flex;
    align-items: center;
    gap: 0.35rem;
    padding: 0.3rem 0.68rem;
    border-radius: 999px;
    font-size: 0.76rem;
    font-weight: 500;
    color: #4A5770;
    background: #EEF2F9;
    border: 1px solid #E2E8F3;
}

.cp-chip b { color: #1F2A3D; font-weight: 650; }

/* ------------------------------------------------------------ section bar */
.cp-section {
    display: flex;
    align-items: flex-start;
    gap: 0.65rem;
    margin: 1.4rem 0 0.7rem 0;
}

.cp-section-bar {
    width: 4px;
    min-height: 34px;
    border-radius: 4px;
    background: linear-gradient(180deg, var(--cp-accent), var(--cp-teal));
    margin-top: 2px;
}

.cp-section-title {
    font-size: 1.06rem;
    font-weight: 650;
    color: var(--cp-text);
    line-height: 1.25;
}

.cp-section-sub {
    font-size: 0.79rem;
    color: var(--cp-muted);
    margin-top: 0.1rem;
}

/* ---------------------------------------------------------------- cards */
.cp-card {
    border-radius: var(--cp-radius);
    border: 1px solid var(--cp-border);
    background: #FFFFFF;
    padding: 1rem 1.1rem;
    height: 100%;
    box-shadow: 0 4px 14px rgba(31, 42, 61, 0.04);
    transition: transform 180ms ease, border-color 180ms ease, box-shadow 180ms ease;
}

.cp-card:hover {
    transform: translateY(-2px);
    border-color: var(--cp-border-strong);
    box-shadow: 0 12px 26px rgba(31, 42, 61, 0.08);
}

.cp-card-title {
    font-size: 0.95rem;
    font-weight: 600;
    color: var(--cp-text);
    margin-bottom: 0.3rem;
    line-height: 1.3;
}

.cp-card-text {
    font-size: 0.83rem;
    color: #5A6780;
    line-height: 1.52;
}

/* ------------------------------------------------------------------ kpi */
.cp-kpi {
    position: relative;
    overflow: hidden;
    border-radius: var(--cp-radius);
    border: 1px solid var(--cp-border);
    background: #FFFFFF;
    padding: 0.9rem 1rem 0.95rem 1rem;
    height: 100%;
    box-shadow: 0 4px 14px rgba(31, 42, 61, 0.04);
    animation: cpRise 300ms ease-out both;
}

.cp-kpi::before {
    content: "";
    position: absolute;
    left: 0;
    top: 0;
    bottom: 0;
    width: 3px;
    background: var(--cp-accent);
    opacity: 0.9;
}

.cp-kpi.tone-teal::before { background: var(--cp-teal); }
.cp-kpi.tone-amber::before { background: var(--cp-amber); }
.cp-kpi.tone-rose::before { background: var(--cp-rose); }
.cp-kpi.tone-violet::before { background: var(--cp-violet); }
.cp-kpi.tone-muted::before { background: #9AA7BC; }

.cp-kpi-label {
    font-size: 0.73rem;
    font-weight: 550;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    color: var(--cp-muted);
    margin-bottom: 0.35rem;
}

.cp-kpi-value {
    font-size: 1.72rem;
    font-weight: 700;
    line-height: 1;
    color: var(--cp-text);
    letter-spacing: -0.02em;
}

.cp-kpi-value small {
    font-size: 0.85rem;
    font-weight: 500;
    color: var(--cp-muted);
    margin-left: 0.15rem;
}

.cp-kpi-sub {
    font-size: 0.76rem;
    color: var(--cp-muted);
    margin-top: 0.4rem;
    line-height: 1.4;
}

/* --------------------------------------------------------------- badges */
.cp-badge {
    display: inline-flex;
    align-items: center;
    gap: 0.28rem;
    padding: 0.16rem 0.5rem;
    border-radius: 999px;
    font-size: 0.71rem;
    font-weight: 600;
    letter-spacing: 0.02em;
    border: 1px solid transparent;
    white-space: nowrap;
}

.cp-badge.tone-accent { color: #2E5FBD; background: rgba(91, 141, 239, 0.12); border-color: rgba(91, 141, 239, 0.26); }
.cp-badge.tone-teal   { color: #1E8E7A; background: rgba(46, 196, 168, 0.13); border-color: rgba(46, 196, 168, 0.28); }
.cp-badge.tone-amber  { color: #A97816; background: rgba(242, 177, 52, 0.14); border-color: rgba(242, 177, 52, 0.30); }
.cp-badge.tone-rose   { color: #C13A4E; background: rgba(240, 106, 124, 0.13); border-color: rgba(240, 106, 124, 0.28); }
.cp-badge.tone-violet { color: #6B55C4; background: rgba(155, 134, 240, 0.13); border-color: rgba(155, 134, 240, 0.28); }
.cp-badge.tone-muted  { color: #5A6780; background: #EEF2F9; border-color: #E2E8F3; }

/* -------------------------------------------------------------- timeline */
.cp-timeline { position: relative; padding-left: 1.4rem; }

.cp-timeline::before {
    content: "";
    position: absolute;
    left: 0.38rem;
    top: 0.5rem;
    bottom: 0.4rem;
    width: 2px;
    background: linear-gradient(180deg, rgba(91, 141, 239, 0.55), rgba(46, 196, 168, 0.28), transparent);
}

.cp-tl-item { position: relative; padding-bottom: 0.95rem; }

.cp-tl-item::before {
    content: "";
    position: absolute;
    left: -1.19rem;
    top: 0.34rem;
    width: 11px;
    height: 11px;
    border-radius: 50%;
    background: #FFFFFF;
    border: 2px solid var(--cp-accent);
    box-shadow: 0 0 0 4px rgba(91, 141, 239, 0.12);
}

.cp-tl-period {
    font-size: 0.7rem;
    font-weight: 650;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: var(--cp-teal);
}

.cp-tl-title {
    font-size: 0.94rem;
    font-weight: 620;
    color: var(--cp-text);
    margin: 0.08rem 0 0.24rem 0;
}

.cp-tl-text {
    font-size: 0.83rem;
    line-height: 1.55;
    color: #5A6780;
}

/* ------------------------------------------------------------- rows/list */
.cp-row {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 0.9rem;
    padding: 0.62rem 0.8rem;
    border-radius: 11px;
    border: 1px solid var(--cp-border);
    background: #FFFFFF;
    margin-bottom: 0.42rem;
    transition: background 160ms ease, border-color 160ms ease;
}

.cp-row:hover { background: rgba(91, 141, 239, 0.05); border-color: var(--cp-border-strong); }

.cp-row-main { min-width: 0; }

.cp-row-title {
    font-size: 0.86rem;
    font-weight: 550;
    color: var(--cp-text);
    line-height: 1.35;
}

.cp-row-meta {
    font-size: 0.74rem;
    color: var(--cp-muted);
    margin-top: 0.14rem;
}

.cp-row-side { display: flex; align-items: center; gap: 0.45rem; flex: 0 0 auto; }

/* ------------------------------------------------------------- progress */
.cp-bar {
    height: 7px;
    border-radius: 999px;
    background: #E8EDF5;
    overflow: hidden;
}

.cp-bar > span {
    display: block;
    height: 100%;
    border-radius: 999px;
    background: linear-gradient(90deg, var(--cp-accent), var(--cp-teal));
    transition: width 420ms cubic-bezier(0.22, 1, 0.36, 1);
}

.cp-bar.tone-amber > span { background: linear-gradient(90deg, #F2B134, #F4915B); }
.cp-bar.tone-violet > span { background: linear-gradient(90deg, #9B86F0, #5B8DEF); }

.cp-legend {
    display: flex;
    justify-content: space-between;
    font-size: 0.76rem;
    color: var(--cp-muted);
    margin-bottom: 0.3rem;
}

.cp-legend b { color: var(--cp-text); font-weight: 600; }

/* -------------------------------------------------------------- goal board */
.cp-board {
    border-radius: var(--cp-radius);
    border: 1px solid var(--cp-border);
    background: #F7F9FD;
    padding: 0.75rem 0.8rem;
    min-height: 120px;
}

.cp-board-head {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 0.6rem;
}

.cp-board-name {
    font-size: 0.79rem;
    font-weight: 650;
    letter-spacing: 0.05em;
    text-transform: uppercase;
    color: #4A5770;
}

.cp-mini {
    border-radius: 10px;
    border: 1px solid var(--cp-border);
    background: #FFFFFF;
    padding: 0.55rem 0.65rem;
    margin-bottom: 0.4rem;
    box-shadow: 0 2px 8px rgba(31, 42, 61, 0.04);
}

.cp-mini-title {
    font-size: 0.8rem;
    font-weight: 550;
    color: var(--cp-text);
    line-height: 1.32;
    margin-bottom: 0.35rem;
}

/* ------------------------------------------------------------- skeleton */
.cp-skel {
    border-radius: 14px;
    border: 1px solid var(--cp-border);
    background: #FFFFFF;
    padding: 1rem 1.1rem;
}

.cp-skel-label {
    font-size: 0.76rem;
    color: var(--cp-muted);
    margin-bottom: 0.7rem;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}

.cp-skel-line, .cp-skel-block, .cp-skel-ring {
    background: linear-gradient(90deg, #EEF2F9 8%, #E0E7F2 20%, #EEF2F9 34%);
    background-size: 260% 100%;
    animation: cpShimmer 1.25s linear infinite;
}

.cp-skel-line { height: 11px; border-radius: 6px; margin-bottom: 0.5rem; }
.cp-skel-block { height: 74px; border-radius: 12px; margin-bottom: 0.5rem; }
.cp-skel-row { display: flex; gap: 0.6rem; margin-bottom: 0.6rem; }
.cp-skel-ring { height: 118px; flex: 1; border-radius: 14px; }

@keyframes cpShimmer {
    0% { background-position: 130% 0; }
    100% { background-position: -30% 0; }
}

@keyframes cpFade {
    from { opacity: 0; }
    to { opacity: 1; }
}

@keyframes cpRise {
    from { opacity: 0; transform: translateY(6px); }
    to { opacity: 1; transform: none; }
}

/* --------------------------------------------------------- streamlit bits */
div[data-testid="stVerticalBlockBorderWrapper"] {
    border-radius: var(--cp-radius);
}

.stButton > button {
    border-radius: 10px;
    font-weight: 550;
    border: 1px solid var(--cp-border);
    transition: transform 150ms ease, border-color 150ms ease, background 150ms ease;
}

.stButton > button:hover {
    transform: translateY(-1px);
    border-color: var(--cp-border-strong);
}

.stButton > button[kind="primary"] {
    background: linear-gradient(100deg, #5B8DEF, #2EC4A8);
    border: none;
    color: #FFFFFF;
    font-weight: 650;
    box-shadow: 0 10px 24px rgba(91, 141, 239, 0.22);
}

.stButton > button[kind="primary"]:hover {
    box-shadow: 0 14px 28px rgba(91, 141, 239, 0.32);
}

.stTextInput input, .stTextArea textarea, .stNumberInput input,
div[data-baseweb="select"] > div {
    border-radius: 10px !important;
    background: #FFFFFF !important;
}

.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--cp-border-strong) !important;
    box-shadow: 0 0 0 3px rgba(91, 141, 239, 0.14) !important;
}

div[data-testid="stDataEditor"], div[data-testid="stDataFrame"] {
    border-radius: 14px;
    overflow: hidden;
    border: 1px solid var(--cp-border);
}

div[data-testid="stExpander"] details {
    border-radius: 13px;
    border: 1px solid var(--cp-border);
    background: #FFFFFF;
    overflow: hidden;
}

div[data-testid="stExpander"] summary {
    font-weight: 550;
    font-size: 0.88rem;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 0.35rem;
    border-bottom: 1px solid var(--cp-border);
}

.stTabs [data-baseweb="tab"] {
    border-radius: 9px 9px 0 0;
    padding: 0.45rem 0.85rem;
    font-weight: 550;
    font-size: 0.86rem;
}

.stTabs [aria-selected="true"] {
    background: rgba(91, 141, 239, 0.10);
    color: #1F2A3D;
}

div[data-testid="stToast"] {
    border-radius: 12px;
    border: 1px solid var(--cp-border-strong);
}

hr { border-color: var(--cp-border); }

.cp-note {
    font-size: 0.78rem;
    color: var(--cp-muted);
    line-height: 1.5;
    border-left: 2px solid rgba(242, 177, 52, 0.6);
    padding-left: 0.65rem;
    margin-top: 0.5rem;
}

.cp-quote {
    font-size: 0.9rem;
    line-height: 1.62;
    color: #4A5770;
    border-left: 3px solid var(--cp-violet);
    padding: 0.15rem 0 0.15rem 0.9rem;
    margin: 0.4rem 0 0.6rem 0;
}

.cp-stat-strip {
    display: flex;
    flex-wrap: wrap;
    gap: 0.6rem;
    margin-top: 0.2rem;
}

.cp-stat {
    flex: 1 1 120px;
    border-radius: 12px;
    border: 1px solid var(--cp-border);
    background: #FFFFFF;
    padding: 0.55rem 0.7rem;
    box-shadow: 0 2px 8px rgba(31, 42, 61, 0.03);
}

.cp-stat-label {
    font-size: 0.7rem;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    color: var(--cp-muted);
}

.cp-stat-value {
    font-size: 1.05rem;
    font-weight: 650;
    color: var(--cp-text);
}

.cp-sidebar-metric {
    border-radius: 12px;
    border: 1px solid var(--cp-border);
    background: #FFFFFF;
    padding: 0.55rem 0.7rem;
    margin-bottom: 0.42rem;
}

.cp-sidebar-metric .lab {
    font-size: 0.7rem;
    letter-spacing: 0.07em;
    text-transform: uppercase;
    color: var(--cp-muted);
}

.cp-sidebar-metric .val {
    font-size: 1.15rem;
    font-weight: 680;
    color: var(--cp-text);
}

.cp-sidebar-metric .val small {
    font-size: 0.75rem;
    font-weight: 500;
    color: var(--cp-muted);
}
</style>
"""


def inject() -> None:
    st.markdown(CSS, unsafe_allow_html=True)
