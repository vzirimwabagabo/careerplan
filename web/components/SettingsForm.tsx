"use client";

import { useRouter } from "next/navigation";
import { useState, useTransition } from "react";
import { saveSettings } from "@/lib/actions";

type FieldSpec = { key: string; label: string; rows?: number; help?: string };
type GroupSpec = { title: string; note?: string; fields: FieldSpec[] };

const GROUPS: GroupSpec[] = [
  {
    title: "Identity",
    note: "Shown in the sidebar and page headers.",
    fields: [
      { key: "owner_name", label: "Name", rows: 1 },
      { key: "owner_initials", label: "Initials", rows: 1 },
      { key: "plan_title", label: "Plan title", rows: 1 },
      { key: "plan_version", label: "Plan version", rows: 1 },
      {
        key: "plan_start",
        label: "Plan start date",
        rows: 1,
        help: "Format YYYY-MM-DD. Drives the day counter on the dashboard.",
      },
    ],
  },
  {
    title: "Positioning",
    fields: [
      { key: "headline", label: "Headline", rows: 2 },
      { key: "current_focus", label: "Current focus", rows: 3 },
      { key: "about", label: "About", rows: 6, help: "Blank line between paragraphs." },
      { key: "aspiration", label: "Aspiration", rows: 3 },
      {
        key: "next_roles",
        label: "Roles being targeted",
        rows: 5,
        help: "One role per line.",
      },
      { key: "long_term_direction", label: "Long-term direction", rows: 2 },
      { key: "growth_mindset", label: "Where I stand today", rows: 3 },
      { key: "alternative_paths", label: "Alternative pathways", rows: 2 },
      {
        key: "alternative_paths_caveat",
        label: "Alternative pathways caveat",
        rows: 2,
        help: "Shown under the heading so the targets are never read as promises.",
      },
    ],
  },
  {
    title: "Review and accountability",
    fields: [
      { key: "review_cadence", label: "Review cadence", rows: 2 },
      { key: "my_responsibility", label: "My responsibility", rows: 3 },
      { key: "commitment", label: "Commitment", rows: 2 },
    ],
  },
  {
    title: "Closing",
    fields: [
      { key: "closing_statement", label: "Closing statement", rows: 8 },
      { key: "academic_note", label: "Evidence note", rows: 3 },
    ],
  },
];

export function SettingsForm({ initial }: { initial: Record<string, string> }) {
  const [values, setValues] = useState<Record<string, string>>(initial);
  const [notice, setNotice] = useState<{ kind: "ok" | "err"; text: string } | null>(null);
  const [pending, startTransition] = useTransition();
  const router = useRouter();

  const dirty = GROUPS.some((group) =>
    group.fields.some((field) => (values[field.key] ?? "") !== (initial[field.key] ?? "")),
  );

  function submit() {
    startTransition(async () => {
      const outcome = await saveSettings(values);
      if (outcome.ok) {
        setNotice({ kind: "ok", text: "Plan notes saved." });
        router.refresh();
      } else {
        setNotice({ kind: "err", text: outcome.error });
      }
    });
  }

  return (
    <div className="space-y-4">
      <div className="flex flex-wrap items-center gap-2">
        <button
          type="button"
          className="cp-btn cp-btn-primary"
          onClick={submit}
          disabled={pending || !dirty}
        >
          {pending ? "Saving…" : dirty ? "Save plan notes" : "Saved"}
        </button>
        <span className="text-muted text-xs">
          These are the words the rest of the app quotes back to you.
        </span>
        {notice ? (
          <span className={`cp-toast ${notice.kind}`} role="status">
            {notice.text}
          </span>
        ) : null}
      </div>

      {GROUPS.map((group) => (
        <div className="cp-card" key={group.title}>
          <div className="cp-card-title">{group.title}</div>
          {group.note ? <div className="cp-card-sub">{group.note}</div> : null}

          <div className="mt-4 grid gap-4 lg:grid-cols-2">
            {group.fields.map((field) => (
              <label
                key={field.key}
                className={field.rows && field.rows > 3 ? "lg:col-span-2" : undefined}
              >
                <span className="mb-1 block text-[0.78rem] font-medium text-[#3d4a61]">
                  {field.label}
                </span>
                <textarea
                  rows={field.rows ?? 3}
                  className="cp-cell-input w-full"
                  style={{ minWidth: 0, resize: "vertical", lineHeight: 1.6 }}
                  value={values[field.key] ?? ""}
                  onChange={(event) =>
                    setValues((previous) => ({ ...previous, [field.key]: event.target.value }))
                  }
                />
                {field.help ? (
                  <span className="mt-1 block text-[0.72rem] text-muted">{field.help}</span>
                ) : null}
              </label>
            ))}
          </div>
        </div>
      ))}
    </div>
  );
}
