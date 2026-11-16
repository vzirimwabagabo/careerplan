"""Reusable UI building blocks.

The Streamlit config drives *what* is editable; these helpers decide *how* it
looks and behave.
"""

from __future__ import annotations

import math
import textwrap
import time
from contextlib import contextmanager
from typing import Any, Iterator

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from . import db
from .styles import TONE_COLORS
from .tables import TABLES

PLOT_BG = "rgba(0,0,0,0)"
PLOT_FONT = dict(color="#5A6780", family="Inter, Segoe UI, sans-serif", size=12)


# --------------------------------------------------------------------------- #
# html helpers
# --------------------------------------------------------------------------- #
def markup(fragment: str) -> str:
    """Collapse an indented HTML fragment so Streamlit never treats it as code."""
    return "\n".join(
        line.strip() for line in textwrap.dedent(fragment).strip().splitlines()
    )


def render(fragment: str) -> None:
    st.markdown(markup(fragment), unsafe_allow_html=True)


def escape(value: Any) -> str:
    text = "" if value is None else str(value)
    if text.lower() in {"nan", "none", "nat"}:
        return ""
    return (
        text.replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
    )


def tone_for_status(status: Any) -> str:
    return {
        "Done": "teal",
        "Achieved": "teal",
        "Completed": "teal",
        "Secured": "teal",
        "In progress": "accent",
        "Ongoing": "accent",
        "Not started": "muted",
        "Planned": "muted",
        "Needed": "muted",
        "Paused": "amber",
        "Revised": "amber",
        "Blocked": "rose",
    }.get(str(status or "").strip(), "muted")


def badge(text: Any, tone: str = "muted") -> str:
    if not text:
        return ""
    return f'<span class="cp-badge tone-{tone}">{escape(text)}</span>'


# --------------------------------------------------------------------------- #
# layout primitives
# --------------------------------------------------------------------------- #
def section(title: str, subtitle: str = "") -> None:
    sub = f'<div class="cp-section-sub">{escape(subtitle)}</div>' if subtitle else ""
    render(
        f"""
        <div class="cp-section">
            <div class="cp-section-bar"></div>
            <div>
                <div class="cp-section-title">{escape(title)}</div>
                {sub}
            </div>
        </div>
        """
    )


def kpi(label: str, value: Any, sub: str = "", tone: str = "accent") -> None:
    render(
        f"""
        <div class="cp-kpi tone-{tone}">
            <div class="cp-kpi-label">{escape(label)}</div>
            <div class="cp-kpi-value">{value}</div>
            <div class="cp-kpi-sub">{escape(sub)}</div>
        </div>
        """
    )


def bar(percent: float, tone: str = "accent", label: str = "", value: str = "") -> str:
    pct = max(0.0, min(100.0, float(percent or 0)))
    legend = ""
    if label or value:
        legend = markup(
            f"""
            <div class="cp-legend">
                <span>{escape(label)}</span>
                <b>{escape(value)}</b>
            </div>
            """
        )
    return markup(
        f"""
        {legend}
        <div class="cp-bar tone-{tone}"><span style="width:{pct:.1f}%"></span></div>
        """
    )


def ring(
    percent: float,
    *,
    size: int = 168,
    stroke: int = 14,
    caption: str = "",
    value_text: str | None = None,
    color: str = "#5B8CFF",
    gradient_to: str | None = "#2ED3B7",
) -> str:
    pct = max(0.0, min(100.0, float(percent or 0)))
    radius = (size - stroke) / 2
    circumference = 2 * math.pi * radius
    filled = circumference * pct / 100
    gradient_id = f"cp-grad-{int(pct * 100)}-{size}-{color.lstrip('#')}"
    if gradient_to:
        stroke_paint = f"url(#{gradient_id})"
        defs = markup(
            f"""
            <defs>
                <linearGradient id="{gradient_id}" x1="0%" y1="0%" x2="100%" y2="100%">
                    <stop offset="0%" stop-color="{color}"/>
                    <stop offset="100%" stop-color="{gradient_to}"/>
                </linearGradient>
            </defs>
            """
        )
    else:
        stroke_paint = color
        defs = ""
    shown = value_text if value_text is not None else f"{pct:.0f}%"
    cap = f'<div style="font-size:.74rem;color:#7C8AA3;margin-top:.35rem">{escape(caption)}</div>' if caption else ""
    return markup(
        f"""
        <div style="display:grid;place-items:center;text-align:center">
            <svg width="{size}" height="{size}" viewBox="0 0 {size} {size}">
                {defs}
                <circle cx="{size/2}" cy="{size/2}" r="{radius}" fill="none"
                        stroke="rgba(31,42,61,0.09)" stroke-width="{stroke}"/>
                <circle cx="{size/2}" cy="{size/2}" r="{radius}" fill="none"
                        stroke="{stroke_paint}" stroke-width="{stroke}" stroke-linecap="round"
                        stroke-dasharray="{filled:.2f} {circumference:.2f}"
                        transform="rotate(-90 {size/2} {size/2})"/>
                <text x="50%" y="50%" text-anchor="middle" dominant-baseline="central"
                      fill="#1F2A3D" font-size="{size*0.215:.0f}" font-weight="700">{escape(shown)}</text>
            </svg>
            {cap}
        </div>
        """
    )


