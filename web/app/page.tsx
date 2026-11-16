import { Bars, Donut, Trend } from "@/components/Charts";
import { Badge, Bar, Card, Hero, Kpi, Ring, Section } from "@/components/ui";
import { PILLAR_TONE, summarize } from "@/lib/analytics";
import { num, readActivity, readSettings, readTable } from "@/lib/data";

export const dynamic = "force-dynamic";

const STATUS_COLORS: Record<string, string> = {
  Done: "#17B8A6",
  "In progress": "#4A7DFF",
  "Not started": "#C6D0E0",
  Blocked: "#F2545B",
  Paused: "#F5A524",
  Unset: "#E3E9F4",
};

const BUCKET_COLORS: Record<string, string> = {
  "70 - Practice": "#4A7DFF",
  "20 - People": "#17B8A6",
  "10 - Study": "#8B6CF0",
};

function toneFor(percent: number): string {
  if (percent >= 67) return "#17B8A6";
  if (percent >= 34) return "#F5A524";
  return "#F2545B";
}

function average(values: number[]): number {
  if (!values.length) return 0;
  return values.reduce((sum, value) => sum + value, 0) / values.length;
}

export default async function DashboardPage() {
  const [goals, skills, actions, first90, strengths, reviews, settings, activity] =
    await Promise.all([
      readTable("goals"),
      readTable("skills"),
      readTable("actions_702010"),
      readTable("first90"),
      readTable("strengths"),
      readTable("reviews"),
      readSettings(),
      readActivity(6),
    ]);

  const summary = summarize({ goals, skills, actions, first90, strengths, reviews, settings });

  const buckets = ["70 - Practice", "20 - People", "10 - Study"]
    .map((name) => ({
      name,
      value: Math.round(
        average(actions.filter((row) => String(row.bucket) === name).map((row) => num(row.progress))),
      ),
    }))
    .filter((item) => item.value > 0);

  const phases = [
    "Days 1-30 - Direction and preparation",
    "Days 31-60 - Building evidence",
    "Days 61-90 - Applying and improving",
  ].map((name) => {
    const rows = first90.filter((row) => String(row.phase) === name);
    const done = rows.filter((row) => row.done === true).length;
    return { name: name.replace(/^Days /, "Days "), value: rows.length ? Math.round((done / rows.length) * 100) : 0, done, total: rows.length };
  });

  const statusData = Object.entries(summary.statusCounts).map(([name, value]) => ({
    name,
    value,
    color: STATUS_COLORS[name] ?? "#C6D0E0",
  }));

  const trend = reviews
    .filter((row) => row.review_date)
    .slice()
    .sort((a, b) => String(a.review_date).localeCompare(String(b.review_date)))
    .slice(-8)
    .map((row) => ({
      date: String(row.review_date).slice(5),
      confidence: num(row.confidence),
      energy: num(row.energy),
    }));

  const topGoals = goals
    .filter((row) => String(row.status) !== "Done")
    .slice(0, 5);

  return (
    <div className="space-y-5">
      <Hero
        eyebrow={`Plan version ${settings.plan_version || "November 2026"}`}
        title={settings.owner_name || "Career Plan Monitor"}
        description={settings.headline}
        chips={
          <>
            <Badge tone="accent">Day {summary.planDay} of the plan</Badge>
            <Badge tone={summary.blocked ? "rose" : "teal"}>
              {summary.blocked ? `${summary.blocked} blocked` : "Nothing blocked"}
            </Badge>
            <Badge tone="muted">
              Reviews logged: {summary.reviewCount}
              {summary.nextReview ? ` · next due ${summary.nextReview}` : ""}
            </Badge>
          </>
        }
      />

      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
        <Kpi
          label="Readiness"
          value={`${summary.readiness}%`}
          sub="Weighted across the five pillars"
          tone="brand"
        />
        <Kpi
          label="Open actions"
          value={summary.openTasks}
          sub={`of ${summary.totalTasks} 70-20-10 actions`}
          tone="violet"
        />
        <Kpi
          label="First 90 days"
          value={`${first90.filter((row) => row.done === true).length}/${first90.length}`}
          sub="tasks ticked off"
          tone="teal"
        />
        <Kpi
          label="Overdue"
          value={summary.overdue}
          sub={summary.overdue ? "actions past their due date" : "nothing past due"}
          tone={summary.overdue ? "rose" : "teal"}
        />
      </div>

      <div className="grid gap-4 lg:grid-cols-[320px_minmax(0,1fr)]">
        <Card title="Readiness" subtitle="Weighted from what you have recorded">
          <div className="grid place-items-center py-2">
            <Ring
              percent={summary.readiness}
              tone={toneFor(summary.readiness)}
              caption="of the way there"
            />
          </div>
        </Card>

        <Card title="The five pillars" subtitle="How each part of the plan is moving">
          <div>
            {summary.pillars.map((pillar) => (
              <div className="cp-pillar" key={pillar.key}>
                <Bar
                  percent={pillar.percent}
                  tone={PILLAR_TONE[pillar.key]}
                  label={pillar.label}
                  value={`${pillar.percent.toFixed(1)}%`}
                />
                <div className="text-[0.74rem] text-muted">{pillar.detail}</div>
              </div>
            ))}
          </div>
        </Card>
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <Card title="Where every item stands" subtitle="Goals, skills and actions combined">
          <Donut data={statusData} />
        </Card>

        <Card title="70-20-10 balance" subtitle="Average progress in each learning mode">
          {buckets.length ? (
            <Bars data={buckets} suffix="%" />
          ) : (
            <div className="cp-empty">
              Nothing recorded yet. Update progress on the action plan to see this.
            </div>
          )}
        </Card>
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <Card title="First 90 days" subtitle="Completion by phase">
          <div className="space-y-4">
            {phases.map((phase) => (
              <div key={phase.name}>
                <Bar
                  percent={phase.value}
                  tone={phase.value === 100 ? "teal" : "amber"}
                  label={phase.name}
                  value={`${phase.done}/${phase.total}`}
                />
              </div>
            ))}
          </div>
        </Card>

        <Card title="Goals needing attention" subtitle="Everything not yet marked done">
          {topGoals.length ? (
            <div className="space-y-3">
              {topGoals.map((goal) => (
                <div key={String(goal.id)}>
                  <Bar
                    percent={num(goal.progress)}
                    tone="brand"
                    label={String(goal.goal ?? "")}
                    value={`${num(goal.progress)}%`}
                  />
                </div>
              ))}
            </div>
          ) : (
            <div className="cp-empty">Every goal is marked done.</div>
          )}
        </Card>
      </div>

      <div className="grid gap-4 lg:grid-cols-[minmax(0,1fr)_340px]">
        <Card title="Current focus" subtitle="Carried over from the plan">
          <p className="text-sm leading-7 text-[#33415c]">{settings.current_focus}</p>
          <div className="mt-4 border-t border-dashed border-line pt-4">
            <div className="cp-card-sub">My commitment</div>
            <p className="mt-1 text-sm leading-7 text-[#33415c]">{settings.commitment}</p>
          </div>
        </Card>

        <Card title="Recent activity" subtitle="Every save is logged">
          {activity.length ? (
            <div className="space-y-3">
              {activity.map((item, index) => (
                <div key={index} className="border-b border-dashed border-line pb-2 last:border-0">
                  <div className="text-[0.78rem] font-medium">{item.area}</div>
                  <div className="text-[0.75rem] text-muted">{item.message}</div>
                  <div className="mt-0.5 text-[0.7rem] text-muted">
                    {item.ts ? new Date(item.ts).toLocaleString("en-GB") : ""}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="cp-empty">No activity recorded yet.</div>
          )}
        </Card>
      </div>

      {trend.length > 1 ? (
        <Card title="Confidence and energy" subtitle="From your logged reviews">
          <Trend data={trend} />
        </Card>
      ) : null}
    </div>
  );
}
