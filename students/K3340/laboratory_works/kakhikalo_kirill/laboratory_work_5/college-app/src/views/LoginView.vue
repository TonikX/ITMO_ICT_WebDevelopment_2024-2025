<template>
    <div>
      <h2>Login</h2>
      <form @submit.prevent="login">
        <div>
          <label>Username:</label>
          <input v-model="username" type="text" required />
        </div>
        <div>
          <label>Password:</label>
          <input v-model="password" type="password" required />
        </div>
        <button type="submit">Login</button>
      </form>
      <p v-if="error" style="color:red;">{{ error }}</p>
    </div>
  </template>
  
  <script>
  import api from '@/api'
  
  export default {
    name: 'LoginView',
    data() {
      return {
        username: '',
        password: '',
        error: ''
      }
    },
    methods: {
      login() {
        api.post('/auth/token/login/', {
          username: this.username,
          password: this.password
        })
        .then(response => {
          const token = response.data.auth_token
          localStorage.setItem('authToken', token)
          this.$router.push('/')
        })
        .catch(err => {
          console.error('Login error:', err)
          this.error = 'Invalid credentials, please try again.'
        })
      }
    }
  }
  </script>
  
  <style scoped>
  </style>
  