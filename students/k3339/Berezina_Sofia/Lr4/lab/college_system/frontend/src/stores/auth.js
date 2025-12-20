import { defineStore } from 'pinia'
import { authApi } from '@/api'

export const useAuthStore = defineStore('auth', {
  state: () => ({
    token: localStorage.getItem('token') || null,
    user: JSON.parse(localStorage.getItem('user') || 'null'),
    isAuthenticated: !!localStorage.getItem('token')
  }),

  actions: {
    async login(credentials) {
      try {
        console.log('🔑 Попытка авторизации:', credentials)

        const response = await authApi.login(credentials)
        console.log('📦 Ответ от API:', response.data)

        // Пробуем разные форматы токенов:
        // 1. DRF Token Authentication: { "token": "ваш_токен" }
        // 2. Djoser: { "auth_token": "ваш_токен" }
        // 3. Ваш случай: нужно проверить что именно возвращается
        const token = response.data.token || response.data.auth_token

        if (!token) {
          console.error('❌ Токен не найден в ответе:', response.data)
          throw new Error('Токен не получен от сервера')
        }

        console.log('✅ Получен токен:', token.substring(0, 20) + '...')

        this.token = token
        localStorage.setItem('token', token)

        // Получаем данные пользователя
        try {
          const userResponse = await authApi.getUser()
          console.log('👤 Данные пользователя:', userResponse.data)

          this.user = userResponse.data
          localStorage.setItem('user', JSON.stringify(userResponse.data))
        } catch (userError) {
          console.warn('⚠️ Не удалось получить данные пользователя:', userError)
          // Создаем базового пользователя из credentials
          this.user = {
            id: 1,
            username: credentials.username,
            email: `${credentials.username}@example.com`,
            first_name: credentials.username
          }
          localStorage.setItem('user', JSON.stringify(this.user))
        }

        this.isAuthenticated = true
        return { success: true }

      } catch (error) {
        console.error('💥 Ошибка авторизации:', {
          message: error.message,
          status: error.response?.status,
          data: error.response?.data,
          headers: error.config?.headers
        })

        let errorMessage = 'Ошибка авторизации'

        // Разные форматы ошибок
        if (error.response?.data?.non_field_errors) {
          errorMessage = error.response.data.non_field_errors[0]
        } else if (error.response?.data?.detail) {
          errorMessage = error.response.data.detail
        } else if (error.response?.data?.error) {
          errorMessage = error.response.data.error
        }

        // Если это 404, значит эндпоинт не существует
        if (error.response?.status === 404) {
          errorMessage = 'Эндпоинт авторизации не найден. Проверьте настройки Django.'
        }

        return {
          success: false,
          error: errorMessage
        }
      }
    },

    logout() {
      // Пытаемся выйти через API
      authApi.logout().catch(() => {})

      // Очищаем локальное состояние
      this.token = null
      this.user = null
      this.isAuthenticated = false
      localStorage.removeItem('token')
      localStorage.removeItem('user')
    },

    async checkAuth() {
      if (!this.token) {
        console.log('🔒 Нет токена, пользователь не авторизован')
        return false
      }

      try {
        console.log('🔍 Проверка токена...')
        const response = await authApi.getUser()
        console.log('✅ Токен валиден, пользователь:', response.data.username)
        return true
      } catch (error) {
        console.log('❌ Токен невалиден:', error.message)
        this.logout()
        return false
      }
    }
  }
})