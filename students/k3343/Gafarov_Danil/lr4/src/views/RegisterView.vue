<template>
  <div class="register-container">
    <h2>Register</h2>
    <form @submit.prevent="registerUser">
      <div class="form-group">
        <label for="email">Email</label>
        <input
            type="email"
            id="email"
            v-model="email"
            class="form-control"
            required
        />
      </div>
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
      <div class="form-group">
        <label for="password2">Confirm Password</label>
        <input
            type="password"
            id="password2"
            v-model="password2"
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

export default {
  name: "RegisterView",
  components: {},
  data() {
    return {
      email: "",
      username: "",
      password: "",
      password2: "",
      error: null,
      success: null,
    };
  },
  methods: {
    async registerUser() {
      this.error = null;
      this.success = null;

      if (this.password !== this.password2) {
        this.error = "Passwords do not match.";
        return;
      }

      try {
        await axiosInstance.post("auth/users/", {
          email: this.email,
          username: this.username,
          password: this.password,
        });
        this.success = "Registration successful! You can now log in.";
        setTimeout(router.back(), 3)

      } catch (err) {
        this.error = err.response?.data || "Registration failed.";
      }
    },
  },
};
</script>
