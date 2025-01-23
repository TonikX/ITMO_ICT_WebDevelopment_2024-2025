// src/stores/vacancies.js
import { ref } from 'vue';
import { defineStore } from 'pinia';
import axios from 'axios';

export const useVacanciesStore = defineStore('vacancies', () => {
  const vacancies = ref([]);

  // Получение вакансий по ID пользователя
  const getVacanciesByUserId = async (userId) => {
    const response = await axios.get(`http://localhost:3000/vacancies?userId=${userId}`);
    vacancies.value = response.data.filter(vacancy => vacancy.title && vacancy.id);
    return vacancies.value;
  };

  // Добавление новой вакансии
  const addVacancy = async (vacancy) => {
    await axios.post('http://localhost:3000/vacancies', vacancy);
    await getVacanciesByUserId(vacancy.userId); // Обновляем список вакансий
  };

  // Удаление вакансии
  const deleteVacancy = async (vacancyId) => {
    await axios.delete(`http://localhost:3000/vacancies/${vacancyId}`);
    vacancies.value = vacancies.value.filter(vacancy => vacancy.id !== vacancyId); // Обновляем локальный список
  };

  return {
    vacancies,
    getVacanciesByUserId,
    addVacancy,
    deleteVacancy,
  };
});
