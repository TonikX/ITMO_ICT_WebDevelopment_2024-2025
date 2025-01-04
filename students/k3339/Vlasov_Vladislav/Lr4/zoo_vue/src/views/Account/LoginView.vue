<template>
    <div class="login-container">
      <h2>Вход</h2>
      <form @submit.prevent="login"  class="login-form">
        <input v-model="username" placeholder="Имя пользователя" required />
        <input v-model="password" type="password" placeholder="Пароль" required />
        <button type="submit">Войти</button>
      </form>
      <p>Нет аккаунта? <RouterLink to="/register">Регистрация</RouterLink></p>
    </div>
</template>
  
<script setup>
    import { RouterLink, useRouter } from 'vue-router';
    import axios from 'axios';
    import { ref } from 'vue';

    const username = ref("")
    const password = ref("")
    const router = useRouter();

    async function login() {
      try {
        const response = await axios.post('http://localhost:8000/account/login/', {
          username: username.value,
          password: password.value,
        });
        localStorage.setItem('access_token', response.data.access);
        localStorage.setItem('username', username.value);
        router.push('/');
      } catch (error) {
        console.error(error);
        alert('Ошибка входа');
      }
    }
</script>

<style scoped>
.login-container {
    max-width: 400px;
    margin: 0 auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 8px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.login-form {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.login-form input,
.login-form button {
    padding: 10px;
    font-size: 16px;
}

.login-form button {
    cursor: pointer;
    background-color: #007BFF;
    color: white;
    border: none;
    border-radius: 4px;
}
</style>