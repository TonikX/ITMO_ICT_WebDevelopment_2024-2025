<template>
    <v-layout class="rounded rounded-md">
      <v-navigation-drawer permanent>
        <v-list-item title="Библиотека"></v-list-item>
        <v-divider></v-divider>
        <template v-if="!Token.token">
        <router-link to="/login" style="text-decoration: none; color: inherit;"><v-list-item link title="Войти"></v-list-item></router-link>
        <router-link to="/register" style="text-decoration: none; color: inherit;"><v-list-item link title="Зарегистрироваться"></v-list-item></router-link>
        </template>
        <v-list-item v-else class="text-red" @click="Token.deleteToken">Выйти</v-list-item>

        <router-link to="/categories" style="text-decoration: none; color: inherit;"><v-list-item link title="Категории"></v-list-item></router-link>
        <router-link to="/authors" style="text-decoration: none; color: inherit;"><v-list-item link title="Авторы"></v-list-item></router-link>
        <router-link to="/readingrooms" style="text-decoration: none; color: inherit;"><v-list-item link title="Читальные залы"></v-list-item></router-link>
        <router-link to="/books" style="text-decoration: none; color: inherit;"><v-list-item link title="Книги"></v-list-item></router-link>
        <router-link to="/book-copies" style="text-decoration: none; color: inherit;"><v-list-item link title="Экземпляры книг"></v-list-item></router-link>
        <router-link to="/readers" style="text-decoration: none; color: inherit;"><v-list-item link title="Читатели"></v-list-item></router-link>
        <router-link to="/book-takes" style="text-decoration: none; color: inherit;"><v-list-item link title="Взятые книги"></v-list-item></router-link>

      </v-navigation-drawer>
      <v-main class="d-flex align-center justify-center" style="min-height: 300px;">
       <router-view/>
      </v-main>
    </v-layout>
</template>

<script setup>

import {TokenStore} from "@/stores/TokenStore";

const Token = TokenStore()
</script>

<style>
</style>
