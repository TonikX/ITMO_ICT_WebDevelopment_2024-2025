<script setup>
import { ref } from "vue";
import instance from "@/AxiosInstance.js";
import router from "@/router/index.js";

const form = ref({
  email: "",
  username: "",
  password: "",
  re_password: "",
});

function register() {
  if (!form.value.email) {
    alert("Поле email обязательно для заполнения.");
    return;
  }

  if (!/\S+@\S+\.\S+/.test(form.value.email)) {
    alert("Введите корректный email.");
    return;
  }

  if (form.value.password !== form.value.re_password) {
    alert("Пароли не совпадают");
    return;
  }

  const formData = new FormData();
  formData.append("email", form.value.email);
  formData.append("username", form.value.username);
  formData.append("password", form.value.password);
  formData.append("re_password", form.value.re_password);

  instance
    .post("/auth/users/", formData)
    .then((response) => {
      if (response.status === 201) {
        alert("Регистрация успешна! Теперь вы можете войти.");
        router.push("/login");
      }
    })
    .catch((error) => {
      console.error("Ошибка регистрации:", error.response?.data || error);
      const errorData = error.response?.data;
      if (errorData) {
        if (errorData.email) {
          alert(`Ошибка в поле email: ${errorData.email.join(", ")}`);
        } else if (errorData.username) {
          alert(`Ошибка в поле имя пользователя: ${errorData.username.join(", ")}`);
        } else if (errorData.password) {
          alert(`Ошибка в поле пароль: ${errorData.password.join(", ")}`);
        } else {
          alert(`Ошибка: ${errorData.detail || "Не удалось зарегистрироваться."}`);
        }
      } else {
        alert("Ошибка: Не удалось зарегистрироваться.");
      }
    });
}
</script>

<template>
  <div class="d-flex justify-content-center align-items-center vh-100">
    <div class="card registration-container shadow-sm">
      <div class="logo text-center mb-4">
        <img src="../pictures/logo.jpg" alt="Fitness Platform Logo" class="img-fluid" width="150" />
      </div>
      <h2 class="text-center text-primary">Регистрация</h2>

      <form @submit.prevent="register">
        <div class="mb-3">
          <label for="email" class="form-label">Email</label>
          <input
            type="email"
            class="form-control"
            id="email"
            placeholder="Введите email"
            v-model="form.email"
            required
          />
        </div>

        <div class="mb-3">
          <label for="username" class="form-label">Полное имя</label>
          <input
            type="text"
            class="form-control"
            id="username"
            placeholder="Введите полное имя"
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

        <div class="mb-3">
          <label for="re_password" class="form-label">Подтверждение пароля</label>
          <input
            type="password"
            class="form-control"
            id="re_password"
            placeholder="Повторите пароль"
            v-model="form.re_password"
            required
          />
        </div>

        <button type="submit" class="btn btn-primary w-100">Зарегистрироваться</button>
      </form>

      <div class="text-center mt-3">
        <a href="/login" class="text-decoration-none">Уже есть аккаунт? Войти</a>
      </div>
    </div>
  </div>
</template>

<style scoped>
.registration-container {
  width: 100%;
  max-width: 400px;
  padding: 20px;
  background-color: var(--container-background);
  border-radius: 15px;
}

.logo img {
  width: 150px;
}

body {
  background-color: var(--background-color);
  color: var(--text-color);
}

:root {
  --background-color: #fbeaff;
  --text-color: #333;
  --container-background: #fff;
  --button-background: #ff85c0;
  --button-border: #ff85c0;
  --link-color: #ff2d55;
}

.btn-primary {
  background-color: var(--button-background);
  border-color: var(--button-border);
  color: var(--text-color);
}

a {
  color: var(--link-color);
}

a:hover {
  text-decoration: underline;
}
</style>
