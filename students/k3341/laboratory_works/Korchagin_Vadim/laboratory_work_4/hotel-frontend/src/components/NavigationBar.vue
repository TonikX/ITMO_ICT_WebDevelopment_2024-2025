<template>
  <v-app-bar elevation="8" color="#a5f5f4">
    <v-toolbar-title>Hotel System</v-toolbar-title>
    <v-spacer></v-spacer>

    <v-btn text to="/">Главная</v-btn>
    <v-btn text to="/profile">Профиль</v-btn>
    
    <!-- Кнопки для сотрудников, отображаются только если пользователь является сотрудником -->
    <template v-if="userData.is_staff">
      <v-btn text to="/staff">Сотрудники</v-btn>
      <v-btn text to="/rooms">Номера</v-btn>
      <v-btn text to="/clients">Клиенты</v-btn>
      <v-btn text to="/stays">Проживания</v-btn>
      <v-btn text to="/cleanings">Уборки</v-btn>
      <v-btn text to="/schedules">Расписания</v-btn>
      <v-btn text to="/report">Отчёт</v-btn>
    </template>

    <v-btn variant="elevated" color="error" @click="logout">Выйти</v-btn>
  </v-app-bar>
</template>

<script>
import axios from 'axios'

export default {
  name: 'NavigationBar',
  data() {
    return {
      token: null,
      userData: {}
    }
  },
  created() {
    // Получение токена из локального хранилища при создании компонента
    this.token = localStorage.getItem('token')
    if (this.token) {
      this.fetchUser() // Если токен существует, получить данные пользователя
    }
  },
  methods: {
    async fetchUser() {
      try {
        const response = await axios.get('http://127.0.0.1:8000/auth/users/me/', {
          headers: { Authorization: `Token ${this.token}` }
        })
        this.userData = response.data
      } catch (error) {
        console.error(error) 
      }
    },
    logout() {
      // Удаление токена и данных пользователя при выходе
      localStorage.removeItem('token')
      this.token = null
      this.userData = {}
      this.$router.push('/start') 
    }
  }
}
</script>