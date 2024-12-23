<!-- src/views/ProfilePage.vue -->
<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" sm="8" md="6">
        <v-card class="pa-5" elevation="5">
          <v-card-title class="text-center text-h5">👤 Профиль пользователя</v-card-title>
          <v-card-text>
            <div v-if="isLoading" class="text-center">
              <v-progress-circular indeterminate color="primary" size="50"></v-progress-circular>
            </div>
            <div v-else>
              <v-list>
                <v-list-item>
                  <v-list-item-title>👤 Имя пользователя:</v-list-item-title>
                  <v-list-item-subtitle>{{ user.username || 'Не указано' }}</v-list-item-subtitle>
                </v-list-item>
                <v-list-item>
                  <v-list-item-title>📧 Email:</v-list-item-title>
                  <v-list-item-subtitle>{{ user.email || 'Не указано' }}</v-list-item-subtitle>
                </v-list-item>
              </v-list>
            </div>
          </v-card-text>
          <v-card-actions class="justify-center">
            <v-btn color="primary" @click="logout">🚪 Выйти</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  name: 'ProfilePage',
  computed: {
    user() {
      return this.$store.getters.user;
    },
    isAuthenticated() {
      return this.$store.getters.isAuthenticated;
    },
    isLoading() {
      return this.isAuthenticated && !this.user;
    },
  },
  methods: {
    logout() {
      this.$store.dispatch('logout');
      this.$router.push('/login');
    },
  },
  created() {
    if (this.isAuthenticated && !this.user) {
      this.$store.dispatch('fetchUser').catch((error) => {
        console.error('Ошибка при загрузке данных пользователя:', error);
      });
    }
  },
};
</script>

<style scoped>
</style>
