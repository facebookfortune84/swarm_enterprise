$reactCode = @"
import React, { useState } from 'react';

function App() {
  const [prompt, setPrompt] = useState("");
  const [stack, setStack] = useState("React, Python, Docker");
  const [loading, setLoading] = useState(false);

  const handleBuild = async () => {
    setLoading(true);
    await fetch('https://corp.realms2riches.com/api/build', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt, tech_stack: stack })
    });
    alert("Swarm Activated! Check C:/SwarmEnterprise/output in a few minutes.");
    setLoading(false);
  };

  return (
    <div style={{ padding: '50px', backgroundColor: '#0f172a', color: '#38bdf8', minHeight: '100vh', fontFamily: 'monospace' }}>
      <h1 style={{ borderBottom: '2px solid #38bdf8' }}>REALMS2RICHES SWARM_OS</h1>
      <div style={{ marginTop: '30px' }}>
        <h3>1. DESCRIBE THE APPLICATION (The Vibe)</h3>
        <textarea 
          style={{ width: '100%', height: '100px', backgroundColor: '#1e293b', color: 'white', border: '1px solid #334155' }}
          value={prompt}
          onChange={(e) => setPrompt(e.target.value)}
          placeholder="e.g. Build a high-scale autonomous e-commerce company..."
        />
      </div>
      <div style={{ marginTop: '20px' }}>
        <h3>2. SELECT TECH STACK</h3>
        <input 
          style={{ width: '100%', padding: '10px', backgroundColor: '#1e293b', color: 'white', border: '1px solid #334155' }}
          value={stack}
          onChange={(e) => setStack(e.target.value)}
        />
      </div>
      <button 
        onClick={handleBuild}
        style={{ marginTop: '30px', padding: '15px 30px', backgroundColor: '#0284c7', color: 'white', fontWeight: 'bold', cursor: 'pointer', border: 'none' }}
      >
        {loading ? "AGENTS WORKING..." : "EXECUTE PRODUCTION SPRINT"}
      </button>
    </div>
  );
}

export default App;
"@ | Out-File -FilePath "C:\SwarmEnterprise\frontend\src\App.js" -Encoding utf8