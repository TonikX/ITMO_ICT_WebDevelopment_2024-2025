<template>
  <div class="register-container">
    <h2>Login</h2>
    <form @submit.prevent="login">
      <div class="form-group">
        <label for="username">Username</label>
        <input
            type="text"
            id="username"
            v-model="username"
            class="form-control"
            autocomplete="username"
            required
        />
      </div>
      <div class="form-group">
        <label for="password">Password</label>
        <input
            type="password"
            id="password"
            v-model="password"
            class="form-control"
            autocomplete="current-password"
            required
        />
      </div>
      <button type="submit" class="btn btn-primary">Log into your account</button>
    </form>
    <p v-if="error" class="text-danger mt-3">{{ error }}</p>
    <p v-if="success" class="text-success mt-3">{{ success }}</p>
  </div>
</template>

<script>
import axiosInstance from "@/services/axios";
import router from "@/router/index.js";
import {SetAuthToken} from '@/composables/token.js';

export default {
  name: "LoginView",
  data() {
    return {
      username: "",
      password: "",
      error: null,
      success: null,
    };
  },
  methods: {
    async login() {
      this.error = null;
      this.success = null;

      try {
        const response = await axiosInstance.post("auth/token/login/", {
          username: this.username,
          password: this.password,
        });
        console.log(response);
        const data = await response.data;
        this.success = "Login successful!";
        SetAuthToken(data['auth_token']);
        setTimeout(router.back(), 3)

      } catch (err) {
        this.error = err.response?.data || "Login failed.";
      }
    },
  },
};
</script>
