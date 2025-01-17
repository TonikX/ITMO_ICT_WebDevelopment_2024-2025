<template>
  <div>
    <h2 v-if="isLoginMode">Вход</h2>
    <h2 v-else>Регистрация</h2>

    <form @submit.prevent="handleSubmit">
      <!-- Имя пользователя -->
      <div>
        <label for="username">Имя пользователя:</label>
        <input v-model="username" id="username" type="text" placeholder="Введите имя пользователя" required />
      </div>

      <!-- Email для регистрации -->
      <div v-if="!isLoginMode">
        <label for="email">Email:</label>
        <input v-model="email" id="email" type="email" placeholder="Введите email" required />
      </div>

      <!-- Пароль -->
      <div>
        <label for="password">Пароль:</label>
        <input v-model="password" id="password" type="password" placeholder="Введите пароль" required />
      </div>

      <!-- Кнопка отправки -->
      <button type="submit">
        {{ isLoginMode ? "Войти" : "Зарегистрироваться" }}
      </button>
    </form>

    <!-- Сообщение об ошибке -->
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>

    <!-- Переключение между режимами -->
    <p>
      {{ isLoginMode ? "Нет аккаунта?" : "Уже есть аккаунт?" }}
      <a @click="toggleMode">
        {{ isLoginMode ? "Зарегистрируйтесь!" : "Войдите!" }}
      </a>
    </p>
  </div>
</template>

<script>
import { loginUser, registerUser } from "../api/api";

export default {
  data() {
    return {
      isLoginMode: true, // Управление режимом (вход или регистрация)
      username: "",
      email: "",
      password: "",
      errorMessage: "",
    };
  },
  methods: {
    async handleSubmit() {
      if (this.isLoginMode) {
        await this.login();
      } else {
        await this.register();
      }
    },
    async login() {
      try {
        const response = await loginUser({
          username: this.username,
          password: this.password,
        });
        localStorage.setItem("token", response.data.auth_token); // Сохранение токена

        // Получение данных о пользователе
        const userResponse = await this.$axios.get("/auth/users/me/", {
          headers: { Authorization: `Token ${localStorage.getItem("token")}` }
        });

        // Сохраняем роль пользователя
        const role = userResponse.data.role;
        localStorage.setItem("role", role);

        // Переход на главную страницу
        this.$router.push("/");

      } catch (error) {
        this.errorMessage = "Ошибка входа: " + (error.response?.data?.detail || "Неизвестная ошибка");
        console.error("Ошибка входа:", error);
      }
    },
    async register() {
      try {
        await registerUser({
          username: this.username,
          email: this.email,
          password: this.password,
        });
        this.errorMessage = "";
        this.isLoginMode = true;
      } catch (error) {
        const errors = error.response?.data || {};
        this.errorMessage = Object.keys(errors)
          .map((key) => `${key}: ${errors[key].join(", ")}`)
          .join(". ");
        console.error("Ошибка регистрации:", error);
      }
    },
    toggleMode() {
      this.isLoginMode = !this.isLoginMode;
      this.errorMessage = "";
    },
  },
};
</script>

<style scoped>
.error {
  color: red;
  font-size: 14px;
  margin-top: 10px;
}

button {
  padding: 10px 15px;
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}

a {
  color: #4CAF50;
  cursor: pointer;
  text-decoration: underline;
}

form {
  max-width: 400px;
  margin: 0 auto;
  display: flex;
  flex-direction: column;
  gap: 10px;
}
</style>
