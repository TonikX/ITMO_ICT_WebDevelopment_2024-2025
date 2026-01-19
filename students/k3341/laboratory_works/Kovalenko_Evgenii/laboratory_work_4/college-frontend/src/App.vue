<template>
  <v-app>
    <!-- Проверяем наличие токена вместо Pinia store -->
    <v-navigation-drawer v-model="drawer" v-if="hasToken">
      <v-list>
        <v-list-item prepend-icon="mdi-view-dashboard" title="Дашборд" to="/dashboard" />
        <v-list-item prepend-icon="mdi-account-tie" title="Преподаватели" to="/teachers" />
        <v-list-item prepend-icon="mdi-account-group" title="Студенты" to="/students" />
        <v-list-item prepend-icon="mdi-calendar" title="Расписание" to="/schedule" />
        <v-list-item prepend-icon="mdi-office-building" title="Аудитории" to="/classrooms" />
        <v-list-item prepend-icon="mdi-account-multiple" title="Группы" to="/groups" />
        <v-list-item prepend-icon="mdi-book-open-variant" title="Дисциплины" to="/subjects" />
        <v-list-item prepend-icon="mdi-chart-box" title="Оценки" to="/grades" />
        <v-list-item prepend-icon="mdi-file-chart" title="Отчеты" to="/reports" />
        <v-list-item prepend-icon="mdi-magnify" title="Запросы" to="/queries" />
      </v-list>
    </v-navigation-drawer>

    <v-app-bar>
      <v-app-bar-nav-icon @click="drawer = !drawer" v-if="hasToken" />
      <v-app-bar-title>Учебная часть колледжа</v-app-bar-title>
      
      <v-spacer />
      
      <template v-if="hasToken">
        <v-btn icon="mdi-account" to="/profile" />
        <v-btn icon="mdi-logout" @click="logout" />
      </template>
      <template v-else>
        <v-btn to="/login">Вход</v-btn>
        <v-btn to="/register" variant="outlined">Регистрация</v-btn>
      </template>
    </v-app-bar>

    <v-main>
      <router-view />
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const drawer = ref(true)

// Проверяем токен напрямую из localStorage
const hasToken = computed(() => !!localStorage.getItem('token'))

const logout = () => {
  localStorage.removeItem('token')
  router.push('/login')
}
</script>