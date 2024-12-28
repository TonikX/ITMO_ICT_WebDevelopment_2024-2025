// src/store/index.js
import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

export default new Vuex.Store({
  state: {
    user: null,
    workouts: [],
    savedWorkouts: [],
    completedWorkouts: [],
    posts: [],
    isAuthenticated: false
  },
  mutations: {
    SET_USER(state, user) {
      state.user = user
      state.isAuthenticated = !!user
    },
    SET_WORKOUTS(state, workouts) {
      state.workouts = workouts
    },
    SET_SAVED_WORKOUTS(state, workouts) {
      state.savedWorkouts = workouts
    },
    SET_COMPLETED_WORKOUTS(state, workouts) {
      state.completedWorkouts = workouts
    },
    SET_POSTS(state, posts) {
      state.posts = posts
    }
  },
  actions: {
    async login({ commit }, credentials) {
      try {
        const response = await axios.post('auth/login/', credentials)
        localStorage.setItem('token', response.data.token)
        axios.defaults.headers.common['Authorization'] = `Token ${response.data.token}`
        commit('SET_USER', response.data.user)
        return response
      } catch (error) {
        throw error
      }
    },
    async register({ commit }, userData) {
      try {
        const response = await axios.post('auth/register/', userData)
        localStorage.setItem('token', response.data.token)
        axios.defaults.headers.common['Authorization'] = `Token ${response.data.token}`
        commit('SET_USER', response.data.user)
        return response
      } catch (error) {
        throw error
      }
    },
    async logout({ commit }) {
      try {
        await axios.post('auth/logout/')
        localStorage.removeItem('token')
        delete axios.defaults.headers.common['Authorization']
        commit('SET_USER', null)
      } catch (error) {
        throw error
      }
    },
    async fetchWorkouts({ commit }) {
      try {
        const response = await axios.get('workouts/')
        commit('SET_WORKOUTS', response.data)
      } catch (error) {
        throw error
      }
    },
    async fetchUserWorkouts({ commit }) {
      try {
        const response = await axios.get('account/workouts/')
        commit('SET_COMPLETED_WORKOUTS', response.data)
      } catch (error) {
        throw error
      }
    },
    async fetchPosts({ commit }) {
      try {
        const response = await axios.get('blogs/')
        commit('SET_POSTS', response.data)
      } catch (error) {
        throw error
      }
    }
  }
})