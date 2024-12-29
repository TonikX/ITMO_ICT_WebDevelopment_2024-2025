<template>
  <h2>Sign Up</h2>
  <form @submit.prevent="submitForm">
    <label>Username</label>
    <input
      v-model="username"
      type="text"
    >
    <label>Email</label>
    <input
      v-model="email"
      type="text"
    >
    <label>Password</label>
    <input
      v-model="password"
      type="password"
    >
    <button>Sign Up</button>
  </form>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      username: '',
      email: '',
      password: '',
    }
  },
  methods: {
    async submitForm() {
      await axios.post('/api/auth/users/', {
        username: this.username,
        email: this.email,
        password: this.password,
      })
      this.$router.push('/log-in')
    }
  }
}
</script>

<style scoped>

</style>