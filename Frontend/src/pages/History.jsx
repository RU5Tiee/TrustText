import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from '../components/Header';
import { Search, Loader2, Trash2 } from 'lucide-react';

const History = ({ setAnalysisData }) => {
  const [historyItems, setHistoryItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const navigate = useNavigate();

  const fetchHistory = async () => {
    try {
      const response = await fetch('http://localhost:8000/api/v1/history');
      if (response.ok) {
        const data = await response.json();
        setHistoryItems(data.history || []);
      }
    } catch (e) {
      console.error("Failed to fetch history", e);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchHistory();
  }, []);

  const loadAnalysis = async (id) => {
    try {
      // alert(`Backend integration ready for history ID: ${id}. In a full implementation, this fetches /api/v1/history/${id} and navigates to the dashboard.`);
      const response = await fetch(`http://localhost:8000/api/v1/history/${id}`);
      if (response.ok) {
        const data = await response.json();
        if (setAnalysisData) {
          setAnalysisData(data);
          navigate('/dashboard');
        } else {
          console.error("setAnalysisData prop not provided to History component.");
        }
      } else {
        alert("Failed to load historical analysis data.");
      }
    } catch (e) {
      console.error(e);
      alert("Error loading historical analysis data.");
    }
  };

  const deleteAnalysis = async (id) => {
    try {
      const response = await fetch(`http://localhost:8000/api/v1/history/${id}`, {
        method: 'DELETE'
      });
      if (response.ok) {
        // Refresh the list
        fetchHistory();
      } else {
        alert("Failed to delete analysis.");
      }
    } catch (e) {
      console.error("Error deleting analysis:", e);
      alert("Error deleting analysis.");
    }
  };

  const filtered = historyItems.filter(h => h.title.toLowerCase().includes(searchTerm.toLowerCase()));

  return (
    <div className="app-container animate-fade-in">
      <Header title="Analysis History" />
      
      <div className="main-content" style={{ flexDirection: 'column' }}>
        <div className="glass-panel" style={{ padding: '20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <h2 style={{ fontSize: '1.2rem', marginBottom: '8px' }}>Historical Analysis Archive</h2>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>Review previously analyzed policies and historical analysis sessions.</p>
          </div>
          <div style={{ position: 'relative' }}>
            <Search size={18} style={{ position: 'absolute', left: '12px', top: '12px', color: 'var(--text-muted)' }} />
            <input 
              type="text" 
              placeholder="Search history..." 
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              style={{ 
                background: 'rgba(255,255,255,0.7)', 
                border: '1px solid rgba(0,0,0,0.1)', 
                padding: '10px 16px 10px 40px', 
                borderRadius: '8px',
                color: 'var(--text-main)',
                width: '300px',
                boxShadow: 'inset 0 1px 3px rgba(0,0,0,0.05)'
              }}
            />
          </div>
        </div>

        <div className="glass-panel" style={{ flex: 1, overflow: 'auto', padding: '0', border: '1px solid rgba(0,0,0,0.1)' }}>
          {loading ? (
            <div style={{ display: 'flex', justifyContent: 'center', alignItems: 'center', height: '100%', flexDirection: 'column', gap: '16px' }}>
              <Loader2 className="spinner" size={32} style={{ animation: 'pulse 1s infinite' }} />
              <p>Loading history...</p>
            </div>
          ) : (
            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', background: 'rgba(255,255,255,0.6)' }}>
              <thead style={{ background: '#f8f9fa', position: 'sticky', top: 0, boxShadow: '0 2px 4px rgba(0,0,0,0.05)', zIndex: 1 }}>
                <tr>
                  <th style={{ padding: '12px 16px', borderBottom: '2px solid rgba(0,0,0,0.1)', fontSize: '0.9rem', color: '#495057' }}>Policy Name</th>
                  <th style={{ padding: '12px 16px', borderBottom: '2px solid rgba(0,0,0,0.1)', fontSize: '0.9rem', color: '#495057' }}>Context</th>
                  <th style={{ padding: '12px 16px', borderBottom: '2px solid rgba(0,0,0,0.1)', fontSize: '0.9rem', color: '#495057' }}>Clauses</th>
                  <th style={{ padding: '12px 16px', borderBottom: '2px solid rgba(0,0,0,0.1)', fontSize: '0.9rem', color: '#495057' }}>Actions</th>
                </tr>
              </thead>
              <tbody>
                {filtered.map((h, i) => (
                  <tr key={i} style={{ borderBottom: '1px solid rgba(0,0,0,0.05)', background: i % 2 === 0 ? 'transparent' : 'rgba(0,0,0,0.02)' }}>
                    <td style={{ padding: '16px', fontWeight: 500, fontSize: '0.9rem' }}>{h.title}</td>
                    <td style={{ padding: '16px', color: 'var(--text-muted)', fontSize: '0.9rem' }}>{h.app_context}</td>
                    <td style={{ padding: '16px' }}>
                      <span className="badge">{h.findings_count}</span>
                    </td>
                    <td style={{ padding: '16px', display: 'flex', gap: '8px' }}>
                      <button className="glass-button" style={{ padding: '6px 12px', fontSize: '0.8rem' }} onClick={() => loadAnalysis(h.analysis_id)}>
                        View
                      </button>
                      <button className="glass-button" style={{ padding: '6px 12px', fontSize: '0.8rem', color: 'var(--accent-danger)' }} onClick={() => deleteAnalysis(h.analysis_id)}>
                        <Trash2 size={14} /> Delete
                      </button>
                    </td>
                  </tr>
                ))}
                {filtered.length === 0 && (
                  <tr>
                    <td colSpan="4" style={{ padding: '32px', textAlign: 'center', color: 'var(--text-muted)' }}>
                      No history found.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          )}
        </div>
      </div>
    </div>
  );
};

export default History;
