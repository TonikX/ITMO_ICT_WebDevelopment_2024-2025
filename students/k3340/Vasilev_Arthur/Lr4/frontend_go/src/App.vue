<template>
  <v-app>
    <v-app-bar color="primary" dark sticky class="px-4">
      <v-app-bar-title class="font-weight-bold">📰 Publishing System</v-app-bar-title>
      <v-spacer />
      
      <div v-if="authStore.isAuthenticated" class="d-flex gap-2">
        <v-btn variant="text" to="/" size="small" class="text-white">
          Home
        </v-btn>
        <v-btn variant="text" to="/newspapers" size="small" class="text-white">
          Newspapers
        </v-btn>
        <v-btn variant="text" to="/printing-houses" size="small" class="text-white">
          Printing Houses
        </v-btn>
        <v-btn variant="text" to="/post-offices" size="small" class="text-white">
          Post Offices
        </v-btn>
        <v-btn variant="text" to="/distributions" size="small" class="text-white">
          Distributions
        </v-btn>
        <v-btn variant="text" to="/printing-runs" size="small" class="text-white">
          Print Runs
        </v-btn>
        <v-divider vertical class="mx-2 my-2" />
        <v-btn icon="mdi-account" variant="text" to="/profile" />
        <v-btn icon="mdi-logout" variant="text" @click="handleLogout" />
      </div>
      
      <v-btn v-else icon="mdi-login" variant="text" to="/login" />
    </v-app-bar>

    <v-main class="bg-surface">
      <router-view />
    </v-main>

    <v-footer app class="bg-primary text-white text-center">
      <span>© 2024 Publishing Management System</span>
    </v-footer>
  </v-app>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = useRouter()
const authStore = useAuthStore()

onMounted(async () => {
  if (authStore.token) {
    try {
      await authStore.init()
    } catch (error) {
      console.error('Error initializing auth:', error)
      authStore.logout()
    }
  }
})

function handleLogout() {
  authStore.logout()
  router.push('/login')
}
</script>

<style>
#app {
  font-family: 'Segoe UI', 'Roboto', sans-serif;
}
</style>
