<template>
  <v-app>
    <v-app-bar elevation="1">
      <v-spacer />

      <template v-if="isAuth">
        <v-btn variant="text" to="/categories">Категории</v-btn>
        <v-btn variant="text" to="/tasks">Задачи</v-btn>
        <v-btn variant="text" to="/profile">Профиль</v-btn>

        <v-spacer />

        <v-btn variant="text" @click="logout">Выйти</v-btn>
      </template>

      <template v-else>
        <v-btn variant="text" to="/login">Войти</v-btn>
        <v-btn variant="text" to="/register">Регистрация</v-btn>
      </template>
    </v-app-bar>

    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script setup>
import { computed } from "vue";
import { useRouter } from "vue-router";
import { token, setToken } from "./authState";

const router = useRouter();
const isAuth = computed(() => !!token.value);

function logout() {
  setToken("");
  router.push("/login");
}
</script>
