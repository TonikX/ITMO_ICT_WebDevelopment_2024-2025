<template>
  <div class="register-form">
    <h2>Регистрация</h2>
    <form @submit.prevent="register">
      <div>
        <label for="username">Логин:</label>
        <input type="text" id="username" v-model="username" required />
      </div>
      <div>
        <label for="password">Пароль:</label>
        <input type="password" id="password" v-model="password" required />
      </div>
      <div>
        <label for="re_password">Подтверждение пароля:</label>
        <input type="password" id="re_password" v-model="rePassword" required />
      </div>
      <button type="submit">Создать аккаунт</button>
    </form>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      username: "",
      password: "",
      rePassword: "",
      errorMessage: "",
    };
  },
  methods: {
    async register() {
      if (this.password !== this.rePassword) {
        this.errorMessage = "Пароли не совпадают";
        return;
      }

      try {
        await axios.post("http://127.0.0.1:8000/auth/users/", {
          username: this.username,
          password: this.password,
        });
        this.$router.push("/login");
      } catch (error) {
        this.errorMessage = "Ошибка при создании аккаунта";
      }
    },
  },
};
</script>
