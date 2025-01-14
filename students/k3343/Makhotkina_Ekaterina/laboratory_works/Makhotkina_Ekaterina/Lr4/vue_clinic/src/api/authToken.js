import axios from 'axios';

const BASE_URL = 'http://127.0.0.1:8000/auth/token/login/';

export default {
  login(credentials) {
    return axios.post(BASE_URL, credentials)
      .then(response => {
        const token = response.data.auth_token;
        console.log('Token:', token);
        localStorage.setItem('token', token);
        return token;
      })
      .catch(error => {
        console.error('Ошибка при логине:', error);
        throw error;
      });
  },
  logout() {
    localStorage.removeItem('token');
  },
};
