<script setup>
import { ref } from "vue";
import instance from "@/AxiosInstance.js";
import router from "@/router/index.js";
import { TokenStore } from "@/stores/TokenStore.js";

const Token = TokenStore();

const form = ref({
  username: "",
  password: "",
});

function login() {
  instance
    .post("/auth/token/login", form.value)
    .then((response) => {
      if (response.status === 200) {
        Token.setToken(response.data.auth_token);
        console.log("Токен после авторизации:", Token.token);

        // Очищаем данные предыдущего пользователя
        localStorage.removeItem("user_id");
        localStorage.removeItem("username");

        // Переходим в личный кабинет
        router.push("/acc").then(() => {
          console.log("Переход на личный кабинет завершен.");
        });
      }
    })
    .catch((error) => console.error("Ошибка авторизации:", error));
}
</script>

<template>
  <div class="d-flex justify-content-center align-items-center vh-100">
    <div class="card login-container shadow-sm">
      <div class="logo">
        <img src="../pictures/logo.jpg" alt="Platform Logo" />
        <h2 class="text-primary">Вход</h2>
      </div>

      <!-- Форма логина -->
      <form @submit.prevent="login">
        <div class="mb-3">
          <label for="username" class="form-label">Логин</label>
          <input
            type="text"
            class="form-control"
            id="username"
            placeholder="Введите логин"
            v-model="form.username"
            required
          />
        </div>
        <div class="mb-3">
          <label for="password" class="form-label">Пароль</label>
          <input
            type="password"
            class="form-control"
            id="password"
            placeholder="Введите пароль"
            v-model="form.password"
            required
          />
        </div>
        <button type="submit" class="btn btn-primary w-100">Войти</button>
      </form>

      <!-- Ссылки для восстановления и регистрации -->
      <div class="text-center mt-3">
        <a href="#" class="text-decoration-none">Забыли пароль?</a>
      </div>
      <div class="text-center mt-2">
        <a href="/register" class="text-decoration-none">Еще нет аккаунта? Регистрация</a>
      </div>
    </div>

    <!-- Переключатель темы -->
    <div class="theme-switcher" @click="toggleTheme">
      <i class="bi bi-brightness-high"></i>
    </div>
  </div>
</template>

<style scoped>
:root {
    --background-color: #fbeaff;
    --text-color: #333;
    --container-background: #fff;
    --input-background: #f3e5f5;
    --button-background: #ff85c0;
    --button-border: #ff85c0;
    --link-color: #ff2d55;
}

.blue-theme {
    --background-color: #e0f7fa;
    --text-color: #333;
    --container-background: #ffffff;
    --input-background: #b2ebf2;
    --button-background: #00acc1;
    --button-border: #00acc1;
    --link-color: #00796b;
}

body {
    display: flex;
    justify-content: center;
    align-items: center;
    height: 100vh;
    background-color: var(--background-color);
    color: var(--text-color);
    margin: 0;
    position: relative;
}

.login-container {
    width: 100%;
    max-width: 400px;
    padding: 20px;
    background: var(--container-background);
    border-radius: 15px;
}

.logo {
    text-align: center;
    margin-bottom: 20px;
}

.logo img {
    width: 150px;
}

.form-control {
    background-color: var(--input-background);
    color: var(--text-color);
    border-radius: 10px;
}

.btn-primary {
    background-color: var(--button-background);
    border-color: var(--button-border);
    color: var(--text-color);
}

a {
    color: var(--link-color);
    text-decoration: none;
}

a:hover {
    text-decoration: underline;
}

.theme-switcher i {
    font-size: 2rem;
    color: #000;
    transition: color 0.3s ease;
}

.theme-switcher {
    position: fixed;
    top: 10px;
    left: 10px;
    z-index: 1000;
    cursor: pointer;
}

.theme-switcher:hover i {
    color: #00796b;
}
</style>
