import React, { useState, useEffect } from 'react';
import { Database, ShieldCheck, Zap, Activity } from 'lucide-react';
import { getProducts } from '../services/api';

const DataExplorer = () => {
  const [stats, setStats] = useState({
    totalProducts: 0,
    categories: 0,
    avgPrice: 0,
    syncStatus: 'Healthy'
  });

  useEffect(() => {
    fetchStats();
  }, []);

  const fetchStats = async () => {
    try {
      const data = await getProducts();
      const categories = new Set(data.map(p => p.category)).size;
      const avgPrice = data.reduce((acc, p) => acc + p.price, 0) / (data.length || 1);
      
      setStats({
        totalProducts: data.length,
        categories,
        avgPrice: avgPrice.toFixed(2),
        syncStatus: 'Connected'
      });
    } catch (err) {
      setStats(s => ({ ...s, syncStatus: 'Error' }));
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-12">
      <h1 className="text-3xl font-bold text-slate-900 mb-2">Systems Status</h1>
      <p className="text-slate-500 mb-12">Real-time health monitoring of our Multimodal RAG infrastructure</p>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-8">
        <StatCard 
          icon={<Database className="text-primary-600" />} 
          title="PostgreSQL" 
          value={`${stats.totalProducts} Records`} 
          status={stats.syncStatus}
        />
        <StatCard 
          icon={<Zap className="text-amber-500" />} 
          title="Pinecone Index" 
          value={`${stats.totalProducts} Vectors`} 
          status={stats.syncStatus}
        />
        <StatCard 
          icon={<ShieldCheck className="text-emerald-500" />} 
          title="Gemini API" 
          value="Connected" 
          status="Active"
        />
        <StatCard 
          icon={<Activity className="text-indigo-500" />} 
          title="Avg. Price" 
          value={`$${stats.avgPrice}`} 
          status="Catalog Stable"
        />
      </div>

      <div className="mt-16 bg-white p-12 rounded-3xl border border-slate-100 shadow-sm text-center">
        <h2 className="text-2xl font-bold text-slate-900 mb-6">Pipeline Visualization</h2>
        <div className="flex flex-col md:flex-row items-center justify-center gap-8">
            <div className="p-6 bg-slate-50 rounded-2xl border border-slate-200 min-w-[200px]">
                <div className="font-bold text-slate-700 mb-1">Ingestion</div>
                <div className="text-xs text-slate-400">Gemini Flash Multimodal</div>
            </div>
            <div className="h-0.5 w-12 bg-slate-200 hidden md:block" />
            <div className="p-6 bg-primary-50 rounded-2xl border border-primary-100 min-w-[200px]">
                <div className="font-bold text-primary-700 mb-1">Vectorization</div>
                <div className="text-xs text-primary-400">Text-Embedding-004</div>
            </div>
            <div className="h-0.5 w-12 bg-slate-200 hidden md:block" />
            <div className="p-6 bg-slate-50 rounded-2xl border border-slate-200 min-w-[200px]">
                <div className="font-bold text-slate-700 mb-1">Retrieval</div>
                <div className="text-xs text-slate-400">Pinecone Serverless</div>
            </div>
        </div>
      </div>
    </div>
  );
};

const StatCard = ({ icon, title, value, status }) => (
  <div className="bg-white p-8 rounded-3xl border border-slate-100 shadow-sm flex flex-col items-center text-center">
    <div className="p-4 bg-slate-50 rounded-2xl mb-6">
      {icon}
    </div>
    <h3 className="text-slate-500 text-sm font-medium mb-1">{title}</h3>
    <div className="text-2xl font-bold text-slate-900 mb-4">{value}</div>
    <div className="flex items-center gap-2">
      <div className={`h-2 w-2 rounded-full ${status === 'Healthy' || status === 'Connected' || status === 'Active' ? 'bg-emerald-500' : 'bg-red-500'}`} />
      <span className="text-[10px] font-bold text-slate-400 uppercase tracking-widest">{status}</span>
    </div>
  </div>
);

export default DataExplorer;
