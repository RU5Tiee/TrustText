import { useState } from 'react';
import Header from '../components/Header';
import Sidebar from '../components/Sidebar';
import PolicyViewer from '../components/PolicyViewer';
import ClausePanel from '../components/ClausePanel';

const Dashboard = ({ data }) => {
  const [activeCategory, setActiveCategory] = useState(null);
  const [selectedClause, setSelectedClause] = useState(null);

  if (!data) return null;

  const { summary, risk_assessment, findings } = data;

  // Counts
  const highRiskCount = findings.filter(f => f.RiskLevel === 'HIGH' || f.RiskLevel === 'SEVERE' || f.ReviewStatus === 'REVIEW_REQUIRED').length;
  const mediumRiskCount = findings.filter(f => f.RiskLevel === 'MEDIUM').length;
  const lowRiskCount = findings.filter(f => f.RiskLevel === 'LOW').length;

  return (
    <div className="app-container animate-fade-in">
      <Header title={`Analyzing: ${summary.title}`} />
      
      <div style={{ padding: '16px 24px 0 24px' }}>
        <div className="summary-grid">
          <div className="glass-panel stat-card">
            <span className="stat-label">App Context</span>
            <span className="stat-value" style={{ fontSize: '1.2rem', marginTop: 'auto' }}>
              {summary.app_context || 'Unknown Context'}
            </span>
          </div>
          <div className="glass-panel stat-card">
            <span className="stat-label">Overall Risk</span>
            <span className="stat-value" style={{ fontSize: '1.5rem', marginTop: 'auto' }}>
              {risk_assessment.severity === 'REVIEW' ? 'REVIEW NEEDED' : risk_assessment.severity}
            </span>
          </div>
          <div className="glass-panel stat-card">
            <span className="stat-label">Total Clauses</span>
            <span className="stat-value">{summary.clauses_processed}</span>
          </div>
          <div className="glass-panel stat-card" style={{ borderLeft: '4px solid var(--accent-danger)' }}>
            <span className="stat-label">High Risk Clauses</span>
            <span className="stat-value">{highRiskCount}</span>
          </div>
          <div className="glass-panel stat-card" style={{ borderLeft: '4px solid var(--accent-warning)' }}>
            <span className="stat-label">Medium Risk</span>
            <span className="stat-value">{mediumRiskCount}</span>
          </div>
          <div className="glass-panel stat-card" style={{ borderLeft: '4px solid var(--accent-success)' }}>
            <span className="stat-label">Low Risk</span>
            <span className="stat-value">{lowRiskCount}</span>
          </div>
        </div>
      </div>

      <div className="main-content">
        <Sidebar 
          findings={findings} 
          activeCategory={activeCategory} 
          setActiveCategory={(cat) => { setActiveCategory(cat); setSelectedClause(null); }} 
        />
        
        <PolicyViewer 
          findings={findings} 
          activeCategory={activeCategory} 
          onClauseClick={(clause) => setSelectedClause(clause)} 
        />
        
        <ClausePanel 
          clauseData={selectedClause} 
          onClose={() => setSelectedClause(null)} 
        />
      </div>
    </div>
  );
};

export default Dashboard;
