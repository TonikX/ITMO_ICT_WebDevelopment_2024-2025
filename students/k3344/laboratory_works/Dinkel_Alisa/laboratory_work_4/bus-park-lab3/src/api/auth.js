import axios from 'axios';

const API_URL = 'http://127.0.0.1:8000/auth/';

// Регистрация пользователя
export const registerUser = (newUser) => {
  return axios.post(`${API_URL}users/`, newUser)
    .then(response => response.data)
    .catch(error => {
      console.error('Ошибка регистрации:', error);
      throw error;
    });
};

// Вход пользователя
export const loginUser = (credentials) => {
  return axios.post(`${API_URL}token/login/`, credentials)
    .then(response => {
      localStorage.setItem('authToken', response.data.auth_token); // Сохраняем токен в localStorage
      return response.data;
    })
    .catch(error => {
      console.error('Ошибка входа:', error);
      throw error;
    });
};

// Выход пользователя
export const logoutUser = () => {
  const token = localStorage.getItem('authToken');
  return axios.post(`${API_URL}token/logout/`, {}, {
    headers: {
      Authorization: `Token ${token}`
    }
  })
    .then(() => {
      localStorage.removeItem('authToken'); // Удаляем токен
      console.log('Пользователь вышел');
    })
    .catch(error => {
      console.error('Ошибка выхода:', error);
      throw error;
    });
};
