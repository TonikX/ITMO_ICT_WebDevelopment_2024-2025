<template>
  <div class="login-container">
    <div class="login-card">
      <h3 class="login-title">Вход в аккаунт</h3>
      <form @submit.prevent="login" class="login-form">
        <input
            type="text"
            v-model="username"
            id="username"
            class="login-input"
            placeholder="Имя пользователя"
        />

        <input
            type="password"
            v-model="password"
            id="password"
            class="login-input"
            placeholder="Пароль"
        />

        <button type="submit" class="login-button">Войти</button>
      </form>
      <button class="auth-link" @click="goToRegister">Регистрация</button>
    </div>
  </div>
</template>
<script>
import auth from '../store/auth';

export default {
  data() {
    return {
      username: '',
      password: '',
    };
  },
  methods: {
    async login() {
      try {
        const response = await fetch('http://127.0.0.1:8000/api/token/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            username: this.username,
            password: this.password,
          }),
        });

        if (!response.ok) throw new Error('Invalid credentials');
        const data = await response.json();
        auth.login(data.access);
        this.$router.push('/');
      } catch (error) {
        alert(error.message);
      }
    },
    goToRegister() {
      this.$router.push('/register');
    }
  },
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f5f5f5;
}

.login-card {
  background: #ffffff;
  padding: 2%;
  border-radius: 10px;
  width: 100%;
  max-width: 400px;
}

.login-title {
  font-weight: bold;
  color: #596dff;
  margin-bottom: 5%;
  text-align: center;
}

.login-form {
  display: flex;
  flex-direction: column;
}

.login-input {
  padding: 10px;
  border: 1px solid #cccccc;
  border-radius: 10px;
  margin-bottom: 1rem;
}

.login-input:focus {
  border-color: #596dff;
  outline: none;
}

.login-button {
  padding: 10px;
  color: white;
  background-color: #ffa44b;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  text-align: center;
}

.login-button:hover {
  background-color: #c5813b;
}

.auth-link {
  margin-top: 20%;
  padding: 10px;
  color: white;
  background-color: #596dff;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  text-align: center;
  width: 100%;
}

.auth-link:hover {
  background-color: #4150c7;
}
</style>
