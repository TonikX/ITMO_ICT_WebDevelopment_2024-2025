import { defineStore } from 'pinia'
import { authApi } from '@/services/api'

export const useUserStore = defineStore('user', {
  state: () => ({
    token: localStorage.getItem('access_token') || null,
    user: null,
  }),
  getters: {
    isAuthenticated: (state) => !!state.token,
  },
  actions: {
    async login(username, password) {
      try {
        // Отправляем запрос на получение JWT токена
        const response = await authApi.post('jwt/create/', { username, password })
        
        // Сохраняем ТОЛЬКО access токен (не refresh!)
        this.token = response.data.access
        localStorage.setItem('access_token', this.token)
        
        // Загружаем информацию о пользователе
        await this.fetchUser()
        return true
      } catch (error) {
        console.error('Login error:', error)
        return false
      }
    },
    async register(username, password) {
      try {
        await authApi.post('users/', { username, password })
        return true
      } catch (error) {
        console.error('Registration error:', error)
        return false
      }
    },
    async fetchUser() {
      try {
        const response = await authApi.get('users/me/', {
          headers: { Authorization: `JWT ${this.token}` }
        })
        this.user = response.data
      } catch (error) {
        console.error('Fetch user error:', error)
      }
    },
    logout() {
      this.token = null
      this.user = null
      localStorage.removeItem('access_token')
    },
  },
})