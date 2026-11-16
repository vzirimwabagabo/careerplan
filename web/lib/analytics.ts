import { num, type Row } from "./data";

export type Pillar = {
  key: string;
  label: string;
  source: string;
  percent: number;
  detail: string;
};

export type Summary = {
  readiness: number;
  pillars: Pillar[];
  planDay: number;
  planStart: string;
  openTasks: number;
  totalTasks: number;
  overdue: number;
  blocked: number;
  reviewCount: number;
  nextReview: string | null;
  statusCounts: Record<string, number>;
};

/** Weighting used for the headline readiness figure. */
const WEIGHTS: Record<string, number> = {
  goals: 0.25,
  skills: 0.25,
  actions: 0.2,
  first90: 0.2,
  strengths: 0.1,
};

export const PILLAR_META: Record<string, { label: string; source: string }> = {
  goals: { label: "Career goals", source: "What success looks like" },
  skills: { label: "Skills to build", source: "Skills for the next role" },
  actions: { label: "70-20-10 actions", source: "Development actions" },
  first90: { label: "First 90 days", source: "Execution plan" },
  strengths: { label: "Capability levels", source: "Strengths and development" },
};

export const PILLAR_TONE: Record<string, string> = {
  goals: "brand",
  skills: "teal",
  actions: "violet",
  first90: "amber",
  strengths: "rose",
};

function average(values: number[]): number {
  if (!values.length) return 0;
  return values.reduce((sum, value) => sum + value, 0) / values.length;
}

function round(value: number, places = 1): number {
  const factor = 10 ** places;
  return Math.round(value * factor) / factor;
}

function daysBetween(from: string, to: Date): number {
  const start = new Date(`${from}T00:00:00`);
  if (Number.isNaN(start.getTime())) return 0;
  const diff = Math.floor((to.getTime() - start.getTime()) / 86_400_000);
  return Math.max(diff, 0);
}

function addMonths(iso: string, months: number): string | null {
  const base = new Date(`${iso}T00:00:00`);
  if (Number.isNaN(base.getTime())) return null;
  base.setMonth(base.getMonth() + months);
  return base.toISOString().slice(0, 10);
}

export function summarize(input: {
  goals: Row[];
  skills: Row[];
  actions: Row[];
  first90: Row[];
  strengths: Row[];
  reviews: Row[];
  settings: Record<string, string>;
  today?: Date;
}): Summary {
  const today = input.today ?? new Date();

  const goalPct = average(input.goals.map((row) => num(row.progress)));
  const skillPct = average(input.skills.map((row) => num(row.progress)));
  const actionPct = average(input.actions.map((row) => num(row.progress)));

  const totalTasks = input.first90.length;
  const doneTasks = input.first90.filter((row) => row.done === true).length;
  const first90Pct = totalTasks ? (doneTasks / totalTasks) * 100 : 0;

  const strengthPct = average(
    input.strengths.map((row) => {
      const target = num(row.target_level, 5) || 5;
      return (num(row.current_level) / target) * 100;
    }),
  );

  const percentages: Record<string, number> = {
    goals: goalPct,
    skills: skillPct,
    actions: actionPct,
    first90: first90Pct,
    strengths: strengthPct,
  };

  const readiness = Object.entries(WEIGHTS).reduce(
    (sum, [key, weight]) => sum + percentages[key] * weight,
    0,
  );

  const pillars: Pillar[] = Object.keys(WEIGHTS).map((key) => ({
    key,
    label: PILLAR_META[key].label,
    source: PILLAR_META[key].source,
    percent: round(percentages[key]),
    detail:
      key === "first90"
        ? `${doneTasks} of ${totalTasks} tasks complete`
        : `${percentages[key] > 0 ? "average progress" : "nothing recorded yet"}`,
  }));

  const planStart = input.settings.plan_start || "2026-11-01";
  const planDay = daysBetween(planStart, today);

  const openTasks = input.actions.filter((row) => {
    const status = String(row.status ?? "");
    return status !== "Done" && status !== "Paused";
  }).length;

  const overdue = input.actions.filter((row) => {
    if (!row.due_date) return false;
    if (String(row.status ?? "") === "Done") return false;
    const due = new Date(`${String(row.due_date)}T00:00:00`);
    return !Number.isNaN(due.getTime()) && due < today;
  }).length;

  const blocked =
    input.actions.filter((row) => String(row.status ?? "") === "Blocked").length +
    input.goals.filter((row) => String(row.status ?? "") === "Blocked").length;

  const statusCounts: Record<string, number> = {};
  for (const row of [...input.goals, ...input.skills, ...input.actions]) {
    const status = String(row.status ?? "Unset");
    statusCounts[status] = (statusCounts[status] ?? 0) + 1;
  }

  const reviewDates = input.reviews
    .map((row) => String(row.review_date ?? ""))
    .filter(Boolean)
    .sort();

  const nextReview = reviewDates.length
    ? addMonths(reviewDates[reviewDates.length - 1], 1)
    : null;

  return {
    readiness: round(readiness),
    pillars,
    planDay,
    planStart,
    openTasks,
    totalTasks: input.actions.length,
    overdue,
    blocked,
    reviewCount: input.reviews.length,
    nextReview,
    statusCounts,
  };
}
