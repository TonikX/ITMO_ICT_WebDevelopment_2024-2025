import { defineStore } from 'pinia';
import authApi from '@/api/auth'; // Убедитесь, что путь правильный

export const useAuthStore = defineStore('auth', {
  state: () => ({
    user: null,
    loading: false,
    error: null,
  }),

  actions: {
    async login(credentials) {
      this.loading = true;
      this.error = null;
      try {
        const response = await authApi.loginUser(credentials); // Используйте экземпляр
        this.user = response; // Сохраняем информацию о пользователе
      } catch (error) {
        this.error = error.message; // Записываем ошибку
      } finally {
        this.loading = false;
      }
    },

    async register(data) {
      this.loading = true;
      this.error = null;
      try {
        const response = await authApi.registerUser(data); // Вызов метода регистрации
        console.log('Ответ от сервера при регистрации:', response); // Отладочное сообщение
        this.user = response; // Сохраняем информацию о новом пользователе
        console.log('Пользователь зарегистрирован:', this.user); // Отладочное сообщение
      } catch (error) {
        this.error = error.message; // Записываем ошибку
        console.error('Ошибка регистрации:', error); // Выводим ошибку в консоль
      } finally {
        this.loading = false;
      }
    },

    logout() {
      this.user = null; // Сбрасываем информацию о пользователе
    },
  },
});
