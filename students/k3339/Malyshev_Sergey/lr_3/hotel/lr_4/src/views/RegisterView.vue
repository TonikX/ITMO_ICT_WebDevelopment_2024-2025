<template>
  <v-container fluid class="fill-height">
    <v-row align="center" justify="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card elevation="10" class="pa-6">
          <v-card-title class="text-h5 text-center mb-6">Регистрация</v-card-title>

          <v-card-text>
            <v-alert v-if="auth.error" type="error" class="mb-6" dismissible>
              {{ auth.error }}
            </v-alert>

            <v-form @submit.prevent="handleRegister">
              <v-text-field
                v-model="username"
                label="Логин"
                prepend-inner-icon="mdi-account"
                variant="outlined"
                required
                class="mb-4"
                :error-messages="errors.username"
              ></v-text-field>

              <v-text-field
                v-model="password"
                label="Пароль"
                type="password"
                prepend-inner-icon="mdi-lock"
                variant="outlined"
                required
                class="mb-4"
                :error-messages="errors.password"
              ></v-text-field>

              <v-text-field
                v-model="re_password"
                label="Повторите пароль"
                type="password"
                prepend-inner-icon="mdi-lock-check"
                variant="outlined"
                required
                class="mb-6"
                :error-messages="errors.re_password"
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
                Зарегистрироваться
              </v-btn>
            </v-form>

            <div class="text-center">
              <v-btn
                variant="text"
                color="primary"
                to="/login"
                class="mt-4"
              >
                Уже есть аккаунт? Войти
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
const re_password = ref('')
const router = useRouter()
const auth = useAuthStore()

const errors = ref({})

async function handleRegister() {
  errors.value = {}

  if (password.value !== re_password.value) {
    errors.value.re_password = ['Пароли не совпадают']
    return
  }

  try {
    await auth.register(username.value, password.value)
    router.push('/')
  } catch (e) {
    // Ошибки от сервера уже в store, но можно перехватить
    console.error(e)
  }
}
</script>

<style scoped>
.v-card {
  border-radius: 12px;
}
</style>
