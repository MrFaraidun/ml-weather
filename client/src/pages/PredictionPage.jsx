import { useState } from 'react';
import axios from 'axios';
import { 
  Search, CloudRain, Cloud, Gauge, Thermometer, 
  Droplets, Wind, Sun, Compass, Activity
} from 'lucide-react';

const API_BASE = 'http://localhost:3001';

const PredictionPage = () => {
  const [formData, setFormData] = useState({
    MinTemp: 15.0, MaxTemp: 25.0, Rainfall: 0.0, Evaporation: 5.0, Sunshine: 8.0,
    WindGustSpeed: 40.0, WindSpeed9am: 15.0, WindSpeed3pm: 20.0,
    Humidity9am: 60.0, Humidity3pm: 40.0, Pressure9am: 1015.0, Pressure3pm: 1012.0,
    Cloud9am: 4.0, Cloud3pm: 4.0, Temp9am: 18.0, Temp3pm: 23.0, RainToday: 'No'
  });
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const response = await axios.post(`${API_BASE}/predict`, formData);
      setResult(response.data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const formFields = [
    { key: 'MinTemp', label: 'Min Temp', icon: <Thermometer size={14} />, group: 'Thermal' },
    { key: 'MaxTemp', label: 'Max Temp', icon: <Thermometer size={14} />, group: 'Thermal' },
    { key: 'Temp9am', label: 'Temp (9am)', icon: <Sun size={14} />, group: 'Thermal' },
    { key: 'Temp3pm', label: 'Temp (3pm)', icon: <Sun size={14} />, group: 'Thermal' },
    { key: 'Rainfall', label: 'Rainfall', icon: <Droplets size={14} />, group: 'Hydrology' },
    { key: 'Evaporation', label: 'Evaporation', icon: <Droplets size={14} />, group: 'Hydrology' },
    { key: 'Humidity9am', label: 'Humidity (9am)', icon: <Droplets size={14} />, group: 'Hydrology' },
    { key: 'Humidity3pm', label: 'Humidity (3pm)', icon: <Droplets size={14} />, group: 'Hydrology' },
    { key: 'WindGustSpeed', label: 'Gust Speed', icon: <Wind size={14} />, group: 'Aerodynamics' },
    { key: 'WindSpeed9am', label: 'Wind (9am)', icon: <Wind size={14} />, group: 'Aerodynamics' },
    { key: 'WindSpeed3pm', label: 'Wind (3pm)', icon: <Wind size={14} />, group: 'Aerodynamics' },
    { key: 'Sunshine', label: 'Sunshine', icon: <Sun size={14} />, group: 'Atmosphere' },
    { key: 'Pressure9am', label: 'Pressure (9am)', icon: <Gauge size={14} />, group: 'Atmosphere' },
    { key: 'Pressure3pm', label: 'Pressure (3pm)', icon: <Gauge size={14} />, group: 'Atmosphere' },
    { key: 'Cloud9am', label: 'Cloud (9am)', icon: <Cloud size={14} />, group: 'Atmosphere' },
    { key: 'Cloud3pm', label: 'Cloud (3pm)', icon: <Cloud size={14} />, group: 'Atmosphere' },
  ];

  return (
    <div className="max-w-7xl mx-auto px-6">
      <div className="mb-12">
        <h2 className="text-4xl font-black mb-3">Inference Engine</h2>
        <p className="text-slate-500 dark:text-slate-400 text-lg">Deploy neural models for real-time atmospheric classification.</p>
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-12 gap-10">
        <div className="lg:col-span-8">
          <form onSubmit={handleSubmit} className="card-premium">
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-10">
              {formFields.map((field) => (
                <div key={field.key} className="flex flex-col gap-2">
                  <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest flex items-center gap-2">
                    <span className="p-1 bg-slate-100 dark:bg-slate-800 rounded-md">{field.icon}</span>
                    {field.label}
                  </label>
                  <input
                    type="number" step="any"
                    className="w-full p-3 bg-slate-50 dark:bg-slate-800/50 border border-transparent focus:border-brand-500/50 rounded-xl font-bold outline-none transition-all"
                    value={formData[field.key]}
                    onChange={(e) => setFormData({ ...formData, [field.key]: parseFloat(e.target.value) || 0 })}
                  />
                </div>
              ))}
              <div className="flex flex-col gap-2">
                <label className="text-[10px] font-black text-slate-400 uppercase tracking-widest flex items-center gap-2">
                  <span className="p-1 bg-slate-100 dark:bg-slate-800 rounded-md"><Compass size={14} /></span>
                  Rain Today
                </label>
                <select
                  className="w-full p-3 bg-slate-50 dark:bg-slate-800/50 border border-transparent focus:border-brand-500/50 rounded-xl font-bold outline-none transition-all cursor-pointer"
                  value={formData.RainToday}
                  onChange={(e) => setFormData({ ...formData, RainToday: e.target.value })}
                >
                  <option value="No">No</option>
                  <option value="Yes">Yes</option>
                </select>
              </div>
            </div>
            
            <button type="submit" className="btn-primary w-full !py-5 !text-lg !rounded-[1.5rem] shadow-brand-500/30">
              {loading ? (
                <div className="animate-spin rounded-full h-6 w-6 border-2 border-white/30 border-t-white"></div>
              ) : <Search size={22} />}
              {loading ? 'PROCESSING VECTOR...' : 'INITIALIZE INFERENCE'}
            </button>
          </form>
        </div>

        <div className="lg:col-span-4">
          <div className="lg:sticky lg:top-32">
            {result ? (
              <div className={`card-premium overflow-hidden relative group animate-in fade-in zoom-in duration-700 ${
                result.prediction === 'Yes' 
                  ? 'bg-gradient-to-br from-brand-600 to-indigo-700 text-white border-none shadow-brand-500/40' 
                  : ''
              }`}>
                {result.prediction === 'Yes' && (
                  <CloudRain size={300} className="absolute -right-20 -bottom-20 opacity-10 rotate-12 group-hover:scale-110 transition-transform duration-1000" />
                )}
                
                <div className="relative z-10 text-center">
                  <div className={`w-20 h-20 mx-auto rounded-3xl flex items-center justify-center mb-6 shadow-inner ${
                    result.prediction === 'Yes' ? 'bg-white/20' : 'bg-brand-50 dark:bg-brand-900/30 text-brand-600'
                  }`}>
                    {result.prediction === 'Yes' ? <CloudRain size={40} /> : <Sun size={40} />}
                  </div>
                  
                  <h3 className="text-[10px] font-black uppercase tracking-[0.3em] mb-2 opacity-70">Neural Conclusion</h3>
                  <div className="text-6xl font-black mb-6 tracking-tighter">
                    {result.prediction === 'Yes' ? 'RAIN' : 'CLEAR'}
                  </div>

                  <div className="bg-black/10 dark:bg-white/5 rounded-3xl p-6 mb-6">
                    <div className="flex justify-between items-end mb-3">
                      <span className="text-[10px] font-black uppercase tracking-widest opacity-60">Confidence</span>
                      <span className="text-2xl font-black">{(result.probability * 100).toFixed(1)}%</span>
                    </div>
                    <div className="h-2 w-full bg-black/10 dark:bg-white/10 rounded-full overflow-hidden">
                      <div 
                        className={`h-full transition-all duration-1000 ease-out rounded-full ${result.prediction === 'Yes' ? 'bg-white' : 'bg-brand-600'}`} 
                        style={{ width: `${result.probability * 100}%` }}
                      ></div>
                    </div>
                  </div>

                  <div className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-black/10 dark:bg-white/10 text-[10px] font-black tracking-widest uppercase">
                    <Activity size={12} /> Model: {result.model_used}
                  </div>
                </div>
              </div>
            ) : (
              <div className="card-premium border-dashed border-2 flex flex-col items-center justify-center text-center py-20 grayscale opacity-60">
                <div className="w-20 h-20 bg-slate-100 dark:bg-slate-800 rounded-[2rem] flex items-center justify-center mb-6">
                  <Gauge size={40} className="text-slate-400" />
                </div>
                <h3 className="text-xl font-bold mb-2">Awaiting Parameters</h3>
                <p className="text-sm text-slate-500">Configure the atmospheric vector to begin analysis.</p>
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};

export default PredictionPage;
