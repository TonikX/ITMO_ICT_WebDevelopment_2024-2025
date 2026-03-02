<template>
  <v-app>
    <v-app-bar app color="primary" dark>
  <v-toolbar-title>Гостиница — Админ-панель</v-toolbar-title>

  <v-spacer></v-spacer>

  <v-btn v-if="auth.isAuthenticated" text to="/profile" class="mr-4">
    Профиль ({{ auth.user?.username || '...' }})
  </v-btn>

  <v-btn v-if="auth.isAuthenticated" text to="/" class="mr-4">
    Главная
  </v-btn>

  <v-btn v-if="auth.isAuthenticated" text @click="auth.logout">
    Выйти
  </v-btn>

  <v-btn v-else text to="/login">
    Войти
  </v-btn>
</v-app-bar>

    <v-main>
      <v-container fluid>
        <router-view></router-view>
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { useAuthStore } from '@/stores/auth'

const auth = useAuthStore()

// Автоматически загружаем пользователя при загрузке приложения
auth.fetchUser()
</script>
