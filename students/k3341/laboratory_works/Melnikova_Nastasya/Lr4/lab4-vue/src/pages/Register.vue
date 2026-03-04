<template>
  <v-container class="py-10 d-flex justify-center">
    <v-card class="pa-8" style="max-width: 720px; width: 100%;">
      <h1 class="text-h4 mb-6">Register</h1>

      <v-text-field v-model="username" label="Username" />
      <v-text-field v-model="password" label="Password" type="password" />
      <v-text-field v-model="password2" label="Repeat password" type="password" />

      <v-btn color="primary" size="large" class="mt-3" :loading="loading" @click="onRegister">
        Register
      </v-btn>

      <div class="mt-6 text-body-1">
        Уже есть аккаунт? <router-link to="/login">LOGIN</router-link>
      </div>

      <v-alert v-if="ok" type="success" class="mt-4" variant="tonal">
        {{ ok }}
      </v-alert>

      <v-alert v-if="error" type="error" class="mt-4" variant="tonal">
        {{ error }}
      </v-alert>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import { useAuthStore } from "../stores/auth";

const router = useRouter();
const auth = useAuthStore();

const username = ref("");
const password = ref("");
const password2 = ref("");

const loading = ref(false);
const error = ref("");
const ok = ref("");

function humanizeBackendError(data) {
  // Djoser обычно отдаёт поля массивами строк
  if (!data) return "Не получилось зарегистрироваться";

  if (typeof data === "string") return data;

  if (data.username?.length) return `username: ${data.username[0]}`;
  if (data.password?.length) return `password: ${data.password[0]}`;
  if (data.non_field_errors?.length) return data.non_field_errors[0];
  if (data.detail) return data.detail;

  return "Не получилось зарегистрироваться";
}

async function onRegister() {
  error.value = "";
  ok.value = "";

  if (!username.value || !password.value || !password2.value) {
    error.value = "Заполни все поля";
    return;
  }

  if (password.value !== password2.value) {
    error.value = "Пароли не совпадают";
    return;
  }

  loading.value = true;
  try {
    await auth.register(username.value, password.value);
    ok.value = "Аккаунт создан! Теперь войди.";
    setTimeout(() => router.push("/login"), 400);
  } catch (e) {
    error.value = humanizeBackendError(e?.response?.data);
  } finally {
    loading.value = false;
  }
}
</script>