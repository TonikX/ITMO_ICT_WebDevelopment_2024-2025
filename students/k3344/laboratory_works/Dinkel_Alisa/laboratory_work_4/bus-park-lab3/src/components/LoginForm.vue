<template>
  <div class="login-form">
    <form @submit.prevent="handleLogin" class="form-container">
      <div class="form-group">
        <label for="username">Username:</label>
        <input type="text" id="username" v-model="username" required class="form-input" />
      </div>

      <div class="form-group">
        <label for="password">Password:</label>
        <input type="password" id="password" v-model="password" required class="form-input" />
      </div>

      <button type="submit" class="btn-submit">Войти</button>
    </form>
  </div>
</template>

<script>
import { loginUser } from '@/api/auth';

export default {
  data() {
    return {
      username: '',
      password: ''
    };
  },
  methods: {
  async handleLogin() {
    try {
      const credentials = { username: this.username, password: this.password };
      const data = await loginUser(credentials);
      console.log('Logged in successfully:', data);

      // Сохраняем токен и данные пользователя
      localStorage.setItem('authToken', data.auth_token);
      localStorage.setItem('user', JSON.stringify(data));

      // Редирект на домашнюю страницу после входа
      this.$router.push('/');
    } catch (error) {
      console.error('Login failed:', error);
    }
  }
}

};
</script>

<style scoped>
/* Стили для формы входа */
.login-form {
  padding: 2rem;
}

.form-container {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 1rem;
}

.form-input {
  width: 100%;  /* Обеспечиваем одинаковую ширину для полей */
  padding: 0.75rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.btn-submit {
  width: 100%;  /* Обеспечиваем одинаковую ширину для кнопки */
  padding: 0.75rem;
  font-size: 1rem;
  color: white;
  background-color: #5b80a8;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.btn-submit:hover {
  background-color: #99b6d6;
}
</style>
