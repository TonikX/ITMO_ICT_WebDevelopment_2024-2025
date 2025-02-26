<template>
  <v-container class="mt-4" max-width="400">
    <v-card class="pa-4 elevated-card">
      <h2>Регистрация</h2>
      <v-form @submit.prevent="handleRegister">
        <!-- Поле для ввода логина -->
        <v-text-field
          v-model="form.username"
          label="Логин"
          required
        ></v-text-field>
        <!-- Поле для ввода email -->
        <v-text-field
          v-model="form.email"
          label="Email"
          required
        ></v-text-field>
        <!-- Поле для ввода пароля -->
        <v-text-field
          v-model="form.password"
          label="Пароль"
          type="password"
          required
        ></v-text-field>
        <!-- Поле для повторного ввода пароля -->
        <v-text-field
          v-model="form.password2"
          label="Повтор пароля"
          type="password"
          required
        ></v-text-field>
        <!-- Кнопка для отправки формы регистрации -->
        <v-btn variant="elevated" color="primary" type="submit" class="mr-1">
          Зарегистрироваться
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
  name: 'Register',
  data() {
    return {
      form: {
        username: '',
        email: '',
        password: '',
        password2: ''
      }
    }
  },
  methods: {
    async handleRegister() {
      try {
        // Отправка данных формы на сервер для регистрации пользователя
        await axios.post('http://127.0.0.1:8000/auth/users/', {
          username: this.form.username,
          email: this.form.email,
          password: this.form.password,
          re_password: this.form.password2
        })
        // Переход на страницу логина после успешной регистрации
        this.$router.push('/login')
      } catch (error) {
        console.error(error)
      }
    }
  }
}
</script>