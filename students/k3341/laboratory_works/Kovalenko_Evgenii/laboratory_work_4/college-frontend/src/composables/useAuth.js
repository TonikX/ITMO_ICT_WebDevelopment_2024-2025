import { ref, computed } from 'vue'
import { useRouter } from 'vue-router'
import { authAPI } from '@/api/endpoints'

export function useAuth() {
  const router = useRouter()
  const user = ref(null)
  const token = ref(localStorage.getItem('token'))
  const isLoading = ref(false)
  const error = ref(null)

  const isAuthenticated = computed(() => !!token.value)

  const login = async (credentials) => {
    isLoading.value = true
    error.value = null
    try {
      const response = await authAPI.login(credentials)
      token.value = response.data.auth_token
      localStorage.setItem('token', token.value)
      
      await fetchCurrentUser()
      router.push('/dashboard')
      return { success: true }
    } catch (err) {
      error.value = err.response?.data || 'Ошибка входа'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const register = async (userData) => {
    isLoading.value = true
    try {
      await authAPI.register(userData)
      return await login({
        username: userData.username,
        password: userData.password
      })
    } catch (err) {
      error.value = err.response?.data || 'Ошибка регистрации'
      return { success: false, error: error.value }
    } finally {
      isLoading.value = false
    }
  }

  const logout = async () => {
    try {
      await authAPI.logout()
    } catch (err) {
      console.error('Ошибка при выходе:', err)
    } finally {
      user.value = null
      token.value = null
      localStorage.removeItem('token')
      router.push('/login')
    }
  }

  const fetchCurrentUser = async () => {
    try {
      const response = await authAPI.getCurrentUser()
      user.value = response.data
    } catch (err) {
      console.error('Ошибка получения пользователя:', err)
    }
  }

  return {
    user,
    token,
    isLoading,
    error,
    isAuthenticated,
    login,
    register,
    logout,
    fetchCurrentUser
  }
}