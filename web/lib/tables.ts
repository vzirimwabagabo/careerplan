/**
 * Declarative description of every editable table.
 *
 * One spec per table drives the database column list, the grid columns, the
 * select options and the progress roll-ups. Adding a field here is enough to
 * make it editable in the UI.
 */

export type FieldType = "text" | "select" | "number" | "date" | "checkbox" | "link";

export type Field = {
  col: string;
  type: FieldType;
  label: string;
  editable?: boolean;
  options?: string[];
  minValue?: number;
  maxValue?: number;
  step?: number;
  /** Rendered as a percentage when true. */
  percent?: boolean;
  width?: "small" | "medium" | "large";
  required?: boolean;
  help?: string;
};

export type OrderBy = { column: string; ascending?: boolean };

export type TableSpec = {
  label: string;
  order: OrderBy[];
  fields: Field[];
  /** Column that groups rows into sections, if any. */
  groupBy?: string;
};

export const STATUS = ["Not started", "In progress", "Blocked", "Done", "Paused"] as const;
export const STAGE_STATUS = ["Not started", "In progress", "Achieved", "Revised"] as const;
export const SUPPORT_STATUS = ["Needed", "In progress", "Secured"] as const;
export const EXPERIENCE_STATUS = ["Completed", "Ongoing", "Planned"] as const;
export const REVIEW_KIND = ["Monthly", "Quarterly"] as const;
export const BUCKETS = ["70 - Practice", "20 - People", "10 - Study"] as const;
export const PHASES = [
  "Days 1-30 - Direction and preparation",
  "Days 31-60 - Building evidence",
  "Days 61-90 - Applying and improving",
] as const;

const idField: Field = { col: "id", type: "number", label: "ID", editable: false, width: "small" };
const orderField: Field = {
  col: "sort_order",
  type: "number",
  label: "Order",
  width: "small",
  help: "Controls the display sequence. Gaps of 10 leave room to insert.",
};

const progressField: Field = {
  col: "progress",
  type: "number",
  label: "Progress",
  minValue: 0,
  maxValue: 100,
  step: 5,
  percent: true,
};

