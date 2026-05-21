import { Link, useLocation } from 'react-router-dom';
import { useTheme } from '../context/ThemeContext';
import { 
  CloudRain, Moon, Sun, Home, Search, BarChart2, PieChart, Database, Menu, X 
} from 'lucide-react';
import { useState, useEffect } from 'react';

const Navbar = () => {
  const { isDark, toggleTheme } = useTheme();
  const [isOpen, setIsOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);
  const location = useLocation();

  useEffect(() => {
    const handleScroll = () => setScrolled(window.scrollY > 20);
    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  const navLinks = [
    { to: '/', label: 'Home', icon: <Home size={18} /> },
    { to: '/prediction', label: 'Inference', icon: <Search size={18} /> },
    { to: '/comparison', label: 'Models', icon: <BarChart2 size={18} /> },
    { to: '/statistics', label: 'Analytics', icon: <PieChart size={18} /> },
  ];

  return (
    <nav className={`fixed top-0 w-full z-50 transition-all duration-500 ${
      scrolled ? 'py-4' : 'py-6'
    }`}>
      <div className="max-w-7xl mx-auto px-6">
        <div className={`glass rounded-[2rem] px-6 py-3 flex justify-between items-center transition-all duration-500 ${
          scrolled ? 'shadow-2xl' : 'shadow-lg'
        }`}>
          <Link to="/" className="flex items-center gap-3 group">
            <div className="bg-brand-600 p-2 rounded-xl shadow-lg shadow-brand-500/30 group-hover:scale-110 group-hover:rotate-12 transition-all">
              <CloudRain className="text-white" size={24} />
            </div>
            <span className="text-xl font-black tracking-tighter">
              Weather<span className="text-brand-600">Detector</span>
            </span>
          </Link>

          {/* Desktop Nav */}
          <div className="hidden lg:flex items-center gap-2 bg-slate-100/50 dark:bg-slate-800/50 p-1 rounded-2xl">
            {navLinks.map((link) => (
              <Link
                key={link.to}
                to={link.to}
                className={`px-4 py-2 rounded-xl text-sm font-bold flex items-center gap-2 transition-all ${
                  location.pathname === link.to
                    ? 'bg-white dark:bg-slate-700 text-brand-600 dark:text-white shadow-sm'
                    : 'text-slate-500 hover:text-brand-600 dark:hover:text-white hover:bg-white/50 dark:hover:bg-slate-700/50'
                }`}
              >
                {link.icon} {link.label}
              </Link>
            ))}
          </div>

          <div className="flex items-center gap-3">
            <button
              onClick={toggleTheme}
              className="p-2.5 rounded-xl bg-slate-100 dark:bg-slate-800 text-slate-600 dark:text-slate-300 hover:scale-110 transition-all active:scale-95"
            >
              {isDark ? <Sun size={20} className="text-yellow-400" /> : <Moon size={20} className="text-brand-600" />}
            </button>

            <div className="hidden sm:block">
              <Link to="/dataset" className="btn-primary !py-2.5 !px-5 text-xs uppercase tracking-widest">
                <Database size={16} /> Dataset
              </Link>
            </div>

            <button 
              className="lg:hidden p-2.5 rounded-xl bg-slate-100 dark:bg-slate-800"
              onClick={() => setIsOpen(!isOpen)}
            >
              {isOpen ? <X size={20} /> : <Menu size={20} />}
            </button>
          </div>
        </div>

        {/* Mobile Menu */}
        <div className={`lg:hidden absolute left-6 right-6 mt-4 transition-all duration-500 origin-top ${
          isOpen ? 'scale-y-100 opacity-100' : 'scale-y-0 opacity-0 pointer-events-none'
        }`}>
          <div className="glass rounded-[2rem] p-4 flex flex-col gap-2">
            {navLinks.map((link) => (
              <Link
                key={link.to}
                to={link.to}
                onClick={() => setIsOpen(false)}
                className={`px-4 py-3 rounded-xl text-sm font-bold flex items-center gap-3 transition-all ${
                  location.pathname === link.to
                    ? 'bg-brand-600 text-white'
                    : 'hover:bg-slate-100 dark:hover:bg-slate-800'
                }`}
              >
                {link.icon} {link.label}
              </Link>
            ))}
            <Link 
              to="/dataset" 
              onClick={() => setIsOpen(false)}
              className="mt-2 btn-primary w-full"
            >
              <Database size={18} /> Dataset Explorer
            </Link>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
