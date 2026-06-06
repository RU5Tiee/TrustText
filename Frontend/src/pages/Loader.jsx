import React, { useEffect, useState, useRef } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { CheckCircle2, Loader2, FileSearch, ShieldAlert, Cpu } from 'lucide-react';

const Loader = ({ setAnalysisData }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const file = location.state?.file;

  const [activeStep, setActiveStep] = useState(0);
  const uploadStarted = React.useRef(false);

  const steps = [
    { label: "Upload Complete", icon: CheckCircle2 },
    { label: "Extracting Text", icon: FileSearch },
    { label: "Parsing Document", icon: Loader2 },
    { label: "Chunking Clauses", icon: Loader2 },
    { label: "Running Classification Model", icon: Cpu },
    { label: "Calculating Risk Scores", icon: ShieldAlert },
    { label: "Mapping Regulatory Frameworks", icon: Loader2 },
    { label: "Generating Recommendations", icon: Loader2 },
    { label: "Preparing Dashboard", icon: Loader2 }
  ];

  useEffect(() => {
    if (!file) {
      navigate('/');
      return;
    }
    
    if (uploadStarted.current) return;
    uploadStarted.current = true;

    const uploadFile = async () => {
      const formData = new FormData();
      formData.append('file', file);

      try {
        // We will fake progress steps while waiting for the real request to complete
        const progressInterval = setInterval(() => {
          setActiveStep(prev => prev < steps.length - 1 ? prev + 1 : prev);
        }, 1500);

        const response = await fetch('http://localhost:8000/api/v1/analyze', {
          method: 'POST',
          body: formData,
        });

        clearInterval(progressInterval);

        if (!response.ok) {
          throw new Error('Analysis failed');
        }

        const data = await response.json();
        setActiveStep(steps.length); // complete
        
        setTimeout(() => {
          setAnalysisData(data);
          navigate('/dashboard');
        }, 1000);

      } catch (error) {
        console.error(error);
        alert('An error occurred during analysis. Make sure the backend is running at localhost:8000.');
        navigate('/');
      }
    };

    uploadFile();
  }, [file, navigate, setAnalysisData, steps.length]);

  return (
    <div className="loader-container animate-fade-in">
      <div className="glass-panel loader-card">
        <h2 style={{ marginBottom: '24px', textAlign: 'center' }}>Analyzing Policy...</h2>
        <div style={{ marginBottom: '32px' }}>
          {steps.map((step, index) => {
            const Icon = step.icon;
            let statusClass = '';
            if (index < activeStep) statusClass = 'completed';
            else if (index === activeStep) statusClass = 'active';

            return (
              <div key={index} className={`loader-step ${statusClass}`}>
                <Icon size={20} className={index === activeStep ? 'spinner' : ''} />
                <span>{step.label}</span>
              </div>
            );
          })}
        </div>
        <p style={{ textAlign: 'center', color: 'var(--text-muted)', fontSize: '0.9rem' }}>
          Estimated time: ~10 seconds
        </p>
      </div>
    </div>
  );
};

export default Loader;
