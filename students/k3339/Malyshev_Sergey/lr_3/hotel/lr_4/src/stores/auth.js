import { defineStore } from 'pinia'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: null,
    loading: false,
    error: null,
  }),

  actions: {
    async login(username, password) {
      this.loading = true
      this.error = null

      try {
        const response = await fetch('http://127.0.0.1:8000/auth/token/login/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ username, password }),
        })

        if (!response.ok) {
          const errData = await response.json()
          throw new Error(errData.detail || 'Ошибка входа')
        }

        const data = await response.json()
        this.token = data.auth_token
        localStorage.setItem('token', this.token)

        await this.fetchUser()
        return true
      } catch (err) {
        this.error = err.message
        throw err
      } finally {
        this.loading = false
      }
    },

    async register(username, password) {
      this.loading = true
      this.error = null

      try {
        const response = await fetch('http://127.0.0.1:8000/auth/users/', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            username,
            password,
            re_password: password,
          }),
        })

        if (!response.ok) {
          const errData = await response.json()
          throw new Error(JSON.stringify(errData)) // покажем все ошибки от Djoser
        }

        // После регистрации сразу логинимся
        await this.login(username, password)
        return true
      } catch (err) {
        this.error = err.message
        throw err
      } finally {
        this.loading = false
      }
    },

    async fetchUser() {
      if (!this.token) return

      try {
        const response = await fetch('http://127.0.0.1:8000/auth/users/me/', {
          headers: {
            Authorization: `Token ${this.token}`,
          },
        })

        if (response.ok) {
          this.user = await response.json()
        } else {
          this.logout()
        }
      } catch (err) {
        this.logout()
      }
    },

    logout() {
      this.token = null
      this.user = null
      this.error = null
      localStorage.removeItem('token')
    },
  },

  getters: {
    isAuthenticated: (state) => !!state.token,
    hasError: (state) => !!state.error,
  },
})
