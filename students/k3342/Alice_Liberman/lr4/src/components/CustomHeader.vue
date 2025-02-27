<script setup>
import {clearAuthToken, isAuthenticated} from "@/composables/useAuth.js";
import {useRouter} from "vue-router";
import {isHR} from "@/stores/globalState.js";

function logout() {
  const router = useRouter();
  clearAuthToken()
  router.push({path: router.currentRoute.value.fullPath})
}
</script>

<template>
  <header
      class="d-flex flex-wrap align-items-center justify-content-center justify-content-md-between py-3 mb-4 border-bottom container">
    <div class="col-md-3 mb-2 mb-md-0">
      <a href="/" class="d-inline-flex link-body-emphasis text-decoration-none">
        HH
      </a>
    </div>

    <div v-if="isHR" class="nav col-12 col-md-auto mb-2 justify-content-center mb-md-0">
      <router-link to="/" class="nav-link px-2 link-secondary">HR panel</router-link>
      <router-link to="/vacancies" class="nav-link px-2">Your company's vacancies</router-link>
    </div>
    <div v-else class="nav col-12 col-md-auto mb-2 justify-content-center mb-md-0">
      <router-link to="/" class="nav-link px-2 link-secondary">Job seeker panel</router-link>
      <router-link to="/vacancies" class="nav-link px-2">Browse vacancies</router-link>
      <router-link to="/cvs" class="nav-link px-2" v-if="isAuthenticated">Manage your cv's</router-link>
      <router-link to="/applications" class="nav-link px-2" v-if="isAuthenticated">Your applications</router-link>
    </div>


    <div class="col-md-3 text-end">
      <div v-if="isAuthenticated">
        <router-link to="/account" type="button" class="btn btn-outline-primary me-2">Account</router-link>
        <button type="button" class="btn btn-outline-danger me-2" @click="logout">Logout</button>
      </div>
      <div v-else>
        <router-link to="/login" type="button" class="btn btn-outline-primary me-2">Login</router-link>
        <router-link to="/register" type="button" class="btn btn-primary">Sign-up</router-link>
      </div>
    </div>
  </header>
</template>

<style scoped>

</style>