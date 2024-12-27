import { createStore } from 'vuex';
import AuthService from '@/services/AuthService';

export default createStore({
  state: {
    user: null,
    token: localStorage.getItem('token') || '',
  },
  mutations: {
    setUser(state, user) {
      state.user = user;
    },
    setToken(state, token) {
      state.token = token;
      localStorage.setItem('token', token);
    },
  },
  actions: {
    async login({ commit }, { username, password }) {
      const response = await AuthService.login(username, password);
      commit('setToken', response.access);
    },
    async register({ commit }, user) {
      const response = await AuthService.register(user);
      commit('setUser', response.user);
    },
  },
});
