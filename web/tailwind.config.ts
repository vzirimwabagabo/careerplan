import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./app/**/*.{ts,tsx}", "./components/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        canvas: "#F4F6FB",
        surface: "#FFFFFF",
        line: "#E3E9F4",
        ink: "#1F2A3D",
        muted: "#64748B",
        brand: "#4A7DFF",
        teal: "#17B8A6",
        amber: "#F5A524",
        rose: "#F2545B",
        violet: "#8B6CF0",
      },
      borderRadius: {
        card: "16px",
      },
      boxShadow: {
        card: "0 1px 2px rgba(31,42,61,0.04), 0 8px 24px -12px rgba(31,42,61,0.12)",
        lift: "0 2px 6px rgba(31,42,61,0.06), 0 16px 40px -16px rgba(31,42,61,0.18)",
      },
      fontFamily: {
        sans: ["Inter", "Segoe UI", "system-ui", "sans-serif"],
      },
    },
  },
  plugins: [],
};

export default config;
