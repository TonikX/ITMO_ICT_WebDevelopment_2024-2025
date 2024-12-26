<script setup>

import {tokenStore} from "@/stores/tokenStore.js";
import router from "@/router/index.js";

const token = tokenStore()

function logout() {
  token.deleteToken()
  router.push("/login")
}
</script>

<template>
  <v-layout class="rounded rounded-md">
    <v-app-bar permanent>
      <div class="d-flex align-center">
        <template v-if="token.token">
          <router-link to="/users" style="text-decoration: none; color: inherit;">
            <v-list-item link title="Пользователи"></v-list-item>
          </router-link>
          <router-link to="/newspapers" style="text-decoration: none; color: inherit;">
            <v-list-item link title="Газеты"></v-list-item>
          </router-link>
          <router-link to="/printinghouses" style="text-decoration: none; color: inherit;">
            <v-list-item link title="Типографии"></v-list-item>
          </router-link>
          <router-link to="/postoffices" style="text-decoration: none; color: inherit;">
            <v-list-item link title="Почтовые отделения"></v-list-item>
          </router-link>
          <router-link to="/editions" style="text-decoration: none; color: inherit;">
            <v-list-item link title="Тиражи"></v-list-item>
          </router-link>
          <router-link to="/distributions" style="text-decoration: none; color: inherit;">
            <v-list-item link title="Поставки"></v-list-item>
          </router-link>
          <router-link to="/analytics" style="text-decoration: none; color: inherit;">
            <v-list-item link title="Аналитика"></v-list-item>
          </router-link>
          <router-link to="/reports" style="text-decoration: none; color: inherit;">
            <v-list-item link title="Отчёты"></v-list-item>
          </router-link>
        </template>
      </div>

      <v-spacer/>

      <div class="d-flex align-center">
        <template v-if="!token.token">
          <router-link to="/login" style="text-decoration: none; color: inherit;">
            <v-list-item link title="Авторизация"></v-list-item>
          </router-link>
          <router-link to="/register" style="text-decoration: none; color: inherit;">
            <v-list-item link title="Регистрация"></v-list-item>
          </router-link>
        </template>
        <template v-else>
          <v-list-item class="text-red" @click="logout">Выйти</v-list-item>
        </template>
      </div>
    </v-app-bar>

    <v-main class="d-flex align-center justify-center" style="min-height: 300px;">
      <router-view/>
    </v-main>
  </v-layout>
</template>


<style scoped>

</style>
