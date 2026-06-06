import { categoryColors } from '../utils/constants';

const Sidebar = ({ findings, activeCategory, setActiveCategory }) => {
  // Aggregate stats
  const catStats = {};
  findings.forEach(f => {
    const cat = f.Category || f.PredictedCategory || 'Other';
    if (!catStats[cat]) catStats[cat] = { count: 0, highRisk: false };
    catStats[cat].count += 1;
    if (f.RiskLevel === 'HIGH' || f.RiskLevel === 'SEVERE' || f.ReviewStatus === 'REVIEW_REQUIRED') {
      catStats[cat].highRisk = true;
    }
  });

  const reviewCount = findings.filter(f => f.ReviewStatus === 'REVIEW_REQUIRED' || f.RiskLevel === 'REVIEW').length;

  return (
    <div className="glass-panel sidebar">
      <h3 style={{ fontSize: '0.85rem', textTransform: 'uppercase', color: 'var(--text-muted)', marginBottom: '8px' }}>
        Categories
      </h3>
      
      <div 
        className={`category-item ${activeCategory === null ? 'active' : ''}`}
        onClick={() => setActiveCategory(null)}
      >
        <span>All Clauses</span>
        <span className="badge">{findings.length}</span>
      </div>

      {reviewCount > 0 && (
        <div 
          className={`category-item ${activeCategory === 'REVIEW' ? 'active' : ''}`}
          onClick={() => setActiveCategory('REVIEW')}
          style={{ borderLeft: '3px solid var(--accent-danger)' }}
        >
          <span style={{ color: 'var(--accent-danger)', fontWeight: 600 }}>Needs Review</span>
          <span className="badge" style={{ background: 'rgba(239, 68, 68, 0.2)', color: 'var(--accent-danger)' }}>{reviewCount}</span>
        </div>
      )}

      {Object.keys(catStats).map(cat => (
        <div 
          key={cat} 
          className={`category-item ${activeCategory === cat ? 'active' : ''}`}
          onClick={() => setActiveCategory(cat)}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
            <div 
              className="cat-indicator" 
              style={{ backgroundColor: categoryColors[cat] || '#64748b' }}
            ></div>
            <span style={{ fontSize: '0.9rem', maxWidth: '180px', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
              {cat}
            </span>
          </div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '6px' }}>
            {catStats[cat].highRisk && (
              <span style={{ color: 'var(--accent-danger)', fontSize: '1rem', lineHeight: 1 }}>!</span>
            )}
            <span className="badge">{catStats[cat].count}</span>
          </div>
        </div>
      ))}
    </div>
  );
};

export default Sidebar;
