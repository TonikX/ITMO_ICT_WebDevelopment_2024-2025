<template>
  <v-container class="login">
    <v-row class="justify-center">
      <v-col cols="12" md="6">
        <h1 class="text-center">Авторизация</h1>
        <v-form @submit.prevent="login" class="mt-5">
          <v-text-field
            v-model="form.username"
            label="Логин"
            required
            outlined
            class="mb-4"
          ></v-text-field>
          <v-text-field
            v-model="form.password"
            label="Пароль"
            type="password"
            required
            outlined
            class="mb-4"
          ></v-text-field>
          <v-btn type="submit" color="indigo" block large>Войти</v-btn>
        </v-form>
        <div class="text-center mt-6">
          <p class="text-large mb-3">Нет аккаунта?</p>
          <v-btn color="indigo-lighten-4" large outlined to="/register">Регистрация</v-btn>
        </div>
        <div v-if="message" class="text-center mt-4 text-error">
          {{ message }}
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { login } from '../store/auth';

export default {
  data() {
    return {
      form: {
        username: '',
        password: '',
      },
      message: '',
    };
  },
  methods: {
    async login() {
      try {
        const response = await this.$axios.post('/auth/token/login/', this.form);
        const token = response.data.auth_token;

        localStorage.setItem('token', token);

        const userResponse = await this.$axios.get('/auth/users/me/', {
          headers: { Authorization: `Token ${token}` },
        });

        if (!userResponse.data.airline) {
          this.message = 'Ваш профиль в процессе обработки';
          return;
        }

        login();

        this.$router.push('/flights');
      } catch (error) {
        if (error.response?.status === 404) {
          this.message = 'Пользователь не найден';
        } else if (error.response?.status === 400) {
          this.message = 'Неверный логин или пароль';
        } else {
          this.message = 'Ошибка авторизации: ' + JSON.stringify(error.response?.data || error.message);
        }
      }
    },
  },
};
</script>

<style>
.login {
  margin-top: 50px;
}
.text-large {
  font-size: 18px;
  font-weight: 500;
}
.text-error {
  color: red;
}
</style>
