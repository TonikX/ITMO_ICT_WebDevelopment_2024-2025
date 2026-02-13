<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>Вход в систему</v-card-title>
          <v-card-text>
            <v-form @submit.prevent="handleLogin">
              <v-text-field v-model="username" label="Логин" required></v-text-field>
              <v-text-field
                v-model="password"
                label="Пароль"
                type="password"
                required
              ></v-text-field>
              <v-btn type="submit" color="primary" block>Войти</v-btn>
              <v-alert v-if="error" type="error" class="mt-3">{{ error }}</v-alert>
            </v-form>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '@/services/api'

const username = ref('')
const password = ref('')
const error = ref('')
const router = useRouter()

const handleLogin = async () => {
  try {
    const response = await api.login({
      username: username.value,
      password: password.value,
    })
    localStorage.setItem('token', response.data.auth_token)
    router.push('/rooms')
  } catch (err) {
    error.value = 'Неверный логин или пароль'
  }
}
</script>
