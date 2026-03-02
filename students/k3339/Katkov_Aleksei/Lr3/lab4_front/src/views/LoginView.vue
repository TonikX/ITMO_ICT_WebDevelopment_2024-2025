<template>
  <v-container style="max-width: 520px">
    <v-card class="pa-4">
      <h2 class="mb-4">Вход</h2>

      <v-text-field v-model="username" label="Username" />
      <v-text-field v-model="password" label="Password" type="password" />

      <v-alert v-if="error" type="error" class="mb-3">{{ error }}</v-alert>

      <v-btn block @click="submit" :loading="loading">Войти</v-btn>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { login } from "../api/auth";
import { setToken } from "../authState";

const router = useRouter();
const username = ref("");
const password = ref("");
const error = ref("");
const loading = ref(false);

function extractToken(res) {
  // поддержка двух вариантов:
  // 1) axios response: { data: { auth_token: "..." } }
  // 2) уже data: { auth_token: "..." }
  return res?.data?.auth_token || res?.auth_token || "";
}

async function submit() {
  error.value = "";
  loading.value = true;

  try {
    const res = await login(username.value, password.value);
    const newToken = extractToken(res);

    if (!newToken) {
      throw new Error("Token not found in login() result");
    }

    setToken(newToken);
    router.push("/tasks");
  } catch (e) {
    error.value = "Не удалось войти. Проверь логин/пароль.";
  } finally {
    loading.value = false;
  }
}
</script>
