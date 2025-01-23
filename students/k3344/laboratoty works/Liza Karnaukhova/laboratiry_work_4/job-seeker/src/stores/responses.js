import { ref } from 'vue';
import { defineStore } from 'pinia';
import axios from 'axios';

export const useResponsesStore = defineStore('responses', () => {
  const responses = ref([]);

  // Получение всех откликов с данными резюме
  const getAllResponsesWithResumes = async () => {
    const [responsesRes, resumesRes] = await Promise.all([
      axios.get('http://localhost:3000/responses'),
      axios.get('http://localhost:3000/resumes')
    ]);

    // Объединяем данные откликов с данными резюме
    responses.value = responsesRes.data.map(response => {
      const resume = resumesRes.data.find(r => r.id === response.resumeId);
      return {
        ...response,
        experience: resume?.experience || 'Не указано',
        education: resume?.education || 'Не указано',
        skills: resume?.skills || 'Не указано'
      };
    });

    return responses.value;
  };

  // Удаление отклика
  const deleteResponse = async (responseId) => {
    await axios.delete(`http://localhost:3000/responses/${responseId}`);
    responses.value = responses.value.filter(response => response.id !== responseId);
  };

  return {
    responses,
    getAllResponsesWithResumes,
    deleteResponse,
  };
});
