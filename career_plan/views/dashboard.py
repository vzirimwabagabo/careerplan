"""Overview dashboard: the whole plan on a single screen."""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from .. import analytics, db
from .. import components as ui
from ..styles import ACCENT, AMBER, TEAL, VIOLET

PILLAR_TONES = {
    "goals": "accent",
    "skills": "violet",
    "actions": "teal",
    "first90": "amber",
    "strengths": "accent",
}

STATUS_ORDER = ["Not started", "In progress", "Blocked", "Done", "Paused"]
STATUS_TONES = {
    "Not started": "muted",
    "In progress": "accent",
    "Blocked": "rose",
    "Done": "teal",
    "Paused": "amber",
}


def _hero(summary: dict) -> None:
    settings = db.read_settings()
    chips = [
        ("Current focus", settings.get("current_focus", "")),
        ("Day in plan", f"{summary['plan_day']}"),
        ("Readiness", f"{summary['readiness']:.0f}%"),
        ("Version", settings.get("plan_version", "")),
    ]
    chip_html = "".join(
        ui.markup(
            f'<span class="cp-chip">{ui.escape(label)}: <b>{ui.escape(value)}</b></span>'
        )
        for label, value in chips
        if value
    )
    ui.render(
        f"""
        <div class="cp-hero">
            <div class="cp-hero-inner">
                <div class="cp-eyebrow">
                    {ui.escape(settings.get("plan_title", "Career Development Plan"))}
                    · {ui.escape(settings.get("plan_version", ""))}
                </div>
                <h1>{ui.escape(settings.get("owner_name", "Career Plan"))}</h1>
                <p>{ui.escape(settings.get("headline", ""))}</p>
                <div class="cp-chip-row">{chip_html}</div>
            </div>
        </div>
        """
    )


def _kpis(summary: dict) -> None:
    columns = st.columns(5)
    total = summary["total_tasks"]
    with columns[0]:
        ui.kpi(
            "Plan readiness",
            f"{summary['readiness']:.0f}<small>%</small>",
            "Weighted across the five pillars below",
            "accent",
        )
    with columns[1]:
        ui.kpi(
            "Open items",
            f"{summary['open_tasks']}<small>/{total}</small>",
            "Actions and 90-day tasks still open",
            "teal",
        )
    with columns[2]:
        ui.kpi(
            "Overdue",
            summary["overdue"],
            "Past their due date with work remaining",
            "rose" if summary["overdue"] else "muted",
        )
    with columns[3]:
        ui.kpi(
            "Blocked",
            summary["blocked"],
            "Flagged as blocked and needing help",
            "amber" if summary["blocked"] else "muted",
        )
    with columns[4]:
        next_review = summary["next_review"]
        ui.kpi(
            "Reviews logged",
            summary["review_count"],
            f"Next review around {next_review.isoformat()}" if next_review else "Log your first review",
            "violet",
        )


def _readiness_block(summary: dict) -> None:
    left, right = st.columns([1, 1.35])
    with left:
        ui.render(ui.ring(summary["readiness"], caption="Weighted plan readiness"))
    with right:
        for key, percent in summary["pillars"].items():
            title, source = analytics.PILLAR_META[key]
            weight = analytics.WEIGHTS[key] * 100
            st.markdown(
                ui.bar(
                    percent,
                    PILLAR_TONES[key],
                    label=f"{title} · weight {weight:.0f}%",
                    value=f"{percent:.0f}%",
                ),
                unsafe_allow_html=True,
            )
            st.write("")


def _capability_chart() -> None:
    frame = db.read_table("strengths")
    if frame.empty:
        ui.empty_state("No capabilities recorded yet.")
        return

    frame = frame.copy()
    frame["current_level"] = pd.to_numeric(frame["current_level"], errors="coerce").fillna(0)
    frame["target_level"] = pd.to_numeric(frame["target_level"], errors="coerce").fillna(0)
    frame = frame.iloc[::-1]

    figure = go.Figure()
    figure.add_trace(
        go.Bar(
            y=frame["name"],
            x=frame["target_level"],
            name="Target",
            orientation="h",
            marker=dict(color="rgba(31,42,61,0.10)", line=dict(color="rgba(31,42,61,0.16)", width=1)),
            hovertemplate="%{y}<br>Target: %{x}/5<extra></extra>",
        )
    )
    figure.add_trace(
        go.Bar(
            y=frame["name"],
            x=frame["current_level"],
            name="Current",
            orientation="h",
            marker=dict(color=ACCENT),
            hovertemplate="%{y}<br>Current: %{x}/5<extra></extra>",
        )
    )
    figure.update_layout(barmode="overlay", bargap=0.35)
    figure.update_xaxes(range=[0, 5], dtick=1, title="Self-rated level (1–5)")
    figure.update_yaxes(tickfont=dict(size=10))
    figure = ui.theme_figure(figure, height=max(320, 26 * len(frame) + 90))
    ui.show_figure(figure)


