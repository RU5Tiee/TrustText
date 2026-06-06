import { useState } from 'react';
import Header from '../components/Header';

const FrameworkView = ({ data }) => {
  const [searchTerm, setSearchTerm] = useState('');

  if (!data) return null;

  const findings = data.findings.filter(f => f.GDPR_References || f.DPDP_References);

  const filteredFindings = findings.filter(f => 
    f.clause.toLowerCase().includes(searchTerm.toLowerCase()) || 
    (f.Category || f.PredictedCategory || '').toLowerCase().includes(searchTerm.toLowerCase())
  );

  return (
    <div className="app-container animate-fade-in">
      <Header title="Framework Compliance View" />
      
      <div className="main-content" style={{ flexDirection: 'column' }}>
        <div className="glass-panel" style={{ padding: '20px', display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
          <div>
            <h2 style={{ fontSize: '1.2rem', marginBottom: '8px' }}>Regulatory Framework Mappings</h2>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.9rem' }}>Explore policy clause mappings to GDPR and DPDPA frameworks.</p>
          </div>
          <input 
            type="text" 
            placeholder="Search mappings..." 
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            style={{ 
              background: 'rgba(255,255,255,0.7)', 
              border: '1px solid rgba(0,0,0,0.1)', 
              padding: '10px 16px', 
              borderRadius: '8px',
              color: 'var(--text-main)',
              width: '300px',
              boxShadow: 'inset 0 1px 3px rgba(0,0,0,0.05)'
            }}
          />
        </div>

        <div className="glass-panel" style={{ flex: 1, overflow: 'auto', padding: '0', border: '1px solid rgba(0,0,0,0.1)' }}>
          <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'left', background: 'rgba(255,255,255,0.6)' }}>
            <thead style={{ background: '#f8f9fa', position: 'sticky', top: 0, boxShadow: '0 2px 4px rgba(0,0,0,0.05)', zIndex: 1 }}>
              <tr>
                <th style={{ padding: '12px 16px', borderRight: '1px solid rgba(0,0,0,0.1)', borderBottom: '2px solid rgba(0,0,0,0.1)', width: '40%', fontSize: '0.9rem', color: '#495057' }}>Clause</th>
                <th style={{ padding: '12px 16px', borderRight: '1px solid rgba(0,0,0,0.1)', borderBottom: '2px solid rgba(0,0,0,0.1)', fontSize: '0.9rem', color: '#495057' }}>Category</th>
                <th style={{ padding: '12px 16px', borderRight: '1px solid rgba(0,0,0,0.1)', borderBottom: '2px solid rgba(0,0,0,0.1)', fontSize: '0.9rem', color: '#495057' }}>GDPR References</th>
                <th style={{ padding: '12px 16px', borderBottom: '2px solid rgba(0,0,0,0.1)', fontSize: '0.9rem', color: '#495057' }}>DPDPA References</th>
              </tr>
            </thead>
            <tbody>
              {filteredFindings.map((f, i) => {
                const formatRef = (fw, ref) => {
                  const match = ref.match(/(?:Article|Rule|Section|Schedule)\s*([A-Za-z0-9().-]+)/i);
                  return match ? `${fw}: ${match[1]}` : ref;
                };
                return (
                  <tr key={i} style={{ borderBottom: '1px solid rgba(0,0,0,0.05)', background: i % 2 === 0 ? 'transparent' : 'rgba(0,0,0,0.02)' }}>
                    <td style={{ padding: '12px 16px', fontSize: '0.9rem', borderRight: '1px solid rgba(0,0,0,0.05)' }}>{f.clause}</td>
                    <td style={{ padding: '12px 16px', fontSize: '0.85rem', borderRight: '1px solid rgba(0,0,0,0.05)' }}>
                      <span className="badge">{f.Category || f.PredictedCategory}</span>
                    </td>
                    <td style={{ padding: '12px 16px', fontSize: '0.85rem', color: '#2563eb', borderRight: '1px solid rgba(0,0,0,0.05)' }}>
                      {f.GDPR_References?.map(r => formatRef('GDPR', r)).join(', ') || '-'}
                    </td>
                    <td style={{ padding: '12px 16px', fontSize: '0.85rem', color: '#059669' }}>
                      {f.DPDP_References?.map(r => formatRef('DPDPA', r)).join(', ') || '-'}
                    </td>
                  </tr>
                );
              })}
              {filteredFindings.length === 0 && (
                <tr>
                  <td colSpan="4" style={{ padding: '32px', textAlign: 'center', color: 'var(--text-muted)' }}>
                    No mappings found matching your search.
                  </td>
                </tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};

export default FrameworkView;
