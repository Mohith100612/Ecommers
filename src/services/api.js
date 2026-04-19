import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000',
});

export const searchCatalog = async (params) => {
  const { data } = await api.post('/search', null, { params });
  return data;
};

export const getProducts = async () => {
  const { data } = await api.get('/products');
  return data;
};

export const createProduct = async (product) => {
  const { data } = await api.post('/products', product);
  return data;
};

export const deleteProduct = async (id) => {
  await api.delete(`/products/${id}`);
};

export const updateProduct = async (id, product) => {
  const { data } = await api.put(`/products/${id}`, product);
  return data;
};

export default api;
