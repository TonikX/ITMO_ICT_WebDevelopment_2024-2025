<script>
import { RouterLink, RouterView } from 'vue-router'
import { mapStores } from 'pinia';
import { useAuthStore } from './stores/auth';


export default {
  data() {
    return {
      drawer: true,
    };
  },
  computed: {
    ...mapStores(useAuthStore)
  },
  methods: {
    async handleLogout() {
      await this.authStore.logout()
      this.$router.push('/')
    }
  },
  mounted() {
    this.authStore.checkAuth()
  }
};
</script>

<template>
  <v-responsive class="border rounded" min-height="1000">
    <v-app>
      <v-app-bar>
        <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
        <v-toolbar-title>Alpine clubs manager</v-toolbar-title>
      </v-app-bar>

      <v-navigation-drawer v-model="drawer" app>
        <v-list>
          <v-list-item to="/" title="Ascents"></v-list-item>
          <v-list-item to="/clubs" title="Clubs"></v-list-item>
          <v-list-item to="/report" title="Report"></v-list-item>
        </v-list>
        <v-divider></v-divider>
        <v-list v-if="!authStore.isAuthenticated">
          <v-list-item prepend-icon="mdi-login" to="/login" title="Log in"></v-list-item>
          <v-list-item prepend-icon="mdi-account-plus" to="/register" title="Register"></v-list-item>
        </v-list>
        <v-list v-if="authStore.isAuthenticated">
          <v-list-item to="/ascents/me" title="My ascents"></v-list-item>
          <v-list-item prepend-icon="mdi-account" to="/me" title="Profile"></v-list-item>
          <v-divider></v-divider>
          <v-list-item @click="handleLogout" prepend-icon="mdi-logout" title="Log out"></v-list-item>
        </v-list>
      </v-navigation-drawer>

      <v-main>
        <v-container>
          <RouterView />
        </v-container>
      </v-main>
    </v-app>
  </v-responsive>
</template>