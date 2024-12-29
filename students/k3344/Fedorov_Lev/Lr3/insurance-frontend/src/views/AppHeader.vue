<template>
  <header class="app-header">
    <div class="logo">
      <img src="@/assets/logo.png" alt="Logo" />
      <h1>Insurance</h1>
    </div>
    <nav>
      <router-link v-if="isAuthenticated" to="/contracts">Контракты</router-link>
      <router-link v-if="isAuthenticated && user.role !== 'agent'" to="/employees">Работники</router-link>
      <router-link v-if="isAuthenticated" to="/dashboard">Профиль</router-link>
      <router-link v-if="isAuthenticated" to="/insurance-cases">Страховые случаи</router-link>
      <button v-if="isAuthenticated" @click="logout">Выйти</button>
      <router-link v-else to="/login">Войти</router-link>
      <router-link v-if="!isAuthenticated" to="/register">Зарегистрироваться</router-link>
    </nav>
  </header>
</template>

<script>
import apiClient from '@/services/apiClient';
import AuthService from '@/services/AuthService';

export default {
  data() {
    return {
      user: {},
      isAuthenticated: false,
    };
  },
  async created() {
    await this.fetchUser();
  },
  methods: {
    async fetchUser() {
      try {
        const response = await apiClient.get('/insurance/user/profile/');
        this.user = response.data;
        this.isAuthenticated = true;
      } catch (error) {
        console.error('Ошибка загрузки профиля:', error.response?.data || error);
        this.isAuthenticated = false;
      }
    },
    logout() {
      AuthService.logout();
      this.isAuthenticated = false;
      this.$router.push('/login');
    },
  },
};
</script>

<style scoped>
.app-header {
  background: #fff;
  color: #333;
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 15px 30px;
  border-bottom: 1px solid #ddd;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
}
.app-header .logo {
  display: flex;
  align-items: center;
}
.app-header img {
  height: 40px;
  margin-right: 10px;
}
.app-header nav a, .app-header nav button {
  color: #333;
  margin-left: 20px;
  text-decoration: none;
  font-weight: 500;
  background: none;
  border: none;
  cursor: pointer;
}
.app-header nav a:hover, .app-header nav button:hover {
  color: #007bff;
}
</style>