<template>
  <div class="login-container">
    <h1>Добро Пожаловать!</h1>
    <p>Мы рады видеть вас снова!</p>
    <form class="login-form" @submit.prevent="handleLogin">
      <input type="email" v-model="email" placeholder="Email" required />
      <input type="password" v-model="password" placeholder="Пароль" required />
      <button type="submit" :disabled="authStore.loading">Войти</button>
    </form>
    <p v-if="authStore.error" class="error">{{ authStore.error }}</p>
    <router-link to="/register" class="switch-page-btn">Еще не зарегистрированы?</router-link>
  </div>
</template>
<script>
import {ref} from 'vue';
import {useAuthStore} from '@/stores/auth.js';
import {useRouter} from 'vue-router';

export default {
  setup() {
    const email = ref('');
    const password = ref('');
    const authStore = useAuthStore();
    const router = useRouter();

    const handleLogin = async () => {
      const success = await authStore.login({email: email.value, password: password.value});
      if (success) {
        router.push('/');
      }
    };

    return {email, password, authStore, handleLogin};
  },
};
</script>
<style>
.login-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  background-color: #F5F5DC;
  font-family: 'Pacifico', cursive;
  padding: 20px;
  box-sizing: border-box;
  text-align: center;
}

.login-container h1 {
  font-size: 36px;
  color: #800020;
}

.login-container p {
  margin: 10px 0;
  font-size: 18px;
  color: #333;
}

.login-form {
  background-color: #FFF8DC;
  padding: 30px;
  border: 2px solid #800020;
  border-radius: 10px;
  width: 100%;
  max-width: 400px;
  display: flex;
  flex-direction: column;
  align-items: center;
}

.login-form input {
  width: 100%;
  padding: 12px 15px;
  margin-bottom: 15px;
  border: 2px solid #CCC;
  border-radius: 25px;
  font-family: 'Great Vibes', cursive;
  font-size: 16px;
  transition: border 0.3s, box-shadow 0.3s;
}

.login-form input:focus {
  border-color: #800020;
  box-shadow: 0 0 8px rgba(128, 0, 32, 0.5);
  outline: none;
}

.login-form button {
  background-color: #FFAA33;
  color: #fff;
  padding: 10px 25px;
  border: none;
  border-radius: 25px;
  font-size: 18px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.3s;
  width: 100%;
}

.login-form button:hover:not(:disabled) {
  background-color: #800020;
  transform: scale(1.05);
}

.error {
  color: #D32F2F;
  margin-top: 10px;
}

.switch-page-btn {
  margin-top: 20px;
  display: inline-block;
  color: #0066cc;
  font-size: 16px;
  text-decoration: none;
  transition: color 0.3s;
}

.switch-page-btn:hover {
  color: #800020;
}
</style>