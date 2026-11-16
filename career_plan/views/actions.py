"""The 70-20-10 development actions and the first-90-days execution plan."""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from .. import analytics, db
from .. import components as ui
from ..styles import ACCENT, AMBER, TEAL, VIOLET

BUCKET_META = {
    "70 — Practice": ("70%", "Learning through practical work", TEAL),
    "20 — People": ("20%", "Learning from others", ACCENT),
    "10 — Study": ("10%", "Structured learning", VIOLET),
}


def _bucket_cards() -> None:
    grouped = analytics.bucket_breakdown()
    if grouped.empty:
        ui.empty_state("No 70–20–10 actions recorded yet.")
        return
    columns = st.columns(max(len(grouped), 1))
    lookup = {str(row["bucket"]): row for _, row in grouped.iterrows()}
    for column, (bucket, (share, blurb, tone)) in zip(columns, BUCKET_META.items()):
        row = lookup.get(bucket)
        percent = float(row["progress"]) if row is not None else 0.0
        count = int(row["actions"]) if row is not None else 0
        done = int(row["done"]) if row is not None else 0
        with column:
            ui.render(
                ui.markup(
                    f"""
                    <div class="cp-card">
                        <div class="cp-kpi-label">{ui.escape(share)} · {ui.escape(bucket.split(' — ')[-1])}</div>
                        <div class="cp-card-title">{ui.escape(blurb)}</div>
                        <div style="margin:.6rem 0 .4rem 0">{ui.bar(percent, tone)}</div>
                        <div class="cp-row-meta">{percent:.0f}% average · {done}/{count} complete</div>
                    </div>
                    """
                )
            )


def _status_donut() -> None:
    frame = db.read_table("actions_702010")
    if frame.empty:
        return
    counts = frame["status"].fillna("Not started").value_counts()
    colors = {
        "Not started": "rgba(143,163,192,0.5)",
        "In progress": ACCENT,
        "Blocked": "#FF6B8A",
        "Done": TEAL,
        "Paused": AMBER,
    }
    figure = go.Figure(
        go.Pie(
            labels=counts.index,
            values=counts.values,
            hole=0.62,
            marker=dict(colors=[colors.get(str(label), ACCENT) for label in counts.index]),
            textinfo="label+value",
            textfont=dict(size=11),
            hovertemplate="%{label}: %{value} action(s)<extra></extra>",
        )
    )
    figure.update_layout(height=250)
    ui.show_figure(ui.theme_figure(figure, height=250))


def _review_window() -> None:
    """Visualise where the 90-day window currently sits."""
    start = analytics.parse_date(db.get_setting("plan_start", "2026-11-01"))
    if start is None:
        return
    day = analytics.plan_day()
    position = max(0, min(day, 90))
    phase = "Days 1–30" if day <= 30 else ("Days 31–60" if day <= 60 else "Days 61–90")
    ui.render(
        ui.markup(
            f"""
            <div class="cp-card">
                <div class="cp-kpi-label">90-day window · started {start.isoformat()}</div>
                <div class="cp-card-title">Day {day} of the plan — currently in {ui.escape(phase)}</div>
                <div style="margin:.7rem 0 .35rem 0">
                    {ui.bar(position / 90 * 100, 'amber')}
                </div>
                <div class="cp-row-meta">Elapsed {position} of 90 days ({position/90*100:.0f}%)</div>
            </div>
            """
        )
    )


def render() -> None:
    summary = analytics.summary()
    first90 = db.read_table("first90")
    ninety_done = int(pd.to_numeric(first90.get("done"), errors="coerce").fillna(0).sum()) if not first90.empty else 0

    ui.page_header(
        "Action plan",
        "Slide 6 — the 70–20–10 development actions, and Slide 11 — the first 90 days.",
        [
            ("Open", f"{summary['open_tasks']}/{summary['total_tasks']}"),
            ("Overdue", str(summary["overdue"])),
            ("90-day tasks", f"{ninety_done}/{len(first90)} done"),
        ],
    )

    columns = st.columns(4)
    with columns[0]:
        ui.kpi("70–20–10 progress", f"{summary['pillars']['actions']:.0f}<small>%</small>", "Average across all actions", "teal")
    with columns[1]:
        ui.kpi("90-day checkbox", f"{summary['pillars']['first90']:.0f}<small>%</small>", "Slide 11 tasks completed", "amber")
    with columns[2]:
        ui.kpi(
            "Blocked",
            summary["blocked"],
            "Flagged as blocked — ask your mentor",
            "rose" if summary["blocked"] else "muted",
        )
    with columns[3]:
        ui.kpi(
            "Overdue",
            summary["overdue"],
            "Past the due date with work remaining",
            "rose" if summary["overdue"] else "muted",
        )

    tabs = st.tabs(["70–20–10 actions", "First 90 days"])

    with tabs[0]:
        ui.section(
            "Development balance",
            "The plan splits development into practical work, learning from others, and study.",
        )
        _bucket_cards()

        left, right = st.columns([1, 1])
        with left:
            ui.section("Action status", "Where each action currently stands")
            _status_donut()
        with right:
            ui.section("Due soonest", "Set a due date to make this list useful")
            overdue = analytics.attention_items(6)
            if overdue.empty:
                ui.empty_state("Nothing outstanding.", "All 70–20–10 actions and 90-day tasks are complete.")
            else:
                for _, row in overdue.iterrows():
                    if str(row.get("area")) != "70–20–10":
                        continue
                    ui.render(
                        ui.markup(
                            f"""
                            <div class="cp-row">
                                <div class="cp-row-main">
                                    <div class="cp-row-title">{ui.escape(row.get('item'))}</div>
                                    <div class="cp-row-meta">{ui.escape(row.get('bucket'))}</div>
                                </div>
                                <div class="cp-row-side">
                                    {ui.badge(row.get('status'), ui.tone_for_status(row.get('status')))}
                                </div>
                            </div>
                            """
                        )
                    )

        ui.section("All 70–20–10 actions", "Edit inline: bucket, status, due date, and drag the progress bar")
        ui.table_editor("actions_702010")

    with tabs[1]:
        ui.section("90-day window", "Progress through the execution window from the plan")
        _review_window()

        ui.section("Phase progress", "Dedicated blocks for direction, evidence, and applying")
        grouped = analytics.phase_breakdown()
        if grouped.empty:
            ui.empty_state("No 90-day tasks recorded yet.")
        else:
            for _, row in grouped.iterrows():
                head, tail = str(row["phase"]).split(" — ", 1) if " — " in str(row["phase"]) else (str(row["phase"]), "")
                ui.render(
                    ui.markup(
                        f"""
                        <div class="cp-row">
                            <div class="cp-row-main" style="flex:1">
                                <div class="cp-row-title">{ui.escape(head)}</div>
                                <div class="cp-row-meta">{ui.escape(tail)}</div>
                                <div style="margin-top:.45rem">{ui.bar(row['percent'], 'amber')}</div>
                            </div>
                            <div class="cp-row-side">
                                {ui.badge(f"{int(row['done'])}/{int(row['tasks'])} done", 'amber')}
                            </div>
                        </div>
                        """
                    )
                )

        ui.section("90-day task list", "Tick the box when a task is genuinely finished, then set the date")
        ui.table_editor("first90")
