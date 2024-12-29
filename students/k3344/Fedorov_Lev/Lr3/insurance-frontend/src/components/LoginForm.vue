<template>
  <div class="login-form">
    <div class="login-card">
      <h1>Вход</h1>
      <form @submit.prevent="login">
        <div class="input-group">
          <input
            v-model="username"
            type="text"
            placeholder="Имя пользователя"
            required
          />
        </div>

        <div class="input-group">
          <input
              v-model="password"
              type="password"
              placeholder="Пароль"
              required
          />
        </div>

        <button type="submit" :disabled="loading">
          {{ loading ? "Загрузка..." : "Войти" }}
        </button>
      </form>

      <p class="forgot-password" @click="resetPassword">
        Забыли пароль?
      </p>

      <div class="error-message" v-if="error">
        {{ error }}
      </div>
    </div>
  </div>
</template>

<script>
import AuthService from "@/services/AuthService";

export default {
  data() {
    return {
      username: "",
      password: "",
      loading: false,
      error: null,
    };
  },
  methods: {
    async login() {
      this.loading = true;
      this.error = null;
      try {
        const response = await AuthService.login(
            this.username,
            this.password
        );

        console.log("Токены:", response);

        if (response.access) {
          localStorage.setItem("token", response.access);
          localStorage.setItem("refreshToken", response.refresh);
          this.$router.push("/dashboard");
        } else {
          this.error = "Ошибка: Токен не получен.";
        }
      } catch (error) {
        console.error(
            "Ошибка входа:",
            error.response ? error.response.data : error
        );
        this.error = "Ошибка входа. Проверьте логин или пароль.";
      } finally {
        this.loading = false;
      }
    },
    resetPassword() {
      alert("Переход к восстановлению пароля!");
    },
  },
};
</script>

<style scoped>
.login-form {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background: linear-gradient(145deg, #2b5876, #4e4376);
}

.login-card {
  background: #ffffff;
  padding: 2rem;
  border-radius: 12px;
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
  text-align: center;
}

h1 {
  margin-bottom: 1.5rem;
  color: #333;
}

.input-group {
  margin-bottom: 1rem;
}

input {
  width: 100%;
  padding: 0.8rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  transition: border-color 0.3s;
}

input:focus {
  border-color: #4e4376;
  outline: none;
}

button {
  background-color: #4e4376;
  color: #fff;
  border: none;
  padding: 0.9rem;
  font-size: 1rem;
  border-radius: 8px;
  width: 100%;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #372c54;
}

button:disabled {
  background-color: #aaa;
  cursor: not-allowed;
}

.forgot-password {
  margin-top: 1rem;
  color: #4e4376;
  cursor: pointer;
  text-decoration: underline;
}

.error-message {
  color: red;
  margin-top: 1rem;
}
</style>
