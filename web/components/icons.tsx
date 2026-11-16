type IconProps = { className?: string };

const base = {
  width: 18,
  height: 18,
  viewBox: "0 0 24 24",
  fill: "none",
  stroke: "currentColor",
  strokeWidth: 1.7,
  strokeLinecap: "round" as const,
  strokeLinejoin: "round" as const,
};

export function GridIcon({ className }: IconProps) {
  return (
    <svg {...base} className={className}>
      <rect x="3" y="3" width="7.5" height="7.5" rx="2" />
      <rect x="13.5" y="3" width="7.5" height="7.5" rx="2" />
      <rect x="3" y="13.5" width="7.5" height="7.5" rx="2" />
      <rect x="13.5" y="13.5" width="7.5" height="7.5" rx="2" />
    </svg>
  );
}

export function TargetIcon({ className }: IconProps) {
  return (
    <svg {...base} className={className}>
      <circle cx="12" cy="12" r="9" />
      <circle cx="12" cy="12" r="4.6" />
      <circle cx="12" cy="12" r="1.1" fill="currentColor" stroke="none" />
    </svg>
  );
}

export function ChecklistIcon({ className }: IconProps) {
  return (
    <svg {...base} className={className}>
      <path d="M9.5 6H20" />
      <path d="M9.5 12H20" />
      <path d="M9.5 18H20" />
      <path d="M3.6 6l1.5 1.5L8 4.6" />
      <path d="M3.6 12l1.5 1.5L8 10.6" />
      <path d="M3.6 18l1.5 1.5L8 16.6" />
    </svg>
  );
}

export function RouteIcon({ className }: IconProps) {
  return (
    <svg {...base} className={className}>
      <circle cx="6" cy="6" r="2.6" />
      <circle cx="18" cy="18" r="2.6" />
      <path d="M8.6 6H14a4 4 0 0 1 0 8h-4a4 4 0 0 0 0 8h.4" />
    </svg>
  );
}

export function NotebookIcon({ className }: IconProps) {
  return (
    <svg {...base} className={className}>
      <path d="M5 5.5A2.5 2.5 0 0 1 7.5 3H19v18H7.5A2.5 2.5 0 0 1 5 18.5z" />
      <path d="M9 3v18" />
      <path d="M13 8h3.5" />
      <path d="M13 12h3.5" />
    </svg>
  );
}

export function PeopleIcon({ className }: IconProps) {
  return (
    <svg {...base} className={className}>
      <circle cx="9.2" cy="8.2" r="3.2" />
      <path d="M3.4 20a5.8 5.8 0 0 1 11.6 0" />
      <path d="M16.2 5.6a3.2 3.2 0 0 1 0 5.9" />
      <path d="M17.4 20a5.9 5.9 0 0 0-1.9-4.4" />
    </svg>
  );
}

export function SlidersIcon({ className }: IconProps) {
  return (
    <svg {...base} className={className}>
      <path d="M4 6h9" />
      <path d="M18.5 6H20" />
      <circle cx="15.7" cy="6" r="2.2" />
      <path d="M4 12h3.5" />
      <path d="M12.5 12H20" />
      <circle cx="10" cy="12" r="2.2" />
      <path d="M4 18h9" />
      <path d="M18.5 18H20" />
      <circle cx="15.7" cy="18" r="2.2" />
    </svg>
  );
}
