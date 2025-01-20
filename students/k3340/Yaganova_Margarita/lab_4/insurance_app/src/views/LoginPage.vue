<template>
<div class="auth-container">
    <div class="card col-md-6">
    <div class="card-body">
        <form class="auth-form" id="entranceForm" @submit.prevent="handleLogin">
          <h2>Login</h2>
          <div class="mb-3">
            <label for="username" class="form-label">Username</label>
            <input
              type="text"
              id="username"
              class="form-control"
              required
              v-model="username"
            />
          </div>
          <div class="mb-3">
            <label for="password" class="form-label">Password</label>
            <input type="password" class="form-control" id="password" required v-model="password" />
          </div>
          <button type="submit" class="btn btn-primary">Log in</button>
        </form>
    </div>
    </div>
  </div>
</template>

<script>
import { login } from '@/services/authService';
import router from '@/router';

export default {
  data() {
    return {
      username: '',
      password: '',
    };
  },
  methods: {
    async handleLogin() {
      try {
        const token = await login(this.username, this.password)
        router.push({name: 'account'})
      } catch (error) {
        console.error(error);
    }
  },
}}
</script>

<style scoped>
.auth-container {
  display: flex;
  justify-content: center;
  margin-top: 5%;
}
</style>