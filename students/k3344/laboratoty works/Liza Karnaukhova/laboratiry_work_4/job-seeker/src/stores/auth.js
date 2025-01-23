import { defineStore } from 'pinia';
import { authApi } from '@/api';

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,  // Текущий авторизованный пользователь
    loading: false,  // Статус загрузки
    error: null,  // Ошибка при авторизации
  }),

  actions: {
    async login(credentials) {
      this.loading = true;
      this.error = null;
      try {
        const response = await authApi.login(credentials);
        this.user = response.data;  // Сохраняем информацию о пользователе
      } catch (error) {
        this.error = error.message;  // Записываем ошибку
      } finally {
        this.loading = false;
      }
    },

    async register(data) {
      this.loading = true;
      this.error = null;
      try {
        const response = await authApi.register(data);
        this.user = response.data;  // Сохраняем информацию о новом пользователе
      } catch (error) {
        this.error = error.message;  // Записываем ошибку
      } finally {
        this.loading = false;
      }
    },

    logout() {
      this.user = null;  // Сбрасываем информацию о пользователе
    },
  },
});
