<template>
  <div class="login-form">
    <h2>Вход</h2>
    <form @submit.prevent="login">
      <div>
        <label for="username">Логин:</label>
        <input type="text" id="username" v-model="username" required />
      </div>
      <div>
        <label for="password">Пароль:</label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <button type="submit">Войти</button>
    </form>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      username: "",
      password: "",
      errorMessage: "",
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post("http://127.0.0.1:8000/auth/token/login/", {
          username: this.username,
          password: this.password,
        });
        localStorage.setItem("auth_token", response.data.auth_token);
        this.$router.push("/dashboard"); // Переход на страницу после авторизации
      } catch (error) {
        this.errorMessage = "Неверное имя пользователя или пароль";
      }
    },
  },
};
</script>

<style>
/* Простые стили */
.error {
  color: red;
}
</style>
