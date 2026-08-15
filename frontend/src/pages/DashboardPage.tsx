import { useEffect, useState } from "react";
import {
  ResponsiveContainer, AreaChart, Area, XAxis, YAxis, Tooltip, CartesianGrid,
  PieChart, Pie, Cell, BarChart, Bar,
} from "recharts";
import { ShieldAlert, FileWarning, FolderLock, ActivitySquare } from "lucide-react";
import { api } from "../api/client";
import StatCard from "../components/StatCard";
import PageHeader from "../components/PageHeader";

const SEVERITY_COLORS: Record<string, string> = {
  critical: "#f43f5e",
  high: "#f59e0b",
  medium: "#eab308",
  low: "#22c55e",
};

interface Alert {
  id: number;
  severity: string;
  score: number;
  mitre_techniques?: string;
  timestamp: string;
}

export default function DashboardPage() {
  const [alerts, setAlerts] = useState<Alert[]>([]);
  const [incidentCount, setIncidentCount] = useState(0);
  const [quarantineCount, setQuarantineCount] = useState(0);
  const [processCount, setProcessCount] = useState(0);

  useEffect(() => {
    api.get("/alerts?limit=200").then((r) => setAlerts(r.data)).catch(() => {});
    api.get("/incidents").then((r) => setIncidentCount(r.data.length)).catch(() => {});
    api.get("/quarantine").then((r) => setQuarantineCount(r.data.length)).catch(() => {});
    api.get("/events/processes?limit=1").then((r) => setProcessCount(r.data.length)).catch(() => {});
  }, []);

  const severityCounts = alerts.reduce<Record<string, number>>((acc, a) => {
    acc[a.severity] = (acc[a.severity] || 0) + 1;
    return acc;
  }, {});
  const pieData = Object.entries(severityCounts).map(([name, value]) => ({ name, value }));

  // Alerts bucketed by hour for a simple trend line
  const trendMap: Record<string, number> = {};
  alerts.forEach((a) => {
    const d = new Date(a.timestamp);
    const key = `${d.getHours()}:00`;
    trendMap[key] = (trendMap[key] || 0) + 1;
  });
  const trendData = Object.entries(trendMap).map(([time, count]) => ({ time, count }));

  const mitreCounts: Record<string, number> = {};
  alerts.forEach((a) => {
    (a.mitre_techniques || "").split(",").forEach((t) => {
      const id = t.trim();
      if (id) mitreCounts[id] = (mitreCounts[id] || 0) + 1;
    });
  });
  const mitreData = Object.entries(mitreCounts).map(([technique, count]) => ({ technique, count }));

  return (
    <div>
      <PageHeader
        eyebrow="Security Operations Center"
        title="Overview"
        description="Real-time behavioral detection across watched endpoints — file activity, process behavior, and containment status."
      />

      <div style={{ display: "flex", gap: "1rem", flexWrap: "wrap", marginBottom: "1.25rem" }}>
        <StatCard label="Total Alerts" value={alerts.length} icon={ShieldAlert} accent="#60a5fa" />
        <StatCard label="Incidents" value={incidentCount} icon={FileWarning} accent="#f43f5e" />
        <StatCard label="Quarantined Items" value={quarantineCount} icon={FolderLock} accent="#f59e0b" />
        <StatCard label="Processes Tracked" value={processCount || "—"} icon={ActivitySquare} accent="#22c55e" />
      </div>

      <div style={{ display: "grid", gridTemplateColumns: "1.4fr 1fr", gap: "1rem", marginBottom: "1rem" }}>
        <div className="card" style={{ minWidth: 0, overflow: "hidden" }}>
          <div style={{ fontSize: "0.85rem", fontWeight: 600, marginBottom: 4 }}>Alert Activity</div>
          <div style={{ fontSize: "0.75rem", color: "var(--text-muted)", marginBottom: 12 }}>Detections grouped by hour</div>
          {trendData.length > 0 ? (
            <div style={{ width: "100%", height: 220 }}>
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={trendData}>
                <defs>
                  <linearGradient id="colorCount" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.4} />
                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#16203a" vertical={false} />
                <XAxis dataKey="time" stroke="#5c6c8a" fontSize={11} tickLine={false} axisLine={false} />
                <YAxis stroke="#5c6c8a" fontSize={11} tickLine={false} axisLine={false} allowDecimals={false} />
                <Tooltip contentStyle={{ background: "#0d1424", border: "1px solid #1b2740", borderRadius: 8, fontSize: 12 }} />
                <Area type="monotone" dataKey="count" stroke="#3b82f6" strokeWidth={2} fill="url(#colorCount)" />
              </AreaChart>
            </ResponsiveContainer>
            </div>
          ) : (
            <EmptyChart text="No alerts yet — trend will appear once detections start." />
          )}
        </div>

        <div className="card" style={{ minWidth: 0, overflow: "hidden" }}>
          <div style={{ fontSize: "0.85rem", fontWeight: 600, marginBottom: 4 }}>Severity Breakdown</div>
          <div style={{ fontSize: "0.75rem", color: "var(--text-muted)", marginBottom: 12 }}>By alert count</div>
          {pieData.length > 0 ? (
            <div style={{ width: "100%", height: 220 }}>
            <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie data={pieData} dataKey="value" nameKey="name" innerRadius={55} outerRadius={80} paddingAngle={3}>
                  {pieData.map((entry) => (
                    <Cell key={entry.name} fill={SEVERITY_COLORS[entry.name] || "#3b82f6"} />
                  ))}
                </Pie>
                <Tooltip contentStyle={{ background: "#0d1424", border: "1px solid #1b2740", borderRadius: 8, fontSize: 12 }} />
              </PieChart>
            </ResponsiveContainer>
            </div>
          ) : (
            <EmptyChart text="No alerts yet." />
          )}
          <div style={{ display: "flex", gap: "0.75rem", flexWrap: "wrap", marginTop: 8, justifyContent: "center" }}>
            {pieData.map((entry) => (
              <div key={entry.name} style={{ display: "flex", alignItems: "center", gap: 6, fontSize: "0.72rem", color: "var(--text-secondary)" }}>
                <span style={{ width: 8, height: 8, borderRadius: 2, background: SEVERITY_COLORS[entry.name] || "#3b82f6" }} />
                {entry.name} ({entry.value})
              </div>
            ))}
          </div>
        </div>
      </div>

      <div className="card" style={{ minWidth: 0, overflow: "hidden" }}>
        <div style={{ fontSize: "0.85rem", fontWeight: 600, marginBottom: 4 }}>MITRE ATT&CK Technique Frequency</div>
        <div style={{ fontSize: "0.75rem", color: "var(--text-muted)", marginBottom: 12 }}>How many alerts matched each technique</div>
        {mitreData.length > 0 ? (
          <div style={{ width: "100%", height: 200 }}>
          <ResponsiveContainer width="100%" height="100%">
            <BarChart data={mitreData}>
              <CartesianGrid strokeDasharray="3 3" stroke="#16203a" vertical={false} />
              <XAxis dataKey="technique" stroke="#5c6c8a" fontSize={11} tickLine={false} axisLine={false} />
              <YAxis stroke="#5c6c8a" fontSize={11} tickLine={false} axisLine={false} allowDecimals={false} />
              <Tooltip contentStyle={{ background: "#0d1424", border: "1px solid #1b2740", borderRadius: 8, fontSize: 12 }} />
              <Bar dataKey="count" fill="#3b82f6" radius={[6, 6, 0, 0]} />
            </BarChart>
          </ResponsiveContainer>
          </div>
        ) : (
          <EmptyChart text="No MITRE-mapped alerts yet." />
        )}
      </div>
    </div>
  );
}

function EmptyChart({ text }: { text: string }) {
  return (
    <div style={{ height: 180, display: "flex", alignItems: "center", justifyContent: "center", color: "var(--text-muted)", fontSize: "0.82rem" }}>
      {text}
    </div>
  );
}
