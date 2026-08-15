import { useEffect, useState } from "react";
import { FileDown, FileWarning } from "lucide-react";
import { api } from "../api/client";
import PageHeader from "../components/PageHeader";

interface Incident {
  id: number;
  title: string;
  hostname?: string;
  user?: string;
  status: string;
  started_at: string;
  resolved_at?: string;
}

const STATUS_BADGE: Record<string, string> = {
  open: "badge-critical",
  contained: "badge-high",
  simulated: "badge-medium",
  recovered: "badge-low",
  closed: "badge-low",
};

export default function IncidentsPage() {
  const [incidents, setIncidents] = useState<Incident[]>([]);
  const [downloading, setDownloading] = useState<number | null>(null);

  useEffect(() => {
    api.get("/incidents").then((r) => setIncidents(r.data)).catch(() => {});
  }, []);

  const downloadReport = async (id: number) => {
    setDownloading(id);
    try {
      const res = await api.get(`/incidents/${id}/report`);
      alert(`PDF generated on the server at:\n${res.data.report_path}\n\n(Saved inside backend/reports_output/)`);
    } catch {
      alert("Failed to generate report. Check the backend terminal for errors.");
    } finally {
      setDownloading(null);
    }
  };

  return (
    <div>
      <PageHeader
        eyebrow="Case Management"
        title="Incidents"
        description="Confirmed ransomware incidents (risk score ≥ 80). Generate a full PDF report for any incident."
      />

      <div className="card" style={{ padding: 0, overflow: "hidden" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 8, padding: "0.9rem 1rem", borderBottom: "1px solid var(--border-soft)" }}>
          <FileWarning size={14} color="var(--critical)" />
          <span style={{ fontSize: "0.8rem", color: "var(--text-secondary)" }}>{incidents.length} incidents on record</span>
        </div>
        <table className="data-table">
          <thead>
            <tr>
              <th>Title</th>
              <th>Hostname</th>
              <th>User</th>
              <th>Status</th>
              <th>Started</th>
              <th>Report</th>
            </tr>
          </thead>
          <tbody>
            {incidents.map((i) => (
              <tr key={i.id}>
                <td style={{ fontSize: "0.82rem" }}>{i.title}</td>
                <td className="mono" style={{ fontSize: "0.78rem" }}>{i.hostname || "-"}</td>
                <td className="mono" style={{ fontSize: "0.78rem" }}>{i.user || "-"}</td>
                <td><span className={`badge ${STATUS_BADGE[i.status] || "badge-medium"}`}>{i.status}</span></td>
                <td className="mono" style={{ fontSize: "0.72rem", color: "var(--text-muted)" }}>{new Date(i.started_at).toLocaleString()}</td>
                <td>
                  <button className="btn" onClick={() => downloadReport(i.id)} disabled={downloading === i.id} style={{ display: "flex", alignItems: "center", gap: 6 }}>
                    <FileDown size={13} /> {downloading === i.id ? "Generating..." : "Download PDF"}
                  </button>
                </td>
              </tr>
            ))}
            {incidents.length === 0 && (
              <tr><td colSpan={6} style={{ padding: "2rem", textAlign: "center", color: "var(--text-muted)" }}>No incidents yet — one is created automatically when a detection scores 80+.</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
