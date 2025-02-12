<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <h2 class="text-center mb-4">Вход</h2>
        <form @submit.prevent="login" class="card p-4 shadow">
          <div class="form-group mb-3">
            <label for="username">Имя пользователя</label>
            <input
              id="username"
              v-model="form.username"
              class="form-control"
              placeholder="Введите имя пользователя"
              required
            />
          </div>
          <div class="form-group mb-3">
            <label for="password">Пароль</label>
            <input
              id="password"
              v-model="form.password"
              type="password"
              class="form-control"
              placeholder="Введите пароль"
              required
            />
          </div>
          <button type="submit" class="btn btn-primary w-100">Войти</button>
        </form>
        <div class="text-center mt-3">
          <span>Нет аккаунта? </span>
          <router-link to="/register">Регистрация</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "@/api/axios";

export default {
  data() {
    return {
      form: {
        username: "",
        password: ""
      }
    };
  },
  methods: {
    async login() {
      try {
        const response = await axios.post("http://127.0.0.1:8000/auth/token/login/", this.form);
        console.log("Вход успешен:", response.data);
        // Сохраните токен в localStorage или Vuex
        localStorage.setItem("authToken", response.data.auth_token);
        this.$router.push("/home-page"); // Перенаправление на главную страницу
      } catch (error) {
        console.error("Ошибка входа:", error.response?.data || error.message);
        alert("Ошибка входа: проверьте имя пользователя и пароль.");
      }
    }
  }
};
</script>
