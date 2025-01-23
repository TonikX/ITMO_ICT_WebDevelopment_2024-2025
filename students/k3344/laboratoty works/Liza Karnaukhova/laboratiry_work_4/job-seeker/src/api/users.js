import axios from 'axios';

const API_URL = 'http://localhost:3000';
class UsersApi {
  constructor(instance) {
    this.API = instance;
  }

  getProfile = async () => this.API({ url: '/users' });

  updateProfile = async (data) =>
    this.API({
      method: 'PUT',
      url: '/users',
      data,
      headers: { 'Content-Type': 'application/json' },
    });

  getRole = async () => this.API({ url: '/users/role' });
}

// Создание экземпляра UsersApi
const instance = axios.create({
  baseURL: API_URL,
});

const usersApi = new UsersApi(instance); // Создаем экземпляр UsersApi

export default usersApi; // Экспортируем экземпляр
