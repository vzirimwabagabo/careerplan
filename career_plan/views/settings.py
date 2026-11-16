"""Plan profile, narrative sections, and local data management."""

from __future__ import annotations

import json
from datetime import date, datetime

import streamlit as st

from .. import analytics, db
from .. import components as ui

SHORT_FIELDS = [
    ("owner_name", "Full name"),
    ("owner_initials", "Initials (used in the sidebar avatar)"),
    ("plan_title", "Plan title"),
    ("plan_version", "Plan version"),
    ("headline", "Headline"),
    ("current_focus", "Current focus"),
    ("long_term_direction", "Long-term direction"),
    ("review_cadence", "Review cadence"),
]

LONG_FIELDS = [
    ("about", "About me"),
    ("aspiration", "Career aspiration"),
    ("next_roles", "Potential next roles (one per line)"),
    ("growth_mindset", "Growth mindset statement"),
    ("alternative_paths", "Alternative career paths"),
    ("alternative_paths_caveat", "Caveat on the pathways"),
    ("my_responsibility", "My responsibility"),
    ("closing_statement", "Closing statement"),
    ("commitment", "Commitment"),
    ("academic_note", "Evidence warning shown on the experience grid"),
]


def _profile_form() -> None:
    settings = db.read_settings()
    with st.form("plan-profile"):
        columns = st.columns(2)
        for index, (key, label) in enumerate(SHORT_FIELDS):
            with columns[index % 2]:
                st.text_input(label, value=settings.get(key, ""), key=f"profile::{key}")
        start_value = analytics.parse_date(settings.get("plan_start", "")) or date.today()
        st.date_input(
            "Plan start date (drives the day counter and the 90-day window)",
            value=start_value,
            key="profile::plan_start",
        )
        if st.form_submit_button("Save profile", type="primary"):
            values = {key: st.session_state.get(f"profile::{key}", "") for key, _ in SHORT_FIELDS}
            start = st.session_state.get("profile::plan_start")
            values["plan_start"] = start.isoformat() if start else ""
            db.set_settings(values)
            db.log("Settings", "Plan profile updated")
            st.toast("Profile saved.")
            st.rerun()


def _narrative_form() -> None:
    settings = db.read_settings()
    with st.form("plan-narrative"):
        for key, label in LONG_FIELDS:
            st.text_area(label, value=settings.get(key, ""), height=130, key=f"narrative::{key}")
        if st.form_submit_button("Save narrative sections", type="primary"):
            values = {key: st.session_state.get(f"narrative::{key}", "") for key, _ in LONG_FIELDS}
            db.set_settings(values)
            db.log("Settings", "Plan narrative updated")
            st.toast("Narrative sections saved.")
            st.rerun()


def _data_management() -> None:
    st.download_button(
        "Download a JSON backup",
        data=db.export_bundle(),
        file_name=f"career-plan-backup-{datetime.now():%Y%m%d-%H%M}.json",
        mime="application/json",
        width="stretch",
    )

    upload = st.file_uploader("Restore from a JSON backup", type=["json"], key="restore-upload")
    if upload is not None and st.button("Restore this backup", key="restore-apply"):
        try:
            counts = db.import_bundle(upload.getvalue().decode("utf-8"))
        except (json.JSONDecodeError, UnicodeDecodeError) as error:
            st.error(f"That file could not be read as a backup: {error}")
        else:
            db.log("Settings", f"Backup restored ({sum(counts.values())} rows)")
            st.toast("Backup restored.")
            st.rerun()

    if st.button("Reset everything back to the November 2026 plan", key="reset-seed"):
        db.reset_to_seed()
        st.toast("Tracker reset to the original plan content.")
        st.rerun()


def render() -> None:
    db_path = db.DB_PATH
    settings = db.read_settings()

    ui.page_header(
        "Plan settings",
        "The plan profile, narrative sections, and the local data file that stores everything you change.",
        [
            ("Owner", settings.get("owner_name", "")),
            ("Version", settings.get("plan_version", "")),
            ("Plan day", str(analytics.plan_day())),
        ],
    )

    columns = st.columns(4)
    with columns[0]:
        ui.kpi("Plan version", settings.get("plan_version", "—"), "From the source document", "accent")
    with columns[1]:
        ui.kpi("Plan start", settings.get("plan_start", "—"), "Day 0 of the 90-day window", "violet")
    with columns[2]:
        ui.kpi("Days elapsed", analytics.plan_day(), "Days since the plan start date", "teal")
    with columns[3]:
        rows = sum(len(db.read_table(table)) for table in ["goals", "skills", "actions_702010", "first90", "reviews"])
        ui.kpi("Tracked records", rows, "Rows you can edit across the tracker", "amber")

    ui.section("Plan profile", "These values drive the header, sidebar, and day counters")
    _profile_form()

    ui.section("Narrative sections", "Slides 3, 4, 7, 10, and 12 — kept in one place for easy editing")
    _narrative_form()

    ui.section("Local data", "Everything is stored on this machine in a single SQLite file")
    ui.render(
        ui.markup(
            f"""
            <div class="cp-card">
                <div class="cp-kpi-label">Database file</div>
                <div class="cp-card-title" style="word-break:break-all">{ui.escape(str(db_path))}</div>
                <div class="cp-card-text">
                    Copy this file to back up the tracker, or move it to another machine to keep working.
                </div>
            </div>
            """
        )
    )
    st.write("")
    left, right = st.columns(2)
    with left:
        _data_management()
    with right:
        ui.note(
            "Restoring a backup replaces the current contents of every table. Reset rebuilds the "
            "tracker from the original November 2026 plan and discards your edits."
        )
        environment = {
            "records": {table: len(db.read_table(table)) for table in [
                "journey", "experiences", "strengths", "actions_702010",
                "career_stages", "skills", "goals", "first90", "support", "reviews",
            ]},
            "settings": len(settings),
        }
        st.caption("Current row counts")
        st.code(json.dumps(environment["records"], indent=2), language="json")
