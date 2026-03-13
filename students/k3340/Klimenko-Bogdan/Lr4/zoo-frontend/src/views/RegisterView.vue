<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>Регистрация</v-card-title>
          <v-card-text>
            <v-form @submit.prevent="handleRegister">
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
              <v-btn type="submit" color="primary" block>Зарегистрироваться</v-btn>
            </v-form>
            <p class="mt-4 text-center">
              Уже есть аккаунт? <router-link to="/login">Войти</router-link>
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

const handleRegister = async () => {
  const success = await userStore.register(username.value, password.value)
  if (success) {
    alert('Регистрация успешна! Теперь можно войти.')
    router.push('/login')
  } else {
    alert('Ошибка регистрации (возможно, имя уже занято)')
  }
}
</script>