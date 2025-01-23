import axios from 'axios';

const API_URL = 'http://localhost:3000';
class ResumesApi {
  constructor(instance) {
    this.API = instance;
  }

  // Получение всех резюме кандидата
  getAll = async () => {
    return this.API({ url: '/resumes' });
  };

  // Создание нового резюме
  createResume = async (data) => {
    return this.API({
      method: 'POST',
      url: '/resumes',
      data,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  };

  // Обновление резюме
  updateResume = async (id, data) => {
    return this.API({
      method: 'PUT',
      url: `/resumes/${id}`,
      data,
      headers: {
        'Content-Type': 'application/json',
      },
    });
  };

  // Удаление резюме
  deleteResume = async (id) => {
    return this.API({
      method: 'DELETE',
      url: `/resumes/${id}`,
    });
  };
}

// Создание экземпляра ResumesApi
const instance = axios.create({
  baseURL: API_URL,
});

const resumesApi = new ResumesApi(instance); // Создаем экземпляр ResumesApi

export default resumesApi; // Экспортируем экземпляр
