<script setup lang="ts">
import {isAuthenticated, logout} from "@/services/AuthService.ts";
</script>

<template>
  <div class="container">
    <header
        class="d-flex flex-wrap align-items-center justify-content-center justify-content-md-between py-3 mb-4 border-bottom">
      <div class="col-md-3 mb-2 mb-md-0">
        <a href="/" class="d-inline-flex link-body-emphasis text-decoration-none">
          <svg class="bi" width="40" height="32" role="img" aria-label="Bootstrap">
            <use xlink:href="#bootstrap"></use>
          </svg>
        </a>
      </div>

      <ul class="nav col-12 col-md-auto mb-2 justify-content-center mb-md-0">
        <li>
          <router-link class="nav-link px-2 link-secondary" to="/recipes">Рецепты</router-link>
        </li>
        <li>
          <router-link to="/recipes" class="nav-link px-2">Поиск</router-link>
        </li>
        <li v-if="isAuthenticated"><router-link to="/favourites" class="nav-link px-2">Ваши любимые</router-link></li>
      </ul>

      <div class="col-md-3 text-end" v-if="!isAuthenticated">
        <router-link to="/login" type="button" class="btn btn-outline-primary me-2">Войти</router-link>
        <router-link to="/register" class="btn btn-primary">Регистрироваться</router-link>
      </div>
      <div v-else class="col-md-3 text-end">
        <router-link to="/account" type="button" class="btn btn-outline-primary me-2">Аккаунт</router-link>
        <button class="btn btn-outline-danger" @click="logout()">Выйти</button>
      </div>
    </header>
  </div>
</template>

<style scoped>

</style>