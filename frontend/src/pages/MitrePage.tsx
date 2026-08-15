import { useEffect, useState } from "react";
import { api } from "../api/client";
import PageHeader from "../components/PageHeader";

const TECHNIQUES: { id: string; name: string; tactic: string }[] = [
  { id: "T1486", name: "Data Encrypted for Impact", tactic: "Impact" },
  { id: "T1083", name: "File and Directory Discovery", tactic: "Discovery" },
  { id: "T1490", name: "Inhibit System Recovery", tactic: "Impact" },
  { id: "T1057", name: "Process Discovery", tactic: "Discovery" },
  { id: "T1105", name: "Ingress Tool Transfer", tactic: "Command and Control" },
];

export default function MitrePage() {
  const [summary, setSummary] = useState<Record<string, number>>({});

  useEffect(() => {
    api.get("/mitre/summary").then((r) => setSummary(r.data)).catch(() => {});
  }, []);

  const maxCount = Math.max(1, ...Object.values(summary));

  return (
    <div>
      <PageHeader
        eyebrow="ATT&CK Coverage"
        title="MITRE ATT&CK Matrix"
        description="How many recorded alerts matched each MITRE technique, mapped from behavioral signals in real time."
      />

      <div style={{ display: "grid", gridTemplateColumns: "repeat(auto-fill, minmax(280px, 1fr))", gap: "1rem" }}>
        {TECHNIQUES.map((t) => {
          const count = summary[t.id] || 0;
          const pct = Math.round((count / maxCount) * 100);
          return (
            <div key={t.id} className="card card-glow">
              <div style={{ display: "flex", justifyContent: "space-between", alignItems: "flex-start" }}>
                <span className="mono badge" style={{ background: "rgba(59,130,246,0.1)", color: "var(--blue-400)", border: "1px solid rgba(59,130,246,0.25)" }}>
                  {t.id}
                </span>
                <span style={{ fontSize: "0.68rem", color: "var(--text-muted)" }}>{t.tactic}</span>
              </div>
              <div style={{ fontWeight: 600, fontSize: "0.92rem", margin: "0.75rem 0 0.4rem", color: "var(--text-primary)" }}>{t.name}</div>
              <div style={{ fontFamily: "var(--font-display)", fontSize: "1.9rem", fontWeight: 700 }}>{count}</div>
              <div style={{ height: 5, borderRadius: 3, background: "var(--border-soft)", marginTop: 10, overflow: "hidden" }}>
                <div style={{ height: "100%", width: `${count > 0 ? Math.max(pct, 8) : 0}%`, background: "linear-gradient(90deg, var(--blue-500), var(--blue-400))", borderRadius: 3 }} />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
