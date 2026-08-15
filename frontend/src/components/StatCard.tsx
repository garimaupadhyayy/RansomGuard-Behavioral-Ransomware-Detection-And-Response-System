import type { LucideIcon } from "lucide-react";

interface StatCardProps {
  label: string;
  value: string | number;
  icon: LucideIcon;
  accent?: string;
  sub?: string;
}

export default function StatCard({ label, value, icon: Icon, accent = "var(--blue-400)", sub }: StatCardProps) {
  return (
    <div className="card card-glow" style={{ flex: 1, minWidth: 200 }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
        <div>
          <div style={{ fontSize: "0.75rem", color: "var(--text-muted)", fontWeight: 600, textTransform: "uppercase", letterSpacing: "0.04em" }}>
            {label}
          </div>
          <div style={{ fontFamily: "var(--font-display)", fontSize: "2.1rem", fontWeight: 700, marginTop: 6, color: "var(--text-primary)" }}>
            {value}
          </div>
          {sub && <div style={{ fontSize: "0.75rem", color: "var(--text-secondary)", marginTop: 4 }}>{sub}</div>}
        </div>
        <div
          style={{
            width: 38, height: 38, borderRadius: 10,
            background: "rgba(59,130,246,0.08)",
            display: "flex", alignItems: "center", justifyContent: "center",
          }}
        >
          <Icon size={18} color={accent} strokeWidth={2} />
        </div>
      </div>
    </div>
  );
}
