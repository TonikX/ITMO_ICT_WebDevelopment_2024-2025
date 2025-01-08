<template>
  <v-app>
    <app-header v-if="isInitialized && isAuthenticated"></app-header>
    
    <v-main :class="{ 'pt-0': !isAuthenticated }">
      <router-view v-if="isInitialized"></router-view>
      <v-overlay v-else>
        <v-progress-circular indeterminate></v-progress-circular>
      </v-overlay>
    </v-main>
  </v-app>
</template>

<script>
import AppHeader from '@/components/AppHeader.vue'
import { mapState } from 'vuex'

export default {
  name: 'App',

  components: {
    AppHeader
  },

  data: () => ({
    isInitialized: false
  }),

  computed: {
    ...mapState('auth', ['isAuthenticated'])
  },

  async created() {
    await this.$store.dispatch('auth/initAuth')
    this.isInitialized = true
  }
}
</script>

<style>
.v-application {
  width: 100%;
  max-width: 100%;
}

.v-main {
  width: 100%;
  max-width: 100%;
  padding-top: 64px !important;
}

.v-main.pt-0 {
  padding-top: 0 !important;
}

.v-container {
  max-width: 100% !important;
}
</style>
