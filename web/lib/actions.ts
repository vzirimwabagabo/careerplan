"use server";

import { supabase } from "./supabase";
import { TABLES, editableColumns, fieldType, type TableName } from "./tables";
import type { Row } from "./data";

export type SaveOutcome =
  | { ok: true; rows: Row[]; inserted: number; updated: number; deleted: number; skipped: number }
  | { ok: false; error: string };

/** Convert a raw form value into the shape Postgres expects for that column. */
function coerce(type: string | undefined, value: unknown): unknown {
  switch (type) {
    case "checkbox":
      return value === true || value === "true" || value === 1 || value === "1";
    case "number": {
      if (value === "" || value === null || value === undefined) return 0;
      const parsed = Number(value);
      return Number.isFinite(parsed) ? Math.round(parsed) : 0;
    }
    case "date": {
      if (!value) return null;
      const iso = String(value).slice(0, 10);
      return /^\d{4}-\d{2}-\d{2}$/.test(iso) ? iso : null;
    }
    default: {
      if (value === null || value === undefined) return null;
      const trimmed = String(value).trim();
      return trimmed === "" ? null : trimmed;
    }
  }
}

function isBlank(payload: Row, required: string | undefined): boolean {
  if (required && !payload[required]) return true;
  return Object.values(payload).every(
    (value) => value === null || value === "" || value === 0 || value === false,
  );
}

export async function saveTable(table: string, rows: Row[]): Promise<SaveOutcome> {
  if (!(table in TABLES)) return { ok: false, error: `Unknown table "${table}".` };
  const name = table as TableName;
  const columns = editableColumns(name);
  const spec = TABLES[name];
  const required = spec.fields.find((field) => field.required)?.col;
  const hasOrder = columns.includes("sort_order");

  const { data: existing, error: readError } = await supabase.from(name).select("id");
  if (readError) return { ok: false, error: readError.message };
  const existingIds = new Set((existing ?? []).map((item) => Number(item.id)));

  let highestOrder = 0;
  for (const row of rows) {
    const value = Number(row.sort_order);
    if (Number.isFinite(value) && value > highestOrder) highestOrder = value;
  }
  let pendingOrder = (highestOrder || 0) + 10;

  const inserts: Row[] = [];
  const updates: { id: number; payload: Row }[] = [];
  const kept = new Set<number>();
  let skipped = 0;

  for (const row of rows) {
    const payload: Row = {};
    for (const col of columns) payload[col] = coerce(fieldType(name, col), row[col]);

    const rawId = row.id;
    const hasId = rawId !== null && rawId !== undefined && rawId !== "" && Number.isFinite(Number(rawId));

    if (!hasId) {
      if (isBlank(payload, required)) {
        skipped += 1;
        continue;
      }
      if (hasOrder && !payload.sort_order) {
        payload.sort_order = pendingOrder;
        pendingOrder += 10;
      }
      inserts.push(payload);
      continue;
    }

    const id = Number(rawId);
    kept.add(id);
    if (existingIds.has(id)) updates.push({ id, payload });
  }

  const removed = [...existingIds].filter((id) => !kept.has(id));

  try {
    if (inserts.length) {
      const { error } = await supabase.from(name).insert(inserts);
      if (error) throw new Error(error.message);
    }

    for (const { id, payload } of updates) {
      const { error } = await supabase.from(name).update(payload).eq("id", id);
      if (error) throw new Error(error.message);
    }

    if (removed.length) {
      const { error } = await supabase.from(name).delete().in("id", removed);
      if (error) throw new Error(error.message);
    }
  } catch (error) {
    const message = error instanceof Error ? error.message : String(error);
    return { ok: false, error: message };
  }

  let query = supabase.from(name).select("*");
  for (const clause of spec.order) {
    query = query.order(clause.column, { ascending: clause.ascending ?? true });
  }
  const { data, error } = await query;
  if (error) return { ok: false, error: error.message };

  if (inserts.length || updates.length || removed.length) {
    await supabase.from("activity").insert({
      area: spec.label,
      message: `Saved ${inserts.length} new, ${updates.length} changed, ${removed.length} removed.`,
    });
  }

  return {
    ok: true,
    rows: (data ?? []) as Row[],
    inserted: inserts.length,
    updated: updates.length,
    deleted: removed.length,
    skipped,
  };
}

export async function saveSettings(
  entries: Record<string, string>,
): Promise<{ ok: true } | { ok: false; error: string }> {
  const payload = Object.entries(entries).map(([key, value]) => ({ key, value: value ?? "" }));
  const { error } = await supabase.from("settings").upsert(payload, { onConflict: "key" });
  if (error) return { ok: false, error: error.message };
  await supabase.from("activity").insert({ area: "Plan settings", message: "Plan notes updated." });
  return { ok: true };
}

export async function resetActivity(): Promise<{ ok: true } | { ok: false; error: string }> {
  const { error } = await supabase.from("activity").delete().gte("id", 0);
  if (error) return { ok: false, error: error.message };
  return { ok: true };
}
