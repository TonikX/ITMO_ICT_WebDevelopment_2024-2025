<template>
    <div class="registration-container">
        <h2>Регистрация</h2>
        <form @submit.prevent="register" class="registration-form">
            <input v-model="username" placeholder="Имя пользователя" required />
            <input v-model="email" type="email" placeholder="Email" required />
            <input v-model="password" type="password" placeholder="Пароль" required />
            <button type="submit">Зарегистрироваться</button>
        </form>
        <p>Есть аккаунт? <RouterLink to="/login">Авторизация</RouterLink></p>
    </div>  
</template>

<script setup>
    import axios from 'axios';
    import { ref } from 'vue';
    import { RouterLink, useRouter } from 'vue-router';

    const username = ref("")
    const email = ref("")
    const password = ref("")
    const router = useRouter();

    async function register() {
        try {
            await axios.post('http://localhost:8000/account/register/', {
            username: username.value,
            email: email.value,
            password: password.value,
        });
            login()
        } catch (error) {
            console.error(error);
            alert('Ошибка регистрации');
        }
    }

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
.registration-container {
    max-width: 400px;
    margin: 0 auto;
    padding: 20px;
    border: 1px solid #ccc;
    border-radius: 8px;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
}

.registration-form {
    display: flex;
    flex-direction: column;
    gap: 10px;
}

.registration-form input,
.registration-form button {
    padding: 10px;
    font-size: 16px;
}

.registration-form button {
    cursor: pointer;
    background-color: #007BFF;
    color: white;
    border: none;
    border-radius: 4px;
}

.registration-container p {
    margin-top: 15px;
}
</style>