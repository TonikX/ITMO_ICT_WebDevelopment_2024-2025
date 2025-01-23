import { defineStore } from 'pinia';
import usersApi from '@/api/users';

export const useUsersStore = defineStore('users', {
  state: () => ({
    profile: null,  // Информация о текущем пользователе
    role: null,  // Роль пользователя (работодатель или кандидат)
  }),

  actions: {
    async loadProfile() {
      try {
        const response = await usersApi.getProfile();
        console.log(response.data); // Проверьте, содержит ли `username`
        this.profile = response.data;  // Загружаем информацию о пользователе
      } catch (error) {
        console.error('Ошибка при загрузке профиля:', error);
      }
    },

    async loadRole() {
      try {
        const response = await usersApi.getRole();
        this.role = response.data;  // Загружаем роль пользователя
      } catch (error) {
        console.error('Ошибка при загрузке роли:', error);
      }
    },

    updateProfile(data) {
      this.profile = { ...this.profile, ...data };  // Обновляем информацию о профиле
    },
  },
});
