<script setup lang="ts">
import { ref } from "vue";
import {register} from "@/composables/AccountActions.ts";
import router from "@/router";

const form = ref({
  email: "",
  username: "",
  password: "",
  re_password: "",
});

const loading = ref(false);
const errorMessage = ref<string | null>(null);
const success = ref<string>("");

const submitForm = async () => {
  errorMessage.value = null;
  loading.value = true;
  if (form.value.password !== form.value.re_password) {
    loading.value = false;
    errorMessage.value = "Passwords do not match";
    return
  }
  try {
    await register(form.value.email, form.value.password, form.value.re_password, form.value.username);
    console.log("Registration successful");
    success.value = 'Registration successful. You will automatically log in and be redirected to home';
    setTimeout(() => {
      router.push("/");
    }, 3000);
  } catch (error: any) {
    errorMessage.value = error.response?.data?.detail || "Registration failed";
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div class="d-flex justify-content-center align-items-center vh-100">
    <div class="card text-bg-dark p-4" style="width: 100%; max-width: 400px;">
      <h2 class="text-center mb-3">Register</h2>
      <form @submit.prevent="submitForm">
        <div class="mb-3">
          <label for="email" class="form-label">Email</label>
          <input
              id="email"
              v-model="form.email"
              type="email"
              class="form-control"
              required
          />
        </div>
        <div class="mb-3">
          <label for="username" class="form-label">Username</label>
          <input
              id="username"
              v-model="form.username"
              type="text"
              class="form-control"
              required
          />
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Password</label>
          <input
              id="password"
              v-model="form.password"
              type="password"
              class="form-control"
              required
          />
        </div>
        <div class="mb-3">
          <label for="re_password" class="form-label">Confirm Password</label>
          <input
              id="re_password"
              v-model="form.re_password"
              type="password"
              class="form-control"
              required
          />
        </div>
        <button type="submit" class="btn btn-primary w-100" :disabled="loading">
          {{ loading ? "Registering..." : "Register" }}
        </button>
        <p v-if="errorMessage" class="text-danger text-center mt-3">
          {{ errorMessage }}
        </p>
        <p v-if="success" class="text-center mt-3 text-success">
          {{ success }}
        </p>
      </form>
    </div>
  </div>
</template>

<style scoped>
.card {
  border-radius: 10px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}
</style>
