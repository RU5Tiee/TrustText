import { useRef, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { UploadCloud, Shield, FileText } from 'lucide-react';

const LandingPage = () => {
  const navigate = useNavigate();
  const fileInputRef = useRef(null);
  const [dragOver, setDragOver] = useState(false);

  const handleFileSelect = (e) => {
    const file = e.target.files[0];
    if (file) {
      startAnalysis(file);
    }
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    const file = e.dataTransfer.files[0];
    if (file) {
      startAnalysis(file);
    }
  };

  const startAnalysis = (file) => {
    navigate('/loader', { state: { file } });
  };

  return (
    <div className="landing-container animate-fade-in">
      <div className="glass-panel upload-card">
        <div className="logo" style={{ justifyContent: 'center', fontSize: '2rem', marginBottom: '16px' }}>
          <Shield size={36} color="var(--accent-primary)" />
          <span>TrustText</span>
        </div>
        <h1 style={{ marginBottom: '12px', fontWeight: 600 }}>AI-Powered Privacy Policy Intelligence</h1>
        <p style={{ color: 'var(--text-muted)', marginBottom: '32px' }}>
          Analyze privacy policies against Industry Data Security Frameworks.
        </p>

        <button 
          className="glass-button primary" 
          style={{ fontSize: '1.1rem', padding: '16px 32px' }}
          onClick={() => fileInputRef.current.click()}
        >
          <UploadCloud />
          Upload Policy
        </button>

        <div 
          className={`upload-area ${dragOver ? 'drag-over' : ''}`}
          onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
          onDragLeave={() => setDragOver(false)}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current.click()}
        >
          <FileText size={48} color="var(--text-muted)" style={{ marginBottom: '16px' }} />
          <p>Drag and drop your document here</p>
          <p style={{ fontSize: '0.85rem', color: 'var(--text-muted)', marginTop: '8px' }}>
            Supported formats: PDF, DOCX, TXT, HTML, XML
          </p>
        </div>

        <input 
          type="file" 
          ref={fileInputRef} 
          style={{ display: 'none' }} 
          accept=".pdf,.docx,.txt,.html,.xml"
          onChange={handleFileSelect}
        />

        <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginTop: '32px' }}>
          Your documents remain private and are processed securely.<br/><br/>
          This system provides AI-assisted analysis and AI can make mistakes. Results should be reviewed by qualified legal, compliance, or privacy professionals before use in production decisions.
        </p>
      </div>
    </div>
  );
};

export default LandingPage;
