"""Goals, success indicators, and the skills to build for the next role."""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from .. import analytics, db
from .. import components as ui
from ..styles import ACCENT, TEAL

STATUS_COLORS = {
    "Not started": "rgba(143,163,192,0.55)",
    "In progress": ACCENT,
    "Blocked": "#FF6B8A",
    "Done": TEAL,
    "Paused": "#F5B54A",
}


def _goal_chart() -> None:
    frame = db.read_table("goals")
    if frame.empty:
        ui.empty_state("No goals recorded yet.")
        return
    frame = frame.copy()
    frame["progress"] = pd.to_numeric(frame["progress"], errors="coerce").fillna(0)
    frame = frame.sort_values("progress")
    colors = [STATUS_COLORS.get(str(s), ACCENT) for s in frame["status"]]

    figure = go.Figure(
        go.Bar(
            x=frame["progress"],
            y=frame["goal"],
            orientation="h",
            marker=dict(color=colors),
            text=[f"{v:.0f}%" for v in frame["progress"]],
            textposition="outside",
            hovertemplate="%{y}<br>Progress: %{x:.0f}%<extra></extra>",
        )
    )
    figure.update_xaxes(range=[0, 112], title="Progress (%)")
    figure.update_yaxes(tickfont=dict(size=10))
    ui.show_figure(ui.theme_figure(figure, height=max(260, 30 * len(frame) + 90)))


def _skill_chart() -> None:
    frame = db.read_table("skills")
    if frame.empty:
        ui.empty_state("No skills recorded yet.")
        return
    frame = frame.copy()
    frame["progress"] = pd.to_numeric(frame["progress"], errors="coerce").fillna(0)
    has_evidence = frame["evidence_link"].notna() & (frame["evidence_link"].astype(str).str.len() > 0)
    colors = [
        TEAL if flag else "rgba(91,140,255,0.55)"
        for flag in has_evidence.reindex(frame.index).fillna(False)
    ]

    figure = go.Figure(
        go.Bar(
            x=frame["progress"],
            y=frame["priority_area"],
            orientation="h",
            marker=dict(color=colors),
            text=[
                "evidence linked" if flag else "evidence missing"
                for flag in has_evidence.reindex(frame.index).fillna(False)
            ],
            textposition="outside",
            hovertemplate="%{y}<br>Progress: %{x:.0f}%<extra></extra>",
        )
    )
    figure.update_xaxes(range=[0, 150], title="Progress (%)")
    figure.update_yaxes(autorange="reversed", tickfont=dict(size=10))
    ui.show_figure(ui.theme_figure(figure, height=max(260, 34 * len(frame) + 90)))


def render() -> None:
    goals = db.read_table("goals")
    skills = db.read_table("skills")

    goals_progress = analytics.pillar_percentages()["goals"]
    skills_progress = analytics.pillar_percentages()["skills"]
    goals_done = int((pd.to_numeric(goals.get("progress"), errors="coerce").fillna(0) >= 100).sum()) if not goals.empty else 0
    evidence_ready = (
        int((skills["evidence_link"].notna() & (skills["evidence_link"].astype(str).str.len() > 0)).sum())
        if not skills.empty
        else 0
    )

    ui.page_header(
        "Goals & skills",
        "Slide 9 — What success looks like, and Slide 8 — the skills to build for the next role.",
        [
            ("Goals", str(len(goals))),
            ("Goals complete", f"{goals_done}"),
            ("Skill areas", str(len(skills))),
            ("Evidence linked", f"{evidence_ready}/{len(skills)}"),
        ],
    )

    columns = st.columns(4)
    with columns[0]:
        ui.kpi("Goal progress", f"{goals_progress:.0f}<small>%</small>", "Average across all goals", "accent")
    with columns[1]:
        ui.kpi("Goals complete", f"{goals_done}<small>/{len(goals)}</small>", "Marked 100% complete", "teal")
    with columns[2]:
        ui.kpi("Skill progress", f"{skills_progress:.0f}<small>%</small>", "Average across skill areas", "violet")
    with columns[3]:
        ui.kpi(
            "Evidence coverage",
            f"{evidence_ready}<small>/{len(skills)}</small>",
            "Skill areas with a proof link attached",
            "amber",
        )

    ui.section("Goal progress", "Each goal against its own progress dial")
    _goal_chart()

    ui.section("Career goals", "Slide 9 — edit any cell directly, drag progress, add or remove rows")
    ui.note(
        "The review frequency from the plan is: "
        + db.get_setting("review_cadence", "Monthly, with a more detailed review every three months.")
    )
    ui.table_editor("goals")

    ui.section("Skills to build for the next role", "Slide 8 — priority, planned action, and evidence of success")
    _skill_chart()
    ui.table_editor("skills")
