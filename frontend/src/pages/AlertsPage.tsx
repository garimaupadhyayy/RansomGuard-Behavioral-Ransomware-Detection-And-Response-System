import { useEffect, useRef, useState } from "react";
import { Radio } from "lucide-react";
import { api, WS_URL } from "../api/client";
import PageHeader from "../components/PageHeader";

interface AlertItem {
  id: number;
  score: number;
  severity: string;
  reasons: string;
  mitre_techniques: string;
  file_path?: string;
  process_name?: string;
  is_ransomware: boolean;
  action_taken?: string;
  timestamp: string;
}

export default function AlertsPage() {
  const [alerts, setAlerts] = useState<AlertItem[]>([]);
  const [flash, setFlash] = useState<number | null>(null);

  useEffect(() => {
    api.get("/alerts?limit=100").then((r) => setAlerts(r.data)).catch(() => {});

    const ws = new WebSocket(WS_URL);
    ws.onmessage = (event) => {
      try {
        const newAlert = JSON.parse(event.data);
        setAlerts((prev) => [newAlert, ...prev]);
        setFlash(newAlert.id ?? Date.now());
        setTimeout(() => setFlash(null), 1500);
      } catch { /* ignore */ }
    };
    return () => ws.close();
  }, []);

  return (
    <div>
      <PageHeader
        eyebrow="Detection Feed"
        title="Live Alerts"
        description="Every behavioral signal that crossed the alert threshold, streamed live via WebSocket as it happens."
      />

      <div className="card" style={{ padding: 0, overflow: "hidden" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 8, padding: "0.9rem 1rem", borderBottom: "1px solid var(--border-soft)" }}>
          <Radio size={14} color="var(--blue-400)" />
          <span style={{ fontSize: "0.8rem", color: "var(--text-secondary)" }}>{alerts.length} alerts recorded</span>
        </div>
        <div style={{ overflowX: "auto" }}>
          <table className="data-table" style={{ tableLayout: "fixed" }}>
            <thead>
              <tr>
                <th>Severity</th>
                <th>Score</th>
                <th>Target</th>
                <th>Reasons</th>
                <th>MITRE</th>
                <th>Action</th>
                <th>Time</th>
              </tr>
            </thead>
            <tbody>
              {alerts.map((a) => (
                <tr key={a.id} style={{ background: flash === a.id ? "rgba(59,130,246,0.08)" : "transparent" }}>
                  <td><span className={`badge badge-${a.severity}`}>{a.severity}</span></td>
                  <td className="mono" style={{ color: "var(--text-primary)" }}>{a.score}</td>
                  <td className="mono" style={{ fontSize: "0.78rem", maxWidth: 260 }}>
                    <span className="truncate-path" title={a.process_name || a.file_path || "-"}>
                      {a.process_name || a.file_path || "-"}
                    </span>
                  </td>
                  <td style={{ fontSize: "0.78rem", maxWidth: 260 }}>
                    <span className="truncate-path" title={a.reasons}>{a.reasons}</span>
                  </td>
                  <td className="mono" style={{ fontSize: "0.75rem", color: "var(--blue-400)" }}>{a.mitre_techniques}</td>
                  <td style={{ fontSize: "0.78rem" }}>{a.action_taken || "-"}</td>
                  <td className="mono" style={{ fontSize: "0.72rem", color: "var(--text-muted)" }}>
                    {new Date(a.timestamp).toLocaleString()}
                  </td>
                </tr>
              ))}
              {alerts.length === 0 && (
                <tr><td colSpan={7} style={{ padding: "2rem", textAlign: "center", color: "var(--text-muted)" }}>No alerts yet. The system is watching quietly.</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
}