def _bucket_chart() -> None:
    grouped = analytics.bucket_breakdown()
    if grouped.empty:
        ui.empty_state("No 70–20–10 actions recorded yet.")
        return

    colors = [TEAL, ACCENT, VIOLET]
    figure = go.Figure()
    for index, row in grouped.reset_index(drop=True).iterrows():
        figure.add_trace(
            go.Bar(
                y=[row["bucket"]],
                x=[row["progress"]],
                orientation="h",
                name=str(row["bucket"]),
                marker=dict(color=colors[index % len(colors)]),
                text=[f"{row['done']:.0f}/{row['actions']:.0f} done"],
                textposition="inside",
                insidetextanchor="end",
                hovertemplate="%{y}<br>Average progress: %{x:.0f}%<extra></extra>",
                showlegend=False,
            )
        )
    figure.update_xaxes(range=[0, 100], title="Average progress (%)")
    figure.update_yaxes(autorange="reversed")
    figure = ui.theme_figure(figure, height=240)
    ui.show_figure(figure)


def _phase_progress() -> None:
    grouped = analytics.phase_breakdown()
    if grouped.empty:
        ui.empty_state("No 90-day tasks recorded yet.")
        return
    for _, row in grouped.iterrows():
        ui.render(
            ui.markup(
                f"""
                <div class="cp-row">
                    <div class="cp-row-main" style="flex:1">
                        <div class="cp-row-title">{ui.escape(str(row['phase']).split(' — ')[0])}</div>
                        <div class="cp-row-meta">{ui.escape(str(row['phase']).split(' — ')[-1])}</div>
                        <div style="margin-top:.45rem">
                            {ui.bar(row['percent'], 'amber')}
                        </div>
                    </div>
                    <div class="cp-row-side">
                        {ui.badge(f"{int(row['done'])}/{int(row['tasks'])} done", 'amber')}
                    </div>
                </div>
                """
            )
        )


def _momentum_chart() -> None:
    frame = analytics.momentum()
    if frame.empty or len(frame) < 1:
        ui.empty_state(
            "No review entries yet.",
            "Log a monthly review to start tracking confidence and energy over time.",
        )
        return
    figure = go.Figure()
    figure.add_trace(
        go.Scatter(
            x=frame["review_date"],
            y=frame["confidence"],
            name="Confidence",
            mode="lines+markers",
            line=dict(color=TEAL, width=2.5, shape="spline"),
            marker=dict(size=8, color=TEAL, line=dict(color="#FFFFFF", width=2)),
            hovertemplate="%{x|%d %b %Y}<br>Confidence: %{y}/5<extra></extra>",
        )
    )
    figure.add_trace(
        go.Scatter(
            x=frame["review_date"],
            y=frame["energy"],
            name="Energy",
            mode="lines+markers",
            line=dict(color=AMBER, width=2.5, dash="dot", shape="spline"),
            marker=dict(size=8, color=AMBER, line=dict(color="#FFFFFF", width=2)),
            hovertemplate="%{x|%d %b %Y}<br>Energy: %{y}/5<extra></extra>",
        )
    )
    figure.update_yaxes(range=[0.5, 5.5], dtick=1, title="Score (1–5)")
    figure = ui.theme_figure(figure, height=280)
    ui.show_figure(figure)


