// Store/modules/auth.js
import axios from 'axios'
const state = {
  user: JSON.parse(localStorage.getItem('user')) || null,
  token: localStorage.getItem('access_token') || null,
  isAuthenticated: !!localStorage.getItem('access_token'),
};

const mutations = {
  SET_USER(state, user) {
    state.user = user;
    localStorage.setItem('user', JSON.stringify(user));
  },
  SET_TOKEN(state, token) {
    state.token = token;
    state.isAuthenticated = !!token;
    localStorage.setItem('access_token', token)
  },
  CLEAR_TOKEN(state){
    state.token = null
    state.isAuthenticated = false
    localStorage.removeItem('access_token')
      localStorage.removeItem('user');
    state.user = null
  }
};

const actions = {
  async login({ commit }, { username, password }) {
    try {
      const response = await axios.post('https://localhost:8000/login/', {
        username,
        password,
      });
      if (response.status === 200) {
        commit('SET_TOKEN', response.data.access);
          const userResponse = await axios.get('https://localhost:8000/api/auth/users/me/', {
            headers: {
              Authorization: `Bearer ${response.data.access}`,
            },
          });
        commit('SET_USER', userResponse.data)
          localStorage.setItem('user', JSON.stringify(userResponse.data))
        return true; // Indicate successful login
      }
    } catch (error) {
      console.error(error);
      return false; // Indicate login failure
    }
  },
  logout({ commit }) {
    commit('CLEAR_TOKEN');
  },
};

export default {
  namespaced: true,
  state,
  mutations,
  actions,
};
