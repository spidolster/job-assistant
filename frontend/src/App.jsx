import React, { useEffect, useMemo, useState } from 'react';

const API_BASE = import.meta.env.VITE_API_BASE || 'http://localhost:8000';

async function api(path, options = {}) {
  const response = await fetch(`${API_BASE}${path}`, options);
  const data = await response.json();
  if (!response.ok) {
    throw new Error(data.detail || 'Request failed');
  }
  return data;
}

export default function App() {
  const [resumes, setResumes] = useState([]);
  const [tracker, setTracker] = useState([]);
  const [providers, setProviders] = useState({});
  const [selectedProvider, setSelectedProvider] = useState('openai');
  const [selectedModel, setSelectedModel] = useState('');
  const [resumeId, setResumeId] = useState('');
  const [jdText, setJdText] = useState('');
  const [result, setResult] = useState(null);
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  const modelOptions = useMemo(() => providers[selectedProvider] || [], [providers, selectedProvider]);

  async function loadData() {
    const [resumeData, trackerData, providerData] = await Promise.all([
      api('/resumes'),
      api('/tracker'),
      api('/providers'),
    ]);
    setResumes(resumeData);
    setTracker(trackerData);
    setProviders(providerData.providers || {});
  }

  useEffect(() => {
    loadData().catch((e) => setError(e.message));
  }, []);

  useEffect(() => {
    if (modelOptions.length > 0) {
      setSelectedModel(modelOptions[0]);
    }
  }, [modelOptions]);

  async function onUploadResume(event) {
    const file = event.target.files?.[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      setLoading(true);
      setError('');
      const saved = await api('/resumes/upload', { method: 'POST', body: formData });
      setResumeId(String(saved.id));
      await loadData();
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  async function onAnalyze() {
    try {
      setLoading(true);
      setError('');
      const data = await api('/analyze', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          jd_text: jdText,
          provider: selectedProvider,
          model_name: selectedModel,
          resume_id: resumeId ? Number(resumeId) : null,
          save_to_tracker: true,
        }),
      });
      setResult(data);
      await loadData();
    } catch (e) {
      setError(e.message);
    } finally {
      setLoading(false);
    }
  }

  return (
    <main style={{ fontFamily: 'Arial, sans-serif', maxWidth: 1000, margin: '0 auto', padding: 24 }}>
      <h1>Job Assistant — Phase 3</h1>
      <p>Frontend React + backend FastAPI. Analyze & tracker sekarang terpisah dari Streamlit monolith.</p>

      {error && <p style={{ color: 'crimson' }}>Error: {error}</p>}

      <section style={{ border: '1px solid #ddd', padding: 16, borderRadius: 8, marginBottom: 16 }}>
        <h2>Resume</h2>
        <input type="file" accept="application/pdf" onChange={onUploadResume} disabled={loading} />
        <div style={{ marginTop: 8 }}>
          <select value={resumeId} onChange={(e) => setResumeId(e.target.value)}>
            <option value="">Pilih resume...</option>
            {resumes.map((item) => (
              <option key={item.id} value={item.id}>
                {item.filename}
              </option>
            ))}
          </select>
        </div>
      </section>

      <section style={{ border: '1px solid #ddd', padding: 16, borderRadius: 8, marginBottom: 16 }}>
        <h2>Analyze</h2>
        <div style={{ display: 'flex', gap: 12, marginBottom: 8 }}>
          <select value={selectedProvider} onChange={(e) => setSelectedProvider(e.target.value)}>
            {Object.keys(providers).map((provider) => (
              <option key={provider} value={provider}>
                {provider}
              </option>
            ))}
          </select>
          <select value={selectedModel} onChange={(e) => setSelectedModel(e.target.value)}>
            {modelOptions.map((model) => (
              <option key={model} value={model}>
                {model}
              </option>
            ))}
          </select>
        </div>
        <textarea
          rows={8}
          value={jdText}
          placeholder="Paste Job Description di sini"
          onChange={(e) => setJdText(e.target.value)}
          style={{ width: '100%', marginBottom: 8 }}
        />
        <button type="button" onClick={onAnalyze} disabled={loading || !jdText.trim() || !resumeId}>
          {loading ? 'Memproses...' : 'Analisis'}
        </button>
      </section>

      {result && (
        <section style={{ border: '1px solid #ddd', padding: 16, borderRadius: 8, marginBottom: 16 }}>
          <h2>Hasil</h2>
          <p><strong>{result.company}</strong> — {result.role}</p>
          <p>Match score: {result.match_score}%</p>
          <p>Salary range: {result.salary_range}</p>
          <pre style={{ background: '#f8f8f8', padding: 12, whiteSpace: 'pre-wrap' }}>{result.analysis_result}</pre>
        </section>
      )}

      <section style={{ border: '1px solid #ddd', padding: 16, borderRadius: 8 }}>
        <h2>Tracker</h2>
        <table width="100%" cellPadding="8" style={{ borderCollapse: 'collapse' }}>
          <thead>
            <tr>
              <th align="left">Tanggal</th>
              <th align="left">Company</th>
              <th align="left">Role</th>
              <th align="left">Score</th>
              <th align="left">Salary</th>
            </tr>
          </thead>
          <tbody>
            {tracker.map((item) => (
              <tr key={item.id} style={{ borderTop: '1px solid #eee' }}>
                <td>{item.created_at}</td>
                <td>{item.company}</td>
                <td>{item.role}</td>
                <td>{item.Match_score ?? '-'}</td>
                <td>{item.salary_range || '-'}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>
    </main>
  );
}
