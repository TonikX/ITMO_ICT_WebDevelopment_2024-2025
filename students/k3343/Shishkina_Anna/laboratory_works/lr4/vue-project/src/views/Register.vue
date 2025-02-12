<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <h2 class="text-center mb-4">Регистрация</h2>
        <form @submit.prevent="register" class="card p-4 shadow">
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
          <div class="form-group mb-3">
            <label for="email">Электронная почта</label>
            <input
              id="email"
              v-model="form.email"
              type="email"
              class="form-control"
              placeholder="Введите email"
              required
            />
          </div>
          <div class="form-group mb-3">
            <label for="first_name">Имя</label>
            <input
              id="first_name"
              v-model="form.first_name"
              class="form-control"
              placeholder="Введите имя"
              required
            />
          </div>
          <div class="form-group mb-3">
            <label for="last_name">Фамилия</label>
            <input
              id="last_name"
              v-model="form.last_name"
              class="form-control"
              placeholder="Введите фамилию"
              required
            />
          </div>
          <button type="submit" class="btn btn-primary w-100">
            Зарегистрироваться
          </button>
        </form>
        <div class="text-center mt-3">
          <span>Уже есть аккаунт? </span>
          <router-link to="/login">Войти</router-link>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "@/api/axios"; // Ваш API клиент

export default {
  data() {
    return {
      form: {
        username: "",
        password: "",
        email: "",
        first_name: "",
        last_name: ""
      }
    };
  },
  methods: {
    async register() {
      try {
        console.log(this.form);
        const response = await axios.post("http://127.0.0.1:8000/auth/users/", this.form);
        console.log("Регистрация успешна:", response.data);
        this.$router.push("/login"); // Перенаправление на страницу входа
      } catch (error) {
        console.error("Ошибка регистрации:", error.response?.data || error.message);
      }
    }
  }
};
</script>
