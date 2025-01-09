<script setup>
import { ref } from "vue";
import instance from "@/api/instance";

const formData = ref({
  username: "",
  email: "",
  password: "",
  confirmPassword: "",
});

function toggleTheme() {
  const body = document.body;
  body.dataset.theme = body.dataset.theme === "dark" ? "" : "dark";
}

const message = ref(null);
const messageType = ref("");

async function handleRegistration() {
  message.value = null;
  messageType.value = "";

  if (formData.value.password !== formData.value.confirmPassword) {
    message.value = "Пароли не совпадают!";
    messageType.value = "alert alert-danger";
    return;
  }

  try {
    await instance.post("/auth/users/", {
      username: formData.value.username,
      email: formData.value.email,
      password: formData.value.password,
    });

    message.value = "Успешная регистрация! Вы можете войти в систему.";
    messageType.value = "alert alert-success";

    formData.value = {
      username: "",
      email: "",
      password: "",
      confirmPassword: "",
    };
  } catch (error) {
    message.value = error.response?.data?.detail || "Ошибка регистрации!";
    messageType.value = "alert alert-danger";
  }
}
</script>

<template>
  <main class="registration-container" role="main">
    <h2 class="text-center">Регистрация</h2>
    <form @submit.prevent="handleRegistration" aria-label="Форма регистрации">
      <div class="theme-switcher">
        <label for="themeToggle" class="form-check-label">Тема</label>
        <input
          type="checkbox"
          id="themeToggle"
          class="form-check-input"
          @change="toggleTheme"
        />
      </div>

      <div class="mb-3">
        <label for="username" class="form-label">Имя пользователя</label>
        <input
          v-model="formData.username"
          type="text"
          class="form-control"
          id="username"
          placeholder="Введите имя пользователя"
          required
        />
      </div>

      <div class="mb-3">
        <label for="email" class="form-label">Электронная почта</label>
        <input
          v-model="formData.email"
          type="email"
          class="form-control"
          id="email"
          placeholder="Введите email"
          required
        />
      </div>

      <div class="mb-3">
        <label for="password" class="form-label">Пароль</label>
        <input
          v-model="formData.password"
          type="password"
          class="form-control"
          id="password"
          placeholder="Введите пароль"
          required
        />
      </div>

      <div class="mb-3">
        <label for="confirmPassword" class="form-label">Подтвердите пароль</label>
        <input
          v-model="formData.confirmPassword"
          type="password"
          class="form-control"
          id="confirmPassword"
          placeholder="Подтвердите пароль"
          required
        />
      </div>

      <button type="submit" class="btn btn-primary register-btn">
        Зарегистрироваться
      </button>
    </form>

    <div v-if="message" :class="messageType" class="mt-3">
      {{ message }}
    </div>

    <div class="already-registered">
      <p>
        Уже зарегистрированы?
        <router-link to="/auth/token/login">Войти</router-link>
      </p>
    </div>
  </main>
</template>

<style>

.text-center{
    color: var(--text-center-color);
    font-size: 24px;
    font-weight: bold;
}

body {
    font-family: Quicksand, sans-serif;
    background-color: var(--bg-color);
    color: var(--text-color);
    transition: background-color 0.3s, color 0.3s;
}

.registration-container {
    max-width: 500px;
    margin: 50px auto;
    padding: 30px;
    background-color: var(--form-bg-color);
    border-radius: 15px;
    box-shadow: 0 0 10px var(--form-border-color);
}

.form-label {
    color: var(--text-color);
}

.form-control:focus {
    border-color: var(--highlight-color);
    color: var(--text-color);
    box-shadow: 0 0 5px var(--highlight-color);
    outline: none;
}

.register-btn {
    background-color: var(--btn-bg-color);
    color: #fff;
    border: none;
    border-radius: 10px;
    width: 100%;
    padding: 10px;
    font-weight: bold;
    font-size: 18px;
    transition: background-color 0.3s;
}

.register-btn:hover {
    background-color: var(--btn-hover-color);
}

.register-btn:focus {
    background-color: var(--btn-hover-color);
}

.already-registered{
    margin-top: 10px;
}

.already-registered a {
    color: var(--link-color);
    text-decoration: none;
}

.already-registered a:hover {
    text-decoration: underline;
}
</style>
