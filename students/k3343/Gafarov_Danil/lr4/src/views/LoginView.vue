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
            required
        />
      </div>
      <button type="submit" class="btn btn-primary">Register</button>
    </form>
    <p v-if="error" class="text-danger mt-3">{{ error }}</p>
    <p v-if="success" class="text-success mt-3">{{ success }}</p>
  </div>
</template>

<script>
import axiosInstance from "@/services/axios";
import router from "@/router/index.js";
import {setAuthToken} from '@/composables/tokenActions.js';

export default {
  name: "LoginView",
  components: {},
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
        setAuthToken(data['auth_token']);
        setTimeout(router.back(), 3)

      } catch (err) {
        this.error = err.response?.data?.detail || "Login failed.";
      }
    },
  },
};
</script>
