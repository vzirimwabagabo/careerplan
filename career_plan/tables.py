"""Declarative description of every editable table.

Each table spec drives both the SQLite layer (which columns are writable)
and the Streamlit UI (column type, label, options, help text). Adding a
field in one place is enough to make it editable in the app.
"""

from __future__ import annotations

STATUS = ["Not started", "In progress", "Blocked", "Done", "Paused"]
STAGE_STATUS = ["Not started", "In progress", "Achieved", "Revised"]
SUPPORT_STATUS = ["Needed", "In progress", "Secured"]
EXPERIENCE_STATUS = ["Completed", "Ongoing", "Planned"]
REVIEW_KIND = ["Monthly", "Quarterly"]
BUCKETS = ["70 — Practice", "20 — People", "10 — Study"]
PHASES = [
    "Days 1–30 — Direction and preparation",
    "Days 31–60 — Building evidence",
    "Days 61–90 — Applying and improving",
]

TABLES: dict[str, dict] = {
    "goals": {
        "label": "Career goals",
        "order_by": "sort_order, id",
        "fields": [
            {"col": "id", "type": "number", "label": "ID", "editable": False, "width": "small"},
            {
                "col": "goal",
                "type": "text",
                "label": "Goal",
                "width": "medium",
                "required": True,
            },
            {
                "col": "success_looks_like",
                "type": "text",
                "label": "What success looks like",
                "width": "large",
            },
            {
                "col": "category",
                "type": "select",
                "label": "Category",
                "options": [
                    "Technical",
                    "Portfolio",
                    "Experience",
                    "Communication",
                    "Network",
                    "Education",
                    "Impact",
                ],
            },
            {"col": "status", "type": "select", "label": "Status", "options": STATUS},
            {
                "col": "progress",
                "type": "number",
                "label": "Progress %",
                "min_value": 0,
                "max_value": 100,
                "step": 5,
                "format": "%d%%",
                "help": "Type a number from 0 to 100.",
            },
            {"col": "target_date", "type": "date", "label": "Target date"},
            {"col": "notes", "type": "text", "label": "Notes", "width": "large"},
            {"col": "sort_order", "type": "number", "label": "Order", "width": "small"},
        ],
    },
    "skills": {
        "label": "Skills to build",
        "order_by": "sort_order, id",
        "fields": [
            {"col": "id", "type": "number", "label": "ID", "editable": False, "width": "small"},
            {
                "col": "priority_area",
                "type": "text",
                "label": "Development priority",
                "width": "medium",
                "required": True,
            },
            {
                "col": "planned_action",
                "type": "text",
                "label": "Planned action",
                "width": "large",
            },
            {
                "col": "evidence_of_success",
                "type": "text",
                "label": "Evidence of success",
                "width": "large",
            },
            {"col": "status", "type": "select", "label": "Status", "options": STATUS},
            {
                "col": "progress",
                "type": "number",
                "label": "Progress %",
                "min_value": 0,
                "max_value": 100,
                "step": 5,
                "format": "%d%%",
                "help": "Type a number from 0 to 100.",
            },
            {"col": "evidence_link", "type": "link", "label": "Evidence link"},
            {"col": "last_practiced", "type": "date", "label": "Last practised"},
            {"col": "sort_order", "type": "number", "label": "Order", "width": "small"},
        ],
    },
    "actions_702010": {
        "label": "70–20–10 actions",
        "order_by": "sort_order, id",
        "fields": [
            {"col": "id", "type": "number", "label": "ID", "editable": False, "width": "small"},
            {"col": "bucket", "type": "select", "label": "Bucket", "options": BUCKETS},
            {
                "col": "action",
                "type": "text",
                "label": "Action",
                "width": "medium",
                "required": True,
            },
            {"col": "detail", "type": "text", "label": "Detail", "width": "large"},
            {"col": "status", "type": "select", "label": "Status", "options": STATUS},
            {
                "col": "progress",
                "type": "number",
                "label": "Progress %",
                "min_value": 0,
                "max_value": 100,
                "step": 5,
                "format": "%d%%",
                "help": "Type a number from 0 to 100.",
            },
            {"col": "due_date", "type": "date", "label": "Due"},
            {"col": "notes", "type": "text", "label": "Notes", "width": "large"},
            {"col": "sort_order", "type": "number", "label": "Order", "width": "small"},
        ],
    },
    "first90": {
        "label": "First 90 days",
        "order_by": "sort_order, id",
        "fields": [
            {"col": "id", "type": "number", "label": "ID", "editable": False, "width": "small"},
            {"col": "phase", "type": "select", "label": "Phase", "options": PHASES},
            {
                "col": "task",
                "type": "text",
                "label": "Task",
                "width": "medium",
                "required": True,
            },
            {"col": "done", "type": "checkbox", "label": "Done"},
            {"col": "done_date", "type": "date", "label": "Completed on"},
            {"col": "notes", "type": "text", "label": "Notes", "width": "large"},
            {"col": "sort_order", "type": "number", "label": "Order", "width": "small"},
        ],
    },
    "journey": {
        "label": "Career journey",
        "order_by": "sort_order, id",
        "fields": [
            {"col": "id", "type": "number", "label": "ID", "editable": False, "width": "small"},
            {
                "col": "period",
                "type": "text",
                "label": "Period",
                "width": "small",
                "required": True,
            },
            {
                "col": "title",
                "type": "text",
                "label": "Milestone",
                "width": "medium",
                "required": True,
            },
            {"col": "description", "type": "text", "label": "What happened", "width": "large"},
            {"col": "theme", "type": "text", "label": "Theme", "width": "small"},
            {"col": "sort_order", "type": "number", "label": "Order", "width": "small"},
        ],
    },
    "experiences": {
        "label": "Experiences and achievements",
        "order_by": "sort_order, id",
        "fields": [
            {"col": "id", "type": "number", "label": "ID", "editable": False, "width": "small"},
            {
                "col": "category",
                "type": "select",
                "label": "Category",
                "options": ["Academic", "Professional", "Entrepreneurship", "Community", "Project"],
            },
            {
                "col": "title",
                "type": "text",
                "label": "Title",
                "width": "medium",
                "required": True,
            },
            {"col": "description", "type": "text", "label": "Description", "width": "large"},
            {"col": "start_date", "type": "date", "label": "Start"},
            {"col": "end_date", "type": "date", "label": "End"},
            {
                "col": "status",
                "type": "select",
                "label": "Status",
                "options": EXPERIENCE_STATUS,
            },
            {
                "col": "verified",
                "type": "checkbox",
                "label": "Evidence verified",
                "help": "Only tick when you hold proof (certificate, reference, link, artefact).",
            },
            {"col": "evidence", "type": "link", "label": "Evidence"},
            {"col": "sort_order", "type": "number", "label": "Order", "width": "small"},
        ],
    },
    "strengths": {
        "label": "Strengths and development areas",
        "order_by": "sort_order, id",
        "fields": [
            {"col": "id", "type": "number", "label": "ID", "editable": False, "width": "small"},
            {
                "col": "kind",
                "type": "select",
                "label": "Type",
                "options": ["Strength", "Development area"],
            },
            {
                "col": "name",
                "type": "text",
                "label": "Capability",
                "width": "medium",
                "required": True,
            },
            {
                "col": "current_level",
                "type": "number",
                "label": "Current (1–5)",
                "min_value": 1,
                "max_value": 5,
                "step": 1,
            },
            {
                "col": "target_level",
                "type": "number",
                "label": "Target (1–5)",
                "min_value": 1,
                "max_value": 5,
                "step": 1,
            },
            {"col": "evidence", "type": "text", "label": "Evidence", "width": "large"},
            {"col": "next_action", "type": "text", "label": "Next action", "width": "large"},
            {"col": "sort_order", "type": "number", "label": "Order", "width": "small"},
        ],
    },
    "career_stages": {
        "label": "Career succession plan",
        "order_by": "sort_order, id",
        "fields": [
            {"col": "id", "type": "number", "label": "ID", "editable": False, "width": "small"},
            {
                "col": "stage",
                "type": "text",
                "label": "Stage",
                "width": "small",
                "required": True,
            },
            {"col": "timeframe", "type": "text", "label": "Timeframe", "width": "small"},
            {"col": "title", "type": "text", "label": "Title", "width": "medium"},
            {"col": "description", "type": "text", "label": "What this stage means", "width": "large"},
            {"col": "status", "type": "select", "label": "Status", "options": STAGE_STATUS},
            {
                "col": "progress",
                "type": "number",
                "label": "Progress %",
                "min_value": 0,
                "max_value": 100,
                "step": 5,
                "format": "%d%%",
                "help": "Type a number from 0 to 100.",
            },
            {"col": "sort_order", "type": "number", "label": "Order", "width": "small"},
        ],
    },
    "support": {
        "label": "Feedback and support",
        "order_by": "sort_order, id",
        "fields": [
            {"col": "id", "type": "number", "label": "ID", "editable": False, "width": "small"},
            {"col": "category", "type": "text", "label": "Category", "width": "small"},
            {
                "col": "need",
                "type": "text",
                "label": "Support needed",
                "width": "large",
                "required": True,
            },
            {"col": "status", "type": "select", "label": "Status", "options": SUPPORT_STATUS},
            {"col": "who", "type": "text", "label": "Who / source", "width": "medium"},
            {"col": "notes", "type": "text", "label": "Notes", "width": "large"},
            {"col": "sort_order", "type": "number", "label": "Order", "width": "small"},
        ],
    },
    "reviews": {
        "label": "Reviews and journal",
        "order_by": "review_date DESC, id DESC",
        "fields": [
            {"col": "id", "type": "number", "label": "ID", "editable": False, "width": "small"},
            {
                "col": "review_date",
                "type": "date",
                "label": "Date",
                "required": True,
            },
            {"col": "kind", "type": "select", "label": "Type", "options": REVIEW_KIND},
            {"col": "wins", "type": "text", "label": "Wins", "width": "large"},
            {"col": "blockers", "type": "text", "label": "Blockers", "width": "large"},
            {"col": "next_focus", "type": "text", "label": "Next focus", "width": "large"},
            {
                "col": "confidence",
                "type": "number",
                "label": "Confidence (1–5)",
                "min_value": 1,
                "max_value": 5,
                "step": 1,
            },
            {
                "col": "energy",
                "type": "number",
                "label": "Energy (1–5)",
                "min_value": 1,
                "max_value": 5,
                "step": 1,
            },
            {"col": "notes", "type": "text", "label": "Notes", "width": "large"},
        ],
    },
}


def editable_columns(table: str) -> list[str]:
    return [f["col"] for f in TABLES[table]["fields"] if f.get("editable", True)]


def field_types(table: str) -> dict[str, str]:
    return {f["col"]: f["type"] for f in TABLES[table]["fields"]}
