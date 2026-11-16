"""Career Plan Monitor — entry point.

Local:  streamlit run app.py
Docker: docker compose up --build
"""

from __future__ import annotations

import hmac
import os

import streamlit as st

from career_plan import analytics, db, styles
from career_plan import components as ui

st.set_page_config(
    page_title="Career Plan Monitor",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Imported after set_page_config so each view can also be run standalone.
from career_plan.views import (  # noqa: E402
    actions,
    dashboard,
    goals,
    journey,
    reviews,
    settings,
    support,
)

SECTIONS = {
    "Dashboard": dashboard.render,
    "Goals & skills": goals.render,
    "Action plan": actions.render,
    "Journey & profile": journey.render,
    "Reviews & journal": reviews.render,
    "Support & accountability": support.render,
    "Plan settings": settings.render,
}

PASSWORD_SECRET_KEY = "app_password"
PASSWORD_ENV_VAR = "CAREER_PLAN_APP_PASSWORD"


# --------------------------------------------------------------------------- #
# access control
# --------------------------------------------------------------------------- #
def _configured_password() -> str | None:
    """Gate password from st.secrets, falling back to an environment variable.

    Keeping the env-var path means the Docker image never has to bake a
    secrets file into itself.
    """
    try:
        value = st.secrets.get(PASSWORD_SECRET_KEY)
    except Exception:
        value = None
    if value:
        return str(value)
    return os.environ.get(PASSWORD_ENV_VAR) or None


def _is_authenticated() -> bool:
    password = _configured_password()
    st.session_state["auth_enabled"] = bool(password)
    if not password:
        return True
    return bool(st.session_state.get("unlocked"))


def _login_screen() -> None:
    _, middle, _ = st.columns([1, 1.2, 1])
    with middle:
        st.write("")
        ui.render(
            """
            <div class="cp-hero" style="padding:1.6rem 1.6rem 1.5rem 1.6rem">
                <div class="cp-hero-inner">
                    <div class="cp-eyebrow">Private</div>
                    <h1 style="font-size:1.55rem">Career Plan Monitor</h1>
                    <p style="margin-bottom:0">
                        This tracker holds personal career information. Enter the password to continue.
                    </p>
                </div>
            </div>
            """
        )
        st.write("")
        with st.form("unlock"):
            entered = st.text_input("Password", type="password", key="unlock_password")
            submitted = st.form_submit_button("Unlock", type="primary", width="stretch")
        if submitted:
            expected = _configured_password() or ""
            if expected and hmac.compare_digest(
                entered.encode("utf-8"), expected.encode("utf-8")
            ):
                st.session_state["unlocked"] = True
                st.rerun()
            else:
                st.error("Incorrect password.")


# --------------------------------------------------------------------------- #
# layout
# --------------------------------------------------------------------------- #
def _sidebar(summary: dict) -> str:
    settings_map = db.read_settings()
    with st.sidebar:
        ui.render(
            f"""
            <div class="cp-brand">
                <div class="cp-brand-avatar">{ui.escape(settings_map.get("owner_initials", "CP"))}</div>
                <div>
                    <div class="cp-brand-name">{ui.escape(settings_map.get("owner_name", "Career plan"))}</div>
                    <div class="cp-brand-sub">
                        {ui.escape(settings_map.get("plan_title", ""))}
                        · {ui.escape(settings_map.get("plan_version", ""))}
                    </div>
                </div>
            </div>
            """
        )

        choice = st.radio("Section", list(SECTIONS), label_visibility="collapsed")

        st.markdown("---")
        st.markdown(
            ui.ring(summary["readiness"], size=116, stroke=11, value_text=f"{summary['readiness']:.0f}%"),
            unsafe_allow_html=True,
        )
        st.markdown(
            ui.markup(
                f"""
                <div style="text-align:center;font-size:.72rem;letter-spacing:.08em;
                            text-transform:uppercase;color:#8FA3C0;margin:.1rem 0 .8rem 0">
                    Plan readiness
                </div>
                <div class="cp-sidebar-metric">
                    <div class="lab">Day in plan</div>
                    <div class="val">{summary['plan_day']}<small> days</small></div>
                </div>
                <div class="cp-sidebar-metric">
                    <div class="lab">Open items</div>
                    <div class="val">{summary['open_tasks']}<small>/{summary['total_tasks']}</small></div>
                </div>
                <div class="cp-sidebar-metric">
                    <div class="lab">Overdue</div>
                    <div class="val" style="color:{'#FF6B8A' if summary['overdue'] else '#E7EEF9'}">
                        {summary['overdue']}
                    </div>
                </div>
                <div class="cp-sidebar-metric">
                    <div class="lab">Reviews logged</div>
                    <div class="val">{summary['review_count']}</div>
                </div>
                """
            ),
            unsafe_allow_html=True,
        )

        st.markdown("---")
        if st.button("Refresh from disk", key="sidebar-refresh", width="stretch"):
            st.session_state["refresh_token"] = st.session_state.get("refresh_token", 0) + 1
        if st.session_state.get("auth_enabled"):
            if st.button("Lock this session", key="sidebar-lock", width="stretch"):
                st.session_state["unlocked"] = False
                st.rerun()
        st.caption("Saved locally to data/career_plan.db")
    return choice


def main() -> None:
    styles.inject()

    if not _is_authenticated():
        _login_screen()
        return

    try:
        with ui.loading("Preparing your career plan"):
            db.init_db()
            summary = analytics.summary()
    except Exception as error:  # surfaced instead of a blank page
        st.error(f"The tracker could not open its local database: {error}")
        st.stop()
        return

    choice = _sidebar(summary)

    if st.session_state.get("refresh_token"):
        with ui.loading(f"Refreshing {choice.lower()}", min_seconds=0.45):
            summary = analytics.summary()
        st.session_state["refresh_token"] = 0

    SECTIONS[choice]()


main()
