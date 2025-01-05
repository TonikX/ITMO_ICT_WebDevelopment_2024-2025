import axios from 'axios';

const axiosApi = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/',
  withCredentials: true,
});

axiosApi.interceptors.request.use((config) => {
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});

export default axiosApi;
