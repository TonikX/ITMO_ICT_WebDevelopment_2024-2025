import { defineStore } from 'pinia';
import resumesApi from '@/api/resumes'; // Импортируем API для работы с резюме

export const useResumesStore = defineStore('resumes', {
  state: () => ({
    resumes: [], // Массив для хранения резюме
  }),

  actions: {
    // Метод для загрузки всех резюме кандидата
    async loadResumes() {
      try {
        const response = await resumesApi.getAll();
        this.resumes = response.data; // Заполняем список резюме
      } catch (error) {
        console.error('Ошибка при загрузке резюме:', error);
      }
    },

    // Метод для создания нового резюме
    async createResume(data) {
      try {
        const response = await resumesApi.createResume(data);
        this.resumes.push(response.data); // Добавляем новое резюме
      } catch (error) {
        console.error('Ошибка при создании резюме:', error);
      }
    },

    // Метод для обновления резюме
    async updateResume(id, data) {
      try {
        const response = await resumesApi.updateResume(id, data);
        const index = this.resumes.findIndex((resume) => resume.id === id);
        if (index !== -1) {
          this.resumes[index] = response.data; // Обновляем резюме в списке
        }
      } catch (error) {
        console.error('Ошибка при обновлении резюме:', error);
      }
    },

    // Метод для удаления резюме
    async deleteResume(id) {
      try {
        await resumesApi.deleteResume(id);
        this.resumes = this.resumes.filter((resume) => resume.id !== id); // Удаляем резюме из списка
      } catch (error) {
        console.error('Ошибка при удалении резюме:', error);
      }
    },
  },
});
