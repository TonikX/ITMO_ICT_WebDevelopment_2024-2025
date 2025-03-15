<template>
  <v-layout class="rounded rounded-md">
    <v-navigation-drawer permanent>
      <router-link to="/"><v-list-item title="Библиотека"></v-list-item></router-link>
      <v-divider></v-divider>
      <template v-if="!Token.token">
      <router-link to="/login"><v-list-item link title="Войти"></v-list-item></router-link>
      <router-link to="/register"><v-list-item link title="Зарегистрироваться"></v-list-item></router-link>
      </template>
      <template v-else>
      <v-list-item class="text-red" @click="Token.deleteToken">Выйти</v-list-item>

      <router-link to="/genre"><v-list-item link title="Жанры"></v-list-item></router-link>
      <router-link to="/author"><v-list-item link title="Авторы"></v-list-item></router-link>
      <router-link to="/room" ><v-list-item link title="Читальные залы"></v-list-item></router-link>
      <router-link to="/book" ><v-list-item link title="Книги"></v-list-item></router-link>
      <router-link to="/book_copy"><v-list-item link title="Копии книг"></v-list-item></router-link>
      <router-link to="/reader"><v-list-item link title="Читатели"></v-list-item></router-link>
    </template>
    </v-navigation-drawer>
    <v-main class="d-flex align-center justify-center" style="min-height: 300px;">
      <router-view/>
    </v-main>
  </v-layout>
</template>

<script setup>
import instance from './AxiosInstance';
import { TokenStore } from './stores/TokenStore';

const Token = TokenStore();

instance.interceptors.request.use(
    (config) => {
        const token = Token.token;

        if (token) {
            config.headers.Authorization = `Token ${token}`;
        }

        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);
</script>

<style>
</style>