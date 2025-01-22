<script setup>
import {tokenStore} from "@/stores/token.js";
import router from "@/utils/router.js";
import axios from "axios";
const token = tokenStore()
if (token.token) {
  axios.defaults.headers.common['Authorization'] = `Token ${token.token}`
}
function logout() {
  token.deleteToken()
  router.push("/login")
}
</script>

<template>
  <v-layout class="rounded rounded-md">
    <v-app-bar permanent>
      <div class="d-flex align-center">
      <v-list-item>
        <template v-slot:title>Страховая организация</template>
      </v-list-item>
      <router-link to="/agents" class="menu-link">
        <v-list-item link>Агенты</v-list-item>
      </router-link>
      <router-link to="/clients" class="menu-link">
        <v-list-item link>Индивидуальные клиенты</v-list-item>
      </router-link>
      <router-link to="/organizations" class="menu-link">
        <v-list-item link>Организации</v-list-item>
      </router-link>
      <router-link to="/report" class="menu-link">
        <v-list-item link>Отчёт</v-list-item>
      </router-link>
    </div>

      <v-spacer/>

      <div class="d-flex align-center">
        <template v-if="!token.token">
          <router-link to="/login" style="text-decoration: none; color: green;">
            <v-list-item link title="Войти"></v-list-item>
          </router-link>
          <router-link to="/register" style="text-decoration: none; color: green;">
            <v-list-item link title="Зарегистрироваться"></v-list-item>
          </router-link>
        </template>
        <template v-else>
          <v-list-item class="text-green" @click="logout">Выйти</v-list-item>
        </template>
      </div>
    </v-app-bar>

    <v-main class="d-flex align-center justify-center" style="min-height: 300px;">
      <router-view/>
    </v-main>
  </v-layout>
</template>


<style scoped>
.menu-link {
  color: green; /* Цвет ссылок в меню */
}

.menu-link:hover {
  text-decoration: underline; /* Подчеркивание при наведении */
}
</style>
