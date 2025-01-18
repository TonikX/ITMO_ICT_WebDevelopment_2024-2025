<script setup>
import {ClearAuthToken, IsAuthenticated} from "@/composables/token.js";
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
          <RouterLink to="/" class="nav-link px-2 link-secondary">Home</RouterLink>
        </li>
        <li>
          <RouterLink to="/tenant" class="nav-link px-2">Browse properties</RouterLink>
        </li>
        <li>
          <RouterLink to="/tenant/history" class="nav-link px-2" v-if="IsAuthenticated">Your leases</RouterLink>
        </li>
        <li>
          <RouterLink to="/landlord/me" class="nav-link px-2" v-if="IsAuthenticated">Your properties</RouterLink>
        </li>
        <li>
          <RouterLink to="/landlord/archive" class="nav-link px-2" v-if="IsAuthenticated">Your applicants</RouterLink>
        </li>
      </ul>

      <div class="col-md-3 text-end">
        <div v-if="IsAuthenticated">
          <router-link type="button" class="btn btn-outline-primary me-2" to="/landlord/me">Ваш аккаунт</router-link>
          <button type="button" class="btn btn-primary" @click="ClearAuthToken">Выйти</button>
        </div>
        <div v-else>
          <router-link type="button" class="btn btn-outline-primary me-2" to="/login">Войти</router-link>
          <router-link type="button" class="btn btn-primary" to="/register">Регистрация</router-link>
        </div>
      </div>
    </header>
  </div>
</template>

<style scoped>

</style>