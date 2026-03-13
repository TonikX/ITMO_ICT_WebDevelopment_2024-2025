<template>
  <v-container class="fill-height" max-width="420">

    <!-- Карточка регистрации -->
    <v-card class="pa-6 w-100" elevation="4">

      <v-card-title class="text-center text-h5 mb-4">
        <v-icon icon="mdi-account-plus" class="mr-2" />Регистрация
      </v-card-title>

      <!-- Поле логина -->
      <v-text-field
        v-model="username"
        label="Логин"
        prepend-inner-icon="mdi-account"
        variant="outlined"
        class="mb-3"
      />

      <!-- Поле пароля -->
      <v-text-field
        v-model="password"
        label="Пароль"
        type="password"
        prepend-inner-icon="mdi-lock"
        variant="outlined"
        class="mb-3"
      />

      <!-- Сообщение об ошибке (например: "Пользователь уже существует") -->
      <v-alert v-if="error" type="error" variant="tonal" class="mb-3">{{ error }}</v-alert>

      <!-- Сообщение об успехе после регистрации -->
      <v-alert v-if="success" type="success" variant="tonal" class="mb-3">{{ success }}</v-alert>

      <v-btn color="primary" block size="large" :loading="loading" @click="register">
        Зарегистрироваться
      </v-btn>

      <!-- Ссылка на страницу входа -->
      <div class="text-center mt-4">
        <router-link to="/login">Уже есть аккаунт? Войти</router-link>
      </div>

    </v-card>
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      username: '',
      password: '',
      error: '',
      success: '',
      loading: false,
    }
  },

  methods: {
    async register() {
      this.error = ''
      this.loading = true

      try {
        // POST-запрос к эндпоинту Djoser для создания пользователя.
        // Djoser автоматически регистрирует маршрут /auth/users/
        // и обрабатывает создание пользователя Django.
        await axios.post('http://127.0.0.1:8000/auth/users/', {
          username: this.username,
          password: this.password,
        })

        this.success = 'Регистрация прошла успешно! Теперь войдите.'

        // Через 1.5 секунды переходим на страницу входа
        setTimeout(() => this.$router.push('/login'), 1500)

      } catch (err) {
        if (!err.response) {
          // Сервер не отвечает
          this.error = 'Сервер недоступен. Убедитесь, что Django запущен на порту 8000.'
        } else {
          // Разбираем ошибки валидации от Django/Djoser.
          // Django возвращает объект с полями-массивами ошибок:
          // { "username": ["Пользователь уже существует."], "password": [...] }
          const data = err.response.data
          if (data?.username) this.error = data.username[0]
          else if (data?.password) this.error = data.password[0]
          else this.error = 'Ошибка регистрации'
        }
      } finally {
        this.loading = false
      }
    },
  },
}
</script>
