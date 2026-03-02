<template>
  <v-container style="max-width: 520px">
    <v-card class="pa-4">
      <h2 class="mb-4">Регистрация</h2>

      <v-text-field v-model="username" label="Username" />
      <v-text-field v-model="password" label="Password" type="password" />

      <v-alert v-if="ok" type="success" class="mb-3">
        Аккаунт создан. Теперь можно войти.
      </v-alert>

      <v-alert v-if="error" type="error" class="mb-3">{{ error }}</v-alert>

      <v-btn block @click="submit" :loading="loading">Создать</v-btn>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref } from "vue";
import { register } from "../api/auth";

const username = ref("");
const password = ref("");
const error = ref("");
const ok = ref(false);
const loading = ref(false);

async function submit() {
  error.value = "";
  ok.value = false;
  loading.value = true;
  try {
    await register(username.value, password.value);
    ok.value = true;
  } catch {
    error.value = "Не удалось зарегистрироваться (возможно, username занят).";
  } finally {
    loading.value = false;
  }
}
</script>
