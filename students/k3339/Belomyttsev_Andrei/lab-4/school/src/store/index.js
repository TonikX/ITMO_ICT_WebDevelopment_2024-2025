import { createStore } from 'vuex'

export default createStore({
  state: {
    token: ''
  },
  getters: {
    auth(state){
      return Boolean(state.token)
    }
  },
  mutations: {
    initializeStore(state) {
      if (localStorage.getItem('token')){
        state.token = localStorage.getItem('token')
      }
      else {
        state.token = ''
      }
    },
    setToken(state, token) {
      state.token = token
    },
    removeToken(state) {
      state.token = ''
    }
  },
  actions: {

  },
  modules: {

  },
})