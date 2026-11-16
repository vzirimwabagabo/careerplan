import { DataGrid } from "@/components/DataGrid";
import { Card, Hero, Kpi, Section } from "@/components/ui";
import { num, readTable } from "@/lib/data";

export const dynamic = "force-dynamic";

function average(values: number[]): number {
  if (!values.length) return 0;
  return values.reduce((sum, value) => sum + value, 0) / values.length;
}

export default async function ActionsPage() {
  const [actions, first90] = await Promise.all([
    readTable("actions_702010"),
    readTable("first90"),
  ]);

  const counts = {
    practice: actions.filter((row) => String(row.bucket) === "70 - Practice").length,
    people: actions.filter((row) => String(row.bucket) === "20 - People").length,
    study: actions.filter((row) => String(row.bucket) === "10 - Study").length,
  };

  const done = first90.filter((row) => row.done === true).length;
  const blocked = actions.filter((row) => String(row.status) === "Blocked").length;
  const blockedPct = Math.round((blocked / Math.max(actions.length, 1)) * 100);

  return (
    <div className="space-y-6">
      <Hero
        eyebrow="70-20-10 and the first 90 days"
        title="Action plan"
        description="70% practice, 20% people, 10% structured study — then the specific tasks that turn the plan into the first three months of work."
      />

      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
        <Kpi label="70 — Practice" value={counts.practice} sub="hands-on actions" tone="brand" />
        <Kpi label="20 — People" value={counts.people} sub="learning from others" tone="teal" />
        <Kpi label="10 — Study" value={counts.study} sub="structured learning" tone="violet" />
        <Kpi
          label="First 90 days"
          value={`${done}/${first90.length}`}
          sub={blockedPct ? `${blocked} action(s) blocked` : "nothing blocked"}
          tone={blockedPct ? "amber" : "teal"}
        />
      </div>

      <Card>
        <Section
          title="70-20-10 actions"
          subtitle="Progress feeds the readiness score. Use Blocked only when something is genuinely stuck."
        />
        <DataGrid table="actions_702010" initialRows={actions} />
      </Card>

      <Card>
        <Section
          title="First 90 days"
          subtitle="Tick a task off and set the completion date — this drives the execution pillar."
        />
        <DataGrid table="first90" initialRows={first90} />
      </Card>

      <Card title="Average progress by bucket" subtitle="Where your effort is actually landing">
        <div className="space-y-4">
          {[
            ["70 - Practice", "brand"],
            ["20 - People", "teal"],
            ["10 - Study", "violet"],
          ].map(([bucket, tone]) => {
            const rows = actions.filter((row) => String(row.bucket) === bucket);
            const percent = Math.round(average(rows.map((row) => num(row.progress))));
            return (
              <div key={bucket}>
                <div className="cp-legend">
                  <span>{bucket}</span>
                  <b>
                    {percent}% · {rows.length} action{rows.length === 1 ? "" : "s"}
                  </b>
                </div>
                <div className={`cp-bar tone-${tone}`}>
                  <span style={{ width: `${percent}%` }} />
                </div>
              </div>
            );
          })}
        </div>
      </Card>
    </div>
  );
}