def comparison_row(
    name: str,
    detail: str,
    percent: float,
    *,
    tone: str = "accent",
    status: str = "",
    meta: str = "",
) -> None:
    tone_name = tone if tone != "accent" else tone_for_status(status) if status else "accent"
    badges = f'<div class="cp-row-side">{badge(status, tone_for_status(status))}</div>' if status else ""
    render(
        f"""
        <div class="cp-row">
            <div class="cp-row-main" style="flex:1">
                <div class="cp-row-title">{escape(name)}</div>
                <div class="cp-row-meta">{escape(detail)}</div>
                <div style="margin-top:.45rem">{bar(percent, tone_name)}</div>
                {f'<div class="cp-row-meta" style="margin-top:.35rem">{escape(meta)}</div>' if meta else ''}
            </div>
            {badges}
        </div>
        """
    )


def card(title: str, text: str, footer: str = "") -> str:
    tail = f'<div class="cp-card-text" style="margin-top:.5rem">{escape(footer)}</div>' if footer else ""
    return markup(
        f"""
        <div class="cp-card">
            <div class="cp-card-title">{escape(title)}</div>
            <div class="cp-card-text">{escape(text)}</div>
            {tail}
        </div>
        """
    )


def stat_strip(items: list[tuple[str, str]]) -> str:
    cells = "".join(
        markup(
            f"""
            <div class="cp-stat">
                <div class="cp-stat-label">{escape(label)}</div>
                <div class="cp-stat-value">{escape(value)}</div>
            </div>
            """
        )
        for label, value in items
    )
    return markup(f'<div class="cp-stat-strip">{cells}</div>')


def note(text: str) -> None:
    render(f'<div class="cp-note">{escape(text)}</div>')


def quote(text: str) -> None:
    render(f'<div class="cp-quote">{escape(text)}</div>')


def empty_state(text: str, hint: str = "") -> None:
    hint_html = f'<div class="cp-row-meta" style="margin-top:.3rem">{escape(hint)}</div>' if hint else ""
    render(
        f"""
        <div class="cp-card" style="text-align:center;padding:1.4rem">
            <div class="cp-card-text">{escape(text)}</div>
            {hint_html}
        </div>
        """
    )


# --------------------------------------------------------------------------- #
# skeleton loader
# --------------------------------------------------------------------------- #
def _skeleton_html(label: str) -> str:
    return markup(
        f"""
        <div class="cp-skel">
            <div class="cp-skel-label">{escape(label)}</div>
            <div class="cp-skel-row">
                <div class="cp-skel-ring"></div>
                <div class="cp-skel-ring"></div>
                <div class="cp-skel-ring"></div>
            </div>
            <div class="cp-skel-block"></div>
            <div class="cp-skel-line" style="width:72%"></div>
            <div class="cp-skel-line" style="width:54%"></div>
        </div>
        """
    )


@contextmanager
def loading(label: str = "Loading", min_seconds: float = 0.0) -> Iterator[None]:
    """Show a shimmering placeholder while real work happens, then clear it."""
    placeholder = st.empty()
    placeholder.markdown(_skeleton_html(label), unsafe_allow_html=True)
    started = time.perf_counter()
    try:
        yield
    finally:
        elapsed = time.perf_counter() - started
        if elapsed < min_seconds:
            time.sleep(min_seconds - elapsed)
        placeholder.empty()


# --------------------------------------------------------------------------- #
# plotly theming
# --------------------------------------------------------------------------- #
def theme_figure(fig: go.Figure, height: int | None = None, show_legend: bool = True) -> go.Figure:
    fig.update_layout(
        paper_bgcolor=PLOT_BG,
        plot_bgcolor=PLOT_BG,
        font=PLOT_FONT,
        margin=dict(l=8, r=8, t=18, b=8),
        height=height,
        showlegend=show_legend,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.04,
            xanchor="left",
            x=0,
            bgcolor="rgba(0,0,0,0)",
        ),
        hoverlabel=dict(bgcolor="#FFFFFF", bordercolor="rgba(31,42,61,0.16)", font=PLOT_FONT),
    )
    fig.update_xaxes(showgrid=False, zeroline=False, linecolor="rgba(31,42,61,0.12)", color="#7C8AA3")
    fig.update_yaxes(gridcolor="rgba(31,42,61,0.08)", zeroline=False, color="#7C8AA3")
    return fig


def show_figure(fig: go.Figure) -> None:
    st.plotly_chart(fig, width="stretch", config={"displayModeBar": False})


