"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import type { ReactNode } from "react";
import {
  ChecklistIcon,
  GridIcon,
  NotebookIcon,
  PeopleIcon,
  RouteIcon,
  SlidersIcon,
  TargetIcon,
} from "./icons";

const NAV: { href: string; label: string; icon: ReactNode }[] = [
  { href: "/", label: "Dashboard", icon: <GridIcon /> },
  { href: "/goals", label: "Goals & skills", icon: <TargetIcon /> },
  { href: "/actions", label: "Action plan", icon: <ChecklistIcon /> },
  { href: "/journey", label: "Journey & profile", icon: <RouteIcon /> },
  { href: "/reviews", label: "Reviews & journal", icon: <NotebookIcon /> },
  { href: "/support", label: "Support & accountability", icon: <PeopleIcon /> },
  { href: "/settings", label: "Plan settings", icon: <SlidersIcon /> },
];

export function Shell({
  children,
  owner,
  initials,
  version,
}: {
  children: ReactNode;
  owner: string;
  initials: string;
  version: string;
}) {
  const pathname = usePathname();

  return (
    <div className="cp-shell">
      <aside className="cp-sidebar">
        <div className="cp-sidebar-brand">
          <div className="cp-avatar">{initials || "CP"}</div>
          <div>
            <div className="cp-brand-title">{owner || "Career Plan"}</div>
            <div className="cp-brand-sub">Career Development Plan</div>
          </div>
        </div>

        <nav className="cp-nav">
          {NAV.map((item) => {
            const active = pathname === item.href;
            return (
              <Link
                key={item.href}
                href={item.href}
                className={`cp-nav-link${active ? " is-active" : ""}`}
                aria-current={active ? "page" : undefined}
              >
                <span className="cp-nav-icon">{item.icon}</span>
                {item.label}
              </Link>
            );
          })}
        </nav>

        <div className="cp-sidebar-foot">
          Plan version {version || "November 2026"}
          <br />
          Edits save to Supabase and apply immediately for everyone with the link.
        </div>
      </aside>

      <main className="cp-main">
        <div className="cp-content">{children}</div>
      </main>
    </div>
  );
}
