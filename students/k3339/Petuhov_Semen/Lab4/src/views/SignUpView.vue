<template>
  <div class="auth-container">
    <div class="auth-card">
      <h2 class="auth-title">Регистрация</h2>
      <form @submit.prevent="handleSubmit">
        <!-- Поле Email -->
        <div class="input-group">
          <label for="email">Email</label>
          <input
              type="email"
              id="email"
              v-model="email"
              placeholder="Введите ваш email"
              required
          />
        </div>

        <!-- Поле Username -->
        <div class="input-group">
          <label for="username">Username</label>
          <input
              type="text"
              id="username"
              v-model="username"
              placeholder="Введите логин"
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

        <!-- Поле Confirm Password -->
        <div class="input-group">
          <label for="confirmPassword">Подтвердите пароль</label>
          <input
              type="password"
              id="confirmPassword"
              v-model="confirmPassword"
              placeholder="Повторите пароль"
              required
          />
        </div>

        <!-- Кнопка отправки -->
        <button type="submit" class="submit-btn">Зарегистрироваться</button>

        <!-- Сообщение об ошибке -->
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
      </form>

      <p class="footer-text">
        Уже есть аккаунт? <a href="/login">Войдите</a>
      </p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      email: "",
      username: "",
      password: "",
      confirmPassword: "",
      errorMessage: null,
    };
  },
  methods: {
    async handleSubmit() {
      // Проверка совпадения паролей
      if (this.password !== this.confirmPassword) {
        this.errorMessage = "Пароли не совпадают!";
        return;
      }

      // Данные для отправки
      const data = {
        email: this.email,
        username: this.username,
        password: this.password,
      };

      try {
        // Отправляем запрос для создания нового пользователя
        const response = await axios.post("/api/auth/users/", data);

        // Если запрос успешен, перенаправляем пользователя на страницу логина
        if (response.status === 201) {
          this.$router.push("/login");
        }
      } catch (error) {
        // Обработка ошибок
        if (error.response && error.response.data) {
          const errors = error.response.data;
          this.errorMessage = errors.email || errors.username || errors.password || "Ошибка регистрации.";
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
