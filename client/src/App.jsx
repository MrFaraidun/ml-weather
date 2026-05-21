import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from './context/ThemeContext';
import Layout from './components/Layout';
import HomePage from './pages/HomePage';
import PredictionPage from './pages/PredictionPage';
import ComparisonPage from './pages/ComparisonPage';
import StatisticsPage from './pages/StatisticsPage';
import DatasetPage from './pages/DatasetPage';

function App() {
  return (
    <ThemeProvider>
      <Router>
        <Layout>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/prediction" element={<PredictionPage />} />
            <Route path="/comparison" element={<ComparisonPage />} />
            <Route path="/statistics" element={<StatisticsPage />} />
            <Route path="/dataset" element={<DatasetPage />} />
          </Routes>
        </Layout>
      </Router>
    </ThemeProvider>
  );
}

export default App;
