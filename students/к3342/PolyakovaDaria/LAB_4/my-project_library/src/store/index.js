import { createStore } from 'vuex';
import axiosAuth from '@/axiosAuth';

export default createStore({
  state: {
    user: null,
    token: localStorage.getItem('token') || '',
  },
  mutations: {
    setUser(state, user) {
      state.user = user;
    },
    clearUser(state) {
      state.user = null;
    },
    setToken(state, token) {
      state.token = token;
      localStorage.setItem('token', token);
    },
    clearToken(state) {
      state.token = '';
      localStorage.removeItem('token');
    },
    clearAuthData(state) {
      state.token = '';
      state.user = null;
    },
  },
  actions: {
    async login({ commit }, credentials) {
      try {
        const response = await axiosAuth.post('/auth/token/login/', credentials);
        const token = response.data.auth_token;
        commit('setToken', token);

        const userResponse = await axiosAuth.get('/auth/users/me/');
        commit('setUser', userResponse.data);
      } 
      // eslint-disable-next-line no-useless-catch
      catch (error) {
        commit('clearToken');
        commit('clearUser');
        localStorage.removeItem('token');
        throw error;
      }
    },
    logout({ commit }) {
      commit('clearAuthData');
    },
    async fetchUser({ commit, state }) {
      if (state.token) {
        try {
          const response = await axiosAuth.get('/auth/users/me/');
          commit('setUser', response.data);
        } 
        // eslint-disable-next-line no-useless-catch
        catch (error) {
          commit('clearUser');
          commit('clearToken');
          localStorage.removeItem('token');
          throw error;
        }
      }
    },
  },
  getters: {
    isAuthenticated: (state) => !!state.token,
    user: (state) => state.user,
  },
});
