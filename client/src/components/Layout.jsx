import Navbar from './Navbar';

const Layout = ({ children }) => {
  return (
    <div className="min-h-screen transition-colors duration-500">
      <Navbar />
      <main className="pt-32 pb-20">
        {children}
      </main>
      
      {/* Background Decorative Elements - Aurora Evolved */}
      <div className="fixed top-0 left-0 w-full h-full pointer-events-none -z-10 overflow-hidden bg-slate-50 dark:bg-[#020617] transition-colors duration-700">
        <div className="absolute top-[-20%] left-[-10%] w-[60%] h-[60%] bg-brand-400/20 dark:bg-brand-500/15 rounded-full blur-[140px] animate-pulse-slow"></div>
        <div className="absolute bottom-[-20%] right-[-10%] w-[60%] h-[60%] bg-accent-400/20 dark:bg-accent-500/15 rounded-full blur-[140px] animate-pulse-slow" style={{ animationDelay: '3s' }}></div>
        <div className="absolute top-[20%] right-[-5%] w-[40%] h-[40%] bg-indigo-400/10 dark:bg-indigo-500/10 rounded-full blur-[120px] animate-pulse-slow" style={{ animationDelay: '1.5s' }}></div>
        <div className="absolute bottom-[20%] left-[-5%] w-[40%] h-[40%] bg-emerald-400/10 dark:bg-emerald-500/10 rounded-full blur-[120px] animate-pulse-slow" style={{ animationDelay: '4.5s' }}></div>
      </div>
    </div>
  );
};

export default Layout;
