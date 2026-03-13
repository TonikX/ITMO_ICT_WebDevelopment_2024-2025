<template>
  <!-- fill-height — растягивает контейнер на всю высоту экрана,
       чтобы карточка была по центру -->
  <v-container class="fill-height" max-width="420">

    <!-- Карточка входа -->
    <v-card class="pa-6 w-100" elevation="4">

      <v-card-title class="text-center text-h5 mb-4">
        <v-icon icon="mdi-login" class="mr-2" />Вход в систему
      </v-card-title>

      <!-- Поле ввода логина.
           v-model="username" — двусторонняя привязка к данным компонента -->
      <v-text-field
        v-model="username"
        label="Логин"
        prepend-inner-icon="mdi-account"
        variant="outlined"
        class="mb-3"
      />

      <!-- Поле ввода пароля.
           type="password" — скрывает символы при вводе -->
      <v-text-field
        v-model="password"
        label="Пароль"
        type="password"
        prepend-inner-icon="mdi-lock"
        variant="outlined"
        class="mb-3"
      />

      <!-- Сообщение об ошибке — показывается если error не пустой -->
      <v-alert v-if="error" type="error" variant="tonal" class="mb-3">{{ error }}</v-alert>

      <!-- Сообщение об успехе — показывается после успешного входа -->
      <v-alert v-if="success" type="success" variant="tonal" class="mb-3">{{ success }}</v-alert>

      <!-- Кнопка входа.
           :loading="loading" — показывает спиннер пока идёт запрос -->
      <v-btn color="primary" block size="large" :loading="loading" @click="login">
        Войти
      </v-btn>

      <!-- Ссылка на страницу регистрации -->
      <div class="text-center mt-4">
        <router-link to="/register">Нет аккаунта? Зарегистрироваться</router-link>
      </div>

    </v-card>
  </v-container>
</template>

<script>
// axios — библиотека для HTTP-запросов к Django API
import axios from 'axios'

export default {
  data() {
    return {
      username: '',   // значение поля "Логин"
      password: '',   // значение поля "Пароль"
      error: '',      // текст ошибки (пустой = ошибки нет)
      success: '',    // текст успеха
      loading: false, // флаг загрузки (для спиннера на кнопке)
    }
  },

  methods: {
    async login() {
      this.error = ''
      this.loading = true

      try {
        // POST-запрос к эндпоинту Djoser для получения токена.
        // Djoser — библиотека для аутентификации в Django REST Framework.
        // В ответ приходит: { "auth_token": "abc123..." }
        const res = await axios.post('http://127.0.0.1:8000/auth/token/login/', {
          username: this.username,
          password: this.password,
        })

        // Сохраняем токен в localStorage — он будет использоваться
        // во всех последующих запросах к API (в заголовке Authorization)
        localStorage.setItem('token', res.data.auth_token)

        this.success = 'Вы успешно вошли!'

        // Через 800мс переходим на главную страницу
        setTimeout(() => this.$router.push('/dashboard'), 800)

      } catch (err) {
        if (!err.response) {
          // Нет ответа от сервера — Django не запущен
          this.error = 'Сервер недоступен. Убедитесь, что Django запущен на порту 8000.'
        } else {
          // Сервер ответил ошибкой — неверные логин/пароль
          this.error = 'Неверный логин или пароль'
        }
      } finally {
        // finally выполняется всегда — убираем спиннер
        this.loading = false
      }
    },
  },
}
</script>
