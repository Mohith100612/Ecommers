import React, { useState, useEffect } from 'react';
import { Plus, Edit2, Trash2, Save, X, RefreshCw } from 'lucide-react';
import { getProducts, createProduct, updateProduct, deleteProduct } from '../services/api';
import { motion, AnimatePresence } from 'framer-motion';

const AdminDashboard = () => {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(false);
  const [isEditing, setIsEditing] = useState(null); // ID of product being edited
  const [showAddForm, setShowAddForm] = useState(false);
  const [formData, setFormData] = useState({
    product_id: '', title: '', category: '', brand: '', 
    price: 0, rating: 0, review_count: 0, description: '', 
    features: '', image_url: ''
  });

  useEffect(() => {
    fetchProducts();
  }, []);

  const fetchProducts = async () => {
    setLoading(true);
    try {
      const data = await getProducts();
      setProducts(data);
    } catch (err) {
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  const handleCreate = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const payload = { 
        ...formData, 
        features: formData.features.split(',').map(f => f.trim()) 
      };
      await createProduct(payload);
      setShowAddForm(false);
      setFormData({ product_id: '', title: '', category: '', brand: '', price: 0, rating: 0, review_count: 0, description: '', features: '', image_url: '' });
      fetchProducts();
    } catch (err) {
      alert("Failed to create product. Check backend logs.");
    } finally {
      setLoading(false);
    }
  };

  const handleDelete = async (id) => {
    if (!window.confirm("Are you sure? This will remove from both DB and Pinecone.")) return;
    try {
      await deleteProduct(id);
      fetchProducts();
    } catch (err) {
      alert("Failed to delete product.");
    }
  };

  return (
    <div className="max-w-7xl mx-auto px-4 py-12">
      <div className="flex justify-between items-center mb-12">
        <div>
          <h1 className="text-3xl font-bold text-slate-900">Admin Dashboard</h1>
          <p className="text-slate-500">Manage your product catalog and vector sync status</p>
        </div>
        <div className="flex gap-4">
          <button 
            onClick={fetchProducts}
            className="p-2 text-slate-400 hover:text-primary-600 transition-colors"
          >
            <RefreshCw className={`h-5 w-5 ${loading ? 'animate-spin' : ''}`} />
          </button>
          <button 
            onClick={() => setShowAddForm(true)}
            className="bg-primary-600 hover:bg-primary-700 text-white px-6 py-2 rounded-xl font-semibold flex items-center gap-2 transition-all shadow-md active:scale-95"
          >
            <Plus className="h-5 w-5" /> Add Product
          </button>
        </div>
      </div>

      <AnimatePresence>
        {showAddForm && (
          <motion.div 
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -20 }}
            className="bg-white p-8 rounded-2xl border border-slate-200 mb-12 shadow-xl"
          >
            <div className="flex justify-between items-center mb-6">
              <h2 className="text-xl font-bold text-slate-900">Add New Product</h2>
              <button onClick={() => setShowAddForm(false)} className="text-slate-400 hover:text-slate-600"><X /></button>
            </div>
            <form onSubmit={handleCreate} className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              <div className="space-y-1">
                <label className="text-sm font-semibold text-slate-600">Product ID</label>
                <input required type="text" className="w-full p-3 bg-slate-50 border border-slate-200 rounded-lg" value={formData.product_id} onChange={e => setFormData({...formData, product_id: e.target.value})} />
              </div>
              <div className="space-y-1">
                <label className="text-sm font-semibold text-slate-600">Title</label>
                <input required type="text" className="w-full p-3 bg-slate-50 border border-slate-200 rounded-lg" value={formData.title} onChange={e => setFormData({...formData, title: e.target.value})} />
              </div>
              <div className="space-y-1">
                <label className="text-sm font-semibold text-slate-600">Price ($)</label>
                <input required type="number" step="0.01" className="w-full p-3 bg-slate-50 border border-slate-200 rounded-lg" value={formData.price} onChange={e => setFormData({...formData, price: parseFloat(e.target.value)})} />
              </div>
              <div className="space-y-1 col-span-full">
                <label className="text-sm font-semibold text-slate-600">Image URL</label>
                <input required type="text" className="w-full p-3 bg-slate-50 border border-slate-200 rounded-lg" value={formData.image_url} onChange={e => setFormData({...formData, image_url: e.target.value})} />
              </div>
              <div className="space-y-1 col-span-full">
                <label className="text-sm font-semibold text-slate-600">Features (comma separated)</label>
                <input type="text" className="w-full p-3 bg-slate-50 border border-slate-200 rounded-lg" value={formData.features} onChange={e => setFormData({...formData, features: e.target.value})} />
              </div>
              <div className="space-y-1 col-span-full">
                <label className="text-sm font-semibold text-slate-600">Description</label>
                <textarea className="w-full p-3 bg-slate-50 border border-slate-200 rounded-lg h-24" value={formData.description} onChange={e => setFormData({...formData, description: e.target.value})} />
              </div>
              <div className="col-span-full flex justify-end">
                <button type="submit" className="bg-primary-600 text-white px-10 py-3 rounded-xl font-bold shadow-lg hover:shadow-primary-200 transition-all">Save to Catalog</button>
              </div>
            </form>
          </motion.div>
        )}
      </AnimatePresence>

      <div className="bg-white rounded-2xl border border-slate-200 overflow-hidden shadow-sm">
        <table className="w-full text-left">
          <thead className="bg-slate-50 text-slate-500 uppercase text-[11px] font-bold tracking-widest border-b border-slate-100">
            <tr>
              <th className="px-6 py-4">Product</th>
              <th className="px-6 py-4">ID</th>
              <th className="px-6 py-4">Price</th>
              <th className="px-6 py-4">Category</th>
              <th className="px-6 py-4 text-right">Actions</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-slate-100">
            {products.map(p => (
              <tr key={p.id} className="hover:bg-slate-50/50 transition-colors">
                <td className="px-6 py-4">
                  <div className="flex items-center gap-4">
                    <img src={p.image_url} className="h-10 w-10 rounded-lg object-cover shadow-sm" alt="" />
                    <span className="font-semibold text-slate-900">{p.title}</span>
                  </div>
                </td>
                <td className="px-6 py-4 text-sm text-slate-500">{p.product_id}</td>
                <td className="px-6 py-4 font-bold text-slate-700">${p.price}</td>
                <td className="px-6 py-4">
                   <span className="bg-primary-50 text-primary-700 px-2 py-1 rounded-md text-[10px] font-bold uppercase">{p.category}</span>
                </td>
                <td className="px-6 py-4 text-right">
                  <div className="flex justify-end gap-2">
                    <button className="p-2 text-slate-400 hover:text-primary-600 transition-colors"><Edit2 className="h-4 w-4" /></button>
                    <button onClick={() => handleDelete(p.product_id)} className="p-2 text-slate-400 hover:text-red-600 transition-colors"><Trash2 className="h-4 w-4" /></button>
                  </div>
                </td>
              </tr>
            ))}
          </tbody>
        </table>
        {products.length === 0 && !loading && (
          <div className="py-20 text-center text-slate-400">No products in catalog. Try seeding or adding one.</div>
        )}
      </div>
    </div>
  );
};

export default AdminDashboard;
