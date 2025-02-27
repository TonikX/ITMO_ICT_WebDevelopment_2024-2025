import { createStore } from 'vuex'

export default createStore({
  state: {
    accessToken: null,
    refreshToken: null,
    isLoggedIn: false,
    isAdmin: false
  },
  mutations: {
    SET_ACCESS_TOKEN (state, token) {
      state.accessToken = token
    },
    SET_REFRESH_TOKEN (state, token) {
      state.refreshToken = token
    },
    SET_IS_LOGGED_IN (state, isLoggedIn) {
      state.isLoggedIn = isLoggedIn
    },
    SET_IS_ADMIN (state, isAdmin) {
      state.isAdmin = isAdmin
    }
  },
  actions: {
    login ({ commit }, data) {
      commit('SET_ACCESS_TOKEN', data.access)
      commit('SET_REFRESH_TOKEN', data.refresh)
      commit('SET_IS_LOGGED_IN', true)
      commit('SET_IS_ADMIN', data.is_admin)
    },
    logout ({ commit }) {
      commit('SET_ACCESS_TOKEN', null)
      commit('SET_REFRESH_TOKEN', null)
      commit('SET_IS_LOGGED_IN', false)
      commit('SET_IS_ADMIN', false)
    }
  },
  modules: {}
})
