<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1>Профиль пользователя</h1>
        <v-card v-if="userStore.user">
          <v-card-text>
            <p><strong>Имя пользователя:</strong> {{ userStore.user.username }}</p>
            <p><strong>Email:</strong> {{ userStore.user.email || 'не указан' }}</p>
          </v-card-text>
          <v-card-actions>
            <v-btn color="error" @click="logout">Выйти</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'

const userStore = useUserStore()
const router = useRouter()

const logout = () => {
  userStore.logout()
  router.push('/')
}
</script>