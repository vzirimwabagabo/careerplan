"""Journey, capabilities, experience, and the succession plan."""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from .. import db
from .. import components as ui
from ..styles import TEAL


def _timeline() -> None:
    frame = db.read_table("journey")
    if frame.empty:
        ui.empty_state("No journey milestones recorded yet.")
        return
    items = "".join(
        ui.markup(
            f"""
            <div class="cp-tl-item">
                <div class="cp-tl-period">{ui.escape(row['period'])}
                    {' · ' + ui.escape(row['theme']) if row.get('theme') else ''}
                </div>
                <div class="cp-tl-title">{ui.escape(row['title'])}</div>
                <div class="cp-tl-text">{ui.escape(row['description'])}</div>
            </div>
            """
        )
        for _, row in frame.iterrows()
    )
    ui.render(f'<div class="cp-card"><div class="cp-timeline">{items}</div></div>')


def _capability_chart() -> None:
    frame = db.read_table("strengths")
    if frame.empty:
        ui.empty_state("No capabilities recorded yet.")
        return
    frame = frame.copy()
    frame["current_level"] = pd.to_numeric(frame["current_level"], errors="coerce").fillna(0)
    frame["target_level"] = pd.to_numeric(frame["target_level"], errors="coerce").fillna(0)
    gap = (frame["target_level"] - frame["current_level"]).clip(lower=0)
    frame["gap"] = gap
    frame = frame.sort_values(["kind", "gap"], ascending=[True, False])

    figure = go.Figure()
    figure.add_trace(
        go.Bar(
            y=frame["name"],
            x=frame["current_level"],
            name="Current level",
            orientation="h",
            marker=dict(color=TEAL),
            hovertemplate="%{y}<br>Current: %{x}/5<extra></extra>",
        )
    )
    figure.add_trace(
        go.Bar(
            y=frame["name"],
            x=frame["gap"],
            name="Gap to target",
            orientation="h",
            marker=dict(color="rgba(245,181,74,0.65)"),
            hovertemplate="%{y}<br>Gap: %{x}<extra></extra>",
        )
    )
    figure.update_layout(barmode="stack", bargap=0.34)
    figure.update_xaxes(range=[0, 5], dtick=1, title="Level (1–5)")
    figure.update_yaxes(tickfont=dict(size=10))
    ui.show_figure(ui.theme_figure(figure, height=max(320, 26 * len(frame) + 100)))


def _experience_board() -> None:
    frame = db.read_table("experiences")
    if frame.empty:
        ui.empty_state("No experiences recorded yet.")
        return
    unverified = 0
    for status in ["Completed", "Ongoing", "Planned"]:
        rows = frame[frame["status"] == status]
        if rows.empty:
            continue
        cards = []
        for _, row in rows.iterrows():
            verified = bool(pd.to_numeric(row.get("verified"), errors="coerce") or 0)
            if not verified:
                unverified += 1
            cards.append(
                ui.markup(
                    f"""
                    <div class="cp-mini">
                        <div class="cp-mini-title">{ui.escape(row['title'])}</div>
                        <div class="cp-row-meta" style="margin-bottom:.4rem">
                            {ui.escape(row.get('category') or '')}
                        </div>
                        <div class="cp-row-meta" style="margin-bottom:.4rem">{ui.escape(row.get('description'))}</div>
                        {ui.badge('evidence verified' if verified else 'evidence to add', 'teal' if verified else 'amber')}
                    </div>
                    """
                )
            )
        ui.section(status, f"{len(rows)} record(s)")
        ui.render("".join(cards))


def _succession_board() -> None:
    frame = db.read_table("career_stages")
    if frame.empty:
        ui.empty_state("No career stages recorded yet.")
        return
    columns = st.columns(max(len(frame), 1))
    for column, (_, row) in zip(columns, frame.iterrows()):
        progress = float(pd.to_numeric(row.get("progress"), errors="coerce") or 0)
        with column:
            ui.render(
                ui.markup(
                    f"""
                    <div class="cp-card">
                        <div class="cp-kpi-label">{ui.escape(row.get('timeframe'))}</div>
                        <div class="cp-card-title">{ui.escape(row.get('title'))}</div>
                        <div style="margin:.6rem 0 .45rem 0">{ui.bar(progress, 'violet')}</div>
                        <div class="cp-row-meta" style="margin-bottom:.5rem">
                            {ui.badge(row.get('status'), ui.tone_for_status(row.get('status')))}
                            &nbsp;{progress:.0f}%
                        </div>
                        <div class="cp-card-text">{ui.escape(row.get('description'))}</div>
                    </div>
                    """
                )
            )
    caveat = db.get_setting("alternative_paths_caveat")
    if caveat:
        ui.note(caveat)


def render() -> None:
    journey = db.read_table("journey")
    strengths = db.read_table("strengths")
    experiences = db.read_table("experiences")
    stages = db.read_table("career_stages")
    strength_count = int((strengths["kind"] == "Strength").sum()) if not strengths.empty else 0
    development_count = int((strengths["kind"] == "Development area").sum()) if not strengths.empty else 0

    ui.page_header(
        "Journey & profile",
        "Slides 2, 4, 5, and 7 — the path so far, current capability, evidence of work, and the succession plan.",
        [
            ("Milestones", str(len(journey))),
            ("Capabilities", f"{strength_count} strengths / {development_count} to develop"),
            ("Experiences", str(len(experiences))),
        ],
    )

    tabs = st.tabs(["Journey", "Capabilities", "Experience", "Succession plan"])

    with tabs[0]:
        ui.section("My career journey", "Slide 2 — from learning to building")
        _timeline()
        ui.section("Journey milestones", "Edit any cell, add a milestone, or remove one")
        ui.table_editor("journey")

    with tabs[1]:
        ui.section(
            "Capability levels",
            "Slide 4 — self-rated 1–5. Move the numbers as your evidence improves.",
        )
        _capability_chart()
        ui.table_editor("strengths")

    with tabs[2]:
        ui.section("Experiences and achievements", "Slide 5 — grouped by status")
        ui.note(db.get_setting("academic_note", ""))
        _experience_board()
        ui.section("Experience records", "Only tick “evidence verified” when you hold actual proof")
        ui.table_editor("experiences")

    with tabs[3]:
        ui.section("Career succession plan", "Slide 7 — target pathways, not guaranteed promotions")
        _succession_board()
        ui.table_editor("career_stages")
        alt = db.get_setting("alternative_paths")
        if alt:
            ui.section("Alternative career paths")
            ui.quote(alt)
