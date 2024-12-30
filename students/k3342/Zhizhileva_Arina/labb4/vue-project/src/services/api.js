import axios from 'axios';

const API_URL = 'http://localhost:8000/api/';

export const register = (username, password, email) => {
  return axios.post(`${API_URL}register/`, {
    email,
    password,
  });
};

export const login = (username, password) => {
  return axios.post(`${API_URL}login/`, {
    username,
    password
  });
};
