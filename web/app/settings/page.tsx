import { SettingsForm } from "@/components/SettingsForm";
import { Card, Hero, Section } from "@/components/ui";
import { readActivity, readSettings } from "@/lib/data";
import { TABLES } from "@/lib/tables";

export const dynamic = "force-dynamic";

function projectHost(): string {
  const url = process.env.NEXT_PUBLIC_SUPABASE_URL ?? "";
  try {
    return new URL(url).host;
  } catch {
    return "not configured";
  }
}

export default async function SettingsPage() {
  const [settings, activity] = await Promise.all([readSettings(), readActivity(20)]);

  return (
    <div className="space-y-6">
      <Hero
        eyebrow="Plan settings"
        title="Plan settings"
        description="Edit the narrative that the rest of the tracker quotes, and see exactly where your data lives."
      />

      <SettingsForm initial={settings} />

      <div className="grid gap-4 lg:grid-cols-2">
        <Card title="Where the data lives" subtitle="No local files, no database to back up by hand">
          <div className="space-y-3 text-sm">
            <div className="flex items-center justify-between gap-3 border-b border-dashed border-line pb-2">
              <span className="text-muted">Hosted on</span>
              <strong>{projectHost()}</strong>
            </div>
            <div className="flex items-center justify-between gap-3 border-b border-dashed border-line pb-2">
              <span className="text-muted">Editable tables</span>
              <strong>{Object.keys(TABLES).length}</strong>
            </div>
            <div className="flex items-center justify-between gap-3">
              <span className="text-muted">Plan version</span>
              <strong>{settings.plan_version || "November 2026"}</strong>
            </div>
          </div>
          <p className="cp-note mt-4">
            Every change is written straight to Supabase, so it shows up on every device that opens
            the link. Export a copy from the Supabase dashboard if you want a personal backup.
          </p>
        </Card>

        <Card title="Activity log" subtitle="The last 20 saves">
          {activity.length ? (
            <div className="space-y-2">
              {activity.map((item, index) => (
                <div
                  key={index}
                  className="flex items-baseline justify-between gap-3 border-b border-dashed border-line pb-2 text-[0.78rem] last:border-0"
                >
                  <div>
                    <div className="font-medium">{item.area}</div>
                    <div className="text-muted">{item.message}</div>
                  </div>
                  <div className="whitespace-nowrap text-[0.7rem] text-muted">
                    {item.ts ? new Date(item.ts).toLocaleString("en-GB") : ""}
                  </div>
                </div>
              ))}
            </div>
          ) : (
            <div className="cp-empty">Nothing logged yet.</div>
          )}
        </Card>
      </div>

      <Card>
        <Section
          title="Resetting the plan"
          subtitle="The original November 2026 content can always be restored"
        />
        <p className="cp-note">
          Re-running <strong>supabase/migrations/0001_init.sql</strong> only inserts content into
          tables that are empty, so it will never overwrite your edits. To start over completely,
          delete the rows in the Supabase table editor first, then run the file again.
        </p>
      </Card>
    </div>
  );
}
