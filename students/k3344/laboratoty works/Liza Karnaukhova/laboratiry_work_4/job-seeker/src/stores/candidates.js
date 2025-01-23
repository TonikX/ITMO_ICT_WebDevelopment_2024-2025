import { defineStore } from 'pinia';
import { candidatesApi } from '@/api';

export const useCandidatesStore = defineStore('candidates', {
  state: () => ({
    profile: null,  // Информация о кандидате
  }),

  actions: {
    async loadProfile() {
      try {
        const response = await candidatesApi.getProfile();
        this.profile = response.data;  // Загружаем информацию о кандидате
      } catch (error) {
        console.error('Ошибка при загрузке профиля кандидата:', error);
      }
    },

    updateProfile(data) {
      this.profile = { ...this.profile, ...data };  // Обновляем информацию о кандидате
    },
  },
});
