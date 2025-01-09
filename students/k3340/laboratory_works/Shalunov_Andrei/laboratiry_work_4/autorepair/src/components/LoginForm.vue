<template>
  <v-container>
    <v-form @submit.prevent="login">
      <v-text-field
        v-model="username"
        label="Username"
        required
      ></v-text-field>
      <v-text-field
        v-model="password"
        label="Password"
        type="password"
        required
      ></v-text-field>
      <v-btn type="submit" color="primary">Login</v-btn>
    </v-form>
  </v-container>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      username: "",
      password: "",
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post("/auth/token/login/", {
          username: this.username,
          password: this.password,
        });
        localStorage.setItem("authToken", response.data.auth_token);
        this.$store.commit("setToken", response.data.auth_token);
        this.$router.push("/");
      } catch (error) {
        console.error("Login failed:", error);
      }
    },
  },
};
</script>
