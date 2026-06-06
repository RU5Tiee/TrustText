import { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import LandingPage from './pages/LandingPage';
import Loader from './pages/Loader';
import Dashboard from './pages/Dashboard';
import History from './pages/History';
import FrameworkView from './pages/FrameworkView';

function App() {
  const [analysisData, setAnalysisData] = useState(null);

  return (
    <Router>
      <Routes>
        <Route path="/" element={<LandingPage />} />
        <Route path="/loader" element={<Loader setAnalysisData={setAnalysisData} />} />
        <Route 
          path="/dashboard" 
          element={analysisData ? <Dashboard data={analysisData} /> : <Navigate to="/" />} 
        />
        <Route path="/history" element={<History setAnalysisData={setAnalysisData} />} />
        <Route path="/frameworks" element={analysisData ? <FrameworkView data={analysisData} /> : <Navigate to="/" />} />
      </Routes>
    </Router>
  );
}

export default App;
