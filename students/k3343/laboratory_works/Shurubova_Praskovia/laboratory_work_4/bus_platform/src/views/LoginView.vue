<template>
  <div class="login-container">

    <h1>Вход в систему</h1>

    <form @submit.prevent="handleLogin" class="login-form">
      <div class="form-group">
        <label for="username">Имя пользователя:</label>
        <input id="username" type="text" v-model="username" placeholder="Введите имя пользователя" required />
      </div>

      <div class="form-group">
        <label for="password">Пароль:</label>
        <input id="password" type="password" v-model="password" placeholder="Введите пароль" required />
      </div>

      <button type="submit" class="btn-login">Войти</button>
    </form>

    <p class="registration-link">
      Ещё не зарегистрированы? <router-link to="/register">Регистрация</router-link>
    </p>
  </div>
</template>

<script>
import authService from '@/api/authService';


export default {
  data() {
    return {
      username: '',
      password: '',
    };
  },
  methods: {
    async handleLogin() {
      try {
        const credentials = {
          username: this.username,
          password: this.password,
        };
        await authService.login(credentials);
        this.$router.push('/drivers');
      } catch (error) {
        console.error('Ошибка при авторизации:', error);
        alert('Неправильное имя пользователя или пароль');
      }
    },
  },
};
</script>

<style scoped>

.login-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  min-height: 100vh;
  background-color: #f4f7fa; /* Светлый фон */
  padding: 20px;
  box-sizing: border-box;
}

h1 {
  font-size: 2rem;
  color: #2c3643;
  margin-bottom: 20px;
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
  width: 100%;
  max-width: 400px;
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.form-group {
  display: flex;
  flex-direction: column;
  text-align: left;
}

label {
  font-size: 1rem;
  color: #2c3643;
  margin-bottom: 8px;
}

input {
  padding: 10px;
  font-size: 1rem;
  border-radius: 6px;
  border: 1px solid #ccc;
  width: 100%;
}

input:focus {
  border-color: #2c3643;
  outline: none;
  box-shadow: 0 0 5px rgba(44, 54, 67, 0.5);
}

.btn-login {
  padding: 10px 15px;
  font-size: 1rem;
  color: #fff;
  background-color: #2c3643;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-login:hover {
  background-color: #1d2a35;
}

.registration-link {
  margin-top: 15px;
  font-size: 1rem;
  color: #2c3643;
}

.registration-link router-link {
  font-weight: bold;
  color: #2c3643;
  text-decoration: none;
  transition: color 0.3s ease;
}

.registration-link router-link:hover {
  color: #1d2a35;
}
</style>
