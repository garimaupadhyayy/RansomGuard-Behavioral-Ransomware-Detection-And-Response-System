import { useEffect, useState } from "react";
import { AlertTriangle, FilePlus, FileEdit, FileX, ArrowRightLeft } from "lucide-react";
import { api } from "../api/client";
import PageHeader from "../components/PageHeader";

interface FileEventItem {
  id: number;
  event_type: string;
  file_path: string;
  entropy?: number;
  is_canary: boolean;
  suspicious_extension: boolean;
  timestamp: string;
}

const EVENT_ICON: Record<string, any> = {
  created: FilePlus,
  modified: FileEdit,
  deleted: FileX,
  moved: ArrowRightLeft,
};

export default function TimelinePage() {
  const [events, setEvents] = useState<FileEventItem[]>([]);

  useEffect(() => {
    api.get("/events/files?limit=150").then((r) => setEvents(r.data)).catch(() => {});
  }, []);

  return (
    <div>
      <PageHeader
        eyebrow="Investigation View"
        title="Incident Timeline"
        description="Chronological file-system activity across every watched folder — newest first."
      />

      <div className="card">
        <div style={{ borderLeft: "2px solid var(--border)", paddingLeft: "1.5rem", marginLeft: 8 }}>
          {events.map((e) => {
            const Icon = EVENT_ICON[e.event_type] || FileEdit;
            const isFlag = e.is_canary || e.suspicious_extension;
            return (
              <div key={e.id} style={{ marginBottom: "1.25rem", position: "relative" }}>
                <div
                  style={{
                    position: "absolute", left: "-2.05rem", top: 2,
                    width: 26, height: 26, borderRadius: "50%",
                    background: isFlag ? "rgba(244,63,94,0.15)" : "rgba(59,130,246,0.1)",
                    display: "flex", alignItems: "center", justifyContent: "center",
                    border: `1px solid ${isFlag ? "var(--critical)" : "var(--border)"}`,
                  }}
                >
                  <Icon size={12} color={isFlag ? "var(--critical)" : "var(--blue-400)"} />
                </div>
                <div className="mono" style={{ fontSize: "0.7rem", color: "var(--text-muted)" }}>
                  {new Date(e.timestamp).toLocaleString()}
                </div>
                <div style={{ marginTop: 2 }}>
                  <span style={{ fontWeight: 600, fontSize: "0.85rem", textTransform: "uppercase", color: "var(--text-primary)" }}>
                    {e.event_type}
                  </span>
                  <span className="mono truncate-path" title={e.file_path} style={{ marginLeft: 8, fontSize: "0.82rem", color: "var(--text-secondary)", display: "inline-block", maxWidth: 480, verticalAlign: "middle" }}>
                    {e.file_path}
                  </span>
                  {e.entropy != null && (
                    <span className="mono" style={{ marginLeft: 10, fontSize: "0.72rem", color: "var(--text-muted)" }}>
                      entropy {e.entropy}
                    </span>
                  )}
                  {e.is_canary && (
                    <span className="badge badge-critical" style={{ marginLeft: 10 }}>
                      <AlertTriangle size={10} /> Canary Triggered
                    </span>
                  )}
                  {e.suspicious_extension && !e.is_canary && (
                    <span className="badge badge-high" style={{ marginLeft: 10 }}>Suspicious Extension</span>
                  )}
                </div>
              </div>
            );
          })}
          {events.length === 0 && <div style={{ color: "var(--text-muted)", padding: "1rem 0" }}>No file activity recorded yet.</div>}
        </div>
      </div>
    </div>
  );
}
