<template>
  <v-app>
    <v-app-bar elevation="8" color="#FFFFFF">
      <v-toolbar-title>Hotel Management System</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn text to="/">Главная</v-btn>
      <v-btn text to="/profile">Профиль</v-btn>
      <v-btn text to="/clients">Клиенты</v-btn>
      <v-btn text to="/staff">Сотрудники</v-btn>
      <v-btn text to="/rooms">Номера</v-btn>
      <v-btn text to="/stays">Проживания</v-btn>
      <v-btn text to="/schedules">Расписания</v-btn>
      <v-btn text to="/report">Отчёт</v-btn>
      <v-btn variant="elevated" color="error" @click="logout">Выйти</v-btn>
    </v-app-bar>

    <v-main>
      <v-container fluid class="pa-4">
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: "App",
  data() {
    return {
      userLoggedIn: false,
    };
  },
  created() {
    this.checkAuth();
  },
  methods: {
    checkAuth() {
      const token = localStorage.getItem("token");
      this.userLoggedIn = !!token;
      if (!this.userLoggedIn && this.$route.path !== "/start") {
        this.$router.push("/start");
      }
    },
    logout() {
      localStorage.removeItem("token");
      this.userLoggedIn = false;
      this.$router.push("/start");
    },
  },
};
</script>
