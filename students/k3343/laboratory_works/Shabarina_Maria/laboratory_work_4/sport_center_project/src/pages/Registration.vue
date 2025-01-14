<template>
  <div class="register-container">
    <div class="register-card">
      <h3 class="register-title">Регистрация</h3>
      <form @submit.prevent="register" class="register-form">
        <input
            type="text"
            v-model="username"
            id="username"
            class="register-input"
            placeholder="Имя пользователя"
            required
        />

        <input
            type="email"
            v-model="email"
            id="email"
            class="register-input"
            placeholder="Email"
            required
        />

        <input
            type="password"
            v-model="password"
            id="password"
            class="register-input"
            placeholder="Пароль"
            required
        />

        <input
            type="password"
            v-model="confirmPassword"
            id="confirmPassword"
            class="register-input"
            placeholder="Подтвердите пароль"
            required
        />

        <button type="submit" class="register-button">Зарегистрироваться</button>
      </form>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      username: '',
      email: '',
      password: '',
      confirmPassword: ''
    };
  },
  methods: {
    async register() {
      try {
        if (this.password !== this.confirmPassword) {
          alert("Пароли не совпадают");
          return;
        }

        const response = await axios.post('http://127.0.0.1:8000/api/register/', {
          username: this.username,
          email: this.email,
          password: this.password,
          confirm_password: this.confirmPassword
        });

        alert('Регистрация прошла успешно!');
        this.$router.push('/login');
      } catch (error) {
        console.error("Ошибка при регистрации:", error);
        alert("Ошибка при регистрации");
      }
    }
  }
};
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f5f5f5;
}

.register-card {
  background: #ffffff;
  padding: 2%;
  border-radius: 10px;
  width: 100%;
  max-width: 400px;
}

.register-title {
  font-weight: bold;
  color: #596dff;
  margin-bottom: 5%;
  text-align: center;
}

.register-form {
  display: flex;
  flex-direction: column;
}

.register-input {
  padding: 10px;
  border: 1px solid #cccccc;
  border-radius: 10px;
  margin-bottom: 1rem;
}

.register-input:focus {
  border-color: #596dff;
  outline: none;
}

.register-button {
  padding: 10px;
  color: white;
  background-color: #ffa44b;
  border: none;
  border-radius: 10px;
  cursor: pointer;
  text-align: center;
}

.register-button:hover {
  background-color: #c5813b;
}
</style>
