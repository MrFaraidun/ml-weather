import { ExternalLink, Database, FileText } from 'lucide-react';

const DatasetPage = () => {
  return (
    <div className="max-w-5xl mx-auto px-6">
      <div className="text-center mb-16">
        <div className="inline-flex p-4 bg-brand-500/10 rounded-[2rem] text-brand-600 mb-6">
          <Database size={40} />
        </div>
        <h2 className="text-4xl md:text-5xl font-black mb-4 tracking-tight">Metadata Repository</h2>
        <p className="text-slate-500 text-lg max-w-2xl mx-auto">Technical specifications of the RainAUS-Core meteorological dataset.</p>
      </div>

      <div className="card-premium p-6 md:!p-12 relative overflow-hidden group">
        <div className="absolute top-0 right-0 w-64 h-64 bg-brand-500/5 rounded-full blur-[100px] -translate-y-1/2 translate-x-1/2"></div>
        
        <div className="flex flex-col md:flex-row items-center gap-8 mb-12 border-b border-slate-100 dark:border-slate-800 pb-12">
          <div className="flex-1">
            <h3 className="text-3xl font-black mb-4 flex items-center gap-3">
              RainAUS-Core <span className="text-[10px] bg-brand-600 text-white px-3 py-1 rounded-full uppercase tracking-widest">v2.1.0</span>
            </h3>
            <p className="text-slate-500 dark:text-slate-400 text-lg leading-relaxed">
              A high-dimensional longitudinal dataset spanning 10 years of daily observations across the Australian continent. 
              Features 23 meteorological planes per vector.
            </p>
          </div>
          <div className="grid grid-cols-2 gap-4">
            <MetricSquare label="Vectors" value="142k+" />
            <MetricSquare label="Features" value="23" />
          </div>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-x-12 gap-y-8">
          <DatasetFeature title="Thermal Gradients" desc="Diurnal Min/Max temperature vectors captured at 9am and 3pm." />
          <DatasetFeature title="Pluvial Metrics" desc="Daily rainfall accumulation measured in millimeters (mm)." />
          <DatasetFeature title="Evaporation Flux" desc="Class A pan evaporation index representing atmospheric moisture loss." />
          <DatasetFeature title="Solar Density" desc="Daily hours of bright sunshine recorded via heliograph." />
          <DatasetFeature title="Barometric Pressure" desc="Atmospheric pressure reduced to mean sea level (hpa)." />
          <DatasetFeature title="Wind Dynamics" desc="Directional vectors and gust speeds at various intervals." />
        </div>

        <div className="mt-16 flex flex-col sm:flex-row items-center justify-center gap-4">
          <a 
            href="https://www.kaggle.com/datasets/jsphyg/weather-dataset-rattle-package" 
            target="_blank" 
            rel="noreferrer"
            className="btn-primary group"
          >
            Access Repository <ExternalLink size={18} className="group-hover:translate-x-1 group-hover:-translate-y-1 transition-transform" />
          </a>
          <button className="px-8 py-3 rounded-2xl font-bold bg-slate-100 dark:bg-slate-800 hover:bg-slate-200 dark:hover:bg-slate-700 transition-all flex items-center gap-2">
            <FileText size={18} /> Documentation
          </button>
        </div>
      </div>
    </div>
  );
};

const MetricSquare = ({ label, value }) => (
  <div className="bg-slate-50 dark:bg-slate-800 p-4 rounded-2xl text-center border border-slate-100 dark:border-slate-800">
    <div className="text-[10px] font-black uppercase text-slate-400 tracking-widest mb-1">{label}</div>
    <div className="text-2xl font-black text-brand-600 dark:text-brand-400">{value}</div>
  </div>
);

const DatasetFeature = ({ title, desc }) => (
  <div className="flex gap-4">
    <div className="mt-1 w-2 h-2 rounded-full bg-brand-500 shrink-0"></div>
    <div>
      <h4 className="font-bold text-sm uppercase tracking-wider mb-1">{title}</h4>
      <p className="text-sm text-slate-500 leading-relaxed">{desc}</p>
    </div>
  </div>
);

export default DatasetPage;
