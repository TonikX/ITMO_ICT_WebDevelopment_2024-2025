import { api } from '@/services/api'

export default {
  namespaced: true,
  
  state: {
    isAuthenticated: false,
    user: null
  },

  mutations: {
    setAuth(state, isAuth) {
      state.isAuthenticated = isAuth
    },
    setUser(state, user) {
      state.user = user
    }
  },

  actions: {
    async login({ commit }, credentials) {
      try {
        const response = await api.post('/auth/login', credentials)
        localStorage.setItem('token', response.data.token)
        commit('setAuth', true)
        return response
      } catch (error) {
        throw error
      }
    },

    async logout({ commit }) {
      localStorage.removeItem('token')
      commit('setAuth', false)
      commit('setUser', null)
    },

    async initAuth({ commit, dispatch }) {
      const token = localStorage.getItem('token')
      if (token) {
        try {
          // Пробуем обновить токен при инициализации
          const response = await api.post('/auth/refresh-token', { token })
          localStorage.setItem('token', response.data.token)
          commit('setAuth', true)
        } catch (error) {
          console.error('Token refresh failed:', error)
          await dispatch('logout')
        }
      } else {
        commit('setAuth', false)
        commit('setUser', null)
      }
    }
  }
} 