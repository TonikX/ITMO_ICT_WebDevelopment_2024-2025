<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>Вход</v-card-title>
          <v-card-text>
            <v-form @submit.prevent="handleLogin">
              <v-text-field
                v-model="username"
                label="Имя пользователя"
                required
                prepend-icon="mdi-account"
              ></v-text-field>
              <v-text-field
                v-model="password"
                label="Пароль"
                type="password"
                required
                prepend-icon="mdi-lock"
              ></v-text-field>
              <v-btn type="submit" color="primary" block>Войти</v-btn>
            </v-form>
            <p class="mt-4 text-center">
              Нет аккаунта? <router-link to="/register">Зарегистрироваться</router-link>
            </p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useUserStore } from '@/stores/user'
import { useRouter } from 'vue-router'

const username = ref('')
const password = ref('')
const userStore = useUserStore()
const router = useRouter()

const handleLogin = async () => {
  const success = await userStore.login(username.value, password.value)
  if (success) {
    router.push('/')
  } else {
    alert('Неверные имя пользователя или пароль')
  }
}
</script>