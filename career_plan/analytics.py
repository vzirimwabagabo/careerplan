"""Progress roll-ups and derived indicators used by the dashboard and sidebar."""

from __future__ import annotations

from datetime import date, datetime

import pandas as pd

from . import db

WEIGHTS: dict[str, float] = {
    "goals": 0.25,
    "skills": 0.25,
    "actions": 0.20,
    "first90": 0.20,
    "strengths": 0.10,
}

PILLAR_META = {
    "goals": ("Career goals", "Slide 9 — What success looks like"),
    "skills": ("Skills to build", "Slide 8 — Skills for the next role"),
    "actions": ("70–20–10 actions", "Slide 6 — Development actions"),
    "first90": ("First 90 days", "Slide 11 — Execution plan"),
    "strengths": ("Capability levels", "Slide 4 — Strengths and development"),
}


def parse_date(value) -> date | None:
    if value is None or value == "" or value is pd.NaT:
        return None
    try:
        if isinstance(value, float) and pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass
    try:
        return datetime.strptime(str(value)[:10], "%Y-%m-%d").date()
    except (ValueError, TypeError):
        return None


def _mean_percent(df: pd.DataFrame, column: str) -> float:
    if df.empty or column not in df.columns:
        return 0.0
    series = pd.to_numeric(df[column], errors="coerce").fillna(0)
    if series.empty:
        return 0.0
    return float(series.clip(lower=0, upper=100).mean())


def _done_percent(df: pd.DataFrame, column: str = "done") -> float:
    if df.empty or column not in df.columns:
        return 0.0
    series = pd.to_numeric(df[column], errors="coerce").fillna(0)
    return float((series > 0).mean() * 100)


def _strength_percent(df: pd.DataFrame) -> float:
    if df.empty:
        return 0.0
    current = pd.to_numeric(df.get("current_level"), errors="coerce").fillna(0)
    target = pd.to_numeric(df.get("target_level"), errors="coerce").replace(0, pd.NA)
    ratio = (current / target).astype(float).fillna(0).clip(upper=1)
    return float(ratio.mean() * 100)


def pillar_percentages() -> dict[str, float]:
    goals = db.read_table("goals")
    skills = db.read_table("skills")
    actions = db.read_table("actions_702010")
    first90 = db.read_table("first90")
    strengths = db.read_table("strengths")
    return {
        "goals": round(_mean_percent(goals, "progress"), 1),
        "skills": round(_mean_percent(skills, "progress"), 1),
        "actions": round(_mean_percent(actions, "progress"), 1),
        "first90": round(_done_percent(first90), 1),
        "strengths": round(_strength_percent(strengths), 1),
    }


def readiness() -> float:
    pillars = pillar_percentages()
    return round(sum(pillars[key] * weight for key, weight in WEIGHTS.items()), 1)


def plan_day() -> int:
    start = parse_date(db.get_setting("plan_start", "2026-11-01"))
    if start is None:
        return 0
    return max((date.today() - start).days, 0)


