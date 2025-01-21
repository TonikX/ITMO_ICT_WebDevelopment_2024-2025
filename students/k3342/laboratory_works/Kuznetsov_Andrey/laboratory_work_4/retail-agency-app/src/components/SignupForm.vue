<template>
  <div class="form signup-form">
    <h2>Signup</h2>

    <div class="input-box">
      <input type="email" v-model="email" placeholder="Enter your email" required />
      <i class="uil uil-envelope-alt email"></i>
    </div>

    <div class="input-box">
      <input type="password" v-model="password" placeholder="Create password" required />
      <i class="uil uil-lock password"></i>
      <i class="uil uil-eye-slash pw-hide"></i>
    </div>

    <div class="input-box">
      <input type="password" v-model="confirmPassword" placeholder="Confirm password" required />
      <i class="uil uil-lock password"></i>
      <i class="uil uil-eye-slash pw-hide"></i>
    </div>

    <div class="input-box">
      <input type="text" v-model="name" placeholder="Enter your full name" required />
      <i class="uil uil-user name"></i>
    </div>

    <div class="input-box">
      <input type="text" v-model="status" placeholder="Enter your status" required />
      <i class="uil uil-info-circle status"></i>
    </div>

    <button @click="signup" class="button signup" aria-label="Signup now">Signup Now</button>

    <div class="login-signup">Already have an account? <a href="#" @click="switchToLogin">Login</a></div>
  </div>
</template>

<script>
import { JWT_BASE_URL } from "@/config/config.js";


export default {
  data() {
    return {
      email: "",
      password: "",
      confirmPassword: "",
      name: "",
      status: ""
    };
  },
  methods: {
    async signup(e) {
      e.preventDefault();

      if (this.password !== this.confirmPassword) {
        alert("Passwords do not match.");
        return;
      }

      if (!this.email || !this.password || !this.confirmPassword) {
        alert("Please fill in all fields.");
        return;
      }

      try {
        const response = await fetch(`${JWT_BASE_URL}/register`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            email: this.email,
            password: this.password,
            name: this.name,
            status: this.status
          })
        });

        const data = await response.json();

        if (response.ok) {
          alert("Registration successful. Please log in.");
          this.$emit("switch-form", "login");
        } else {
          alert(`Registration failed: ${data.message || 'Unknown error'}`);
        }
      } catch (error) {
        console.error("Error registering user:", error);
        alert("Error during registration. Please try again later.");
      }
    },
    switchToLogin() {
      this.$emit("switch-form", "login");
    }
  }
};
</script>

<style scoped>
</style>
