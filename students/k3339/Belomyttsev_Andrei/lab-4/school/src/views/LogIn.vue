<template>
  <h2>Log In</h2>
  <form @submit.prevent="submitForm">
    <label>Username</label>
    <input
      v-model="username"
      type="text"
    >
    <label>Password</label>
    <input
      v-model="password"
      type="password"
    >
    <button>Log In</button>
  </form>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      username: '',
      password: '',
    }
  },
  methods: {
    async submitForm() {
      const response = await axios.post('/api/auth/token/login/', {
        username: this.username,
        password: this.password,
      })
      const token = response.data.auth_token
      this.$store.commit('setToken', token)
      axios.defaults.headers.common['Authorization'] = 'Token ' + token
      localStorage.setItem('token', token)
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>

</style>