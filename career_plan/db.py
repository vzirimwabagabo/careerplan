"""SQLite persistence for the Career Plan Monitor.

Everything is stored in a single local file (``data/career_plan.db``) so the
plan can be updated offline and backed up by copying one file.
"""

from __future__ import annotations

import json
import math
import sqlite3
from contextlib import contextmanager
from datetime import date, datetime
from pathlib import Path
from typing import Any, Iterator

import pandas as pd

from .tables import TABLES, editable_columns, field_types

ROOT = Path(__file__).resolve().parent.parent
DATA_DIR = ROOT / "data"
DB_PATH = DATA_DIR / "career_plan.db"

SCHEMA = """
CREATE TABLE IF NOT EXISTS settings (
    key   TEXT PRIMARY KEY,
    value TEXT
);

CREATE TABLE IF NOT EXISTS journey (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    period      TEXT,
    title       TEXT,
    description TEXT,
    theme       TEXT,
    sort_order  INTEGER DEFAULT 0,
    updated_at  TEXT
);

CREATE TABLE IF NOT EXISTS experiences (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    category    TEXT,
    title       TEXT,
    description TEXT,
    start_date  TEXT,
    end_date    TEXT,
    status      TEXT,
    verified    INTEGER DEFAULT 0,
    evidence    TEXT,
    sort_order  INTEGER DEFAULT 0,
    updated_at  TEXT
);

CREATE TABLE IF NOT EXISTS strengths (
    id            INTEGER PRIMARY KEY AUTOINCREMENT,
    kind          TEXT,
    name          TEXT,
    current_level INTEGER DEFAULT 3,
    target_level  INTEGER DEFAULT 5,
    evidence      TEXT,
    next_action   TEXT,
    sort_order    INTEGER DEFAULT 0,
    updated_at    TEXT
);

CREATE TABLE IF NOT EXISTS actions_702010 (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    bucket     TEXT,
    action     TEXT,
    detail     TEXT,
    status     TEXT,
    progress   INTEGER DEFAULT 0,
    due_date   TEXT,
    notes      TEXT,
    sort_order INTEGER DEFAULT 0,
    updated_at TEXT
);

CREATE TABLE IF NOT EXISTS career_stages (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    stage       TEXT,
    timeframe   TEXT,
    title       TEXT,
    description TEXT,
    status      TEXT,
    progress    INTEGER DEFAULT 0,
    sort_order  INTEGER DEFAULT 0,
    updated_at  TEXT
);

CREATE TABLE IF NOT EXISTS skills (
    id                  INTEGER PRIMARY KEY AUTOINCREMENT,
    priority_area       TEXT,
    planned_action      TEXT,
    evidence_of_success TEXT,
    status              TEXT,
    progress            INTEGER DEFAULT 0,
    evidence_link       TEXT,
    last_practiced      TEXT,
    sort_order          INTEGER DEFAULT 0,
    updated_at          TEXT
);

CREATE TABLE IF NOT EXISTS goals (
    id                 INTEGER PRIMARY KEY AUTOINCREMENT,
    goal               TEXT,
    success_looks_like TEXT,
    category           TEXT,
    status             TEXT,
    progress           INTEGER DEFAULT 0,
    target_date        TEXT,
    notes              TEXT,
    sort_order         INTEGER DEFAULT 0,
    updated_at         TEXT
);

CREATE TABLE IF NOT EXISTS first90 (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    phase      TEXT,
    task       TEXT,
    done       INTEGER DEFAULT 0,
    done_date  TEXT,
    notes      TEXT,
    sort_order INTEGER DEFAULT 0,
    updated_at TEXT
);

CREATE TABLE IF NOT EXISTS support (
    id         INTEGER PRIMARY KEY AUTOINCREMENT,
    category   TEXT,
    need       TEXT,
    status     TEXT,
    who        TEXT,
    notes      TEXT,
    sort_order INTEGER DEFAULT 0,
    updated_at TEXT
);

CREATE TABLE IF NOT EXISTS reviews (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    review_date TEXT,
    kind        TEXT,
    wins        TEXT,
    blockers    TEXT,
    next_focus  TEXT,
    confidence  INTEGER DEFAULT 3,
    energy      INTEGER DEFAULT 3,
    notes       TEXT,
    updated_at  TEXT
);

CREATE TABLE IF NOT EXISTS activity (
    id      INTEGER PRIMARY KEY AUTOINCREMENT,
    ts      TEXT,
    area    TEXT,
    message TEXT
);
"""

