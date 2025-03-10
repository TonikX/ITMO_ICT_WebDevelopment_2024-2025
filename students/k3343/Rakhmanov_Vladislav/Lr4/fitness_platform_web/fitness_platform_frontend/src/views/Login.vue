<script setup lang="ts">
import { ref } from "vue";
import { useRouter } from "vue-router";
import { login } from "@/composables/AccountActions.ts"; // Assuming you have a login function

const form = ref({
  username: "",
  password: "",
});

const loading = ref(false);
const errorMessage = ref<string | null>(null);
const success = ref<string | null>(null);

const router = useRouter();

const submitForm = async () => {
  errorMessage.value = null;
  success.value = null;
  loading.value = true;
  try {
    await login(form.value.username, form.value.password);
    console.log("Login successful");

    success.value = "Login successful! Redirecting to home...";
    setTimeout(() => {
      router.push("/");
    }, 3000);
  } catch (error: any) {
    errorMessage.value = error.response?.data?.detail || "Login failed";
  } finally {
    loading.value = false;
  }
};
</script>

<template>
  <div class="d-flex justify-content-center align-items-center vh-100">
    <div class="card text-bg-dark p-4" style="width: 100%; max-width: 400px;">
      <h2 class="text-center mb-3">Login</h2>
      <form @submit.prevent="submitForm">
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
        <button type="submit" class="btn btn-primary w-100" :disabled="loading">
          {{ loading ? "Logging in..." : "Login" }}
        </button>
        <p v-if="success" class="text-success text-center mt-3">
          {{ success }}
        </p>
        <p v-if="errorMessage" class="text-danger text-center mt-3">
          {{ errorMessage }}
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
