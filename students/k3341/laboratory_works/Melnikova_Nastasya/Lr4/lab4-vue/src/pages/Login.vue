<template>
  <v-container class="py-10 d-flex justify-center">
    <v-card class="pa-8" style="max-width: 720px; width: 100%;">
      <h1 class="text-h4 mb-6">Login</h1>

      <v-text-field v-model="username" label="Username" />
      <v-text-field v-model="password" label="Password" type="password" />

      <v-btn color="primary" size="large" class="mt-3" :loading="loading" @click="onLogin">
        Login
      </v-btn>

      <div class="mt-6 text-body-1">
        Нет аккаунта? <router-link to="/register">REGISTER</router-link>
      </div>

      <v-alert v-if="error" type="error" class="mt-4" variant="tonal">
        {{ error }}
      </v-alert>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";

const router = useRouter();
const auth = useAuthStore();

const username = ref("");
const password = ref("");
const loading = ref(false);
const error = ref("");

onMounted(() => {
  if (auth.isAuthenticated) router.push("/");
});

async function onLogin() {
  error.value = "";
  loading.value = true;
  try {
    await auth.login(username.value, password.value);
    router.push("/");
  } catch (e) {
    error.value = "Неверный логин/пароль";
  } finally {
    loading.value = false;
  }
}
</script>