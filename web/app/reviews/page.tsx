import { Trend } from "@/components/Charts";
import { DataGrid } from "@/components/DataGrid";
import { Card, Empty, Hero, Kpi, Section, formatDate } from "@/components/ui";
import { num, readSettings, readTable } from "@/lib/data";

export const dynamic = "force-dynamic";

export default async function ReviewsPage() {
  const [reviews, settings] = await Promise.all([readTable("reviews"), readSettings()]);

  const ordered = reviews
    .filter((row) => row.review_date)
    .slice()
    .sort((a, b) => String(a.review_date).localeCompare(String(b.review_date)));

  const trend = ordered.slice(-8).map((row) => ({
    date: String(row.review_date).slice(5),
    confidence: num(row.confidence),
    energy: num(row.energy),
  }));

  const latest = ordered[ordered.length - 1];
  const confidence = latest ? num(latest.confidence) : 0;
  const energy = latest ? num(latest.energy) : 0;

  const openBlockers = String(latest?.blockers ?? "").trim();

  return (
    <div className="space-y-6">
      <Hero
        eyebrow="Review cadence"
        title="Reviews & journal"
        description={settings.review_cadence}
      />

      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
        <Kpi label="Reviews logged" value={reviews.length} sub="all time" tone="brand" />
        <Kpi
          label="Last review"
          value={latest ? formatDate(latest.review_date) : "—"}
          sub={latest ? String(latest.kind ?? "") : "none yet"}
          tone="violet"
        />
        <Kpi
          label="Confidence"
          value={confidence ? `${confidence}/5` : "—"}
          sub="at the last review"
          tone="teal"
        />
        <Kpi
          label="Energy"
          value={energy ? `${energy}/5` : "—"}
          sub="at the last review"
          tone="amber"
        />
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <Card title="Confidence and energy" subtitle="A flat line is a signal too">
          <Trend data={trend} />
        </Card>

        <Card title="Latest blockers" subtitle="Carried from the most recent entry">
          {openBlockers ? (
            <p className="text-sm leading-7 text-[#33415c]">{openBlockers}</p>
          ) : (
            <Empty>
              Nothing logged. After each review, write down what actually slowed you down — that is
              where the useful information lives.
            </Empty>
          )}
          {latest?.next_focus ? (
            <div className="mt-4 border-t border-dashed border-line pt-4">
              <div className="cp-card-sub">Next focus</div>
              <p className="mt-1 text-sm leading-7 text-[#33415c]">{String(latest.next_focus)}</p>
            </div>
          ) : null}
        </Card>
      </div>

      <Card>
        <Section
          title="Review log"
          subtitle="One row per review. Add wins, blockers, the next focus, and how you felt."
        />
        <DataGrid table="reviews" initialRows={reviews} />
      </Card>
    </div>
  );
}
