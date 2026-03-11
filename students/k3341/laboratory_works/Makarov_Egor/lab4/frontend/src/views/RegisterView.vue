<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '../stores/auth'

const auth = useAuthStore()
const router = useRouter()

const username = ref('')
const email = ref('')
const password = ref('')
const passwordConfirm = ref('')
const localError = ref('')

async function handleSubmit() {
  localError.value = ''
  if (password.value !== passwordConfirm.value) {
    localError.value = 'Пароли не совпадают'
    return
  }
  const ok = await auth.register(username.value, email.value, password.value)
  if (ok) router.push('/profile')
}
</script>

<template>
  <div class="auth-page">
    <div class="auth-card">
      <div class="auth-header">
        <div class="logo-mark">H</div>
        <h1>Регистрация</h1>
        <p class="subtitle">Создайте аккаунт участника хакатона</p>
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
          <label>Email</label>
          <input
            v-model="email"
            type="email"
            placeholder="you@example.com"
            autocomplete="email"
          />
        </div>
        <div class="field">
          <label>Пароль</label>
          <input
            v-model="password"
            type="password"
            placeholder="••••••••"
            autocomplete="new-password"
            required
          />
        </div>
        <div class="field">
          <label>Повторите пароль</label>
          <input
            v-model="passwordConfirm"
            type="password"
            placeholder="••••••••"
            autocomplete="new-password"
            required
          />
        </div>

        <div v-if="localError || auth.error" class="error-msg">
          {{ localError || auth.error }}
        </div>

        <button type="submit" class="btn-primary" :disabled="auth.loading">
          <span v-if="auth.loading" class="spinner"></span>
          <span v-else>Создать аккаунт</span>
        </button>
      </form>

      <p class="auth-link">
        Уже есть аккаунт? <router-link to="/login">Войти</router-link>
      </p>
    </div>
  </div>
</template>