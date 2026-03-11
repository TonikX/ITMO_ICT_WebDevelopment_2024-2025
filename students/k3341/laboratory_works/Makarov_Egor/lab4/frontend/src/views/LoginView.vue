<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const router = useRouter()

const username = ref('')
const password = ref('')

async function handleSubmit() {
  const ok = await auth.login(username.value, password.value)
  if (ok) router.push('/profile')
}
</script>

<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-header">
        <div class="logo-mark">H</div>
        <h1>Войти</h1>
        <p class="subtitle">Введите данные для входа в систему</p>
      </div>

      <form class="auth-form" @submit.prevent="handleSubmit">
        <div class="field">
          <label>Логин</label>
          <input
            v-model="username"
            type="text"
            placeholder="username"
            autocomplete="username"
            required
          />
        </div>
        <div class="field">
          <label>Пароль</label>
          <input
            v-model="password"
            type="password"
            placeholder="••••••••"
            autocomplete="current-password"
            required
          />
        </div>

        <div v-if="auth.error" class="error-msg">{{ auth.error }}</div>

        <button type="submit" class="btn-primary" :disabled="auth.loading">
          <span v-if="auth.loading" class="spinner"></span>
          <span v-else>Войти</span>
        </button>
      </form>

      <p class="auth-link">
        Нет аккаунта? <router-link to="/register">Зарегистрироваться</router-link>
      </p>
    </div>
  </div>
</template>