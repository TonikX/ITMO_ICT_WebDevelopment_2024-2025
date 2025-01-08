import axios from 'axios'
import store from '@/store'
import router from '@/router'

const API_URL = import.meta.env.VITE_API_URL

const api = axios.create({
  baseURL: API_URL
})

// Добавляем перехватчик для добавления токена к запросам
api.interceptors.request.use(
  config => {
    const token = localStorage.getItem('token')
    if (token) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  error => Promise.reject(error)
)

// Добавляем перехватчик для обработки ошибок
api.interceptors.response.use(
  response => response,
  async error => {
    const originalRequest = error.config

    if (error.response?.status === 401 && !originalRequest._retry) {
      originalRequest._retry = true

      try {
        const token = localStorage.getItem('token')
        if (token) {
          const response = await axios.post(`${API_URL}/auth/refresh-token`, {
            token: token
          })
          
          const newToken = response.data.token
          localStorage.setItem('token', newToken)
          store.commit('auth/setAuth', true)
          
          originalRequest.headers.Authorization = `Bearer ${newToken}`
          return api(originalRequest)
        }
      } catch (refreshError) {
        await store.dispatch('auth/logout')
        router.push('/login')
        return Promise.reject(refreshError)
      }
    }
    return Promise.reject(error)
  }
)

export { api } 