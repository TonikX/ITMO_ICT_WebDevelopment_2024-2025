import axios from 'axios'
import {useAuthStore} from '@/stores/auth'
import router from '@/router'

export const api = axios.create({
  baseURL: 'http://127.0.0.1:8000',
  headers: {
    'Content-Type': 'application/json',
    'Accept': 'application/json',
  }
})

api.interceptors.request.use(config => {
  const token = localStorage.getItem('authToken')
  if (token) {
    config.headers.Authorization = `Token ${token}`
  }
  return config
})

api.interceptors.response.use(
  response => response,
  error => {
    if (error.response) {
      if (error.response.status === 401) {
        const authStore = useAuthStore()
        authStore.clearAuth()
        router.push('/login')
      }

      const errorMessage = error.response.data?.message ||
        error.response.data?.detail ||
        'An error occurred'
      return Promise.reject(errorMessage)
    }
    return Promise.reject('Network error - please check your connection')
  }
)
