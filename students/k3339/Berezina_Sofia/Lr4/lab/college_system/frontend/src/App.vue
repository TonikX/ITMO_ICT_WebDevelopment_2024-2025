<template>
  <v-app>
    <v-app-bar v-if="isAuthenticated">
      <v-app-bar-title>Учебный портал</v-app-bar-title>
      <v-spacer></v-spacer>
      <v-btn to="/dashboard">Дашборд</v-btn>
      <v-btn to="/groups">Группы</v-btn>
      <v-btn to="/students">Студенты</v-btn>
      <v-btn @click="logout" class="logout">Выйти</v-btn>
    </v-app-bar>
    <v-main>
      <router-view></router-view>
    </v-main>
  </v-app>
</template>

<script>
export default {
  computed: {
    isAuthenticated() {
      return !!localStorage.getItem('token')
    }
  },
  methods: {
    logout() {
      localStorage.removeItem('token')
      this.$router.push('/login')
    }
  }
}
</script>

<style>
.logout {
  color: #e74c3c !important;
}
</style>