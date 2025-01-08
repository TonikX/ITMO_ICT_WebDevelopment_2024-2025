<template>
  <header class="header">
      <h1 class="header-title">Autoservice</h1>
    </header>
  <div v-if="user">
    <h1>Профиль пользователя</h1>
    <p><strong>Имя пользователя:</strong> {{ user.username }}</p>
    <p><strong>Email:</strong> {{ user.email }}</p>
    <!-- Добавьте дополнительные поля здесь -->
  </div>
  <div v-else>
    <p>Загрузка информации...</p>
  </div>
</template>

<script>
import axios from '@/services/axios';

export default {
  data() {
    return {
      user: null,
    };
  },
  async created() {
    try {
      const response = await axios.get('/user-info/', {
        headers: {
          Authorization: `Bearer ${localStorage.getItem('access_token')}`, // Укажите токен доступа
        },
      });
      this.user = response.data;
    } catch (error) {
      console.error('Ошибка при загрузке данных пользователя:', error);
    }
  },
};
</script>


<style>
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
  background-color: #f2f2f2;
}

/* Header Styles */
.header {
  background-color: darkslategray;
  color: white;
  padding: 20px;
  text-align: center;
}

.header-title {
  margin: 0;
  font-size: 24px;
}


</style>