<template>
  <div>
    <Header />
    <div class="register-container">
      <h1 class="page-title">Регистрация</h1>
      <form @submit.prevent="registerUser">
        <div class="form-group">
          <label for="email" class="form-label">Email</label>
          <input
            v-model="form.email"
            type="email"
            id="email"
            placeholder="Введите email"
            class="form-input"
            required
          />
        </div>
        <div class="form-group">
          <label for="username" class="form-label">Имя пользователя</label>
          <input
            v-model="form.username"
            type="text"
            id="username"
            placeholder="Введите имя пользователя"
            class="form-input"
            required
          />
        </div>
        <div class="form-group">
          <label for="password" class="form-label">Пароль</label>
          <input
            v-model="form.password"
            type="password"
            id="password"
            placeholder="Введите пароль"
            class="form-input"
            required
          />
        </div>
        <div class="form-group">
          <label for="re_password" class="form-label">Подтвердите пароль</label>
          <input
            v-model="form.re_password"
            type="password"
            id="re_password"
            placeholder="Введите пароль повторно"
            class="form-input"
            required
          />
        </div>
        <button type="submit" class="register-button">Зарегистрироваться</button>
      </form>
      <p v-if="error" class="error">{{ error }}</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import Header from "@/components/Header.vue";
export default {
  components: {
    Header,
  },
  data() {
    return {
      form: {
        email: "",
        username: "",
        password: "",
        re_password: "",
      },
      error: null,
    };
  },
  methods: {
    async registerUser() {
      try {
        const response = await axios.post("http://127.0.0.1:8000/auth/users/", this.form);
        alert("Регистрация прошла успешно! Теперь вы можете войти.");
        this.$router.push("/login");
      } catch (error) {
        this.error = "Ошибка при регистрации. Проверьте введённые данные.";
        console.error(error);
      }
    },
  },
};
</script>

<style>
.register-container {
  max-width: 400px;
  margin: 40px auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #f9f9f9;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.page-title {
  text-align: center;
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 20px;
}

.form-group {
  margin-bottom: 15px;
}

.form-label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
}

.form-input {
  width: 100%;
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
  font-size: 14px;
  background-color: #fff;
}

.register-button {
  width: 100%;
  padding: 10px;
  background-color: #628c64;
  color: #ebe9e8;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.register-button:hover {
  background-color: #3d573e;
}

.error {
  color: red;
  text-align: center;
  margin-top: 10px;
}
</style>
