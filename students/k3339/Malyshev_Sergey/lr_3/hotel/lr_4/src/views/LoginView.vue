<template>
  <v-container fluid class="fill-height">
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card elevation="10" class="pa-6">
          <v-card-title class="text-h5 text-center mb-6">Вход</v-card-title>

          <v-card-text>
            <v-alert v-if="auth.error" type="error" class="mb-4">
              {{ auth.error }}
            </v-alert>

            <v-form @submit.prevent="handleLogin">
              <v-text-field
                v-model="username"
                label="Логин"
                prepend-inner-icon="mdi-account"
                variant="outlined"
                required
                class="mb-4"
              ></v-text-field>

              <v-text-field
                v-model="password"
                label="Пароль"
                type="password"
                prepend-inner-icon="mdi-lock"
                variant="outlined"
                required
                class="mb-6"
              ></v-text-field>

              <v-btn
                type="submit"
                color="primary"
                block
                size="large"
                class="mb-4"
                :loading="auth.loading"
                :disabled="auth.loading"
              >
                Войти
              </v-btn>
            </v-form>

            <div class="text-center">
              <v-btn
                variant="text"
                color="primary"
                to="/register"
                class="mt-4"
              >
                Нет аккаунта? Зарегистрироваться
              </v-btn>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const username = ref('')
const password = ref('')
const router = useRouter()
const auth = useAuthStore()

async function handleLogin() {
  try {
    await auth.login(username.value, password.value)
    router.push('/')
  } catch (e) {
    // Ошибка уже в store — просто показываем alert или используем v-alert
    console.error(e)
  }
}
</script>

<style scoped>
.v-card {
  border-radius: 12px;
}
</style>
