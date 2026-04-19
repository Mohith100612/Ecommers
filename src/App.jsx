import React from 'react';
import { BrowserRouter as Router, Routes, Route, Link, NavLink } from 'react-router-dom';
import { Search, ShieldAlert, BarChart3, ShoppingBag } from 'lucide-react';
import SearchPage from './pages/SearchPage';
import AdminDashboard from './pages/AdminDashboard';
import DataExplorer from './pages/DataExplorer';

function App() {
  return (
    <Router>
      <div className="min-h-screen flex flex-col bg-slate-50 font-sans text-slate-900">
        {/* Navigation */}
        <nav className="bg-white border-b border-slate-200 sticky top-0 z-50">
          <div className="max-w-7xl mx-auto px-4 h-20 flex items-center justify-between">
            <Link to="/" className="flex items-center gap-2 group">
              <div className="p-2 bg-primary-600 rounded-xl group-hover:rotate-12 transition-transform shadow-lg shadow-primary-200">
                <ShoppingBag className="text-white h-5 w-5" />
              </div>
              <span className="text-xl font-bold tracking-tight bg-gradient-to-r from-slate-900 to-slate-600 bg-clip-text text-transparent">NexusAI</span>
            </Link>
            
            <div className="flex gap-2">
              <NavButton to="/" icon={<Search className="h-4 w-4" />} label="Search Catalog" />
              <NavButton to="/admin" icon={<ShieldAlert className="h-4 w-4" />} label="Admin Panel" />
              <NavButton to="/stats" icon={<BarChart3 className="h-4 w-4" />} label="Data Explorer" />
            </div>
          </div>
        </nav>

        {/* Content Area */}
        <main className="flex-grow">
          <Routes>
            <Route path="/" element={<SearchPage />} />
            <Route path="/admin" element={<AdminDashboard />} />
            <Route path="/stats" element={<DataExplorer />} />
          </Routes>
        </main>

        {/* Footer */}
        <footer className="bg-white border-t border-slate-100 py-12">
          <div className="max-w-7xl mx-auto px-4 text-center">
            <p className="text-slate-400 text-sm font-medium">© 2026 NexusAI Multimodal Product Search. Built with Gemini & Pinecone.</p>
          </div>
        </footer>
      </div>
    </Router>
  );
}

const NavButton = ({ to, icon, label }) => (
  <NavLink 
    to={to} 
    className={({ isActive }) => `
      flex items-center gap-2 px-6 py-2 rounded-xl font-bold text-sm transition-all
      ${isActive 
        ? 'bg-primary-50 text-primary-700 shadow-sm border border-primary-100' 
        : 'text-slate-500 hover:text-slate-900 hover:bg-slate-50 border border-transparent'}
    `}
  >
    {icon}
    {label}
  </NavLink>
);

export default App;
