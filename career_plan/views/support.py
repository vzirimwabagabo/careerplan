"""Feedback, support network, and the responsibilities that come with them."""

from __future__ import annotations

import streamlit as st

from .. import db
from .. import components as ui

SUPPORT_COLUMNS = [
    ("Needed", "Needed", "rose"),
    ("In progress", "Being arranged", "amber"),
    ("Secured", "Secured", "teal"),
]


def _support_board() -> None:
    frame = db.read_table("support")
    if frame.empty:
        ui.empty_state("No support needs recorded yet.")
        return
    columns = st.columns(3)
    for column, (status, heading, tone) in zip(columns, SUPPORT_COLUMNS):
        rows = frame[frame["status"] == status]
        with column:
            cards = "".join(
                ui.markup(
                    f"""
                    <div class="cp-mini">
                        <div class="cp-mini-title">{ui.escape(row['need'])}</div>
                        <div class="cp-row-meta">
                            {ui.escape(row.get('category') or '')}
                            {' · ' + ui.escape(row.get('who')) if row.get('who') else ''}
                        </div>
                    </div>
                    """
                )
                for _, row in rows.iterrows()
            )
            if not cards:
                cards = ui.markup(
                    '<div class="cp-row-meta" style="padding:.4rem 0">Nothing here.</div>'
                )
            ui.render(
                f"""
                <div class="cp-board">
                    <div class="cp-board-head">
                        <span class="cp-board-name">{ui.escape(heading)}</span>
                        {ui.badge(len(rows), tone)}
                    </div>
                    {cards}
                </div>
                """
            )


def render() -> None:
    support = db.read_table("support")
    secured = int((support["status"] == "Secured").sum()) if not support.empty else 0
    in_progress = int((support["status"] == "In progress").sum()) if not support.empty else 0

    ui.page_header(
        "Support & accountability",
        "Slide 10 — the support needed to progress, and the responsibility that comes with it.",
        [
            ("Support needs", str(len(support))),
            ("Secured", str(secured)),
            ("In progress", str(in_progress)),
        ],
    )

    coverage = (secured / len(support) * 100) if len(support) else 0
    columns = st.columns(4)
    with columns[0]:
        ui.kpi("Support secured", f"{secured}<small>/{len(support)}</small>", "Confirmed sources of support", "teal")
    with columns[1]:
        ui.kpi("In progress", in_progress, "Being arranged or approached", "amber")
    with columns[2]:
        ui.kpi(
            "Still needed",
            max(len(support) - secured - in_progress, 0),
            "Nothing arranged yet",
            "rose",
        )
    with columns[3]:
        ui.kpi("Coverage", f"{coverage:.0f}<small>%</small>", "Share of support needs secured", "accent")

    ui.section("Support pipeline", "Slide 10 — where each support need currently stands")
    _support_board()

    ui.section("Support, feedback, and accountability", "Record who can help, and what you owe them")
    ui.table_editor("support")

    responsibility = db.get_setting("my_responsibility")
    if responsibility:
        ui.section("My responsibility")
        ui.quote(responsibility)
