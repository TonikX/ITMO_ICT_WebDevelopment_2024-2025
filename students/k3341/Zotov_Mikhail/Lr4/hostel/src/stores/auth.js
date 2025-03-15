import {defineStore} from 'pinia'
import {api} from '@/utils/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    token: localStorage.getItem('authToken') || null
  }),

  getters: {
    isAuthenticated: (state) => !!state.token
  },

  actions: {
    async login(credentials) {
      try {
        const tokenResponse = await api.post('/auth/token/login/', credentials)
        this.token = tokenResponse.data.auth_token
        localStorage.setItem('authToken', this.token)

        const userResponse = await api.get('/auth/users/me/')
        this.user = userResponse.data

        return true
      } catch (error) {
        this.clearAuth()
        throw error
      }

    }
    ,

    async logout() {
      try {
        await api.post('/auth/token/logout/')
      } finally {
        this.clearAuth()
      }
    },

    async checkAuth() {
      if (this.token) {
        try {
          const response = await api.get('/auth/users/me/')
          this.user = response.data
        } catch (error) {
          this.clearAuth()
        }
      }
    },

    clearAuth() {
      this.token = null
      this.user = null
      localStorage.removeItem('authToken')
    }
  },
})
