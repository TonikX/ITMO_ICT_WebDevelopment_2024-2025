<template>
  <v-container class="mt-4" max-width="400">
    <v-card class="pa-4 elevated-card">
      <h2>Авторизация</h2>
      <v-form @submit.prevent="handleLogin">
        <!-- Поле для ввода логина -->
        <v-text-field
          v-model="form.username"
          label="Логин"
          required
        ></v-text-field>
        <!-- Поле для ввода пароля -->
        <v-text-field
          v-model="form.password"
          label="Пароль"
          type="password"
          required
        ></v-text-field>
        <!-- Кнопка для отправки формы -->
        <v-btn variant="elevated" color="primary" type="submit" class="mr-1">
          Войти
        </v-btn>
        <!-- Кнопка для возврата на предыдущую страницу -->
        <v-btn variant="outlined" color="error" @click="$router.push('/start')" class="ml-1">
          Назад
        </v-btn>
      </v-form>
    </v-card>
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Login',
  data() {
    return {
      form: {
        username: '',
        password: ''
      }
    }
  },
  methods: {
    async handleLogin() {
      try {
        // Отправка данных для авторизации на сервер
        const response = await axios.post('http://127.0.0.1:8000/auth/token/login/', {
          username: this.form.username,
          password: this.form.password
        })
        // Сохранение токена в localStorage
        const token = response.data.auth_token
        localStorage.setItem('token', token)
        // Переход на главную страницу после успешной авторизации
        this.$router.push({ name: 'home' })
      } catch (error) {
        console.error(error)
      }
    }
  }
}
</script>