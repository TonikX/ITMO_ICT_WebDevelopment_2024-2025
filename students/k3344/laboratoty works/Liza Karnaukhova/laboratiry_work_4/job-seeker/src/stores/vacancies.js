import { defineStore } from 'pinia';
import { vacanciesApi } from '@/api'; // Импортируем API для работы с вакансиями

export const useVacanciesStore = defineStore('vacancies', {
  state: () => ({
    vacancies: [], // Массив для хранения вакансий
    currentVacancy: null, // Текущая выбранная вакансия
  }),

  actions: {
    // Метод для загрузки всех вакансий с фильтрами
    async loadVacancies(filters) {
      try {
        const response = await vacanciesApi.getAll(filters);
        this.vacancies = response.data; // Заполняем список вакансий
      } catch (error) {
        console.error('Ошибка при загрузке вакансий:', error);
      }
    },

    // Метод для загрузки вакансии по ID
    async loadVacancyById(id) {
      try {
        const response = await vacanciesApi.getById(id);
        this.currentVacancy = response.data; // Загружаем подробности вакансии
      } catch (error) {
        console.error('Ошибка при загрузке вакансии:', error);
      }
    },

    // Метод для создания новой вакансии
    async createVacancy(data) {
      try {
        const response = await vacanciesApi.create(data);
        this.vacancies.push(response.data); // Добавляем новую вакансию в список
      } catch (error) {
        console.error('Ошибка при создании вакансии:', error);
      }
    },

    // Метод для обновления вакансии
    async updateVacancy(id, data) {
      try {
        const response = await vacanciesApi.update(id, data);
        const index = this.vacancies.findIndex((vacancy) => vacancy.id === id);
        if (index !== -1) {
          this.vacancies[index] = response.data; // Обновляем вакансию в списке
        }
      } catch (error) {
        console.error('Ошибка при обновлении вакансии:', error);
      }
    },

    // Метод для удаления вакансии
    async deleteVacancy(id) {
      try {
        await vacanciesApi.delete(id);
        this.vacancies = this.vacancies.filter((vacancy) => vacancy.id !== id); // Удаляем вакансию из списка
      } catch (error) {
        console.error('Ошибка при удалении вакансии:', error);
      }
    },
  },
});