# --------------------------------------------------------------------------- #
# editable table
# --------------------------------------------------------------------------- #
def _column_config(field: dict):
    kind = field["type"]
    label = field["label"]
    extra: dict[str, Any] = {}
    if field.get("help"):
        extra["help"] = field["help"]
    if field.get("width"):
        extra["width"] = field["width"]
    editable = field.get("editable", True)

    if kind == "text":
        return st.column_config.TextColumn(label, **extra)
    if kind == "number":
        if field.get("format"):
            extra["format"] = field["format"]
        elif field.get("step") == 1 and field.get("min_value") == 1:
            extra["format"] = "%d"
        return st.column_config.NumberColumn(
            label,
            min_value=field.get("min_value"),
            max_value=field.get("max_value"),
            step=field.get("step"),
            disabled=not editable,
            **extra,
        )
    if kind == "select":
        return st.column_config.SelectboxColumn(label, options=field["options"], **extra)
    if kind == "checkbox":
        return st.column_config.CheckboxColumn(label, **extra)
    if kind == "date":
        return st.column_config.DateColumn(label, format="YYYY-MM-DD", **extra)
    if kind == "link":
        return st.column_config.LinkColumn(label, display_text="open", **extra)
    return st.column_config.TextColumn(label, **extra)


def _prepare_frame(table: str) -> tuple[pd.DataFrame, list[dict]]:
    spec = TABLES[table]
    fields = spec["fields"]
    frame = db.read_table(table)
    for field in fields:
        if field["col"] not in frame.columns:
            frame[field["col"]] = None
    frame = frame[[f["col"] for f in fields]]

    for field in fields:
        column = field["col"]
        if field["type"] == "date":
            parsed = pd.to_datetime(frame[column], errors="coerce")
            frame[column] = parsed.dt.date.where(parsed.notna(), None)
        elif field["type"] == "checkbox":
            frame[column] = frame[column].fillna(0).astype(float).astype(bool)
    return frame, fields


def table_editor(
    table: str,
    *,
    caption: str = "",
    height: int | None = None,
    min_seconds: float = 0.0,
) -> None:
    """Render a fully editable, add/delete-capable grid bound to SQLite."""
    spec = TABLES[table]
    label = spec["label"]

    with loading(f"Loading {label.lower()}", min_seconds=min_seconds):
        frame, fields = _prepare_frame(table)

    if caption:
        note(caption)

    rows = max(len(frame), 6)
    computed_height = height or min(620, 46 * (rows + 2) + 46)

    edited = st.data_editor(
        frame,
        key=f"editor::{table}",
        column_config={f["col"]: _column_config(f) for f in fields},
        num_rows="dynamic",
        width="stretch",
        hide_index=True,
        height=computed_height,
        disabled=[f["col"] for f in fields if not f.get("editable", True)],
    )

    left, middle, right = st.columns([1.3, 1, 2.2])
    with left:
        save = st.button("Save changes", key=f"save::{table}", type="primary", width="stretch")
    with middle:
        reload_clicked = st.button("Discard edits", key=f"reload::{table}", width="stretch")
    with right:
        entry_count = int(edited["id"].notna().sum())
        pending = int(len(edited) - entry_count)
        hint = f"{entry_count} saved row(s)"
        if pending > 0:
            hint += f" · {pending} unsaved new row(s)"
        st.caption(hint)

    if reload_clicked:
        st.rerun()

    if not save:
        return

    required_fields = [f for f in fields if f.get("required")]
    cleaned = edited.copy()
    if required_fields:
        filled = cleaned[[f["col"] for f in required_fields]].notna().any(axis=1)
        if not filled.all():
            dropped = int((~filled).sum())
            cleaned = cleaned[filled]
            st.warning(f"Skipped {dropped} blank row(s): a required field was empty.")

    with loading(f"Saving {label.lower()}"):
        result = db.sync_table(table, cleaned)

    changed = sum(result.values())
    if changed == 0:
        st.toast("No changes to save.")
    else:
        db.log(
            label,
            f"+{result['inserted']} · ~{result['updated']} · -{result['deleted']}",
        )
        st.toast(
            f"Saved: {result['inserted']} added, {result['updated']} updated, "
            f"{result['deleted']} removed."
        )
    st.rerun()


def page_header(title: str, subtitle: str = "", chips: list[tuple[str, str]] | None = None) -> None:
    """Compact banner used at the top of every non-dashboard view."""
    chip_html = "".join(
        markup(f'<span class="cp-chip">{escape(label)}: <b>{escape(value)}</b></span>')
        for label, value in (chips or [])
        if value not in (None, "")
    )
    subtitle_html = f"<p>{escape(subtitle)}</p>" if subtitle else ""
    chips_block = f'<div class="cp-chip-row">{chip_html}</div>' if chip_html else ""
    render(
        f"""
        <div class="cp-hero" style="padding:1.25rem 1.5rem 1.15rem 1.5rem">
            <div class="cp-hero-inner">
                <h1 style="font-size:1.62rem">{escape(title)}</h1>
                {subtitle_html}
                {chips_block}
            </div>
        </div>
        """
    )



