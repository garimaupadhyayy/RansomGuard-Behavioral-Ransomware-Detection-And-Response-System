import { useEffect, useState } from "react";
import Sidebar, { type Tab } from "./components/Sidebar";
import DashboardPage from "./pages/DashboardPage";
import AlertsPage from "./pages/AlertsPage";
import TimelinePage from "./pages/TimelinePage";
import MitrePage from "./pages/MitrePage";
import QuarantinePage from "./pages/QuarantinePage";
import IocSearchPage from "./pages/IocSearchPage";
import IncidentsPage from "./pages/IncidentsPage";
import { api, WS_URL } from "./api/client";

export default function App() {
  const [tab, setTab] = useState<Tab>("dashboard");
  const [wsConnected, setWsConnected] = useState(false);
  const [simulationMode, setSimulationMode] = useState(true);

  useEffect(() => {
    api.get("/system/status").then((r) => setSimulationMode(r.data.simulation_mode)).catch(() => {});

    const ws = new WebSocket(WS_URL);
    ws.onopen = () => setWsConnected(true);
    ws.onclose = () => setWsConnected(false);
    ws.onerror = () => setWsConnected(false);
    return () => ws.close();
  }, []);

  return (
    <div style={{ display: "flex", minHeight: "100vh", width: "100%" }}>
      <Sidebar active={tab} onChange={setTab} wsConnected={wsConnected} simulationMode={simulationMode} />
      <main style={{ flex: 1, minWidth: 0, padding: "2rem 2.5rem", width: "100%", overflowX: "hidden" }}>
        {tab === "dashboard" && <DashboardPage />}
        {tab === "alerts" && <AlertsPage />}
        {tab === "timeline" && <TimelinePage />}
        {tab === "incidents" && <IncidentsPage />}
        {tab === "mitre" && <MitrePage />}
        {tab === "quarantine" && <QuarantinePage />}
        {tab === "ioc" && <IocSearchPage />}
      </main>
    </div>
  );
}
