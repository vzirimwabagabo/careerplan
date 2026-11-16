import type { Metadata } from "next";
import type { ReactNode } from "react";
import { Shell } from "@/components/Shell";
import { readSettings } from "@/lib/data";
import "./globals.css";

export const dynamic = "force-dynamic";

export const metadata: Metadata = {
  title: "Career Plan Monitor",
  description: "Live tracker for the November 2026 Career Development Plan.",
};

export default async function RootLayout({ children }: { children: ReactNode }) {
  // The shell is decorative: if the database is not reachable the page itself
  // will surface the real error, so a failure here must not blank the screen.
  let settings: Record<string, string> = {};
  try {
    settings = await readSettings();
  } catch {
    settings = {};
  }

  return (
    <html lang="en">
      <body>
        <Shell
          owner={settings.owner_name ?? ""}
          initials={settings.owner_initials ?? ""}
          version={settings.plan_version ?? ""}
        >
          {children}
        </Shell>
      </body>
    </html>
  );
}
