import { useState, useEffect, useCallback } from 'react';
import axios from 'axios';
import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend
} from 'recharts';
import { Activity, Cpu, Layers, Sliders } from 'lucide-react';

const API_BASE = 'http://localhost:3001';

const StatisticsPage = () => {
  const [results, setResults] = useState([]);
  const [isTraining, setIsTraining] = useState(false);
  const [trainStatus, setTrainStatus] = useState('');

  const fetchResults = useCallback(() => {
    axios.get(`${API_BASE}/models/results`).then(res => setResults(res.data));
  }, []);

  const checkStatus = useCallback(() => {
    axios.get(`${API_BASE}/status`).then(res => {
      setTrainStatus(res.data.message);
      const running = res.data.status === 'running';
      if (isTraining && !running) {
        fetchResults();
      }
      setIsTraining(running);
    });
  }, [isTraining, fetchResults]);

  useEffect(() => {
    fetchResults();
    const interval = setInterval(checkStatus, 3000);
    return () => clearInterval(interval);
  }, [fetchResults, checkStatus]);

  const handleTrain = async () => {
    try {
      await axios.post(`${API_BASE}/train`);
      setIsTraining(true);
    } catch (error) {
      console.error("Training trigger error:", error);
      alert("Training already in progress");
    }
  };

  const bestResultsMap = results.reduce((acc, curr) => {
    if (!acc[curr.model] || curr.metrics.accuracy > acc[curr.model].metrics.accuracy) {
      acc[curr.model] = curr;
    }
    return acc;
  }, {});

  const bestResults = Object.values(bestResultsMap);
  const annResult = bestResults.find(r => r.model === 'ANN');
  const mlpResult = bestResults.find(r => r.model === 'MLP');

  const lossData = annResult?.metrics?.loss_curve?.map((loss, i) => ({
    epoch: i + 1,
    annLoss: loss,
    mlpLoss: mlpResult?.metrics?.loss_curve?.[i] || null
  })) || [];

  return (
    <div className="max-w-7xl mx-auto px-6">
      <div className="mb-12 flex flex-col md:flex-row md:items-center justify-between gap-6">
        <div>
          <h2 className="text-4xl font-black mb-3">Training Intelligence</h2>
          <p className="text-slate-500 dark:text-slate-400 text-lg">Detailed telemetry from neural convergence and parameter optimization.</p>
        </div>
        <button 
          onClick={handleTrain}
          disabled={isTraining}
          className={`btn-primary py-4! px-8! flex flex-col items-center gap-1 min-w-[240px] ${isTraining ? 'opacity-50 cursor-not-allowed bg-slate-500' : ''}`}
        >
          <div className="flex items-center gap-2">
            {isTraining ? <div className="animate-spin rounded-full h-4 w-4 border-2 border-white/30 border-t-white"></div> : <Activity size={20} />}
            <span className="font-bold uppercase tracking-widest">{isTraining ? 'Training...' : 'Deep Retrain'}</span>
          </div>
          <span className="text-[9px] opacity-60 font-black uppercase tracking-tighter">{trainStatus || 'Neural Engine Ready'}</span>
        </button>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8 mb-12">
        <div className="card-premium min-h-[400px] md:h-[500px] flex flex-col">
          <div className="flex items-center gap-3 mb-10">
            <div className="p-2 bg-brand-500/10 rounded-xl">
              <Activity className="text-brand-500" size={20} />
            </div>
            <h3 className="text-xl font-bold">Convergence Vector</h3>
          </div>
          <div className="flex-1 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={lossData}>
                <defs>
                  <linearGradient id="colorAnn" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.2} />
                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
                  </linearGradient>
                  <linearGradient id="colorMlp" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#10b981" stopOpacity={0.2} />
                    <stop offset="95%" stopColor="#10b981" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" vertical={false} strokeOpacity={0.1} />
                <XAxis dataKey="epoch" axisLine={false} tickLine={false} tick={{ fontSize: 10, fill: '#64748b' }} />
                <YAxis axisLine={false} tickLine={false} tick={{ fontSize: 10, fill: '#64748b' }} />
                <Tooltip 
                   contentStyle={{ borderRadius: '16px', border: 'none', boxShadow: '0 10px 15px -3px rgba(0,0,0,0.1)', backgroundColor: 'var(--card)' }}
                />
                <Legend verticalAlign="top" align="right" iconType="circle" wrapperStyle={{ paddingBottom: '20px' }} />
                <Area type="monotone" name="ANN Loss" dataKey="annLoss" stroke="#3b82f6" strokeWidth={3} fillOpacity={1} fill="url(#colorAnn)" />
                <Area type="monotone" name="MLP Loss" dataKey="mlpLoss" stroke="#10b981" strokeWidth={3} fillOpacity={1} fill="url(#colorMlp)" />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="card-premium flex flex-col min-h-[400px] md:h-[500px]">
          <div className="flex items-center gap-3 mb-10">
            <div className="p-2 bg-indigo-500/10 rounded-xl">
              <Sliders className="text-indigo-500" size={20} />
            </div>
            <h3 className="text-xl font-bold">Validated Hyperparameters</h3>
          </div>
          <div className="flex-1 overflow-auto pr-2 custom-scrollbar">
            <table className="w-full text-left">
              <thead className="sticky top-0 bg-surface z-10">
                <tr className="border-b border-slate-100 dark:border-slate-800">
                  <th className="pb-4 text-[10px] font-black text-slate-400 uppercase tracking-widest">Model</th>
                  <th className="pb-4 text-[10px] font-black text-slate-400 uppercase tracking-widest">Config</th>
                  <th className="pb-4 text-[10px] font-black text-slate-400 uppercase tracking-widest text-right">Score</th>
                </tr>
              </thead>
              <tbody className="divide-y divide-slate-50 dark:divide-slate-800">
                {bestResults.map((r, i) => (
                  <tr key={i} className="group">
                    <td className="py-5 font-black text-xs text-brand-600 dark:text-brand-400">{r.model}</td>
                    <td className="py-5">
                      <div className="flex flex-wrap gap-1.5">
                        {Object.entries(r.params).map(([k, v]) => (
                          <span key={k} className="px-2 py-1 bg-slate-100 dark:bg-slate-800 rounded-lg text-[9px] font-bold text-slate-500">
                            <span className="opacity-50 mr-1">{k}:</span>{String(v)}
                          </span>
                        ))}
                      </div>
                    </td>
                    <td className="py-5 text-right">
                      <span className="bg-brand-600 text-white px-3 py-1 rounded-full text-[10px] font-black">
                        {(r.metrics.accuracy * 100).toFixed(1)}%
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <InfoCard icon={<Cpu className="text-brand-500" />} title="Hardware Acceleration" desc="Models optimized for parallel processing on CUDA-enabled systems." />
        <InfoCard icon={<Layers className="text-indigo-500" />} title="Deep Architectures" desc="Multi-layered perceptrons with adaptive learning rates and dropout." />
        <InfoCard icon={<Activity className="text-emerald-500" />} title="Active Validation" desc="Cross-validation performed on a rolling 10-year meteorological window." />
      </div>
    </div>
  );
};

const InfoCard = ({ icon, title, desc }) => (
  <div className="card-premium p-6! flex flex-col gap-3">
    <div className="p-3 bg-slate-50 dark:bg-slate-800 w-fit rounded-2xl">{icon}</div>
    <h4 className="font-bold">{title}</h4>
    <p className="text-sm text-slate-500 leading-relaxed">{desc}</p>
  </div>
);

export default StatisticsPage;
