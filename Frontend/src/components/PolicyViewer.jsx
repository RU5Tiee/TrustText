import { useEffect, useRef } from 'react';
import { categoryColors } from '../utils/constants';

const PolicyViewer = ({ findings, activeCategory, onClauseClick }) => {
  const viewerRef = useRef(null);

  useEffect(() => {
    if (activeCategory && viewerRef.current) {
      const firstActive = viewerRef.current.querySelector('.is-active-cat');
      if (firstActive) {
        firstActive.scrollIntoView({ behavior: 'smooth', block: 'center' });
        // Give focus to the viewer so keyboard scrolling (arrows/PageDown) works immediately
        viewerRef.current.focus({ preventScroll: true });
      }
    }
  }, [activeCategory]);

  return (
    <div className="glass-panel policy-viewer" ref={viewerRef} tabIndex={-1} style={{ outline: 'none' }}>
      {findings.map((f, i) => {
        const cat = f.Category || f.PredictedCategory || 'Other';
        const color = categoryColors[cat] || '#64748b';
        
        let isActive = false;
        if (activeCategory === null) {
          isActive = true;
        } else if (activeCategory === 'REVIEW') {
          isActive = f.ReviewStatus === 'REVIEW_REQUIRED' || f.RiskLevel === 'REVIEW';
        } else {
          isActive = activeCategory === cat;
        }

        // Increased opacity from 0.3 to 0.5 so the rest of the policy remains readable
        const opacity = isActive ? 1 : 0.5;
        const highlightStyle = isActive && (cat !== 'Other' || activeCategory === 'REVIEW')
          ? { borderLeftColor: activeCategory === 'REVIEW' && isActive ? 'var(--accent-danger)' : color, backgroundColor: activeCategory === 'REVIEW' && isActive ? 'rgba(239, 68, 68, 0.1)' : `${color}1A` } 
          : { borderLeftColor: 'transparent' };

        return (
          <div 
            key={i} 
            className={`policy-clause ${isActive && (cat !== 'Other' || activeCategory === 'REVIEW') ? 'clause-highlight' : ''} ${isActive ? 'is-active-cat' : ''}`}
            style={{ opacity, ...highlightStyle }}
            onClick={() => isActive && onClauseClick(f)}
            title={`Category: ${cat} | Risk: ${f.RiskLevel || 'N/A'}`}
          >
            {f.clause}
          </div>
        );
      })}
    </div>
  );
};

export default PolicyViewer;