export const TABLES: Record<string, TableSpec> = {
  goals: {
    label: "Career goals",
    order: [{ column: "sort_order" }, { column: "id" }],
    fields: [
      idField,
      { col: "goal", type: "text", label: "Goal", width: "medium", required: true },
      {
        col: "success_looks_like",
        type: "text",
        label: "What success looks like",
        width: "large",
      },
      {
        col: "category",
        type: "select",
        label: "Category",
        options: [
          "Technical",
          "Portfolio",
          "Experience",
          "Communication",
          "Network",
          "Education",
          "Impact",
        ],
      },
      { col: "status", type: "select", label: "Status", options: [...STATUS] },
      progressField,
      { col: "target_date", type: "date", label: "Target date" },
      { col: "notes", type: "text", label: "Notes", width: "large" },
      orderField,
    ],
  },

  skills: {
    label: "Skills to build",
    order: [{ column: "sort_order" }, { column: "id" }],
    fields: [
      idField,
      {
        col: "priority_area",
        type: "text",
        label: "Development priority",
        width: "medium",
        required: true,
      },
      { col: "planned_action", type: "text", label: "Planned action", width: "large" },
      { col: "evidence_of_success", type: "text", label: "Evidence of success", width: "large" },
      { col: "status", type: "select", label: "Status", options: [...STATUS] },
      progressField,
      { col: "evidence_link", type: "link", label: "Evidence link" },
      { col: "last_practiced", type: "date", label: "Last practised" },
      orderField,
    ],
  },

  actions_702010: {
    label: "70-20-10 actions",
    order: [{ column: "sort_order" }, { column: "id" }],
    groupBy: "bucket",
    fields: [
      idField,
      { col: "bucket", type: "select", label: "Bucket", options: [...BUCKETS] },
      { col: "action", type: "text", label: "Action", width: "medium", required: true },
      { col: "detail", type: "text", label: "Detail", width: "large" },
      { col: "status", type: "select", label: "Status", options: [...STATUS] },
      progressField,
      { col: "due_date", type: "date", label: "Due" },
      { col: "notes", type: "text", label: "Notes", width: "large" },
      orderField,
    ],
  },

  first90: {
    label: "First 90 days",
    order: [{ column: "sort_order" }, { column: "id" }],
    groupBy: "phase",
    fields: [
      idField,
      { col: "phase", type: "select", label: "Phase", options: [...PHASES] },
      { col: "task", type: "text", label: "Task", width: "medium", required: true },
      { col: "done", type: "checkbox", label: "Done" },
      { col: "done_date", type: "date", label: "Completed on" },
      { col: "notes", type: "text", label: "Notes", width: "large" },
      orderField,
    ],
  },

  journey: {
    label: "Career journey",
    order: [{ column: "sort_order" }, { column: "id" }],
    fields: [
      idField,
      { col: "period", type: "text", label: "Period", width: "small", required: true },
      { col: "title", type: "text", label: "Milestone", width: "medium", required: true },
      { col: "description", type: "text", label: "What happened", width: "large" },
      { col: "theme", type: "text", label: "Theme", width: "small" },
      orderField,
    ],
  },

  experiences: {
    label: "Experiences and achievements",
    order: [{ column: "sort_order" }, { column: "id" }],
    fields: [
      idField,
      {
        col: "category",
        type: "select",
        label: "Category",
        options: ["Academic", "Professional", "Entrepreneurship", "Community", "Project"],
      },
      { col: "title", type: "text", label: "Title", width: "medium", required: true },
      { col: "description", type: "text", label: "Description", width: "large" },
      { col: "start_date", type: "date", label: "Start" },
      { col: "end_date", type: "date", label: "End" },
      { col: "status", type: "select", label: "Status", options: [...EXPERIENCE_STATUS] },
      {
        col: "verified",
        type: "checkbox",
        label: "Evidence verified",
        help: "Only tick when you hold proof (certificate, reference, link, artefact).",
      },
      { col: "evidence", type: "link", label: "Evidence" },
      orderField,
    ],
  },

  strengths: {
    label: "Strengths and development areas",
    order: [{ column: "sort_order" }, { column: "id" }],
    groupBy: "kind",
    fields: [
      idField,
      {
        col: "kind",
        type: "select",
        label: "Type",
        options: ["Strength", "Development area"],
      },
      { col: "name", type: "text", label: "Capability", width: "medium", required: true },
      {
        col: "current_level",
        type: "number",
        label: "Current (1-5)",
        minValue: 1,
        maxValue: 5,
        step: 1,
      },
      {
        col: "target_level",
        type: "number",
        label: "Target (1-5)",
        minValue: 1,
        maxValue: 5,
        step: 1,
      },
      { col: "evidence", type: "text", label: "Evidence", width: "large" },
      { col: "next_action", type: "text", label: "Next action", width: "large" },
      orderField,
    ],
  },

  career_stages: {
    label: "Career succession plan",
    order: [{ column: "sort_order" }, { column: "id" }],
    fields: [
      idField,
      { col: "stage", type: "text", label: "Stage", width: "small", required: true },
      { col: "timeframe", type: "text", label: "Timeframe", width: "small" },
      { col: "title", type: "text", label: "Title", width: "medium" },
      { col: "description", type: "text", label: "What this stage means", width: "large" },
      { col: "status", type: "select", label: "Status", options: [...STAGE_STATUS] },
      progressField,
      orderField,
    ],
  },

  support: {
    label: "Feedback and support",
    order: [{ column: "sort_order" }, { column: "id" }],
    fields: [
      idField,
      { col: "category", type: "text", label: "Category", width: "small" },
      { col: "need", type: "text", label: "Support needed", width: "large", required: true },
      { col: "status", type: "select", label: "Status", options: [...SUPPORT_STATUS] },
      { col: "who", type: "text", label: "Who / source", width: "medium" },
      { col: "notes", type: "text", label: "Notes", width: "large" },
      orderField,
    ],
  },

  reviews: {
    label: "Reviews and journal",
    order: [{ column: "review_date", ascending: false }, { column: "id", ascending: false }],
    fields: [
      idField,
      { col: "review_date", type: "date", label: "Date", required: true },
      { col: "kind", type: "select", label: "Type", options: [...REVIEW_KIND] },
      { col: "wins", type: "text", label: "Wins", width: "large" },
      { col: "blockers", type: "text", label: "Blockers", width: "large" },
      { col: "next_focus", type: "text", label: "Next focus", width: "large" },
      {
        col: "confidence",
        type: "number",
        label: "Confidence (1-5)",
        minValue: 1,
        maxValue: 5,
        step: 1,
      },
      { col: "energy", type: "number", label: "Energy (1-5)", minValue: 1, maxValue: 5, step: 1 },
      { col: "notes", type: "text", label: "Notes", width: "large" },
    ],
  },
};

export type TableName = keyof typeof TABLES;

export const TABLE_NAMES = Object.keys(TABLES) as TableName[];

/** Columns the grid is allowed to write back. */
export function editableColumns(table: TableName): string[] {
  return TABLES[table].fields
    .filter((field) => field.editable !== false)
    .map((field) => field.col);
}

export function fieldType(table: TableName, col: string): FieldType | undefined {
  return TABLES[table].fields.find((field) => field.col === col)?.type;
}

export function primaryField(table: TableName): Field {
  return TABLES[table].fields.find((field) => field.required) ?? TABLES[table].fields[1];
}
