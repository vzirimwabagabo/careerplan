"use client";

import { useRouter } from "next/navigation";
import { Fragment, useMemo, useState, useTransition } from "react";
import { saveTable } from "@/lib/actions";
import type { Row } from "@/lib/data";
import { TABLES, type Field } from "@/lib/tables";

type Notice = { kind: "ok" | "err"; text: string };

function blankRow(fields: Field[]): Row {
  const row: Row = {};
  for (const field of fields) {
    if (field.editable === false) continue;
    if (field.type === "checkbox") row[field.col] = false;
    else if (field.type === "number") row[field.col] = 0;
    else row[field.col] = "";
  }
  return row;
}

function widthFor(field: Field): number {
  return field.width === "small" ? 110 : field.width === "large" ? 280 : 180;
}

/**
 * Values in link fields are user data, so the scheme is checked before the
 * value is ever rendered as a clickable href. Only http and https pass, which
 * stops a stored `javascript:` or `data:` value from becoming a script URL.
 * Returning the re-serialised URL also normalises away control characters.
 */
function safeHref(value: unknown): string | null {
  if (value == null) return null;
  const raw = String(value).trim();
  if (!raw) return null;
  try {
    const parsed = new URL(raw);
    return parsed.protocol === "http:" || parsed.protocol === "https:"
      ? parsed.href
      : null;
  } catch {
    return null;
  }
}

