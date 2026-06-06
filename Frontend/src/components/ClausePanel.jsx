import { X, AlertTriangle, BookOpen, CheckCircle, Lightbulb } from 'lucide-react';
import { categoryColors } from '../utils/constants';

const ClausePanel = ({ clauseData, onClose }) => {
  if (!clauseData) return null;

  const cat = clauseData.Category || clauseData.PredictedCategory || 'Other';
  const risk = clauseData.RiskLevel || clauseData.ReviewStatus || 'N/A';
  
  let riskClass = 'risk-low';
  if (risk === 'MEDIUM') riskClass = 'risk-medium';
  if (risk === 'HIGH') riskClass = 'risk-high';
  if (risk === 'SEVERE' || risk === 'REVIEW_REQUIRED') riskClass = 'risk-severe';

  return (
    <div className={`glass-panel investigation-panel ${clauseData ? 'open' : ''}`}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '20px' }}>
        <h2 style={{ fontSize: '1.2rem', fontWeight: 600 }}>Clause Investigation</h2>
        <button className="glass-button" style={{ padding: '6px' }} onClick={onClose}>
          <X size={18} />
        </button>
      </div>

      <div className="panel-section">
        <div style={{ display: 'flex', gap: '8px', marginBottom: '12px' }}>
          <span className={`risk-badge ${riskClass}`}>{risk}</span>
          <span className="risk-badge" style={{ background: 'rgba(255,255,255,0.1)' }}>
            {cat}
          </span>
          <span className="risk-badge" style={{ background: 'rgba(255,255,255,0.1)' }}>
            {(clauseData.Confidence * 100).toFixed(1)}% Conf
          </span>
        </div>
        
        <div style={{ background: 'rgba(0,0,0,0.2)', padding: '12px', borderRadius: '8px', fontSize: '0.95rem', fontStyle: 'italic', borderLeft: `3px solid ${categoryColors[cat] || '#64748b'}` }}>
          "{clauseData.clause}"
        </div>
      </div>

      {clauseData.Explanation && (
        <div className="panel-section">
          <h3 className="panel-title"><AlertTriangle size={14} style={{ display: 'inline', verticalAlign: '-2px', marginRight: '4px' }} /> Risk Assessment</h3>
          <p style={{ fontSize: '0.9rem', color: 'var(--text-main)', lineHeight: 1.5 }}>
            {clauseData.Explanation}
          </p>
        </div>
      )}

      {clauseData.ReviewExplanation && (
        <div className="panel-section">
          <h3 className="panel-title" style={{ color: 'var(--accent-danger)' }}>Review Required</h3>
          <p style={{ fontSize: '0.9rem', color: 'var(--text-main)', lineHeight: 1.5 }}>
            {clauseData.ReviewExplanation}
          </p>
        </div>
      )}

      {clauseData.LegalContextSummary && (
        <div className="panel-section">
          <h3 className="panel-title"><BookOpen size={14} style={{ display: 'inline', verticalAlign: '-2px', marginRight: '4px' }} /> Legal Interpretation</h3>
          <p style={{ fontSize: '0.9rem', color: 'var(--text-muted)', lineHeight: 1.5 }}>
            {clauseData.LegalContextSummary}
          </p>
        </div>
      )}

      {clauseData.TriggeredRules && clauseData.TriggeredRules.length > 0 && (
        <div className="panel-section">
          <h3 className="panel-title">Triggered Rules</h3>
          <ul style={{ fontSize: '0.85rem', paddingLeft: '20px', color: 'var(--accent-warning)' }}>
            {clauseData.TriggeredRules.map((rule, idx) => (
              <li key={idx}>{rule}</li>
            ))}
          </ul>
        </div>
      )}

      {(clauseData.GDPR_References || clauseData.DPDP_References) && (
        <div className="panel-section">
          <h3 className="panel-title">Framework Mappings</h3>
          <div style={{ display: 'flex', gap: '8px', flexWrap: 'wrap' }}>
            {clauseData.GDPR_References?.map((ref, idx) => {
              const match = ref.match(/(?:Article|Rule|Section|Schedule)\s*([A-Za-z0-9().-]+)/i);
              const display = match ? `GDPR: ${match[1]}` : ref;
              return <span key={`gdpr-${idx}`} className="badge" style={{ background: 'rgba(59, 130, 246, 0.2)', color: '#60a5fa' }}>{display}</span>;
            })}
            {clauseData.DPDP_References?.map((ref, idx) => {
              const match = ref.match(/(?:Article|Rule|Section|Schedule)\s*([A-Za-z0-9().-]+)/i);
              const display = match ? `DPDPA: ${match[1]}` : ref;
              return <span key={`dpdp-${idx}`} className="badge" style={{ background: 'rgba(16, 185, 129, 0.2)', color: '#34d399' }}>{display}</span>;
            })}
          </div>
        </div>
      )}

      {clauseData.ImmediateRemediation && (
        <div className="panel-section" style={{ background: 'rgba(16, 185, 129, 0.05)', padding: '12px', borderRadius: '8px', border: '1px solid rgba(16, 185, 129, 0.2)' }}>
          <h3 className="panel-title" style={{ color: 'var(--accent-success)' }}><CheckCircle size={14} style={{ display: 'inline', verticalAlign: '-2px', marginRight: '4px' }} /> Remediation Suggestion</h3>
          <p style={{ fontSize: '0.9rem', marginBottom: '12px', lineHeight: 1.5 }}>{clauseData.ImmediateRemediation}</p>
        </div>
      )}
    </div>
  );
};

export default ClausePanel;
