<template>
  <div class="auth-container">
    <h2>Вход</h2>
    <form @submit.prevent="login">
      <div class="form-group">
        <label for="username" class="form-label">Имя пользователя:</label>
        <input
          type="text"
          id="username"
          class="form-control"
          v-model="username"
          required
        />
      </div>
      <div class="form-group">
        <label for="password" class="form-label">Пароль:</label>
        <input
          type="password"
          id="password"
          class="form-control"
          v-model="password"
          required
        />
      </div>
      <div class="form-actions">
        <button type="submit" class="btn btn-primary" :disabled="loading">
          Войти
        </button>
      </div>
      <div v-if="error" class="error-message">{{ error }}</div>
    </form>
    <p class="text-center">
      Нет аккаунта?
      <router-link to="/register" class="link">Зарегистрироваться</router-link>
    </p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      username: '',
      password: '',
      loading: false,
      error: null,
    };
  },
  methods: {
    async login() {
      this.loading = true;
      this.error = null;
      try {
        const response = await axios.post(
          'http://127.0.0.1:8000/auth/token/login',
          {
            username: this.username,
            password: this.password,
          }
        );
        const token = response.data.auth_token;
        localStorage.setItem('auth_token', token); // Сохранение токена
        this.$router.push('/reports'); // Редирект после успешного входа
      } catch (err) {
        if (err.response && err.response.data) {
          this.error = err.response.data.non_field_errors
            ? err.response.data.non_field_errors[0]
            : 'Ошибка при входе. Проверьте данные.';
        } else {
          this.error = 'Не удалось подключиться к серверу. Попробуйте позже.';
        }
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
.auth-container {
  max-width: 400px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background-color: #f9f9f9;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.auth-container h2 {
  text-align: center;
  margin-bottom: 20px;
  color: #085d88;
  font-family: Arial, sans-serif;
}

.form-group {
  margin-bottom: 15px;
}

.form-label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #333;
}

.form-control {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
}

.form-control:focus {
  outline: none;
  border-color: #085d88;
  box-shadow: 0 0 5px rgba(8, 93, 136, 0.5);
}

.btn {
  width: 100%;
  padding: 10px;
  background-color: #04b922;
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s ease-in-out;
}

.btn:disabled {
  background-color: #aaa;
  cursor: not-allowed;
}

.btn:hover {
  background-color: #01720a;
}

.error-message {
  color: #dc3545;
  text-align: center;
  margin-top: 10px;
}

.text-center {
  text-align: center;
  margin-top: 15px;
}

.link {
  color: #085d88;
  text-decoration: none;
}

.link:hover {
  text-decoration: underline;
}
</style>
