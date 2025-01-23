// src/stores/companies.js
import { ref } from 'vue';
import { defineStore } from 'pinia';
import axios from 'axios';

export const useCompaniesStore = defineStore('companies', () => {
  const companies = ref([]);

  // Получение информации о компании по имени пользователя
  const getCompanyByUsername = async (username) => {
    const response = await axios.get(`http://localhost:3000/companies?username=${username}`);
    return response.data[0]; // Предполагаем, что возвращается массив, берем первый элемент
  };

  return {
    companies,
    getCompanyByUsername,
  };
});
