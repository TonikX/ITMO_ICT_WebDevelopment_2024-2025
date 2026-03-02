<template>
  <v-container fluid>
    <v-row justify="center">
      <v-col cols="12" sm="8" md="6">
        <v-card elevation="10" class="pa-6">
          <v-card-title class="text-h5 text-center mb-6">Профиль пользователя</v-card-title>

          <v-card-text v-if="auth.user">
            <v-list>
              <v-list-item>
                <v-list-item-title>Логин</v-list-item-title>
                <v-list-item-subtitle>{{ auth.user.username }}</v-list-item-subtitle>
              </v-list-item>

              <v-list-item>
                <v-list-item-title>Email</v-list-item-title>
                <v-list-item-subtitle>{{ auth.user.email || 'Не указан' }}</v-list-item-subtitle>
              </v-list-item>

              <v-list-item>
                <v-list-item-title>Дата регистрации</v-list-item-title>
                <v-list-item-subtitle>{{ auth.user.date_joined || '—' }}</v-list-item-subtitle>
              </v-list-item>
            </v-list>

            <v-btn color="primary" block class="mt-6" to="/">
              На главную
            </v-btn>

            <v-btn color="error" outlined block class="mt-4" @click="auth.logout">
              Выйти
            </v-btn>
          </v-card-text>

          <v-card-text v-else>
            <v-alert type="warning">
              Пожалуйста, <router-link to="/login">войдите</router-link>
            </v-alert>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { onMounted } from 'vue'

const router = useRouter()
const auth = useAuthStore()

onMounted(() => {
  if (!auth.isAuthenticated) {
    router.push('/login')
  } else {
    auth.fetchUser() // подгружаем свежие данные пользователя
  }
})
</script>
