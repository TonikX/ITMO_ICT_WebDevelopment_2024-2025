<template>
  <div class="register">
    <header class="header">
        <h1 class="header-title">Autoservice</h1>
      </header>
    <v-container class="register-container">
      <v-form @submit.prevent="registerUser">
        <v-text-field
          v-model="email"
          label="Email"
          type="email"
          required
        ></v-text-field>
        <v-text-field
          v-model="password"
          label="Password"
          type="password"
          required
        ></v-text-field>
        <v-text-field
          v-model="username"
          label="Username"
          required
        ></v-text-field>
        <v-btn type="submit" class="custom-button" >Register</v-btn>
      </v-form>
    </v-container>
    </div>
</template>

<script>
import { ref } from 'vue';
import axios from 'axios';

export default {
  name: 'RegisterPage',
  setup() {
    const email = ref('');
    const password = ref('');
    const username = ref('');

    const registerUser = async () => {
      try {
        const response = await axios.post('http://localhost:8000/api/register/', {
          email: email.value,
          password: password.value,
          username: username.value
        });
        console.log('Регистрация успешна:', response.data);
      } catch (error) {
        console.error('Ошибка регистрации:', error.response.data);
      }
    };

    return {
      email,
      password,
      username,
      registerUser
    };
  }
};
</script>

<style scoped>

.register {
  background-color: darkseagreen;
  min-height: 100vh; /* Полная высота страницы */
  padding: 0;
  margin: 0;
  display: flex;
  flex-direction: column;
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

.register-container {
  padding-top: 80px; /* Отступ сверху, чтобы не перекрывать шапкой */
  background-color: white; /* Белый цвет фона */
  padding: 20px; /* Внутренние отступы */
  border-radius: 8px; /* Скругленные углы */
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2); /* Легкая тень */
  max-width: 400px; /* Ограничение ширины контейнера */
  margin: auto; /* Центрирование по горизонтали */
}
.custom-button {
  background-color: darkslategray !important; /* Зеленый цвет кнопок */
  color: white !important;
  margin-bottom: 10px;
  text-transform: none !important; /* Отключение заглавных букв */
  font-size: 16px;
}
</style>
