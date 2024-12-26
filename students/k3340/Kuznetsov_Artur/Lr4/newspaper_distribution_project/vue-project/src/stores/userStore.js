import { defineStore } from 'pinia'
import { ref } from 'vue'
import axiosClient from '@/services/axiosClient'

export const userStore = defineStore('userStore', () => {
  const user = ref(null)

  async function fetchUser() {
    try {
      const response = await axiosClient.get('/auth/users/me/')
      user.value = response.data
    } catch (error) {
      console.error('Ошибка получения данных пользователя:', error)
    }
  }

  return { user, fetchUser }
}, { persist: true })
