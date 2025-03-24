<template>
  <div class="text-center">
    <h1>Добро пожаловать в диспетчерскую систему автобусного парка! 🚍</h1>

    <!-- Сообщение о необходимости авторизации, если пользователь не авторизован -->
    <div v-if="!isAuthenticated" class="alert alert-warning mt-4">
      <p>Пожалуйста, авторизуйтесь, чтобы получить доступ ко всем функциям системы.</p>
      <button class="btn btn-primary" @click="goToLogin">Войти</button>
    </div>
  </div>
</template>

<script>
export default {
  computed: {
    // Проверяем, есть ли токен в localStorage
    isAuthenticated() {
      return localStorage.getItem('authToken') !== null;
    }
  },
  methods: {
    goToLogin() {
      this.$router.push('/login'); // Перенаправление на страницу входа
    }
  }
};
</script>

<style scoped>

</style>
