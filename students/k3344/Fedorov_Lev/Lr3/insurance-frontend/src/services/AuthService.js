import axios from 'axios';

const API_URL = 'http://localhost:8000/insurance/';
const LOGIN_URL = 'http://localhost:8000/auth/';

const AuthService = {
  async login(username, password) {
    try {
      const response = await axios.post(`${LOGIN_URL}token/`, {
        username,
        password,
      });
      console.log('Ответ логина:', response.data);
      this.setTokens(response.data);
      return response.data;
    } catch (error) {
      console.error('Ошибка логина:', error.response?.data || error);
      throw error;
    }
  },

  async register(user) {
    try {
      const registerResponse = await axios.post(`${API_URL}register/`, user);
      console.log('Ответ регистрации:', registerResponse.data);
      return await this.login(user.username, user.password);
    } catch (error) {
      console.error('Ошибка регистрации:', error.response?.data || error);
      throw error;
    }
  },

  async refreshToken() {
    const refreshToken = localStorage.getItem('refreshToken');
    if (!refreshToken) {
      console.error('Отсутствует refreshToken');
      throw new Error('Refresh token отсутствует');
    }

    try {
      const response = await axios.post(`${LOGIN_URL}token/refresh/`, {
        refresh: refreshToken,
      });
      if (response.data.access) {
        console.log('Токен успешно обновлён');
        this.setTokens(response.data);
      }
      return response.data;
    } catch (error) {
      console.error('Ошибка обновления токена:', error.response?.data || error);
      this.logout();
      window.location.href = '/login';
      throw error;
    }
  },

  logout() {
    localStorage.removeItem('token');
    localStorage.removeItem('refreshToken');
    window.location.href = '/login';
  },

  setTokens(tokens) {
    localStorage.setItem('token', tokens.access);
    if (tokens.refresh) {
      localStorage.setItem('refreshToken', tokens.refresh);
    }
  },

  isAuthenticated() {
    return !!localStorage.getItem('token');
  },
};

export default AuthService;