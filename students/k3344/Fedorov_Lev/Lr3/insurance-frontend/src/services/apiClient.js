import axios from 'axios';
import AuthService from '@/services/AuthService';

const apiClient = axios.create({
  baseURL: 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// Добавляем токен к каждому запросу
apiClient.interceptors.request.use(
  async (config) => {
    let token = localStorage.getItem('token');
    const refreshToken = localStorage.getItem('refreshToken');

    if (!token && refreshToken) {
      console.log('Токен отсутствует, пытаемся обновить...');
      try {
        const response = await AuthService.refreshToken();
        token = response.access;
      } catch (error) {
        console.error('Ошибка при обновлении токена:', error);
      }
    }

    if (token) {
      console.log('Добавляем токен в заголовок:', token);
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => Promise.reject(error)
);

// Обновление токена при 401 (если не сработало ранее)
apiClient.interceptors.response.use(
  (response) => response,
  async (error) => {
    const originalRequest = error.config;

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true;
      try {
        console.log('401 - обновляем токен...');
        await AuthService.refreshToken();
        originalRequest.headers.Authorization = `Bearer ${localStorage.getItem('token')}`;
        return apiClient(originalRequest);  // Повтор запроса с новым токеном
      } catch (refreshError) {
        console.error('Не удалось обновить токен:', refreshError);
        AuthService.logout();
      }
    }
    return Promise.reject(error);
  }
);

export default apiClient;
