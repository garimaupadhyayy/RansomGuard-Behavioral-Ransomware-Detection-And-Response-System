import { useState } from "react";
import { Search } from "lucide-react";
import { api } from "../api/client";
import PageHeader from "../components/PageHeader";

export default function IocSearchPage() {
  const [query, setQuery] = useState("");
  const [results, setResults] = useState<any>(null);
  const [loading, setLoading] = useState(false);

  const search = async () => {
    if (!query.trim()) return;
    setLoading(true);
    try {
      const res = await api.get(`/ioc/search?q=${encodeURIComponent(query)}`);
      setResults(res.data);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <PageHeader
        eyebrow="Threat Hunting"
        title="IOC Search"
        description="Search stored indicators of compromise — file hashes, filenames, IP addresses, or domains — across every event RansomGuard has recorded."
      />

      <div className="card" style={{ marginBottom: "1rem" }}>
        <div style={{ display: "flex", gap: "0.6rem" }}>
          <div style={{ flex: 1, position: "relative" }}>
            <Search size={15} color="var(--text-muted)" style={{ position: "absolute", left: 12, top: "50%", transform: "translateY(-50%)" }} />
            <input
              className="input"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => e.key === "Enter" && search()}
              placeholder="e.g. a1b2c3d4... or salary.xlsx or 192.168.1.1"
              style={{ width: "100%", paddingLeft: 36 }}
            />
          </div>
          <button className="btn btn-primary" onClick={search}>{loading ? "Searching..." : "Search"}</button>
        </div>
      </div>

      {results && (
        <div style={{ display: "grid", gridTemplateColumns: "1fr 1fr", gap: "1rem" }}>
          <div className="card">
            <div style={{ fontSize: "0.85rem", fontWeight: 600, marginBottom: 10 }}>
              File Events <span className="mono" style={{ color: "var(--text-muted)", fontWeight: 400 }}>({results.file_events?.length || 0})</span>
            </div>
            {(results.file_events || []).map((f: any) => (
              <div key={f.id} className="mono" style={{ fontSize: "0.78rem", padding: "0.4rem 0", borderBottom: "1px solid var(--border-soft)", color: "var(--text-secondary)" }}>
                {f.file_path} <span style={{ color: "var(--blue-400)" }}>· {f.event_type}</span>
              </div>
            ))}
            {(!results.file_events || results.file_events.length === 0) && <div style={{ color: "var(--text-muted)", fontSize: "0.82rem" }}>No matches.</div>}
          </div>
          <div className="card">
            <div style={{ fontSize: "0.85rem", fontWeight: 600, marginBottom: 10 }}>
              Process Events <span className="mono" style={{ color: "var(--text-muted)", fontWeight: 400 }}>({results.process_events?.length || 0})</span>
            </div>
            {(results.process_events || []).map((p: any) => (
              <div key={p.id} className="mono" style={{ fontSize: "0.78rem", padding: "0.4rem 0", borderBottom: "1px solid var(--border-soft)", color: "var(--text-secondary)" }}>
                {p.name} <span style={{ color: "var(--text-muted)" }}>pid {p.pid}</span> <span style={{ color: "var(--blue-400)" }}>{p.sha256?.slice(0, 16)}...</span>
              </div>
            ))}
            {(!results.process_events || results.process_events.length === 0) && <div style={{ color: "var(--text-muted)", fontSize: "0.82rem" }}>No matches.</div>}
          </div>
        </div>
      )}
    </div>
  );
}