def _goal_board() -> None:
    goals = analytics.goal_board()
    if goals.empty:
        ui.empty_state("No goals recorded yet.")
        return

    goals = goals.copy()
    goals["progress"] = pd.to_numeric(goals["progress"], errors="coerce").fillna(0)
    grouped: dict[str, list[pd.Series]] = {status: [] for status in STATUS_ORDER}
    for _, row in goals.iterrows():
        status = str(row.get("status") or "Not started")
        grouped.setdefault(status, []).append(row)

    active = [status for status in STATUS_ORDER if grouped.get(status)]
    active.extend([s for s in grouped if s not in active and grouped[s]])
    if not active:
        ui.empty_state("No goals recorded yet.")
        return

    columns = st.columns(len(active))
    for column, status in zip(columns, active):
        rows = grouped[status]
        with column:
            cards = "".join(
                ui.markup(
                    f"""
                    <div class="cp-mini">
                        <div class="cp-mini-title">{ui.escape(row['goal'])}</div>
                        {ui.bar(row['progress'], STATUS_TONES.get(status, 'accent'))}
                        <div class="cp-row-meta" style="margin-top:.35rem">
                            {ui.escape(row.get('category') or '')}
                            {' · due ' + ui.escape(row.get('target_date')) if row.get('target_date') else ''}
                        </div>
                    </div>
                    """
                )
                for row in rows
            )
            ui.render(
                f"""
                <div class="cp-board">
                    <div class="cp-board-head">
                        <span class="cp-board-name">{ui.escape(status)}</span>
                        {ui.badge(len(rows), STATUS_TONES.get(status, 'accent'))}
                    </div>
                    {cards}
                </div>
                """
            )


def _attention() -> None:
    frame = analytics.attention_items(8)
    if frame.empty:
        ui.empty_state("Nothing is outstanding.", "Every tracked action and 90-day task is complete.")
        return
    for _, row in frame.iterrows():
        overdue = bool(row.get("overdue"))
        due = row.get("due")
        meta_bits = [str(row.get("area")), str(row.get("bucket") or "")]
        if due:
            meta_bits.append(f"due {due.isoformat()}")
        meta = " · ".join(bit for bit in meta_bits if bit)
        ui.render(
            ui.markup(
                f"""
                <div class="cp-row">
                    <div class="cp-row-main" style="flex:1">
                        <div class="cp-row-title">{ui.escape(row.get('item'))}</div>
                        <div class="cp-row-meta">{ui.escape(meta)}</div>
                    </div>
                    <div class="cp-row-side">
                        {ui.badge('overdue' if overdue else str(row.get('status') or 'open'),
                                  'rose' if overdue else ui.tone_for_status(row.get('status')))}
                        {ui.badge(f"{int(row.get('progress') or 0)}%", 'muted')}
                    </div>
                </div>
                """
            )
        )


def _activity() -> None:
    frame = db.recent_activity(10)
    if frame.empty:
        ui.empty_state("No activity recorded yet.")
        return
    for _, row in frame.iterrows():
        ui.render(
            ui.markup(
                f"""
                <div class="cp-row">
                    <div class="cp-row-main">
                        <div class="cp-row-title" style="font-weight:500">{ui.escape(row['message'])}</div>
                        <div class="cp-row-meta">{ui.escape(row['ts'])}</div>
                    </div>
                    <div class="cp-row-side">{ui.badge(row['area'], 'muted')}</div>
                </div>
                """
            )
        )


def render() -> None:
    with ui.loading("Building your dashboard"):
        summary = analytics.summary()

    _hero(summary)
    _kpis(summary)

    ui.section("Plan readiness", "How far the five pillars have moved, weighted by importance")
    _readiness_block(summary)

    left, right = st.columns(2)
    with left:
        ui.section("Capability levels", "Slide 4 — current self-rating against the level you want")
        _capability_chart()
    with right:
        ui.section("70–20–10 balance", "Slide 6 — average progress per development mode")
        _bucket_chart()
        st.write("")

        ui.section("Confidence momentum", "Slide 9 — from your review entries")
        _momentum_chart()

    ui.section("First 90 days", "Slide 11 — execution progress by phase")
    _phase_progress()

    ui.section("Goal board", "Slide 9 — every goal and indicator, grouped by status")
    _goal_board()

    left, right = st.columns([1.25, 1])
    with left:
        ui.section("Needs attention", "Overdue first, then blocked and in-progress work")
        _attention()
    with right:
        ui.section("Recent activity", "Everything you have changed in this tracker")
        _activity()

    settings = db.read_settings()
    if settings.get("commitment"):
        ui.section("Commitment")
        ui.quote(settings["commitment"])
