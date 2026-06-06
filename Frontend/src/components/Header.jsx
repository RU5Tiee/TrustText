import { useNavigate } from 'react-router-dom';
import { Shield, Upload, Download, Clock, Grid } from 'lucide-react';

const Header = ({ title }) => {
  const navigate = useNavigate();

  return (
    <div style={{ display: 'flex', flexDirection: 'column' }}>
      <header className="glass-panel app-header">
        <div className="logo" style={{ cursor: 'pointer' }} onClick={() => navigate('/')}>
          <Shield size={24} color="var(--accent-primary)" />
          <span>TrustText</span>
        </div>
        
        <div style={{ fontWeight: 600, flex: 1, textAlign: 'center', color: 'var(--text-muted)' }}>
          {title || 'Analysis Dashboard'}
        </div>

        <div style={{ display: 'flex', gap: '12px' }}>
          <button className="glass-button" onClick={() => navigate('/dashboard')} title="Dashboard">
            <Grid size={18} />
          </button>
          <button className="glass-button" onClick={() => navigate('/frameworks')} title="Framework View">
            <Shield size={18} />
          </button>
          <button className="glass-button" onClick={() => navigate('/history')} title="History">
            <Clock size={18} />
          </button>
          <button className="glass-button" onClick={() => navigate('/')} title="Upload New">
            <Upload size={18} />
          </button>
        </div>
      </header>
      
      <div style={{ 
        background: 'rgba(245, 158, 11, 0.1)', 
        borderBottom: '1px solid rgba(245, 158, 11, 0.2)',
        padding: '8px', 
        textAlign: 'center', 
        fontSize: '0.8rem', 
        color: 'var(--accent-warning)',
        margin: '0 16px'
      }}>
        Results shown below are generated using AI models and regulatory mappings. Human review is recommended before making legal or compliance decisions.
      </div>
    </div>
  );
};

export default Header;
