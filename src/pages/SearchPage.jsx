import React, { useState } from 'react';
import { Search, Image as ImageIcon, Sparkles, Filter } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import { searchCatalog } from '../services/api';

const SearchPage = () => {
  const [query, setQuery] = useState('');
  const [imageUrl, setImageUrl] = useState('');
  const [results, setResults] = useState([]);
  const [answer, setAnswer] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSearch = async (e) => {
    e.preventDefault();
    if (!query.trim() && !imageUrl.trim()) return;

    setLoading(true);
    setError('');
    try {
      const data = await searchCatalog({ query_text: query, image_url: imageUrl });
      setResults(data.results);
      setAnswer(data.answer);
    } catch (err) {
      setError('Failed to search catalog. Check your backend and API keys.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-12">
      {/* Hero Section */}
      <div className="text-center mb-16">
        <motion.h1 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-5xl font-bold text-slate-900 mb-6"
        >
          Discover Your Perfect <span className="text-primary-600">Product</span>
        </motion.h1>
        <motion.p 
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.1 }}
          className="text-slate-600 text-xl max-w-2xl mx-auto"
        >
          Search using keywords, product descriptions, or even image URLs. 
          Our AI assistant will help you find exactly what you need.
        </motion.p>
      </div>

      {/* Search Container */}
      <div className="max-w-4xl mx-auto mb-16">
        <form onSubmit={handleSearch} className="bg-white p-6 rounded-2xl shadow-xl shadow-slate-200/50 border border-slate-100">
          <div className="flex flex-col md:flex-row gap-4">
            <div className="flex-1 relative">
              <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 h-5 w-5" />
              <input 
                type="text" 
                placeholder="What are you looking for?" 
                className="w-full pl-12 pr-4 py-4 rounded-xl border border-slate-200 focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none transition-all"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
              />
            </div>
            <div className="flex-1 relative">
              <ImageIcon className="absolute left-4 top-1/2 -translate-y-1/2 text-slate-400 h-5 w-5" />
              <input 
                type="text" 
                placeholder="Paste image URL (optional)" 
                className="w-full pl-12 pr-4 py-4 rounded-xl border border-slate-200 focus:ring-2 focus:ring-primary-500 focus:border-transparent outline-none transition-all"
                value={imageUrl}
                onChange={(e) => setImageUrl(e.target.value)}
              />
            </div>
            <button 
              type="submit" 
              disabled={loading}
              className="bg-primary-600 hover:bg-primary-700 text-white px-8 py-4 rounded-xl font-semibold transition-all flex items-center justify-center gap-2 min-w-[140px] disabled:opacity-50"
            >
              {loading ? <div className="h-5 w-5 border-2 border-white/30 border-t-white rounded-full animate-spin" /> : <><Sparkles className="h-5 w-5" /> Search</>}
            </button>
          </div>
        </form>
        {error && <p className="text-red-500 text-center mt-4">{error}</p>}
      </div>

      {/* Main Content */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-12">
        {/* Results Grid */}
        <div className="lg:col-span-2">
          <h2 className="text-2xl font-bold text-slate-900 mb-8 flex items-center gap-2">
            Most Relevant Results
            {results.length > 0 && <span className="bg-slate-100 text-slate-600 text-sm py-1 px-3 rounded-full font-medium">{results.length}</span>}
          </h2>
          
          <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
            <AnimatePresence mode='popLayout'>
              {results.map((res, index) => (
                <motion.div 
                  key={res.product.product_id}
                  initial={{ opacity: 0, scale: 0.95 }}
                  animate={{ opacity: 1, scale: 1 }}
                  transition={{ delay: index * 0.1 }}
                  layout
                  className="bg-white rounded-2xl border border-slate-100 overflow-hidden hover:shadow-lg transition-all group"
                >
                  <div className="aspect-square relative overflow-hidden bg-slate-100">
                    <img 
                      src={res.product.image_url} 
                      alt={res.product.title} 
                      className="object-cover w-full h-full group-hover:scale-105 transition-transform duration-500"
                    />
                    <div className="absolute top-4 right-4 bg-white/90 backdrop-blur px-3 py-1 rounded-full text-xs font-bold text-slate-900 shadow-sm">
                      {res.product.category}
                    </div>
                  </div>
                  <div className="p-6">
                    <div className="flex justify-between items-start mb-2">
                      <h3 className="font-bold text-slate-900 line-clamp-1">{res.product.title}</h3>
                      <span className="text-primary-700 font-bold">${res.product.price}</span>
                    </div>
                    <div className="flex items-center gap-1 mb-4 text-sm text-slate-500">
                      <span className="text-amber-500 font-bold">★ {res.product.rating}</span>
                      <span>({res.product.review_count} reviews)</span>
                    </div>
                    <p className="text-slate-600 text-sm line-clamp-2 mb-4">
                      {res.product.description}
                    </p>
                    <div className="flex flex-wrap gap-2">
                      {res.product.features.slice(0, 2).map((f, i) => (
                        <span key={i} className="text-[10px] bg-slate-50 text-slate-500 px-2 py-1 rounded-md uppercase tracking-wider font-semibold border border-slate-100">
                          {f}
                        </span>
                      ))}
                    </div>
                  </div>
                </motion.div>
              ))}
            </AnimatePresence>
            
            {!loading && results.length === 0 && !error && (
              <div className="col-span-full py-20 text-center bg-white rounded-3xl border-2 border-dashed border-slate-100">
                <Search className="h-12 w-12 text-slate-300 mx-auto mb-4" />
                <p className="text-slate-400">Search results will appear here</p>
              </div>
            )}
          </div>
        </div>

        {/* AI Assistant */}
        <div className="lg:col-span-1">
          <div className="sticky top-8">
            <div className="bg-primary-900 rounded-3xl p-8 text-white shadow-2xl relative overflow-hidden">
              <div className="absolute -top-12 -right-12 w-32 h-32 bg-primary-700 rounded-full blur-3xl opacity-50" />
              <div className="relative z-10">
                <h2 className="text-xl font-bold mb-6 flex items-center gap-2">
                  <Sparkles className="h-5 w-5 text-primary-300" />
                  AI Shopping Assistant
                </h2>
                
                {loading ? (
                  <div className="space-y-4">
                    <div className="h-4 bg-white/10 rounded w-full animate-pulse" />
                    <div className="h-4 bg-white/10 rounded w-3/4 animate-pulse" />
                    <div className="h-4 bg-white/10 rounded w-5/6 animate-pulse" />
                  </div>
                ) : answer ? (
                  <div className="prose prose-invert prose-sm">
                    <p className="text-primary-50 leading-relaxed whitespace-pre-wrap">{answer}</p>
                  </div>
                ) : (
                  <p className="text-primary-300 italic text-sm">
                    Ask a question about the catalog to see my recommendations and insights.
                  </p>
                )}
              </div>
            </div>
            
            <div className="mt-8 bg-white p-6 rounded-2xl border border-slate-100">
              <h3 className="font-bold text-slate-900 mb-4 flex items-center gap-2">
                <Filter className="h-4 w-4" /> Smart Filters
              </h3>
              <div className="space-y-4">
                <div className="text-xs text-slate-400">Advanced filtering coming soon based on vector categories.</div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default SearchPage;
