<template>
  <v-container class="fill-height">
    <v-card width="400">
      <v-card-title class="text-center">Вход в систему</v-card-title>
      <v-card-text>
        <v-alert
          v-if="errorMessage"
          type="error"
          class="mb-4"
        >
          {{ errorMessage }}
        </v-alert>

        <v-form @submit.prevent="login">
          <v-text-field
            v-model="username"
            label="Имя пользователя"
            required
            outlined
          ></v-text-field>

          <v-text-field
            v-model="password"
            label="Пароль"
            type="password"
            required
            outlined
          ></v-text-field>

          <v-btn
            type="submit"
            color="primary"
            block
            :loading="loading"
          >Войти
          </v-btn>
        </v-form>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import {ref} from 'vue'
import {useAuthStore} from '@/stores/auth'
import {useRouter} from 'vue-router'

const username = ref('')
const password = ref('')
const errorMessage = ref('')
const loading = ref(false)
const authStore = useAuthStore()
const router = useRouter()

const login = async () => {
  errorMessage.value = ''
  loading.value = true

  try {
    await authStore.login({
      username: username.value,
      password: password.value
    })

    router.push('/')
  } catch (error) {
    loading.value = false
    if (!error.response) {
      errorMessage.value = 'Неверное имя пользователя или пароль'
    }
  }
}
</script>

<style scoped>
.fill-height {
  height: 100vh;
}

.v-card {
  max-width: 500px;
  width: 100%;
}

.v-container {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 80vh;
}
</style>
