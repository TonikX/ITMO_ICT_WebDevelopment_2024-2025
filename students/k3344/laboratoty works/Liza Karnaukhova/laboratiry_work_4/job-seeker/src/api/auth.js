import axios from 'axios';

const API_URL = 'http://localhost:3000';

class AuthApi {
  constructor(instance) {
    this.instance = instance; // Сохраняем экземпляр axios или другой HTTP-клиент
  }

  async registerUser(registerData) {
    try {
      console.log('Регистрация данных:', registerData); // Отладочное сообщение
      const response = await this.instance.post(`${API_URL}/users`, registerData);
      console.log('Ответ сервера:', response.data); // Отладочное сообщение
      return response.data; // Убедитесь, что возвращаете данные
    } catch (error) {
      console.error('Ошибка регистрации:', error);
      throw error; // Пробрасываем ошибку дальше
    }
  }

  async loginUser(loginData) {
    try {
      const response = await this.instance.get(`${API_URL}/users`, { params: loginData });
      return response.data;
    } catch (error) {
      console.error('Ошибка входа:', error);
      throw error;
    }
  }
}

// Создание экземпляра AuthApi
const instance = axios.create({
  baseURL: API_URL,
});

const authApi = new AuthApi(instance); // Создаем экземпляр AuthApi

export default authApi; // Экспортируем экземпляр