export function DataGrid({
  table,
  initialRows,
  height,
}: {
  table: string;
  initialRows: Row[];
  height?: number;
}) {
  const spec = TABLES[table];
  const editableFields = spec.fields.filter((field) => field.editable !== false);
  const router = useRouter();

  const [rows, setRows] = useState<Row[]>(initialRows);
  const [baseline, setBaseline] = useState(() => JSON.stringify(initialRows));
  const [notice, setNotice] = useState<Notice | null>(null);
  const [pending, startTransition] = useTransition();

  const dirty = useMemo(() => JSON.stringify(rows) !== baseline, [rows, baseline]);

  function update(index: number, col: string, value: unknown) {
    setRows((previous) =>
      previous.map((row, position) => (position === index ? { ...row, [col]: value } : row)),
    );
  }

  function addRow() {
    setRows((previous) => [...previous, blankRow(editableFields)]);
  }

  function removeRow(index: number) {
    setRows((previous) => previous.filter((_, position) => position !== index));
  }

  function save() {
    startTransition(async () => {
      const outcome = await saveTable(table, rows);
      if (!outcome.ok) {
        setNotice({ kind: "err", text: outcome.error });
        return;
      }
      setRows(outcome.rows);
      setBaseline(JSON.stringify(outcome.rows));
      const parts: string[] = [];
      if (outcome.inserted) parts.push(`${outcome.inserted} added`);
      if (outcome.updated) parts.push(`${outcome.updated} updated`);
      if (outcome.deleted) parts.push(`${outcome.deleted} removed`);
      if (outcome.skipped) parts.push(`${outcome.skipped} blank skipped`);
      setNotice({
        kind: "ok",
        text: parts.length ? `Saved — ${parts.join(", ")}.` : "Nothing changed, so nothing was saved.",
      });
      router.refresh();
    });
  }

  const groups = useMemo(() => {
    if (!spec.groupBy) return null;
    const key = spec.groupBy;
    const buckets: { label: string; items: { row: Row; index: number }[] }[] = [];
    rows.forEach((row, index) => {
      const label = row[key] == null ? "" : String(row[key]);
      const last = buckets[buckets.length - 1];
      if (last && last.label === label) last.items.push({ row, index });
      else buckets.push({ label, items: [{ row, index }] });
    });
    return buckets;
  }, [rows, spec.groupBy]);

  function renderCell(field: Field, row: Row, index: number) {
    const value = row[field.col];
    const minWidth = widthFor(field);

    if (field.editable === false) {
      return (
        <span className="text-muted text-xs tabular-nums">{value == null ? "—" : String(value)}</span>
      );
    }

    if (field.type === "checkbox") {
      return (
        <input
          type="checkbox"
          className="cp-cell-check"
          checked={value === true}
          onChange={(event) => update(index, field.col, event.target.checked)}
        />
      );
    }

    if (field.type === "select") {
      return (
        <select
          className="cp-cell-select"
          style={{ minWidth }}
          value={value == null ? "" : String(value)}
          onChange={(event) => update(index, field.col, event.target.value)}
        >
          <option value="">—</option>
          {(field.options ?? []).map((option) => (
            <option key={option} value={option}>
              {option}
            </option>
          ))}
        </select>
      );
    }

    if (field.type === "number") {
      return (
        <div className="flex items-center gap-1">
          <input
            type="number"
            className="cp-cell-input cp-cell-num"
            style={{ minWidth }}
            value={value == null ? "" : String(value)}
            min={field.minValue}
            max={field.maxValue}
            step={field.step ?? 1}
            onChange={(event) =>
              update(index, field.col, event.target.value === "" ? "" : Number(event.target.value))
            }
          />
          {field.percent ? <span className="text-muted text-xs">%</span> : null}
        </div>
      );
    }

    if (field.type === "date") {
      return (
        <input
          type="date"
          className="cp-cell-input"
          style={{ minWidth: 150 }}
          value={value ? String(value).slice(0, 10) : ""}
          onChange={(event) => update(index, field.col, event.target.value)}
        />
      );
    }

    if (field.type === "link") {
      const href = safeHref(value);
      return (
        <div className="flex flex-col gap-1">
          <input
            type="url"
            className="cp-cell-input"
            style={{ minWidth }}
            placeholder="https://"
            value={value == null ? "" : String(value)}
            onChange={(event) => update(index, field.col, event.target.value)}
          />
          {href ? (
            <a
              href={href}
              target="_blank"
              rel="noopener noreferrer"
              className="truncate px-2 text-xs text-brand"
            >
              open
            </a>
          ) : value ? (
            <span className="truncate px-2 text-xs text-muted">
              not an http(s) link
            </span>
          ) : null}
        </div>
      );
    }

    return (
      <input
        type="text"
        className="cp-cell-input"
        style={{ minWidth }}
        value={value == null ? "" : String(value)}
        onChange={(event) => update(index, field.col, event.target.value)}
      />
    );
  }

  function renderRow(row: Row, index: number) {
    return (
      <tr key={row.id != null ? `id-${row.id}` : `new-${index}`}>
        {spec.fields.map((field) => (
          <td key={field.col}>{renderCell(field, row, index)}</td>
        ))}
        <td className="w-[46px]">
          <button
            type="button"
            className="cp-row-del"
            title="Remove this row"
            onClick={() => removeRow(index)}
          >
            ×
          </button>
        </td>
      </tr>
    );
  }

  return (
    <div>
      <div className="mb-3 flex flex-wrap items-center gap-2">
        <button type="button" className="cp-btn" onClick={addRow} disabled={pending}>
          + Add row
        </button>
        <button
          type="button"
          className="cp-btn cp-btn-primary"
          onClick={save}
          disabled={pending || !dirty}
        >
          {pending ? "Saving…" : dirty ? "Save changes" : "Saved"}
        </button>
        <span className="text-muted text-xs">
          {rows.length} row{rows.length === 1 ? "" : "s"}
          {dirty ? " · unsaved edits" : ""}
        </span>
        {notice ? (
          <span className={`cp-toast ${notice.kind}`} role="status">
            {notice.text}
          </span>
        ) : null}
      </div>

      <div className="cp-grid-wrap" style={height ? { maxHeight: height } : undefined}>
        <table className="cp-grid">
          <thead>
            <tr>
              {spec.fields.map((field) => (
                <th key={field.col} title={field.help ?? undefined}>
                  {field.label}
                  {field.required ? <span className="text-rose"> *</span> : null}
                </th>
              ))}
              <th />
            </tr>
          </thead>
          <tbody>
            {groups
              ? groups.map((group, groupIndex) => (
                  <Fragment key={`group-${groupIndex}`}>
                    <tr className="cp-group-row">
                      <td colSpan={spec.fields.length + 1}>{group.label || "Ungrouped"}</td>
                    </tr>
                    {group.items.map((item) => renderRow(item.row, item.index))}
                  </Fragment>
                ))
              : rows.map((row, index) => renderRow(row, index))}
          </tbody>
        </table>
      </div>

      <p className="cp-note mt-3">
        Type straight into the cells. New rows are highlighted until you save; removing a row and
        saving deletes it from the database.
      </p>
    </div>
  );
}
