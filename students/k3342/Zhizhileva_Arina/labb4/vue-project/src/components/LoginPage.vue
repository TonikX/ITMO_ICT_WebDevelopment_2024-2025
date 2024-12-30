<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" sm="6" md="4">
        <v-card>
          <v-card-title class="headline">Вход</v-card-title>
          <v-card-text>
            <!-- Поле для username -->
            <v-text-field v-model="username" label="Username" required></v-text-field>
            <!-- Поле для пароля -->
            <v-text-field v-model="password" label="Пароль" type="password" required></v-text-field>
            <!-- Кнопка для входа -->
            <v-btn @click="loginUser" color="primary" block>Войти</v-btn>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',  // Поле для username
      password: ''   // Поле для пароля
    };
  },
  methods: {
    async loginUser() {
      try {
        // Отправка запроса на сервер с username и password
        const response = await axios.post('http://localhost:8000/api/login/', {
          username: this.username,  // Используем username
          password: this.password   // Используем пароль
        });

        // Сохранение токена в localStorage
        localStorage.setItem('access_token', response.data.access);

        // Перенаправление на страницу сервиса после успешного логина
        this.$router.push('/main');
      } catch (error) {
        // Обработка ошибки при входе
        if (error.response) {
          console.error('Ошибка при входе:', error.response.data);
          alert('Неверный логин или пароль');
        } else {
          console.error('Ошибка сети или сервера:', error);
          alert('Ошибка подключения. Пожалуйста, попробуйте позже.');
        }
      }
    }
  }
};
</script>
