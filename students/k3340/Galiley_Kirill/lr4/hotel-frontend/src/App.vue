<template>
  <v-app>
    <v-app-bar color="primary" dark>
      <v-toolbar-title>Hotel Management</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn to="/">Главная</v-btn>
      <v-btn v-if="isAuthenticated" to="/rooms">Номера</v-btn>
      <v-btn v-if="isAuthenticated" to="/clients">Клиенты</v-btn>
      <v-btn v-if="isAuthenticated" to="/stays">Проживания</v-btn>
      <v-btn v-if="isAuthenticated" to="/reports">Отчеты</v-btn>
      <v-btn v-if="isAuthenticated" @click="logout">Выход</v-btn>
      <v-btn v-else to="/login">Вход</v-btn>
    </v-app-bar>

    <v-main>
      <RouterView />
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { RouterView, useRouter } from 'vue-router'
import api from './services/api'

const router = useRouter()
const token = ref(localStorage.getItem('token'))

const isAuthenticated = computed(() => {
  return !!token.value
})

const logout = async () => {
  try {
    await api.logout()
  } catch (error) {
    console.error(error)
  } finally {
    localStorage.removeItem('token')
    token.value = null
    router.push('/login')
  }
}

router.afterEach(() => {
  token.value = localStorage.getItem('token')
})
</script>
