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

<script setup lang="ts">import { ref } from "vue";
import { useRouter } from "vue-router";
import api from "@/services/AxiosService";

const router = useRouter();

const email = ref("");
const username = ref("");
const password = ref("");
const password2 = ref("");
const error = ref<string | null>(null);
const success = ref<string | null>(null);

const registerUser = async () => {
  error.value = null;
  success.value = null;

  if (password.value !== password2.value) {
    error.value = "Passwords do not match.";
    return;
  }

  try {
    await api.post("auth/users/", {
      email: email.value,
      username: username.value,
      password: password.value,
    });
    success.value = "Registration successful! You can now log in.";
    setTimeout(() => router.back(), 3000);
  } catch (err: any) {
    error.value = err.response?.data || "Registration failed.";
  }
};
</script>