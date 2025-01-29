import axios from "axios";

const API_URL = "http://127.0.0.1:8000";
export const getToken = () => {
  const match = document.cookie.match(/(^|;\s*)auth_token=([^;]+)/);
  return match ? match[2] : null;
};

export const setToken = (token: string) => {
  const days = 7;
  const date = new Date();
  date.setTime(date.getTime() + days * 24 * 60 * 60 * 1000);
  const expires = "expires=" + date.toUTCString();
  document.cookie = `auth_token=${token};${expires};path=/`;
};

export const removeToken = () => {
  document.cookie = "auth_token=; Max-Age=-99999999;path=/";
};

export const api = axios.create({
  baseURL: API_URL,
});

api.interceptors.request.use((config) => {
  if (config.url && config.url.includes("/auth/token/login/")) {
    // Не добавляем токен при логине
    return config;
  }

  const currentToken = getToken();

  
  if (currentToken && config.headers) {
    config.headers.Authorization = `Token ${currentToken}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      removeToken();
    }
    return Promise.reject(error);
  }
);
