<template>
  <div class="auth-container">
    <h2>Регистрация</h2>
    <form @submit.prevent="register">
      <div class="form-group">
        <label for="email" class="form-label">Email:</label>
        <input
          type="email"
          id="email"
          class="form-control"
          v-model="email"
          required
        />
      </div>
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
          Зарегистрироваться
        </button>
      </div>
      <div v-if="error" class="error-message">{{ error }}</div>
    </form>
    <p class="text-center">
      Уже есть аккаунт? <router-link to="/login" class="link">Войти</router-link>
    </p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      email: '',
      username: '',
      password: '',
      loading: false,
      error: null,
    };
  },
  methods: {
    async register() {
      this.loading = true;
      this.error = null;
      try {
        await axios.post('http://127.0.0.1:8000/auth/users/', {
          email: this.email,
          username: this.username,
          password: this.password,
        });
        this.$router.push('/login');
      } catch (err) {
        if (err.response && err.response.data) {
          this.error = Object.values(err.response.data).flat().join(' ');
        } else {
          this.error = 'Ошибка регистрации. Попробуйте снова.';
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
