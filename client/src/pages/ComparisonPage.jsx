import { useState, useEffect } from 'react';
import axios from 'axios';
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer
} from 'recharts';
import { Activity, Award, CheckCircle } from 'lucide-react';

const API_BASE = 'http://localhost:3001';

const ComparisonPage = () => {
  const [results, setResults] = useState([]);

  useEffect(() => {
    axios.get(`${API_BASE}/models/results`).then(res => setResults(res.data));
  }, []);

  const bestResultsMap = results.reduce((acc, curr) => {
    if (!acc[curr.model] || curr.metrics.accuracy > acc[curr.model].metrics.accuracy) {
      acc[curr.model] = curr;
    }
    return acc;
  }, {});

  const bestResults = Object.values(bestResultsMap);

  const chartData = bestResults.map(r => ({
    name: r.model,
    accuracy: (r.metrics.accuracy * 100).toFixed(2),
    f1: (r.metrics.f1 * 100).toFixed(2)
  }));

  const topModel = [...bestResults].sort((a, b) => b.metrics.accuracy - a.metrics.accuracy)[0];

  return (
    <div className="max-w-7xl mx-auto px-6">
      <div className="mb-12 flex flex-col md:flex-row md:items-end justify-between gap-6">
        <div>
          <h2 className="text-4xl font-black mb-3">Architecture Benchmark</h2>
          <p className="text-slate-500 dark:text-slate-400 text-lg">Performance cross-validation across all validated neural structures.</p>
        </div>
        {topModel && (
          <div className="flex items-center gap-4 bg-emerald-500/10 border border-emerald-500/20 px-6 py-3 rounded-2xl">
            <Award className="text-emerald-500" size={24} />
            <div>
              <div className="text-[10px] font-black uppercase text-emerald-600 tracking-widest">Champion Model</div>
              <div className="font-bold">{topModel.model} ({(topModel.metrics.accuracy * 100).toFixed(1)}%)</div>
            </div>
          </div>
        )}
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8 mb-12">
        <div className="lg:col-span-2 card-premium min-h-[400px] md:h-[500px] flex flex-col">
          <div className="flex justify-between items-center mb-8">
            <h3 className="text-xl font-bold flex items-center gap-3">
              <Activity className="text-brand-500" /> Accuracy Variance
            </h3>
          </div>
          <div className="flex-1 w-full">
            <ResponsiveContainer width="100%" height="100%">
              <BarChart data={chartData}>
                <CartesianGrid strokeDasharray="3 3" vertical={false} strokeOpacity={0.1} />
                <XAxis 
                  dataKey="name" 
                  axisLine={false} 
                  tickLine={false} 
                  tick={{ fill: '#64748b', fontSize: 12, fontWeight: 700 }} 
                />
                <YAxis 
                  domain={[0, 100]} 
                  axisLine={false} 
                  tickLine={false} 
                  tick={{ fill: '#64748b', fontSize: 12, fontWeight: 700 }} 
                />
                <Tooltip
                  cursor={{ fill: 'currentColor', opacity: 0.05 }}
                  contentStyle={{ 
                    borderRadius: '20px', 
                    border: 'none', 
                    boxShadow: '0 20px 25px -5px rgba(0,0,0,0.1)',
                    backgroundColor: 'var(--card)',
                    color: 'var(--foreground)'
                  }}
                />
                <Bar dataKey="accuracy" name="Accuracy %" fill="#3b82f6" radius={[10, 10, 0, 0]} barSize={40} />
                <Bar dataKey="f1" name="F1 Score %" fill="#10b981" radius={[10, 10, 0, 0]} barSize={40} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        <div className="bg-gradient-to-br from-brand-600 to-indigo-800 p-10 rounded-[3rem] text-white flex flex-col justify-between relative overflow-hidden shadow-2xl shadow-brand-500/20">
          <div className="absolute top-0 right-0 w-64 h-64 bg-white/10 rounded-full blur-[80px] -translate-y-1/2 translate-x-1/2"></div>
          
          <div>
            <div className="text-[10px] font-black uppercase tracking-[0.3em] mb-4 md:mb-6 opacity-60">Peak Intelligence</div>
            <div className="text-6xl md:text-8xl font-black mb-2 tracking-tighter">
              {topModel ? (topModel.metrics.accuracy * 100).toFixed(1) : '0'}%
            </div>
            <div className="text-brand-100 text-base md:text-lg font-medium opacity-80">Highest Validation Score</div>
          </div>

          <div className="space-y-4 relative z-10">
            <div className="bg-white/10 backdrop-blur-md p-6 rounded-[2rem] border border-white/10">
              <div className="text-brand-200 text-[10px] uppercase font-black tracking-widest mb-2">Dominant Architecture</div>
              <div className="text-2xl font-black">{topModel?.model || 'N/A'}</div>
            </div>
            <div className="flex gap-3">
              <div className="flex-1 bg-emerald-500/20 backdrop-blur-md p-4 rounded-2xl border border-emerald-500/20 text-center">
                <div className="text-[9px] uppercase font-black opacity-60 mb-1">F1 Score</div>
                <div className="text-lg font-black">{topModel ? (topModel.metrics.f1 * 100).toFixed(1) : '0'}%</div>
              </div>
              <div className="flex-1 bg-brand-400/20 backdrop-blur-md p-4 rounded-2xl border border-brand-400/20 text-center">
                <div className="text-[9px] uppercase font-black opacity-60 mb-1">Precision</div>
                <div className="text-lg font-black">{topModel ? (topModel.metrics.precision * 100).toFixed(1) : '0'}%</div>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {bestResults.map((r, i) => (
          <div key={i} className="card-premium group">
            <div className="flex items-center justify-between mb-8">
              <h3 className="font-black text-xs uppercase tracking-widest group-hover:text-brand-600 transition-colors">{r.model}</h3>
              <CheckCircle className="text-emerald-500" size={20} />
            </div>

            <div className="space-y-6 mb-8">
              <MetricBar label="Accuracy" value={(r.metrics.accuracy * 100).toFixed(1)} color="bg-brand-500" />
              <MetricBar label="F1-Score" value={(r.metrics.f1 * 100).toFixed(1)} color="bg-emerald-500" />
            </div>

            <div className="pt-6 border-t border-slate-100 dark:border-slate-800">
              <h4 className="text-[9px] font-black text-slate-400 uppercase tracking-widest mb-4">Confusion Matrix</h4>
              <div className="grid grid-cols-2 gap-2">
                <MatrixItem label="TN" value={r.metrics.confusion_matrix[0][0]} />
                <MatrixItem label="FP" value={r.metrics.confusion_matrix[0][1]} />
                <MatrixItem label="FN" value={r.metrics.confusion_matrix[1][0]} />
                <MatrixItem label="TP" value={r.metrics.confusion_matrix[1][1]} />
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
};

const MetricBar = ({ label, value, color }) => (
  <div className="space-y-2">
    <div className="flex justify-between items-end">
      <span className="text-[10px] font-black text-slate-400 uppercase tracking-widest">{label}</span>
      <span className="text-xs font-black">{value}%</span>
    </div>
    <div className="h-1.5 w-full bg-slate-100 dark:bg-slate-800 rounded-full overflow-hidden">
      <div className={`h-full ${color} rounded-full transition-all duration-1000`} style={{ width: `${value}%` }}></div>
    </div>
  </div>
);

const MatrixItem = ({ label, value }) => (
  <div className="bg-slate-50 dark:bg-slate-800/50 p-2 rounded-xl text-center border border-transparent hover:border-brand-500/20 transition-all">
    <div className="text-[8px] font-black text-slate-400 uppercase mb-1">{label}</div>
    <div className="text-[10px] font-black">{value.toLocaleString()}</div>
  </div>
);

export default ComparisonPage;
