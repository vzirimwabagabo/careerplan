import { DataGrid } from "@/components/DataGrid";
import { BulletList, Card, Hero, Section } from "@/components/ui";
import { readSettings, readTable } from "@/lib/data";

export const dynamic = "force-dynamic";

function splitLines(value: string): string[] {
  return (value ?? "")
    .split("\n")
    .map((line) => line.trim())
    .filter(Boolean);
}

function paragraphs(value: string): string[] {
  return (value ?? "").split("\n\n").filter(Boolean);
}

export default async function JourneyPage() {
  const [journey, experiences, settings] = await Promise.all([
    readTable("journey"),
    readTable("experiences"),
    readSettings(),
  ]);

  return (
    <div className="space-y-6">
      <Hero
        eyebrow="Profile and background"
        title="Journey & profile"
        description={settings.current_focus}
      />

      <Card title="About" subtitle="Who you are and how you work">
        <div className="cp-prose">
          {paragraphs(settings.about).map((block, index) => (
            <p key={index}>{block}</p>
          ))}
        </div>
      </Card>

      <div className="grid gap-4 lg:grid-cols-2">
        <Card title="Aspiration" subtitle="The long game">
          <p className="text-sm leading-7 text-[#33415c]">{settings.aspiration}</p>
        </Card>
        <Card title="Long-term direction" subtitle="Where this is heading">
          <p className="text-sm leading-7 text-[#33415c]">{settings.long_term_direction}</p>
        </Card>
      </div>

      <div className="grid gap-4 lg:grid-cols-2">
        <Card title="Roles being targeted" subtitle="Next move">
          <BulletList items={splitLines(settings.next_roles)} />
        </Card>
        <Card title="Alternative pathways" subtitle={settings.alternative_paths_caveat}>
          <p className="mb-3 text-sm leading-7 text-[#33415c]">{settings.alternative_paths}</p>
          <p className="cp-note">{settings.alternative_paths_caveat}</p>
        </Card>
      </div>

      <Card title="Career journey" subtitle="The road so far, oldest first">
        <div className="cp-timeline">
          {journey.map((item) => (
            <div className="cp-timeline-item" key={String(item.id)}>
              <div className="cp-timeline-period">{String(item.period ?? "")}</div>
              <div className="cp-timeline-title">{String(item.title ?? "")}</div>
              <div className="cp-timeline-body">{String(item.description ?? "")}</div>
            </div>
          ))}
        </div>
      </Card>

      <Card>
        <Section
          title="Journey entries"
          subtitle="Add milestones as they happen. Keep it factual — diaries read better than news releases."
        />
        <DataGrid table="journey" initialRows={journey} />
      </Card>

      <Card>
        <Section
          title="Experiences and achievements"
          subtitle="Tick 'Evidence verified' only when you actually hold the proof."
        />
        <DataGrid table="experiences" initialRows={experiences} />
      </Card>
    </div>
  );
}
