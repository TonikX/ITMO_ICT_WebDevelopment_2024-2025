<template>
  <v-container class="fill-height">
    <v-row justify="center" align="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card>
          <v-card-title class="text-center">Регистрация</v-card-title>
          <v-card-text>
            <v-form @submit.prevent="handleRegister">
              <v-text-field
                v-model="form.username"
                label="Логин"
                required
                prepend-icon="mdi-account"
                :error="!!authError"
              />
              <v-text-field
                v-model="form.email"
                label="Email"
                type="email"
                required
                prepend-icon="mdi-email"
                :error="!!authError"
              />
              <v-text-field
                v-model="form.first_name"
                label="Имя"
                required
                prepend-icon="mdi-account"
              />
              <v-text-field
                v-model="form.last_name"
                label="Фамилия"
                required
                prepend-icon="mdi-account"
              />
              <v-text-field
                v-model="form.password"
                label="Пароль"
                type="password"
                required
                prepend-icon="mdi-lock"
                :error="!!authError"
              />
              <v-text-field
                v-model="form.password_confirm"
                label="Подтверждение пароля"
                type="password"
                required
                prepend-icon="mdi-lock-check"
                :error="!!authError"
              />
              
              <!-- Отображение ошибок -->
              <v-alert 
                v-if="authError" 
                type="error" 
                class="mb-4"
                dense
              >
                {{ formatError(authError) }}
              </v-alert>
              
              <v-btn 
                type="submit" 
                color="primary" 
                block 
                :loading="auth.isLoading.value"
              >
                Зарегистрироваться
              </v-btn>
            </v-form>
            
            <div class="text-center mt-4">
              <router-link to="/login">Уже есть аккаунт? Войдите</router-link>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, reactive } from 'vue'
import { useAuth } from '@/composables/useAuth'
import { useRouter } from 'vue-router'

const auth = useAuth()
const router = useRouter()
const authError = ref('')

const form = reactive({
  username: '',
  email: '',
  first_name: '',
  last_name: '',
  password: '',
  password_confirm: ''
})

const formatError = (error) => {
  if (typeof error === 'string') return error
  if (error && typeof error === 'object') {
    // Обработка ошибок Django REST framework
    if (error.non_field_errors) return error.non_field_errors.join(', ')
    if (error.detail) return error.detail
    
    // Собираем все ошибки полей в одну строку
    const fieldErrors = []
    for (const [field, messages] of Object.entries(error)) {
      if (Array.isArray(messages)) {
        fieldErrors.push(`${field}: ${messages.join(', ')}`)
      } else {
        fieldErrors.push(`${field}: ${messages}`)
      }
    }
    return fieldErrors.join('; ')
  }
  return 'Неизвестная ошибка'
}

const handleRegister = async () => {
  authError.value = ''
  
  // Валидация паролей
  if (form.password !== form.password_confirm) {
    authError.value = 'Пароли не совпадают'
    return
  }
  
  // Валидация длины пароля
  if (form.password.length < 8) {
    authError.value = 'Пароль должен содержать минимум 8 символов'
    return
  }
  
  // Вызов метода регистрации из useAuth
  const result = await auth.register({
    username: form.username,
    email: form.email,
    first_name: form.first_name,
    last_name: form.last_name,
    password: form.password
  })
  
  if (result.success) {
    // При успешной регистрации автоматически логинимся
    const loginResult = await auth.login({
      username: form.username,
      password: form.password
    })
    
    if (loginResult.success) {
      router.push('/dashboard')
    } else {
      authError.value = loginResult.error
    }
  } else {
    authError.value = result.error
  }
}
</script>

<style scoped>
.v-alert {
  margin-top: 10px;
}
</style>