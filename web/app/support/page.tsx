import { DataGrid } from "@/components/DataGrid";
import { Badge, Card, Hero, Kpi, Section } from "@/components/ui";
import { readSettings, readTable } from "@/lib/data";

export const dynamic = "force-dynamic";

export default async function SupportPage() {
  const [support, settings] = await Promise.all([readTable("support"), readSettings()]);

  const secured = support.filter((row) => String(row.status) === "Secured").length;
  const inProgress = support.filter((row) => String(row.status) === "In progress").length;
  const needed = support.filter((row) => String(row.status) === "Needed").length;
  const named = support.filter((row) => String(row.who ?? "").trim()).length;

  return (
    <div className="space-y-6">
      <Hero
        eyebrow="Feedback and support"
        title="Support & accountability"
        description="No plan survives contact with reality unless someone else can see it. Record what you need, who is helping, and what is still outstanding."
      />

      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
        <Kpi label="Secured" value={secured} sub="people or resources in place" tone="teal" />
        <Kpi label="In progress" value={inProgress} sub="being arranged" tone="brand" />
        <Kpi label="Still needed" value={needed} sub="nothing in place yet" tone="amber" />
        <Kpi
          label="Named"
          value={`${named}/${support.length}`}
          sub="with a specific person or source"
          tone={named === support.length ? "teal" : "rose"}
        />
      </div>

      <Card>
        <Section
          title="What I need support with"
          subtitle="Fill in the 'Who / source' column with a real name — vague intentions do not chase themselves."
        />
        <DataGrid table="support" initialRows={support} />
      </Card>

      <Card title="My responsibility in this" subtitle="Support is a two-way arrangement">
        <p className="text-sm leading-7 text-[#33415c]">{settings.my_responsibility}</p>
        <div className="mt-4 flex flex-wrap gap-2">
          <Badge tone="accent">Ask for feedback, then act on it</Badge>
          <Badge tone="violet">Communicate progress without being prompted</Badge>
          <Badge tone="teal">Stay accountable for my own development</Badge>
        </div>
      </Card>
    </div>
  );
}
