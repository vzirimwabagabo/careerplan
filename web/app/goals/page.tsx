import { DataGrid } from "@/components/DataGrid";
import { Card, Hero, Section } from "@/components/ui";
import { readTable } from "@/lib/data";

export const dynamic = "force-dynamic";

export default async function GoalsPage() {
  const [goals, skills, strengths, stages] = await Promise.all([
    readTable("goals"),
    readTable("skills"),
    readTable("strengths"),
    readTable("career_stages"),
  ]);

  return (
    <div className="space-y-6">
      <Hero
        eyebrow="Goals, skills and capability"
        title="Goals & skills"
        description="What success looks like, the skills you are building, where your capability sits today, and the succession plan that ties it together."
      />

      <Card>
        <Section
          title="Career goals"
          subtitle="Update progress as you go — it feeds the readiness figure on the dashboard."
        />
        <DataGrid table="goals" initialRows={goals} />
      </Card>

      <Card>
        <Section title="Skills to build" subtitle="Each skill needs evidence, not just intent." />
        <DataGrid table="skills" initialRows={skills} />
      </Card>

      <Card>
        <Section
          title="Strengths and development areas"
          subtitle="Rate yourself 1–5 today, then set the level you are aiming for."
        />
        <DataGrid table="strengths" initialRows={strengths} />
      </Card>

      <Card>
        <Section
          title="Career succession plan"
          subtitle="0–12 months, 1–3 years, 3–5+ years. Targets, not guaranteed promotions."
        />
        <DataGrid table="career_stages" initialRows={stages} />
      </Card>
    </div>
  );
}
