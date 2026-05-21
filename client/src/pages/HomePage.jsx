import { Link } from 'react-router-dom';
import { 
  ChevronRight, Thermometer, Settings, BarChart2, CloudRain, 
  ArrowRight, Activity, Zap, Shield
} from 'lucide-react';

const HomePage = () => {
  return (
    <div className="max-w-7xl mx-auto px-6">
      {/* Hero Section */}
      <div className="flex flex-col lg:flex-row items-center gap-16 py-10 lg:py-20">
        <div className="lg:w-3/5 text-center lg:text-left">
          <div className="inline-flex items-center gap-2 px-4 py-2 rounded-full bg-brand-50 dark:bg-brand-900/30 text-brand-600 dark:text-brand-400 text-sm font-bold mb-8 animate-bounce-subtle">
            <span className="relative flex h-2 w-2">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-brand-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-brand-500"></span>
            </span>
            Next-Gen Meteorological Intelligence
          </div>
          <h1 className="text-5xl md:text-7xl lg:text-8xl font-black leading-[1.1] mb-8 tracking-tighter">
            Predict the <br />
            <span className="text-gradient">Unpredictable.</span>
          </h1>
          <p className="text-lg md:text-xl text-slate-500 dark:text-slate-400 leading-relaxed mb-10 max-w-2xl mx-auto lg:mx-0">
            Leveraging Deep Neural Networks to transform raw atmospheric data into high-precision rainfall forecasts with up to 98% validated accuracy.
          </p>
          <div className="flex flex-col sm:flex-row justify-center lg:justify-start gap-4">
            <Link to="/prediction" className="btn-primary !px-10 !py-5 text-lg group">
              Start Inference <ArrowRight className="group-hover:translate-x-1 transition-transform" size={24} />
            </Link>
            <Link to="/comparison" className="px-10 py-5 rounded-2xl text-lg font-bold bg-white dark:bg-slate-800 text-slate-900 dark:text-white border border-slate-200 dark:border-slate-800 hover:bg-slate-50 dark:hover:bg-slate-700 transition-all flex items-center gap-2 shadow-sm">
              Explore Models
            </Link>
          </div>
        </div>

        <div className="lg:w-2/5 relative">
          <div className="absolute inset-0 bg-brand-500/20 blur-[100px] rounded-full animate-pulse-slow"></div>
          <div className="relative grid grid-cols-2 gap-4">
            <StatCard icon={<Activity className="text-brand-500" />} label="Real-time" value="Analytics" />
            <StatCard icon={<Zap className="text-yellow-500" />} label="Instant" value="Inference" className="mt-8" />
            <StatCard icon={<Shield className="text-emerald-500" />} label="Secured" value="Data" />
            <StatCard icon={<CloudRain className="text-indigo-500" />} label="Precision" value="98.2%" className="mt-8" />
          </div>
        </div>
      </div>

      {/* Features Grid */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6 mt-12 md:mt-20">
        <FeatureCard
          icon={<Thermometer className="text-orange-500" size={32} />}
          title="Massive Data"
          desc="Trained on 140,000+ high-precision meteorological observations."
        />
        <FeatureCard
          icon={<Settings className="text-brand-500" size={32} />}
          title="Multi-Architect"
          desc="Proprietary comparison of Deep ANN, MLP, and Tree-based models."
        />
        <FeatureCard
          icon={<BarChart2 className="text-emerald-500" size={32} />}
          title="Vector Metrics"
          desc="Real-time tracking of F1-Score, Precision, and Recall vectors."
        />
        <FeatureCard
          icon={<CloudRain className="text-indigo-500" size={32} />}
          title="Cloud Native"
          desc="Architected for instantaneous global weather inference."
        />
      </div>
    </div>
  );
};

const StatCard = ({ icon, label, value, className = "" }) => (
  <div className={`card-premium !p-6 flex flex-col items-center text-center gap-2 ${className}`}>
    <div className="p-3 bg-slate-50 dark:bg-slate-800 rounded-2xl mb-2">
      {icon}
    </div>
    <div className="text-[10px] font-black uppercase tracking-widest text-slate-400">{label}</div>
    <div className="text-xl font-black">{value}</div>
  </div>
);

const FeatureCard = ({ icon, title, desc }) => (
  <div className="card-premium group">
    <div className="mb-6 p-4 rounded-2xl bg-slate-50 dark:bg-slate-800 w-fit group-hover:scale-110 group-hover:rotate-6 transition-all duration-500">
      {icon}
    </div>
    <h3 className="text-xl font-bold mb-3 tracking-tight">{title}</h3>
    <p className="text-slate-500 dark:text-slate-400 text-sm leading-relaxed">{desc}</p>
  </div>
);

export default HomePage;
