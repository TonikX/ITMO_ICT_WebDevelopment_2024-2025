import { createStore } from 'vuex';
import axios from 'axios';

export default createStore({
  state: {
    token: localStorage.getItem('authToken') || null,
    clients: [],
    employees: [],
    automobiles: [],
    contracts: [],
    services: [],
  },
  mutations: {
    setToken(state, token) {
      state.token = token;
      localStorage.setItem('authToken', token);
      axios.defaults.headers.common['Authorization'] = `Token ${token}`;
    },
    clearToken(state) {
      state.token = null;
      localStorage.removeItem('authToken');
      delete axios.defaults.headers.common['Authorization'];
    },
    setClients(state, clients) {
      state.clients = clients;
    },
    setEmployees(state, employees) {
      state.employees = employees;
    },
    setAutomobiles(state, automobiles) {
      state.automobiles = automobiles;
    },
    setContracts(state, contracts) {
      state.contracts = contracts;
    },
    setServices(state, services) {
      state.services = services;
    },
  },
  actions: {
    async fetchClients({ commit }) {
      try {
        const response = await axios.get('/clients/');
        commit('setClients', response.data);
      } catch (error) {
        console.error('Failed to fetch clients:', error);
      }
    },
    async fetchEmployees({ commit }) {
      try {
        const response = await axios.get('/employees/');
        commit('setEmployees', response.data);
      } catch (error) {
        console.error('Failed to fetch employees:', error);
      }
    },
    async fetchAutomobiles({ commit }) {
      try {
        const response = await axios.get('/automobiles/');
        commit('setAutomobiles', response.data);
      } catch (error) {
        console.error('Failed to fetch automobiles:', error);
      }
    },
    async fetchContracts({ commit }) {
      try {
        const response = await axios.get('/contracts/');
        commit('setContracts', response.data);
      } catch (error) {
        console.error('Failed to fetch contracts:', error);
      }
    },
    async fetchServices({ commit }) {
      try {
        const response = await axios.get('/services/');
        commit('setServices', response.data);
      } catch (error) {
        console.error('Failed to fetch services:', error);
      }
    },
    async logout({ commit }) {
      commit('clearToken');
    },
  },
});
