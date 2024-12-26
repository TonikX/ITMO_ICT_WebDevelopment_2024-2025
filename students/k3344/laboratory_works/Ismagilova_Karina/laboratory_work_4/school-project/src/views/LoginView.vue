<template>
  <div>
    <Header />
    <div class="login-container">
      <h1 class="page-title">Вход</h1>
      <form @submit.prevent="loginUser">
        <div class="form-group">
          <label for="username" class="form-label">Username</label>
          <input
            v-model="form.email"
            type="username"
            id="username"
            placeholder="Введите username"
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
        <button type="submit" class="login-button">Войти</button>
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
        password: "",
      },
      error: null,
    };
  },
  methods: {
    async loginUser() {
      try {
        const response = await axios.post("http://127.0.0.1:8000/auth/token/login/", {
          username: this.form.email,
          password: this.form.password
        });

        const token = response.data.auth_token;
        localStorage.setItem("authToken", token);
        alert("Вход выполнен успешно!");
        this.$router.push("/home");
      } catch (error) {
        this.error = "Ошибка при входе. Проверьте данные.";
        console.error(error);
      }
    },
  },
};
</script>

<style>
.login-container {
  max-width: 400px;
  margin: 40px auto;
  padding: 20px;
  border: 1px solid #ddd;
  border-radius: 8px;
  background: #f9f9f9;
  color: #afb3b3;
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

.login-button {
  width: 100%;
  padding: 10px;
  background-color: #006d77;
  color: #ebe9e8;
  border: none;
  border-radius: 4px;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
}

.login-button:hover {
  background-color: #005457;
}

.error {
  color: red;
  text-align: center;
  margin-top: 10px;
}
</style>
