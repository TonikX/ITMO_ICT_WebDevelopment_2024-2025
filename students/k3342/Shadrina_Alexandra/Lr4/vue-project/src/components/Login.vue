<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import instance from "@/api/instance";

const formData = ref({
  email: "",
  password: "",
});

const message = ref(null);
const messageType = ref("");

const router = useRouter();

async function handleLogin() {
  message.value = null;
  messageType.value = "";

  try {
    const response = await instance.post("/auth/token/login/", {
      username: formData.value.email,
      password: formData.value.password,
    });

    localStorage.setItem("auth_token", response.data.auth_token);

    message.value = "Успешный вход!";
    messageType.value = "alert alert-success";

    router.push("/");

  } catch (error) {
    message.value = error.response?.data?.detail || "Ошибка входа!";
    messageType.value = "alert alert-danger";
  }
}

function toggleTheme() {
  const body = document.body;
  body.dataset.theme = body.dataset.theme === "dark" ? "" : "dark";
}
</script>

<template>
  <main class="registration-container" role="main">
    <h2 class="text-center">Вход в аккаунт</h2>
    <form @submit.prevent="handleLogin" aria-label="Форма входа">
      <div class="theme-switcher">
        <label for="themeToggle" class="form-check-label">Тема</label>
        <input
          type="checkbox"
          id="themeToggle"
          class="form-check-input"
          @change="toggleTheme"
          aria-label="Переключатель темы"
        />
      </div>

      <div class="mb-3">
        <label for="email" class="form-label">Имя пользователя или e-mail</label>
        <input
          v-model="formData.email"
          type="text"
          class="form-control"
          id="email"
          placeholder="Введите email или имя пользователя"
          required
          aria-required="true"
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
          aria-required="true"
        />
      </div>

      <button type="submit" class="btn btn-primary register-btn" aria-label="Войти в аккаунт">
        Войти
      </button>
    </form>

    <div v-if="message" :class="messageType" class="mt-3">
      {{ message }}
    </div>

    <p class="already-registered">
      Нет аккаунта?
      <router-link to="/auth/users" aria-label="Зарегистрироваться">Зарегистрироваться</router-link>
    </p>
  </main>
</template>

<style scoped>

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

.already-registered {
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
