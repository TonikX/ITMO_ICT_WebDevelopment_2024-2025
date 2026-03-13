<template>
  <v-app>
    <v-app-bar app color="primary" dark>
      <v-app-bar-nav-icon @click="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>Зоопарк</v-toolbar-title>
      <v-spacer></v-spacer>
      <v-btn text to="/">Главная</v-btn>
      <v-btn text to="/animals">Животные</v-btn>
      <v-menu v-if="userStore.isAuthenticated">
        <template v-slot:activator="{ props }">
          <v-btn text v-bind="props">{{ userStore.user?.username || 'Профиль' }}</v-btn>
        </template>
        <v-list>
          <v-list-item to="/profile">
            <v-list-item-title>Профиль</v-list-item-title>
          </v-list-item>
          <v-list-item @click="logout">
            <v-list-item-title>Выйти</v-list-item-title>
          </v-list-item>
        </v-list>
      </v-menu>
      <template v-else>
        <v-btn text to="/login">Вход</v-btn>
        <v-btn text to="/register">Регистрация</v-btn>
      </template>
    </v-app-bar>

    <v-navigation-drawer v-model="drawer" app temporary>
      <v-list>
        <v-list-item to="/">Главная</v-list-item>
        <v-list-item to="/animals">Животные</v-list-item>
        <v-list-item to="/reports/animal-count">Отчет: животные по отделам</v-list-item>
        <v-list-item to="/reports/empty-enclosures">Пустые вольеры</v-list-item>
        <v-list-item to="/reports/lease-report">Отчет по аренде</v-list-item>
      </v-list>
    </v-navigation-drawer>

    <v-main>
      <v-container fluid>
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from './stores/user'
import { useRouter } from 'vue-router'

const drawer = ref(false)
const userStore = useUserStore()
const router = useRouter()

const logout = () => {
  userStore.logout()
  router.push('/')
}
</script>