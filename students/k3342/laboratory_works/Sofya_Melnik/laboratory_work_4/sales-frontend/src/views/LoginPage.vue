<template>
  <div class="login-container">
    <div class="login-box">
      <h2 class="login-title">Вход</h2>
      <form @submit.prevent="login">
        <div class="input-group">
          <input v-model="username" class="input" placeholder="Логин" required />
        </div>
        <div class="input-group">
          <input
            v-model="password"
            class="input"
            type="password"
            placeholder="Пароль"
            required
          />
        </div>
        <button type="submit" class="login-button">Войти</button>
      </form>
    </div>
  </div>
</template>

<script>
import api from "@/api";

export default {
  data() {
    return { username: "", password: "" };
  },
  methods: {
    async login() {
      try {
        const { data } = await api.post("auth/jwt/create/", {
          username: this.username,
          password: this.password,
        });

        localStorage.setItem("token", data.access);
        localStorage.setItem("refreshToken", data.refresh);

        api.defaults.headers.common["Authorization"] = `Bearer ${data.access}`;

        const userResponse = await api.get("auth/users/me/");
        localStorage.setItem("user", JSON.stringify(userResponse.data));

        if (userResponse.data.is_staff) {
          this.$router.push("/admin");
        } else {
          this.$router.push("/");
        }

      } catch (error) {
        alert("Ошибка входа: " + JSON.stringify(error.response.data));
      }
    },
  },
};
</script>


<style scoped>
/* Основной контейнер для страницы логина */
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f7f7f7;
}

/* Окно формы логина */
.login-box {
  width: 350px;
  padding: 30px;
  background-color: #ffffff;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

/* Заголовок */
.login-title {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
  color: #333333;
}

/* Группа для поля ввода */
.input-group {
  margin-bottom: 15px;
}

/* Стиль для всех полей ввода */
.input {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  border-radius: 5px;
  border: 1px solid #ccc;
  box-sizing: border-box;
}

/* Фокус на поле ввода */
.input:focus {
  border-color: #007bff;
  outline: none;
}

/* Кнопка входа */
.login-button {
  width: 100%;
  padding: 10px;
  font-size: 16px;
  background-color: #007bff;
  color: #ffffff;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

/* Кнопка при наведении */
.login-button:hover {
  background-color: #0056b3;
}

/* Добавим небольшой отступ для кнопки */
button[type="submit"] {
  margin-top: 10px;
}
</style>
