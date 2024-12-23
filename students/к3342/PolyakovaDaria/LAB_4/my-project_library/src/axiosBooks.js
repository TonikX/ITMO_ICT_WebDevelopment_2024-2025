import axios from 'axios';

const axiosBooks = axios.create({
  baseURL: 'http://127.0.0.1:8000/api',
});

axiosBooks.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

export default axiosBooks;
