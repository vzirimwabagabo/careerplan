import { supabase } from "./supabase";
import { TABLES, type TableName } from "./tables";

export type Row = Record<string, unknown>;

/** Read a whole table in its declared display order. */
export async function readTable(name: TableName): Promise<Row[]> {
  let query = supabase.from(name).select("*");
  for (const clause of TABLES[name].order) {
    query = query.order(clause.column, { ascending: clause.ascending ?? true });
  }
  const { data, error } = await query;
  if (error) throw new Error(error.message);
  return (data ?? []) as Row[];
}

export async function readSettings(): Promise<Record<string, string>> {
  const { data, error } = await supabase.from("settings").select("key, value");
  if (error) throw new Error(error.message);
  const map: Record<string, string> = {};
  for (const item of data ?? []) {
    map[String(item.key)] = item.value == null ? "" : String(item.value);
  }
  return map;
}

export type ActivityItem = { ts: string; area: string; message: string };

export async function readActivity(limit = 8): Promise<ActivityItem[]> {
  const { data, error } = await supabase
    .from("activity")
    .select("ts, area, message")
    .order("id", { ascending: false })
    .limit(limit);
  if (error) throw new Error(error.message);
  return (data ?? []) as ActivityItem[];
}

/** Number coercion that tolerates nulls and numeric strings from Postgres. */
export function num(value: unknown, fallback = 0): number {
  const parsed = typeof value === "number" ? value : Number(value);
  return Number.isFinite(parsed) ? parsed : fallback;
}

export function text(value: unknown): string {
  return value == null ? "" : String(value);
}
