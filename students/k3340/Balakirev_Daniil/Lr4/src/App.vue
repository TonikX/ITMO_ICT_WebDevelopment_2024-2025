<template>
  <v-app>
    <v-app-bar app color="teal" dark>
      <div class="d-flex align-center">
        <h1 class="headline"></h1>
      </div>
      <v-toolbar-items class="hidden-sm-and-down">
        <v-btn color="white" plain @click="authAction">
          {{ isLoggedIn ? 'Выйти' : 'Войти' }}
        </v-btn>
        <v-btn v-if="isLoggedIn" color="white" plain @click="rooms">
          Комнаты
        </v-btn>
        <v-btn v-if="isLoggedIn" color="white" plain @click="clients">
          Клиенты
        </v-btn>
        <v-btn v-if="isLoggedIn" color="white" plain @click="bookings">
          Бронирования
        </v-btn>
        <v-btn v-if="isLoggedIn" color="white" plain @click="cleaningSchedules">
          Расписание уборки
        </v-btn>
      </v-toolbar-items>
    </v-app-bar>

    <router-view />
  </v-app>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      isLoggedIn: localStorage.getItem('auth_token') !== null,
    };
  },
  methods: {
    authAction() {
      if (this.isLoggedIn) {
        localStorage.removeItem('auth_token');
        this.$router.push({ name: 'Login' });
      } else {
        this.$router.push({ name: 'Login' });
      }
    },
    rooms() {
      this.$router.push({ name: 'Rooms' });
    },
    clients() {
      this.$router.push({ name: 'Clients' });
    },
    bookings() {
      this.$router.push({ name: 'Bookings' });
    },
    cleaningSchedules() {
      this.$router.push({ name: 'CleaningSchedules' });
    },
  },
  watch: {
    $route() {
      this.isLoggedIn = localStorage.getItem('auth_token') !== null;
    }
  }
};
</script>

<style>
</style>