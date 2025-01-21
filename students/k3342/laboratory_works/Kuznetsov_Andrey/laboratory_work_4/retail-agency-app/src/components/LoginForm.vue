<template>
  <div class="form login-form">
    <h2>Login</h2>

    <div class="input-box">
      <input type="email" v-model="email" placeholder="Enter your email" required />
      <i class="uil uil-envelope-alt email"></i>
    </div>

    <div class="input-box">
      <input type="password" v-model="password" placeholder="Enter your password" required />
      <i class="uil uil-lock password"></i>
      <i class="uil uil-eye-slash pw-hide"></i>
    </div>

    <div class="option-field">
      <span class="checkbox">
        <input type="checkbox" v-model="rememberMe" />
        <label>Remember me</label>
      </span>
      <a href="#" @click="forgotPassword" aria-label="Forgot your password?">Forgot password?</a>
    </div>

    <button @click="login" class="button login" aria-label="Login now">Login Now</button>

    <div class="login-signup">Don't have an account? <a href="#" @click="switchToSignup">Signup</a></div>
  </div>
</template>

<script>
import { JWT_BASE_URL } from "@/config/config.js";

export default {
  data() {
    return {
      email: "",
      password: "",
      rememberMe: false
    };
  },
  methods: {
    async login(e) {
      e.preventDefault();

      if (!this.email || !this.password) {
        alert("Please enter both email and password.");
        return;
      }

      try {
        const response = await fetch(`${JWT_BASE_URL}/login`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ email: this.email, password: this.password })
        });

        const data = await response.json();

        if (data.token) {
          localStorage.setItem("isAuthenticated", "true");
          localStorage.setItem("currentUser", JSON.stringify(data.user));
          localStorage.setItem("jwt", data.token);

          this.$router.push({ name: 'Profile' });
          alert("Login successful.");
        } else {
          alert("Invalid email or password.");
        }
      } catch (error) {
        console.error("Error logging in:", error);
        alert("Error during authentication. Please try again later.");
      }
    },
    switchToSignup() {
      this.$emit("switch-form", "signup");
    },
    forgotPassword() {
      alert("Forgot password clicked.");
    }
  }
};
</script>

<style scoped>
</style>