import axios from 'axios'

// Базовые URL вашего бэкенда (проверьте порт, если Django запущен на другом)
const API_URL = 'http://localhost:8000/api/v1/'
const AUTH_URL = 'http://localhost:8000/auth/'

// Экземпляр для основного API (животные, отчёты и т.д.)
export const api = axios.create({
  baseURL: API_URL,
})

// Экземпляр для аутентификации (регистрация, логин, получение токена)
export const authApi = axios.create({
  baseURL: AUTH_URL,
})

// Добавляем перехватчик запросов для основного API – он будет автоматически
// вставлять JWT-токен в заголовок Authorization, если токен есть в localStorage.
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('access_token')
    if (token) {
      config.headers.Authorization = `JWT ${token}` // формат должен совпадать с AUTH_HEADER_TYPES в Django
    }
    return config
  },
  (error) => {
    return Promise.reject(error)
  }
)