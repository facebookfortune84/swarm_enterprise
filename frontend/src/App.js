import React, { useState, useEffect } from 'react';
import { 
  Cpu, 
  Settings, 
  Terminal, 
  ShieldCheck, 
  Download, 
  Activity, 
  Layers, 
  CheckCircle2, 
  AlertCircle,
  LayoutGrid
} from 'lucide-react';

const API_BASE = "https://corp.realms2riches.com/api";

function App() {
  const [vibe, setVibe] = useState("");
  const [projectName, setProjectName] = useState("LegalFlow AI");
  const [selectedStack, setSelectedStack] = useState("Python FastAPI + React");
  const [projects, setProjects] = useState([]);
  const [activeProject, setActiveProject] = useState(null);
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(false);
  const [systemStatus, setSystemStatus] = useState("OFFLINE");

  // --- 1. INITIALIZATION & POLLING ---
  useEffect(() => {
    checkHealth();
    loadProjects();
    
    // Auto-poll tickets every 5 seconds if a project is active
    const interval = setInterval(() => {
      if (activeProject) refreshTickets(activeProject);
    }, 5000);
    
    return () => clearInterval(interval);
  }, [activeProject]);

  const checkHealth = async () => {
    try {
      const res = await fetch(\`\${API_BASE}/health\`);
      if (res.ok) setSystemStatus("ONLINE");
    } catch (e) {
      setSystemStatus("OFFLINE");
    }
  };

  const loadProjects = async () => {
    try {
      const res = await fetch(\`\${API_BASE}/projects\`);
      const data = await res.json();
      setProjects(data);
    } catch (e) { console.error("Failed to load history"); }
  };

  const refreshTickets = async (projectId) => {
    try {
      const res = await fetch(\`\${API_BASE}/tickets/\${projectId}\`);
      const data = await res.json();
      setTickets(data);
    } catch (e) { console.error("Ticket sync error"); }
  };

  // --- 2. SWARM COMMANDS ---
  const executeSprint = async () => {
    setLoading(true);
    try {
      const res = await fetch(\`\${API_BASE}/build\`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          name: projectName,
          description: vibe,
          stack: selectedStack
        })
      });
      const data = await res.json();
      setActiveProject(data.project_id);
      loadProjects();
    } catch (e) {
      alert("Swarm connection failed. Check your tunnel.");
    }
    setLoading(false);
  };

  const downloadReplica = async () => {
    const res = await fetch(\`\${API_BASE}/replicate\`, { method: 'POST' });
    const data = await res.json();
    window.location.href = data.download_url;
  };

  // --- 3. UI RENDERING ---
  return (
    <div className="min-h-screen bg-[#020617] text-slate-200 font-sans">
      {/* Top Navigation */}
      <nav className="border-b border-slate-800 bg-[#020617]/80 backdrop-blur-md sticky top-0 z-50 px-8 py-4 flex justify-between items-center">
        <div className="flex items-center gap-3">
          <Cpu className="text-cyan-400 animate-pulse" />
          <h1 className="text-xl font-black tracking-tighter text-white uppercase">Swarm OS <span className="text-cyan-500 text-xs">v1.0</span></h1>
        </div>
        <div className="flex items-center gap-6 text-xs font-bold uppercase tracking-widest">
          <div className="flex items-center gap-2">
            <div className={\`w-2 h-2 rounded-full \${systemStatus === 'ONLINE' ? 'bg-green-500 shadow-[0_0_10px_green]' : 'bg-red-500'}\`}></div>
            <span className={systemStatus === 'ONLINE' ? 'text-green-500' : 'text-red-500'}>{systemStatus}</span>
          </div>
          <button onClick={downloadReplica} className="flex items-center gap-2 bg-slate-800 hover:bg-slate-700 px-4 py-2 rounded-lg transition-all border border-slate-700">
            <Download size={14}/> Replicate Company
          </button>
        </div>
      </nav>

      <div className="grid grid-cols-12 gap-8 p-8">
        
        {/* Left: Input Console */}
        <section className="col-span-12 lg:col-span-4 space-y-6">
          <div className="bg-slate-900/50 border border-slate-800 p-6 rounded-2xl shadow-xl">
            <h2 className="text-sm font-black text-cyan-500 uppercase mb-6 flex items-center gap-2">
              <Terminal size={16}/> Command Input
            </h2>
            
            <div className="space-y-4">
              <div>
                <label className="text-[10px] uppercase font-bold text-slate-500 block mb-2">Project Identity</label>
                <input 
                  className="w-full bg-slate-950 border border-slate-800 p-3 rounded-lg focus:outline-none focus:border-cyan-500 transition-colors"
                  value={projectName}
                  onChange={(e) => setProjectName(e.target.value)}
                />
              </div>
              
              <div>
                <label className="text-[10px] uppercase font-bold text-slate-500 block mb-2">Application Vibe (Instructions)</label>
                <textarea 
                  className="w-full h-48 bg-slate-950 border border-slate-800 p-3 rounded-lg focus:outline-none focus:border-cyan-500 transition-colors text-sm"
                  placeholder="e.g. Build a high-scale legal SaaS with Stripe..."
                  value={vibe}
                  onChange={(e) => setVibe(e.target.value)}
                />
              </div>

              <div>
                <label className="text-[10px] uppercase font-bold text-slate-500 block mb-2">Architecture Stack</label>
                <select 
                  className="w-full bg-slate-950 border border-slate-800 p-3 rounded-lg focus:outline-none text-sm"
                  value={selectedStack}
                  onChange={(e) => setSelectedStack(e.target.value)}
                >
                  <option>Python FastAPI + React</option>
                  <option>Node.js Next.js + MongoDB</option>
                  <option>Pure Python + Streamlit</option>
                </select>
              </div>

              <button 
                onClick={executeSprint}
                disabled={loading || systemStatus === 'OFFLINE'}
                className="w-full bg-cyan-600 hover:bg-cyan-500 text-white font-black py-4 rounded-xl shadow-lg shadow-cyan-900/20 transition-all disabled:opacity-50"
              >
                {loading ? 'CONVENING BOARD...' : 'INITIATE FRACTAL SPRINT'}
              </button>
            </div>
          </div>

          {/* History */}
          <div className="bg-slate-900/50 border border-slate-800 p-6 rounded-2xl">
            <h2 className="text-[10px] font-black text-slate-500 uppercase mb-4">Project History</h2>
            <div className="space-y-2 max-h-64 overflow-y-auto">
              {projects.map(p => (
                <div 
                  key={p.id} 
                  onClick={() => setActiveProject(p.id)}
                  className={\`p-3 rounded-lg border cursor-pointer transition-all \${activeProject === p.id ? 'border-cyan-500 bg-cyan-500/10' : 'border-slate-800 hover:bg-slate-800'}\`}
                >
                  <div className="text-xs font-bold text-white">{p.name}</div>
                  <div className="text-[10px] text-slate-500 uppercase">{p.id}</div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Right: Ticket Kanban (Linear Clone) */}
        <section className="col-span-12 lg:col-span-8 bg-slate-900/30 border border-slate-800 p-8 rounded-2xl min-h-[700px]">
          <div className="flex justify-between items-center mb-8">
            <h2 className="text-sm font-black text-cyan-500 uppercase flex items-center gap-2">
              <LayoutGrid size={16}/> Fractal Task Queue
            </h2>
            <div className="text-[10px] text-slate-500 uppercase">
              Project: <span className="text-white font-bold">{activeProject || 'None Selected'}</span>
            </div>
          </div>

          {!activeProject ? (
            <div className="flex flex-col items-center justify-center h-full text-slate-600">
              <Layers size={48} className="mb-4 opacity-20"/>
              <p className="text-sm uppercase tracking-widest">Awaiting Sprint Initialization</p>
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
              {/* Kanban Column: Todo */}
              <div className="space-y-4">
                <div className="text-[10px] font-black text-slate-500 uppercase flex items-center gap-2 border-b border-slate-800 pb-2">
                  <Activity size={12}/> Open Directives
                </div>
                {tickets.filter(t => t.status === 'open').map(t => (
                  <div key={t.id} className="bg-slate-900 border border-slate-800 p-4 rounded-xl shadow-sm border-l-4 border-l-cyan-500">
                    <div className="text-[10px] text-cyan-400 font-bold mb-1">{t.assigned_role}</div>
                    <div className="text-sm font-bold text-white">{t.title}</div>
                  </div>
                ))}
              </div>

              {/* Kanban Column: In Progress */}
              <div className="space-y-4">
                <div className="text-[10px] font-black text-slate-500 uppercase flex items-center gap-2 border-b border-slate-800 pb-2">
                  <Activity size={12} className="animate-spin"/> Executing
                </div>
                {tickets.filter(t => t.status === 'claimed' || t.status === 'in_progress').map(t => (
                  <div key={t.id} className="bg-slate-900 border border-slate-800 p-4 rounded-xl shadow-sm border-l-4 border-l-yellow-500">
                    <div className="text-[10px] text-yellow-400 font-bold mb-1">{t.assigned_role}</div>
                    <div className="text-sm font-bold text-white">{t.title}</div>
                  </div>
                ))}
              </div>

              {/* Kanban Column: Verified */}
              <div className="space-y-4">
                <div className="text-[10px] font-black text-slate-500 uppercase flex items-center gap-2 border-b border-slate-800 pb-2">
                  <CheckCircle2 size={12}/> Verified Output
                </div>
                {tickets.filter(t => t.status === 'verified' || t.status === 'completed').map(t => (
                  <div key={t.id} className="bg-slate-900 border border-slate-800 p-4 rounded-xl shadow-sm border-l-4 border-l-green-500">
                    <div className="text-[10px] text-green-400 font-bold mb-1">{t.assigned_role}</div>
                    <div className="text-sm font-bold text-white">{t.title}</div>
                    <div className="mt-2 text-[10px] text-slate-500 font-mono italic truncate">{t.file}</div>
                  </div>
                ))}
              </div>
            </div>
          )}
        </section>
      </div>
    </div>
  );
}

export default App;