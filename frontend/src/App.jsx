import { useEffect, useMemo, useState } from 'react';
import Home from './pages/Home';
import AnalysisPage from './pages/Analysis';

const navItems = [
  {
    id: 'overview',
    label: 'Overview',
    title: 'Overview',
    description: 'Your workplace prompt optimization workspace.',
  },
  {
    id: 'analyzer',
    label: 'Prompt Analyzer',
    title: 'Prompt Analyzer',
    description: 'Analyze, understand, and optimize your workplace prompts.',
  },
];

export default function App() {
  const [activePage, setActivePage] = useState('overview');
  const [backendStatus, setBackendStatus] = useState(null);
  const [sessionAnalyses, setSessionAnalyses] = useState([]);

  useEffect(() => {
    async function checkBackendStatus() {
      try {
        const response = await fetch('/health');
        const payload = await response.json().catch(() => ({}));
        setBackendStatus(response.ok && payload.status === 'ok' ? 'connected' : 'offline');
      } catch {
        setBackendStatus('offline');
      }
    }

    checkBackendStatus();
    const intervalId = window.setInterval(checkBackendStatus, 15000);
    return () => window.clearInterval(intervalId);
  }, []);

  const currentPage = useMemo(
    () => navItems.find((item) => item.id === activePage) || navItems[0],
    [activePage]
  );

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand-block">
          <div className="brand-mark">S</div>
          <div>
            <div className="brand-name">SmartPrompt</div>
            <div className="brand-subtitle">AI Prompt Assistant</div>
          </div>
        </div>

        <nav className="nav-list" aria-label="Main navigation">
          {navItems.map((item) => (
            <button
              key={item.id}
              type="button"
              className={`nav-item ${activePage === item.id ? 'active' : ''}`}
              onClick={() => setActivePage(item.id)}
            >
              <span className="nav-icon">{item.label.charAt(0)}</span>
              <span>{item.label}</span>
            </button>
          ))}
        </nav>

        <div className="sidebar-footer">
          <p>Dataset</p>
          <span>IFEval-inspired workplace prompt corpus</span>
          <strong>v1.0</strong>
        </div>
      </aside>

      <main className="main-panel">
        <header className="topbar">
          <div>
            <p className="breadcrumb">SmartPrompt / {currentPage.title}</p>
            <h1>{currentPage.title}</h1>
            <p className="header-description">{currentPage.description}</p>
          </div>

          {backendStatus && (
            <div className={`status-pill ${backendStatus === 'connected' ? 'online' : 'offline'}`}>
              <span className="status-dot" />
              {backendStatus === 'connected' ? 'Backend connected' : 'Backend offline'}
            </div>
          )}
        </header>

        <div hidden={activePage !== 'overview'}>
          <Home onNavigate={setActivePage} sessionAnalyses={sessionAnalyses} />
        </div>
        <div hidden={activePage !== 'analyzer'}>
          <AnalysisPage onAnalysis={(result, prompt) => {
            setSessionAnalyses((current) => [...current, { ...result, prompt }]);
          }} />
        </div>
      </main>
    </div>
  );
}
