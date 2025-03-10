<script setup lang="ts">
import {IsAuthenticated} from '@/composables/tokenActions'
import {logout} from "@/composables/AccountActions.ts";
</script>

<template>
  <header class="p-3 text-bg-dark">
    <div class="container">
      <div class="d-flex flex-wrap align-items-center justify-content-center justify-content-lg-start">
        <a href="/" class="d-flex align-items-center mb-2 mb-lg-0 text-white text-decoration-none">
          <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" fill="currentColor" class="bi bi-gem" viewBox="0 0 20 20">
            <path d="M3.1.7a.5.5 0 0 1 .4-.2h9a.5.5 0 0 1 .4.2l2.976 3.974c.149.185.156.45.01.644L8.4 15.3a.5.5 0 0 1-.8 0L.1 5.3a.5.5 0 0 1 0-.6zm11.386 3.785-1.806-2.41-.776 2.413zm-3.633.004.961-2.989H4.186l.963 2.995zM5.47 5.495 8 13.366l2.532-7.876zm-1.371-.999-.78-2.422-1.818 2.425zM1.499 5.5l5.113 6.817-2.192-6.82zm7.889 6.817 5.123-6.83-2.928.002z"/>
          </svg>
        </a>

        <ul class="nav col-12 col-lg-auto me-lg-auto mb-2 justify-content-center mb-md-0">
          <li><router-link to="/" class="nav-link px-2 text-secondary">Home</router-link></li>
          <li v-if="IsAuthenticated"><router-link to="/workouts" class="nav-link px-2 text-white">Workouts</router-link></li>
          <li v-if="IsAuthenticated"><router-link to="/blogposts" class="nav-link px-2 text-white">Blog Posts</router-link></li>
          <li v-if="IsAuthenticated"><router-link to="/progress" class="nav-link px-2 text-white">Your progress</router-link></li>
          <li><a href="http://localhost:8000/admin" class="nav-link px-2 text-white">admin</a></li>
        </ul>


        <div class="text-end" v-if="IsAuthenticated">
          <router-link to="/account" class="btn btn-outline-light me-2">Account</router-link>
          <button type="button" class="btn btn-warning" @click="logout()">Logout</button>
        </div>
        <div class="text-end" v-else>
          <router-link to="/login" class="btn btn-outline-light me-2">Login</router-link>
          <router-link to="/register" class="btn btn-warning">Sign-up</router-link>
        </div>
      </div>
    </div>
  </header>
</template>

<style scoped>

</style>