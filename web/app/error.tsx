"use client";

export default function GlobalError({
  error,
  reset,
}: {
  error: Error & { digest?: string };
  reset: () => void;
}) {
  const message = error?.message ?? "Unknown error";

  return (
    <div className="cp-card">
      <div className="cp-card-title">The tracker could not read its database</div>
      <div className="cp-card-sub">
        This usually means the tables have not been created in Supabase yet.
      </div>

      <pre
        className="mt-4 overflow-auto rounded-xl border border-line bg-[#fbfcfe] p-3 text-[0.78rem] text-muted"
        style={{ whiteSpace: "pre-wrap" }}
      >
        {message}
      </pre>

      <div className="mt-4 cp-note">
        Run <strong>supabase/migrations/0001_init.sql</strong> in the Supabase SQL Editor, then
        reload. Check that <strong>NEXT_PUBLIC_SUPABASE_URL</strong> and{" "}
        <strong>NEXT_PUBLIC_SUPABASE_PUBLISHABLE_KEY</strong> point at the right project.
      </div>

      <button type="button" className="cp-btn cp-btn-primary mt-4" onClick={reset}>
        Try again
      </button>
    </div>
  );
}