def next_review_due() -> date | None:
    reviews = db.read_table("reviews")
    if reviews.empty:
        return None
    dates = [d for d in (parse_date(v) for v in reviews["review_date"]) if d]
    if not dates:
        return None
    last = max(dates)
    return date(last.year + (last.month // 12), (last.month % 12) + 1, min(last.day, 28))


def _task_table() -> pd.DataFrame:
    actions = db.read_table("actions_702010")
    first90 = db.read_table("first90")
    rows = []
    for _, row in actions.iterrows():
        rows.append(
            {
                "area": "70–20–10",
                "item": row.get("action"),
                "bucket": row.get("bucket"),
                "status": row.get("status"),
                "progress": int(pd.to_numeric(row.get("progress"), errors="coerce") or 0),
                "due": parse_date(row.get("due_date")),
                "id": row.get("id"),
            }
        )
    for _, row in first90.iterrows():
        done = bool(pd.to_numeric(row.get("done"), errors="coerce") or 0)
        rows.append(
            {
                "area": "First 90 days",
                "item": row.get("task"),
                "bucket": row.get("phase"),
                "status": "Done" if done else "Not started",
                "progress": 100 if done else 0,
                "due": parse_date(row.get("done_date")),
                "id": row.get("id"),
            }
        )
    return pd.DataFrame(rows)


def attention_items(limit: int = 8) -> pd.DataFrame:
    """Overdue and high-priority open items across both action tables."""
    df = _task_table()
    if df.empty:
        return df
    today = date.today()
    open_rows = df[df["progress"] < 100].copy()
    if open_rows.empty:
        return open_rows
    open_rows["overdue"] = open_rows["due"].apply(
        lambda d: bool(d and d < today)
    )
    open_rows["priority"] = open_rows.apply(
        lambda r: (
            0
            if r["overdue"]
            else (1 if str(r["status"]) in {"Blocked", "In progress"} else 2)
        ),
        axis=1,
    )
    open_rows = open_rows.sort_values(["priority", "progress"], ascending=[True, True])
    return open_rows.head(limit)


def bucket_breakdown() -> pd.DataFrame:
    actions = db.read_table("actions_702010")
    if actions.empty:
        return pd.DataFrame(columns=["bucket", "actions", "progress", "done"])
    actions["progress_num"] = pd.to_numeric(actions["progress"], errors="coerce").fillna(0)
    actions["is_done"] = (actions["progress_num"] >= 100).astype(int)
    grouped = (
        actions.groupby("bucket", dropna=False)
        .agg(actions=("action", "count"), progress=("progress_num", "mean"), done=("is_done", "sum"))
        .reset_index()
    )
    grouped["progress"] = grouped["progress"].round(1)
    order = {"70 — Practice": 0, "20 — People": 1, "10 — Study": 2}
    grouped["_o"] = grouped["bucket"].map(order).fillna(9)
    return grouped.sort_values("_o").drop(columns="_o")


def phase_breakdown() -> pd.DataFrame:
    first90 = db.read_table("first90")
    if first90.empty:
        return pd.DataFrame(columns=["phase", "tasks", "done", "percent"])
    first90["done_num"] = pd.to_numeric(first90["done"], errors="coerce").fillna(0)
    grouped = (
        first90.groupby("phase", dropna=False)
        .agg(tasks=("task", "count"), done=("done_num", "sum"))
        .reset_index()
    )
    grouped["percent"] = (grouped["done"] / grouped["tasks"] * 100).round(1)
    return grouped


def goal_board() -> pd.DataFrame:
    return db.read_table("goals")


def status_counts() -> dict[str, int]:
    df = _task_table()
    if df.empty:
        return {}
    return df["status"].fillna("Not started").value_counts().to_dict()


def momentum() -> pd.DataFrame:
    reviews = db.read_table("reviews")
    if reviews.empty:
        return pd.DataFrame(columns=["review_date", "confidence", "energy", "progress"])
    reviews = reviews.copy()
    reviews["review_date"] = pd.to_datetime(reviews["review_date"], errors="coerce")
    reviews = reviews.dropna(subset=["review_date"]).sort_values("review_date")
    return reviews[["review_date", "confidence", "energy"]]


def summary() -> dict:
    pillars = pillar_percentages()
    tasks = _task_table()
    reviews = db.read_table("reviews")
    open_tasks = tasks[tasks["progress"] < 100] if not tasks.empty else tasks
    today = date.today()
    overdue = 0
    if not open_tasks.empty:
        overdue = int(
            sum(1 for d in open_tasks["due"] if d and d < today)
        )
    return {
        "readiness": readiness(),
        "pillars": pillars,
        "plan_day": plan_day(),
        "open_tasks": 0 if tasks.empty else int(len(open_tasks)),
        "total_tasks": 0 if tasks.empty else int(len(tasks)),
        "overdue": overdue,
        "blocked": int((tasks["status"] == "Blocked").sum()) if not tasks.empty else 0,
        "review_count": int(len(reviews)),
        "next_review": next_review_due(),
        "status_counts": status_counts(),
    }
