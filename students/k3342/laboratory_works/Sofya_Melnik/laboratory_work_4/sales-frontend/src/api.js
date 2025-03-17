import axios from "axios";

// Создаем экземпляр Axios с базовым URL для вашего API
const api = axios.create({
  baseURL: "http://localhost:8000/api/", // Базовый URL для API
  headers: { "Content-Type": "application/json" }, // Заголовки по умолчанию
});

// Добавляем токен в заголовки перед каждым запросом
api.interceptors.request.use((config) => {
  const token = localStorage.getItem("token"); // Получаем токен из localStorage
  if (token) {
    config.headers.Authorization = `Bearer ${token}`; // Добавляем токен в заголовок Authorization
  }
  return config; // Возвращаем обновленную конфигурацию запроса
}, (error) => {
  return Promise.reject(error); // Возвращаем ошибку, если она возникла
});

// Обработка ошибок 401: перенаправляем на страницу входа, если токен отсутствует или истек
api.interceptors.response.use(
  (response) => response, // Если запрос успешен, возвращаем ответ
  (error) => {
    if (error.response && error.response.status === 401) {
      // Перенаправляем на страницу входа, например:
      window.location.href = '/login';
    }
    return Promise.reject(error); // Пробрасываем ошибку дальше
  }
);

export default api;
