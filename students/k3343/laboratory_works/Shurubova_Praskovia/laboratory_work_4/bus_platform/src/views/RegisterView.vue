<template>
  <div class="register-container">

    <h1>Регистрация</h1>

    <form @submit.prevent="handleRegister" class="register-form">
      <div class="form-group">
        <label for="username">Имя пользователя:</label>
        <input id="username" type="text" v-model="username" placeholder="Введите имя пользователя" required />
      </div>

      <div class="form-group">
        <label for="email">Email:</label>
        <input id="email" type="email" v-model="email" placeholder="Введите email" required />
      </div>

      <div class="form-group">
        <label for="password">Пароль:</label>
        <input id="password" type="password" v-model="password" placeholder="Введите пароль" required />
      </div>

      <button type="submit" class="btn-register">Зарегистрироваться</button>
    </form>

    <p class="login-link">
      Уже зарегистрированы? <router-link to="/login">Войти</router-link>
    </p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      username: "",
      email: "",
      password: "",
    };
  },
  methods: {
    async handleRegister() {
      const newUser = {
        username: this.username,
        email: this.email,
        password: this.password,
      };

      try {
        const response = await axios.post("http://127.0.0.1:8000/auth/users/", newUser);
        alert("Регистрация прошла успешно! Теперь вы можете войти.");
        this.$router.push("/login");
      } catch (error) {
        console.error("Ошибка при регистрации:", error);
        alert("Произошла ошибка при регистрации. Попробуйте снова.");
      }
    },
  },
};
</script>

<style scoped>

.register-container {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  min-height: 100vh;
  background-color: #f4f7fa;
  padding: 20px;
  box-sizing: border-box;
}

h1 {
  font-size: 2rem;
  color: #2c3643;
  margin-bottom: 20px;
}


.register-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
  width: 100%;
  max-width: 400px;
  background-color: #fff;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.form-group {
  display: flex;
  flex-direction: column;
  text-align: left;
}

label {
  font-size: 1rem;
  color: #2c3643;
  margin-bottom: 8px;
}

input {
  padding: 10px;
  font-size: 1rem;
  border-radius: 6px;
  border: 1px solid #ccc;
  width: 100%;
}

input:focus {
  border-color: #2c3643;
  outline: none;
  box-shadow: 0 0 5px rgba(44, 54, 67, 0.5);
}

.btn-register {
  padding: 10px 15px;
  font-size: 1rem;
  color: #fff;
  background-color: #2c3643;
  border: none;
  border-radius: 6px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.btn-register:hover {
  background-color: #1d2a35;
}

.login-link {
  margin-top: 15px;
  font-size: 1rem;
  color: #2c3643;
}

.login-link router-link {
  font-weight: bold;
  color: #2c3643;
  text-decoration: none;
  transition: color 0.3s ease;
}

.login-link router-link:hover {
  color: #1d2a35;
}
</style>