LOG_TABLE = "activity"


# --------------------------------------------------------------------------- #
# connection helpers
# --------------------------------------------------------------------------- #
def _now() -> str:
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@contextmanager
def connect() -> Iterator[sqlite3.Connection]:
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(DB_PATH, timeout=20)
    conn.row_factory = sqlite3.Row
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def init_db() -> None:
    """Create the schema and seed the plan content on first run."""
    with connect() as conn:
        conn.executescript(SCHEMA)
    if get_setting("seeded") != "1":
        from .seed import seed_all

        seed_all()
        set_setting("seeded", "1")


# --------------------------------------------------------------------------- #
# normalisation
# --------------------------------------------------------------------------- #
def _norm(value: Any) -> Any:
    """Convert a value coming from a pandas cell into something SQLite likes."""
    if value is None:
        return None
    if isinstance(value, float) and math.isnan(value):
        return None
    if value is pd.NaT:
        return None
    if isinstance(value, (pd.Timestamp, datetime, date)):
        ts = pd.Timestamp(value)
        if pd.isna(ts):
            return None
        return ts.strftime("%Y-%m-%d")
    if isinstance(value, bool):
        return int(value)
    try:
        if pd.isna(value):
            return None
    except (TypeError, ValueError):
        pass
    if hasattr(value, "item") and not isinstance(value, (str, bytes)):
        try:
            value = value.item()
        except (ValueError, AttributeError):
            pass
    if isinstance(value, str):
        stripped = value.strip()
        return stripped or None
    return value


# --------------------------------------------------------------------------- #
# generic table access
# --------------------------------------------------------------------------- #
def read_table(table: str, order_by: str | None = None) -> pd.DataFrame:
    spec = TABLES.get(table, {})
    order = order_by or spec.get("order_by") or "id"
    with connect() as conn:
        return pd.read_sql_query(f"SELECT * FROM {table} ORDER BY {order}", conn)


def read_settings() -> dict[str, str]:
    with connect() as conn:
        rows = conn.execute("SELECT key, value FROM settings").fetchall()
    return {r["key"]: r["value"] for r in rows}


def get_setting(key: str, default: str = "") -> str:
    with connect() as conn:
        row = conn.execute("SELECT value FROM settings WHERE key = ?", (key,)).fetchone()
    return row["value"] if row and row["value"] is not None else default


def set_setting(key: str, value: Any) -> None:
    with connect() as conn:
        conn.execute(
            "INSERT INTO settings (key, value) VALUES (?, ?) "
            "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
            (key, "" if value is None else str(value)),
        )


def set_settings(values: dict[str, Any]) -> None:
    with connect() as conn:
        conn.executemany(
            "INSERT INTO settings (key, value) VALUES (?, ?) "
            "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
            [(k, "" if v is None else str(v)) for k, v in values.items()],
        )


def next_sort_order(table: str) -> int:
    with connect() as conn:
        row = conn.execute(f"SELECT MAX(sort_order) AS m FROM {table}").fetchone()
    current = row["m"] if row and row["m"] is not None else 0
    return int(current) + 10


def _coerce(col: str, ctype: str, value: Any) -> Any:
    norm = _norm(value)
    if ctype == "checkbox":
        return int(bool(norm))
    if ctype == "number":
        if norm is None:
            return 0
        try:
            return float(norm)
        except (TypeError, ValueError):
            return 0
    return norm


