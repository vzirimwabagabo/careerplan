export default function Loading() {
  return (
    <div className="space-y-5">
      <div className="cp-skeleton" style={{ height: 132 }} />

      <div className="grid gap-3 sm:grid-cols-2 lg:grid-cols-4">
        {[0, 1, 2, 3].map((index) => (
          <div key={index} className="cp-skeleton-card">
            <div className="cp-skeleton" style={{ height: 11, width: "52%" }} />
            <div className="cp-skeleton mt-4" style={{ height: 30, width: "68%" }} />
            <div className="cp-skeleton mt-3" style={{ height: 10, width: "84%" }} />
          </div>
        ))}
      </div>

      <div className="grid gap-4 lg:grid-cols-[minmax(0,1fr)_320px]">
        <div className="cp-skeleton-card space-y-4">
          <div className="cp-skeleton" style={{ height: 14, width: 190 }} />
          {[0, 1, 2, 3, 4].map((index) => (
            <div key={index}>
              <div className="cp-skeleton" style={{ height: 10, width: 140 }} />
              <div className="cp-skeleton mt-2" style={{ height: 8 }} />
            </div>
          ))}
        </div>
        <div className="cp-skeleton-card">
          <div className="cp-skeleton" style={{ height: 14, width: 120 }} />
          <div className="cp-skeleton mt-4" style={{ height: 180 }} />
        </div>
      </div>

      <div className="cp-skeleton-card">
        <div className="cp-skeleton" style={{ height: 14, width: 160 }} />
        <div className="cp-skeleton mt-4" style={{ height: 240 }} />
      </div>
    </div>
  );
}
