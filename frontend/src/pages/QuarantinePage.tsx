import { useEffect, useState } from "react";
import { FolderLock } from "lucide-react";
import { api } from "../api/client";
import PageHeader from "../components/PageHeader";

interface QuarantineItem {
  id: number;
  original_path: string;
  quarantine_path: string;
  sha256?: string;
  reason?: string;
  timestamp: string;
}

export default function QuarantinePage() {
  const [items, setItems] = useState<QuarantineItem[]>([]);

  useEffect(() => {
    api.get("/quarantine").then((r) => setItems(r.data)).catch(() => {});
  }, []);

  return (
    <div>
      <PageHeader
        eyebrow="Containment"
        title="Quarantine Manager"
        description="Executables and files isolated after crossing the confirmed-ransomware threshold."
      />

      <div className="card" style={{ padding: 0, overflow: "hidden" }}>
        <div style={{ display: "flex", alignItems: "center", gap: 8, padding: "0.9rem 1rem", borderBottom: "1px solid var(--border-soft)" }}>
          <FolderLock size={14} color="var(--high)" />
          <span style={{ fontSize: "0.8rem", color: "var(--text-secondary)" }}>{items.length} items isolated</span>
        </div>
        <table className="data-table">
          <thead>
            <tr>
              <th>Original Path</th>
              <th>Quarantine Path</th>
              <th>SHA-256</th>
              <th>Reason</th>
              <th>Time</th>
            </tr>
          </thead>
          <tbody>
            {items.map((q) => (
              <tr key={q.id}>
                <td className="mono" style={{ fontSize: "0.78rem", maxWidth: 220 }}><span className="truncate-path" title={q.original_path}>{q.original_path}</span></td>
                <td className="mono" style={{ fontSize: "0.78rem", maxWidth: 220 }}><span className="truncate-path" title={q.quarantine_path}>{q.quarantine_path}</span></td>
                <td className="mono" style={{ fontSize: "0.72rem", color: "var(--blue-400)" }}>{q.sha256?.slice(0, 16)}...</td>
                <td style={{ fontSize: "0.78rem" }}>{q.reason}</td>
                <td className="mono" style={{ fontSize: "0.72rem", color: "var(--text-muted)" }}>{new Date(q.timestamp).toLocaleString()}</td>
              </tr>
            ))}
            {items.length === 0 && (
              <tr><td colSpan={5} style={{ padding: "2rem", textAlign: "center", color: "var(--text-muted)" }}>Nothing quarantined — no confirmed threats yet.</td></tr>
            )}
          </tbody>
        </table>
      </div>
    </div>
  );
}
