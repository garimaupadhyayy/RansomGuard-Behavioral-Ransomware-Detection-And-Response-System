import {
  ShieldCheck, LayoutGrid, Radio, GitBranch, FolderLock,
  Search, Fingerprint, FileWarning, type LucideIcon,
} from "lucide-react";

export type Tab = "dashboard" | "alerts" | "timeline" | "incidents" | "mitre" | "quarantine" | "ioc";

interface NavItem {
  id: Tab;
  label: string;
  icon: LucideIcon;
}

const NAV_ITEMS: NavItem[] = [
  { id: "dashboard", label: "Overview", icon: LayoutGrid },
  { id: "alerts", label: "Live Alerts", icon: Radio },
  { id: "timeline", label: "Timeline", icon: GitBranch },
  { id: "incidents", label: "Incidents", icon: FileWarning },
  { id: "mitre", label: "MITRE Matrix", icon: Fingerprint },
  { id: "quarantine", label: "Quarantine", icon: FolderLock },
  { id: "ioc", label: "IOC Search", icon: Search },
];

interface SidebarProps {
  active: Tab;
  onChange: (tab: Tab) => void;
  wsConnected: boolean;
  simulationMode: boolean;
}

export default function Sidebar({ active, onChange, wsConnected, simulationMode }: SidebarProps) {
  return (
    <aside
      style={{
        width: 240,
        flexShrink: 0,
        height: "100vh",
        position: "sticky",
        top: 0,
        borderRight: "1px solid var(--border-soft)",
        display: "flex",
        flexDirection: "column",
        padding: "1.5rem 1rem",
        background: "rgba(13, 20, 36, 0.4)",
      }}
    >
      <div style={{ display: "flex", alignItems: "center", gap: "0.6rem", padding: "0 0.4rem 1.75rem" }}>
        <div
          style={{
            width: 34, height: 34, borderRadius: 9,
            background: "linear-gradient(135deg, var(--blue-500), #1d4ed8)",
            display: "flex", alignItems: "center", justifyContent: "center",
            boxShadow: "0 0 20px var(--blue-glow)",
          }}
        >
          <ShieldCheck size={18} color="#fff" strokeWidth={2.4} />
        </div>
        <div>
          <div style={{ fontFamily: "var(--font-display)", fontWeight: 700, fontSize: "1.05rem", lineHeight: 1 }}>
            RansomGuard
          </div>
          <div style={{ fontFamily: "var(--font-mono)", fontSize: "0.63rem", color: "var(--text-muted)", marginTop: 3 }}>
            EDR / SOC CONSOLE
          </div>
        </div>
      </div>

      <nav style={{ display: "flex", flexDirection: "column", gap: "0.25rem", flex: 1 }}>
        {NAV_ITEMS.map((item) => {
          const isActive = active === item.id;
          const Icon = item.icon;
          return (
            <button
              key={item.id}
              onClick={() => onChange(item.id)}
              style={{
                display: "flex", alignItems: "center", gap: "0.7rem",
                padding: "0.6rem 0.75rem",
                borderRadius: 9,
                border: "none",
                background: isActive ? "rgba(59, 130, 246, 0.12)" : "transparent",
                color: isActive ? "var(--blue-300)" : "var(--text-secondary)",
                fontFamily: "var(--font-body)",
                fontWeight: isActive ? 600 : 500,
                fontSize: "0.87rem",
                cursor: "pointer",
                textAlign: "left",
                borderLeft: isActive ? "2px solid var(--blue-500)" : "2px solid transparent",
                transition: "all 0.15s ease",
              }}
            >
              <Icon size={16} strokeWidth={2.2} />
              {item.label}
            </button>
          );
        })}
      </nav>

      <div style={{ borderTop: "1px solid var(--border-soft)", paddingTop: "1rem", display: "flex", flexDirection: "column", gap: "0.6rem" }}>
        <div style={{ display: "flex", alignItems: "center", gap: "0.5rem", fontSize: "0.75rem", color: "var(--text-secondary)" }}>
          <span className="pulse-dot" style={{ background: wsConnected ? "var(--safe)" : "var(--text-muted)" }} />
          {wsConnected ? "Live feed connected" : "Reconnecting..."}
        </div>
        <div
          className="badge"
          style={{
            background: simulationMode ? "rgba(245, 158, 11, 0.1)" : "rgba(244, 63, 94, 0.1)",
            color: simulationMode ? "var(--high)" : "var(--critical)",
            border: `1px solid ${simulationMode ? "rgba(245,158,11,0.3)" : "rgba(244,63,94,0.3)"}`,
            width: "fit-content",
          }}
        >
          {simulationMode ? "Simulation Mode" : "Live Response Mode"}
        </div>
      </div>
    </aside>
  );
}
