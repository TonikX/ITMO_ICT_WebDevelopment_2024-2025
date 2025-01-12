<template>
  <div class="auth-container">
    <div class="auth-card">
      <h2 class="auth-title">Вход</h2>
      <form @submit.prevent="handleSubmit">
        <!-- Поле Username -->
        <div class="input-group">
          <label for="username">Логин</label>
          <input
              type="text"
              id="username"
              v-model="username"
              placeholder="Введите ваш логин"
              required
          />
        </div>

        <!-- Поле Password -->
        <div class="input-group">
          <label for="password">Пароль</label>
          <input
              type="password"
              id="password"
              v-model="password"
              placeholder="Введите пароль"
              required
          />
        </div>

        <!-- Кнопка отправки -->
        <button type="submit" class="submit-btn">Войти</button>

        <!-- Сообщение об ошибке -->
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
      </form>

      <p class="footer-text">
        Еще нет аккаунта? <a href="/signup">Зарегистрируйтесь</a>
      </p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      username: "", // Используем поле для username
      password: "",
      errorMessage: null,
    };
  },
  methods: {
    async handleSubmit() {
      // Данные для отправки на сервер
      const data = {
        username: this.username, // Используем поле username
        password: this.password,
      };

      try {
        // Отправляем запрос на вход пользователя с использованием username и password
        const response = await axios.post("/api/auth/token/login/", data);

        // Если запрос успешен, сохраняем токен и перенаправляем на страницу
        if (response.status === 200) {
          // Сохраняем токен в localStorage
          localStorage.setItem("auth_token", response.data.auth_token);
          // Перенаправляем на страницу dashboard (или другую страницу)
          this.$router.push("/dashboard");
        }
      } catch (error) {
        // Обработка ошибок
        if (error.response && error.response.data) {
          this.errorMessage = error.response.data.detail || "Ошибка входа";
        } else {
          this.errorMessage = "Ошибка сервера. Повторите попытку позже.";
        }
      }
    },
  },
};
</script>

<style scoped>
/* Основные стили, такие же, как у вас */
.auth-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 100vh;
  background-color: #f4f6fc;
}

.auth-card {
  background-color: white;
  padding: 30px;
  border-radius: 8px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

.auth-title {
  text-align: center;
  font-size: 24px;
  color: #333;
  margin-bottom: 20px;
}

/* Стили для полей ввода */
.input-group {
  margin-bottom: 15px;
}

.input-group label {
  display: block;
  font-size: 14px;
  color: #555;
  margin-bottom: 8px;
}

.input-group input {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-sizing: border-box;
}

.input-group input:focus {
  border-color: #5b9af6;
  outline: none;
}

.submit-btn {
  width: 100%;
  padding: 12px;
  background-color: #4caf50;
  color: white;
  font-size: 16px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

.submit-btn:hover {
  background-color: #45a049;
}

.footer-text {
  text-align: center;
  margin-top: 20px;
  font-size: 14px;
  color: #555;
}

.footer-text a {
  color: #4caf50;
  text-decoration: none;
}

.footer-text a:hover {
  text-decoration: underline;
}

.error-message {
  color: red;
  font-size: 14px;
  text-align: center;
  margin-top: 15px;
}
</style>
