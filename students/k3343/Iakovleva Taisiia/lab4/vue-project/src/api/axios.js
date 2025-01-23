import axios from 'axios';

const apiClient = axios.create({
  baseURL: 'http://127.0.0.1:8000', // Укажите базовый URL вашего API
  headers: {
    'Content-Type': 'application/json',
    Authorization: `Token 3a829d0fd079f700e1b90155922a6117bf734228`, // Замените токен на ваш
  },
});

export default apiClient;
