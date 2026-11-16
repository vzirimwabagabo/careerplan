"""Review cadence, journal entries, and the change history."""

from __future__ import annotations

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from .. import analytics, db
from .. import components as ui
from ..styles import AMBER, TEAL


def _momentum_chart() -> None:
    frame = analytics.momentum()
    if frame.empty:
        ui.empty_state(
            "No reviews logged yet.",
            "Add your first monthly review below to start the trend line.",
        )
        return
    figure = go.Figure()
    figure.add_trace(
        go.Scatter(
            x=frame["review_date"],
            y=frame["confidence"],
            name="Confidence",
            mode="lines+markers",
            line=dict(color=TEAL, width=3, shape="spline"),
            marker=dict(size=10, color=TEAL, line=dict(color="#FFFFFF", width=2)),
            fill="tozeroy",
            fillcolor="rgba(46,211,183,0.10)",
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
    figure.update_yaxes(range=[0, 5.5], dtick=1, title="Score (1–5)")
    ui.show_figure(ui.theme_figure(figure, height=320))


def _review_cards() -> None:
    frame = db.read_table("reviews")
    if frame.empty:
        ui.empty_state("No reviews logged yet.", "The first review is the hardest one to write.")
        return
    for _, row in frame.head(4).iterrows():
        date = analytics.parse_date(row.get("review_date"))
        confidence = int(pd.to_numeric(row.get("confidence"), errors="coerce") or 0)
        energy = int(pd.to_numeric(row.get("energy"), errors="coerce") or 0)
        blocks = []
        for label, value, tone in [
            ("Wins", row.get("wins"), "teal"),
            ("Blockers", row.get("blockers"), "rose"),
            ("Next focus", row.get("next_focus"), "accent"),
        ]:
            if value:
                blocks.append(
                    ui.markup(
                        f"""
                        <div style="margin-top:.5rem">
                            <div class="cp-kpi-label">{ui.escape(label)}</div>
                            <div class="cp-card-text">{ui.escape(value)}</div>
                        </div>
                        """
                    )
                )
        ui.render(
            ui.markup(
                f"""
                <div class="cp-card" style="margin-bottom:.6rem">
                    <div class="cp-row" style="background:transparent;border:none;padding:0;margin-bottom:.2rem">
                        <div class="cp-row-main">
                            <div class="cp-card-title">
                                {ui.escape(date.isoformat() if date else row.get('review_date'))}
                            </div>
                        </div>
                        <div class="cp-row-side">
                            {ui.badge(row.get('kind'), 'violet')}
                            {ui.badge(f"confidence {confidence}/5", 'teal')}
                            {ui.badge(f"energy {energy}/5", 'amber')}
                        </div>
                    </div>
                    {''.join(blocks)}
                </div>
                """
            )
        )


def _history() -> None:
    frame = db.recent_activity(25)
    if frame.empty:
        ui.empty_state("No changes recorded yet.")
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
    reviews = db.read_table("reviews")
    summary = analytics.summary()

    dates = []
    if not reviews.empty:
        dates = [d for d in (analytics.parse_date(v) for v in reviews["review_date"]) if d]
    last_review = max(dates).isoformat() if dates else "not yet"
    average_confidence = (
        round(pd.to_numeric(reviews["confidence"], errors="coerce").mean(), 1)
        if not reviews.empty
        else 0
    )

    ui.page_header(
        "Reviews & journal",
        db.get_setting("review_cadence", "Monthly, with a more detailed review every three months."),
        [
            ("Reviews logged", str(len(reviews))),
            ("Last review", last_review),
            ("Average confidence", f"{average_confidence}/5"),
        ],
    )

    columns = st.columns(4)
    with columns[0]:
        ui.kpi("Reviews logged", len(reviews), "Monthly entries recorded", "violet")
    with columns[1]:
        ui.kpi("Last review", last_review, "Most recent entry in the journal", "accent")
    with columns[2]:
        next_review = summary["next_review"]
        ui.kpi(
            "Next review",
            next_review.isoformat() if next_review else "—",
            "One month after the last entry",
            "amber",
        )
    with columns[3]:
        ui.kpi("Average confidence", f"{average_confidence}<small>/5</small>", "Self-rated across all reviews", "teal")

    if not reviews.empty and not summary["next_review"]:
        ui.note("Add a review date so the cadence indicator can work.")

    ui.section("Confidence and energy", "Slide 9 — the trend that matters more than any single score")
    _momentum_chart()

    ui.section("Recent reviews", "The four most recent entries, newest first")
    _review_cards()

    ui.section("Write a review", "Add a row, fill it in, then save. Dates must be set for the trend chart.")
    ui.table_editor("reviews")

    ui.section("Change history", "Every save you make in this tracker, most recent first")
    _history()
    if st.button("Clear change history", key="clear-activity"):
        db.clear_activity()
        st.toast("Change history cleared.")
        st.rerun()