def sync_table(table: str, edited: pd.DataFrame) -> dict[str, int]:
    """Persist an edited dataframe back into SQLite.

    New rows (no id) are inserted, changed rows are updated, and rows that
    disappeared from the editor are deleted. Returns a change summary.
    """
    cols = editable_columns(table)
    types = field_types(table)

    with connect() as conn:
        rows = conn.execute(f"SELECT * FROM {table}").fetchall()
    current = {int(r["id"]): dict(r) for r in rows}

    seen: set[int] = set()
    inserted = updated = deleted = 0
    pending_order = next_sort_order(table)
    has_order = "sort_order" in cols

    with connect() as conn:
        for _, record in edited.iterrows():
            raw_id = record.get("id")
            payload = {c: _coerce(c, types.get(c, "text"), record.get(c)) for c in cols}
            if raw_id is None or _norm(raw_id) is None:
                if has_order and not payload.get("sort_order"):
                    payload["sort_order"] = pending_order
                    pending_order += 10
                conn.execute(
                    f"INSERT INTO {table} ({', '.join(cols)}, updated_at) "
                    f"VALUES ({', '.join('?' for _ in cols)}, ?)",
                    [*payload.values(), _now()],
                )
                inserted += 1
                continue

            row_id = int(raw_id)
            seen.add(row_id)
            previous = current.get(row_id)
            if previous is None:
                continue
            changed = {
                c: v
                for c, v in payload.items()
                if _norm(previous.get(c)) != v
            }
            if changed:
                assignments = ", ".join(f"{c} = ?" for c in changed)
                conn.execute(
                    f"UPDATE {table} SET {assignments}, updated_at = ? WHERE id = ?",
                    [*changed.values(), _now(), row_id],
                )
                updated += 1

        for row_id in set(current) - seen:
            conn.execute(f"DELETE FROM {table} WHERE id = ?", (row_id,))
            deleted += 1

    return {"inserted": inserted, "updated": updated, "deleted": deleted}


# --------------------------------------------------------------------------- #
# activity log
# --------------------------------------------------------------------------- #
def log(area: str, message: str) -> None:
    with connect() as conn:
        conn.execute(
            f"INSERT INTO {LOG_TABLE} (ts, area, message) VALUES (?, ?, ?)",
            (_now(), area, message),
        )


def recent_activity(limit: int = 12) -> pd.DataFrame:
    with connect() as conn:
        return pd.read_sql_query(
            f"SELECT ts, area, message FROM {LOG_TABLE} ORDER BY id DESC LIMIT ?",
            conn,
            params=(limit,),
        )


def clear_activity() -> None:
    with connect() as conn:
        conn.execute(f"DELETE FROM {LOG_TABLE}")


# --------------------------------------------------------------------------- #
# import / export / reset
# --------------------------------------------------------------------------- #
def export_bundle() -> str:
    tables = list(TABLES) + ["settings"]
    bundle: dict[str, Any] = {"format": "career-plan-monitor", "version": 1, "tables": {}}
    for table in tables:
        with connect() as conn:
            bundle["tables"][table] = [
                dict(r) for r in conn.execute(f"SELECT * FROM {table}").fetchall()
            ]
    return json.dumps(bundle, indent=2, default=str)


def import_bundle(text: str) -> dict[str, int]:
    bundle = json.loads(text)
    tables = bundle.get("tables") or {}
    counts: dict[str, int] = {}
    with connect() as conn:
        for table, rows in tables.items():
            if table not in TABLES and table != "settings":
                continue
            conn.execute(f"DELETE FROM {table}")
            if not rows:
                counts[table] = 0
                continue
            keys = list(rows[0].keys())
            conn.executemany(
                f"INSERT INTO {table} ({', '.join(keys)}) "
                f"VALUES ({', '.join('?' for _ in keys)})",
                [[row.get(k) for k in keys] for row in rows],
            )
            counts[table] = len(rows)
    return counts


def reset_to_seed() -> None:
    from .seed import seed_all

    with connect() as conn:
        for table in TABLES:
            conn.execute(f"DELETE FROM {table}")
        conn.execute(f"DELETE FROM {LOG_TABLE}")
        conn.execute("DELETE FROM settings")
    seed_all()
    set_setting("seeded", "1")
