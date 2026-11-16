import type { ReactNode } from "react";

export const TONE: Record<string, string> = {
  Done: "teal",
  Achieved: "teal",
  Completed: "teal",
  Secured: "teal",
  "In progress": "accent",
  Ongoing: "accent",
  "Not started": "muted",
  Planned: "muted",
  Needed: "muted",
  Paused: "amber",
  Revised: "amber",
  Blocked: "rose",
};

export function Badge({ children, tone = "muted" }: { children: ReactNode; tone?: string }) {
  if (children === null || children === undefined || children === "") return null;
  return <span className={`cp-badge tone-${tone}`}>{children}</span>;
}

export function StatusBadge({ status }: { status: unknown }) {
  const label = status == null ? "" : String(status);
  if (!label) return <span className="text-muted text-xs">—</span>;
  return <Badge tone={TONE[label] ?? "muted"}>{label}</Badge>;
}

export function Section({ title, subtitle }: { title: string; subtitle?: string }) {
  return (
    <div className="cp-section">
      <div className="cp-section-bar" />
      <div>
        <div className="cp-section-title">{title}</div>
        {subtitle ? <div className="cp-section-sub">{subtitle}</div> : null}
      </div>
    </div>
  );
}

export function Card({
  title,
  subtitle,
  actions,
  children,
  className = "",
}: {
  title?: string;
  subtitle?: string;
  actions?: ReactNode;
  children: ReactNode;
  className?: string;
}) {
  return (
    <div className={`cp-card ${className}`}>
      {title ? (
        <div className="mb-4 flex items-start justify-between gap-3">
          <div>
            <div className="cp-card-title">{title}</div>
            {subtitle ? <div className="cp-card-sub">{subtitle}</div> : null}
          </div>
          {actions}
        </div>
      ) : null}
      {children}
    </div>
  );
}

export function Kpi({
  label,
  value,
  sub,
  tone = "brand",
}: {
  label: string;
  value: ReactNode;
  sub?: ReactNode;
  tone?: string;
}) {
  return (
    <div className={`cp-kpi tone-${tone}`}>
      <div className="cp-kpi-label">{label}</div>
      <div className="cp-kpi-value">{value}</div>
      {sub ? <div className="cp-kpi-sub">{sub}</div> : null}
    </div>
  );
}

export function Bar({
  percent,
  tone = "brand",
  label,
  value,
}: {
  percent: number;
  tone?: string;
  label?: string;
  value?: ReactNode;
}) {
  const clamped = Math.max(0, Math.min(100, Number.isFinite(percent) ? percent : 0));
  return (
    <div>
      {label || value ? (
        <div className="cp-legend">
          <span>{label}</span>
          <b>{value}</b>
        </div>
      ) : null}
      <div className={`cp-bar tone-${tone}`}>
        <span style={{ width: `${clamped}%` }} />
      </div>
    </div>
  );
}

export function Ring({
  percent,
  size = 150,
  stroke = 12,
  tone = "#4A7DFF",
  caption,
}: {
  percent: number;
  size?: number;
  stroke?: number;
  tone?: string;
  caption?: ReactNode;
}) {
  const clamped = Math.max(0, Math.min(100, Number.isFinite(percent) ? percent : 0));
  const radius = (size - stroke) / 2;
  const circumference = 2 * Math.PI * radius;
  const dash = (clamped / 100) * circumference;

  return (
    <div className="relative grid place-items-center" style={{ width: size, height: size }}>
      <svg width={size} height={size} className="-rotate-90">
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke="#EDF1F8"
          strokeWidth={stroke}
        />
        <circle
          cx={size / 2}
          cy={size / 2}
          r={radius}
          fill="none"
          stroke={tone}
          strokeWidth={stroke}
          strokeLinecap="round"
          strokeDasharray={`${dash} ${circumference - dash}`}
          style={{ transition: "stroke-dasharray 0.5s ease" }}
        />
      </svg>
      <div className="absolute text-center">
        <div className="text-3xl font-semibold tracking-tight">{clamped.toFixed(1)}%</div>
        {caption ? <div className="mt-0.5 text-[0.72rem] text-muted">{caption}</div> : null}
      </div>
    </div>
  );
}

export function Empty({ children }: { children: ReactNode }) {
  return <div className="cp-empty">{children}</div>;
}

export function Prose({ blocks }: { blocks: string[] }) {
  return (
    <div className="cp-prose">
      {blocks.filter(Boolean).map((block, index) => (
        <p key={index}>{block}</p>
      ))}
    </div>
  );
}

export function BulletList({ items }: { items: string[] }) {
  return (
    <div className="cp-list">
      {items.filter(Boolean).map((item, index) => (
        <div className="cp-list-item" key={index}>
          <span className="cp-list-dot" />
          <span>{item}</span>
        </div>
      ))}
    </div>
  );
}

export function Hero({
  eyebrow,
  title,
  description,
  chips,
}: {
  eyebrow?: string;
  title: string;
  description?: string;
  chips?: ReactNode;
}) {
  return (
    <div className="cp-hero">
      {eyebrow ? <div className="cp-eyebrow">{eyebrow}</div> : null}
      <h1>{title}</h1>
      {description ? <p>{description}</p> : null}
      {chips ? <div className="mt-4 flex flex-wrap items-center gap-2">{chips}</div> : null}
    </div>
  );
}

export function formatDate(value: unknown): string {
  if (!value) return "—";
  const raw = String(value).slice(0, 10);
  const parsed = new Date(`${raw}T00:00:00`);
  if (Number.isNaN(parsed.getTime())) return raw;
  return parsed.toLocaleDateString("en-GB", { day: "2-digit", month: "short", year: "numeric" });
}
