import { defineStore } from 'pinia'
import { ref, computed } from 'vue'
import api from '@/services/api'

interface User {
  id: number
  username: string
  email: string
  first_name?: string
  last_name?: string
  full_name?: string
}

export const useAuthStore = defineStore('auth', () => {
  // Инициализация из localStorage
  const storedUser = localStorage.getItem('user')
  const user = ref<User | null>(storedUser ? JSON.parse(storedUser) : null)
  const token = ref<string | null>(localStorage.getItem('auth_token'))
  const loading = ref(false)
  const error = ref<string | null>(null)

  const isAuthenticated = computed(() => !!token.value)

  async function init() {
    if (token.value && !user.value) {
      try {
        const userData = await api.getCurrentUser()
        user.value = userData
        localStorage.setItem('user', JSON.stringify(userData))
      } catch {
        logout()
      }
    }
  }

  async function login(username: string, password: string) {
    loading.value = true
    error.value = null
    try {
      const response = await api.login(username, password)
      token.value = response.token
      user.value = response.user
      localStorage.setItem('auth_token', response.token)
      localStorage.setItem('user', JSON.stringify(response.user))
      return { success: true }
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Ошибка входа. Проверьте правильность данных.'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  async function register(username: string, email: string, password: string, firstName?: string, lastName?: string) {
    loading.value = true
    error.value = null
    try {
      const response = await api.register(username, password, email, firstName, lastName)
      token.value = response.token
      user.value = response.user
      localStorage.setItem('auth_token', response.token)
      localStorage.setItem('user', JSON.stringify(response.user))
      return { success: true }
    } catch (err: any) {
      error.value = err.response?.data?.error || 'Ошибка регистрации'
      return { success: false, error: error.value }
    } finally {
      loading.value = false
    }
  }

  async function fetchCurrentUser() {
    if (!token.value) return
    
    try {
      const userData = await api.getCurrentUser()
      user.value = userData
      localStorage.setItem('user', JSON.stringify(userData))
    } catch (err: any) {
      console.error('Failed to fetch user:', err)
      logout()
    }
  }

  function logout() {
    user.value = null
    token.value = null
    localStorage.removeItem('auth_token')
    localStorage.removeItem('user')
  }

  return {
    user,
    token,
    loading,
    error,
    isAuthenticated,
    init,
    login,
    register,
    fetchCurrentUser,
    logout,
  }
})
