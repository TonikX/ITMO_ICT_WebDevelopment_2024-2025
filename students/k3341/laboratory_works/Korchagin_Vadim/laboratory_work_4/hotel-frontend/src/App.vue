<template>
  <v-app>
    <!-- Навигация только если авторизован -->
    <NavigationBar v-if="userLoggedIn" />
    <v-main>
      <v-container fluid class="pa-4">
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
import NavigationBar from './components/NavigationBar.vue'

export default {
  name: 'App',
  components: { NavigationBar },
  data() {
    return {
      userLoggedIn: false
    }
  },
  created() {
    this.checkAuth()
  },
  watch: {
    $route() {
      this.checkAuth()
    }
  },
  methods: {
    checkAuth() {
      const token = localStorage.getItem('token')
      this.userLoggedIn = !!token
    }
  }
}
</script>