"use client";

import {
  Bar,
  BarChart,
  CartesianGrid,
  Cell,
  Legend,
  Line,
  LineChart,
  Pie,
  PieChart,
  ResponsiveContainer,
  Tooltip,
  XAxis,
  YAxis,
} from "recharts";

const AXIS = { fontSize: 11, fill: "#64748B" };
const GRID = "#E9EEF7";
const TOOLTIP = {
  contentStyle: {
    borderRadius: 10,
    border: "1px solid #E3E9F4",
    boxShadow: "0 8px 24px -12px rgba(31,42,61,0.25)",
    fontSize: 12,
  },
  labelStyle: { color: "#1F2A3D", fontWeight: 600 },
};

export function Donut({
  data,
  height = 220,
}: {
  data: { name: string; value: number; color: string }[];
  height?: number;
}) {
  const usable = data.filter((item) => item.value > 0);
  if (!usable.length) {
    return <div className="cp-empty">No data recorded yet.</div>;
  }
  return (
    <div style={{ width: "100%", height }}>
      <ResponsiveContainer>
        <PieChart>
          <Pie
            data={usable}
            dataKey="value"
            nameKey="name"
            innerRadius="58%"
            outerRadius="84%"
            paddingAngle={2}
            stroke="#fff"
            strokeWidth={2}
          >
            {usable.map((item) => (
              <Cell key={item.name} fill={item.color} />
            ))}
          </Pie>
          <Tooltip {...TOOLTIP} />
          <Legend
            verticalAlign="bottom"
            iconType="circle"
            wrapperStyle={{ fontSize: 11, color: "#64748B" }}
          />
        </PieChart>
      </ResponsiveContainer>
    </div>
  );
}

export function Bars({
  data,
  height = 220,
  color = "#4A7DFF",
  suffix = "",
}: {
  data: { name: string; value: number }[];
  height?: number;
  color?: string;
  suffix?: string;
}) {
  if (!data.length) return <div className="cp-empty">No data recorded yet.</div>;
  const tall = data.length > 6;
  return (
    <div style={{ width: "100%", height: tall ? height + data.length * 22 : height }}>
      <ResponsiveContainer>
        <BarChart
          data={data}
          layout="vertical"
          margin={{ top: 4, right: 26, bottom: 4, left: 4 }}
        >
          <CartesianGrid horizontal={false} stroke={GRID} />
          <XAxis type="number" tick={AXIS} axisLine={false} tickLine={false} />
          <YAxis
            type="category"
            dataKey="name"
            width={150}
            tick={AXIS}
            axisLine={false}
            tickLine={false}
          />
          <Tooltip
            {...TOOLTIP}
            formatter={(value: number) => [`${value}${suffix}`, ""]}
            cursor={{ fill: "rgba(74,125,255,0.06)" }}
          />
          <Bar dataKey="value" fill={color} radius={[0, 6, 6, 0]} barSize={14} />
        </BarChart>
      </ResponsiveContainer>
    </div>
  );
}

export function Trend({
  data,
  height = 220,
}: {
  data: { date: string; confidence: number; energy: number }[];
  height?: number;
}) {
  if (data.length < 2) {
    return (
      <div className="cp-empty">
        Two or more reviews are needed before a trend appears.
      </div>
    );
  }
  return (
    <div style={{ width: "100%", height }}>
      <ResponsiveContainer>
        <LineChart data={data} margin={{ top: 8, right: 18, bottom: 4, left: -18 }}>
          <CartesianGrid stroke={GRID} vertical={false} />
          <XAxis dataKey="date" tick={AXIS} axisLine={false} tickLine={false} />
          <YAxis domain={[0, 5]} tick={AXIS} axisLine={false} tickLine={false} />
          <Tooltip {...TOOLTIP} />
          <Legend wrapperStyle={{ fontSize: 11, color: "#64748B" }} />
          <Line
            type="monotone"
            dataKey="confidence"
            name="Confidence"
            stroke="#4A7DFF"
            strokeWidth={2.4}
            dot={{ r: 3 }}
          />
          <Line
            type="monotone"
            dataKey="energy"
            name="Energy"
            stroke="#17B8A6"
            strokeWidth={2.4}
            dot={{ r: 3 }}
          />
        </LineChart>
      </ResponsiveContainer>
    </div>
  );
}
