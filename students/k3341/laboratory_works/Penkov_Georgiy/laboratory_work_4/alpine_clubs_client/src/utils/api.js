import axios from 'axios';

export const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',
})

api.interceptors.request.use(config => {
  const token = localStorage.getItem('authToken');
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
})
