<template>
  <v-container class="fill-height">
    <v-row justify="center" align="center">
      <v-col cols="12" sm="8" md="6" lg="4">
        <v-card>
          <v-card-title class="text-center">Вход в систему</v-card-title>
          <v-card-text>
            <v-form @submit.prevent="handleLogin">
              <v-text-field
                v-model="form.username"
                label="Логин"
                required
                prepend-icon="mdi-account"
              />
              <v-text-field
                v-model="form.password"
                label="Пароль"
                type="password"
                required
                prepend-icon="mdi-lock"
              />
              
              <v-alert v-if="authError" type="error" class="mb-4">
                {{ authError }}
              </v-alert>
              
              <v-btn 
                type="submit" 
                color="primary" 
                block 
                :loading="auth.isLoading.value"
              >
                Войти
              </v-btn>
            </v-form>
            
            <div class="text-center mt-4">
              <router-link to="/register">Нет аккаунта? Зарегистрируйтесь</router-link>
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

const auth = useAuth()
const authError = ref('')
const form = reactive({
  username: '',
  password: ''
})

const handleLogin = async () => {
  authError.value = ''
  const result = await auth.login(form)
  if (!result.success) {
    authError.value = result.error?.non_field_errors?.[0] || 'Ошибка входа'
  }
}
</script>