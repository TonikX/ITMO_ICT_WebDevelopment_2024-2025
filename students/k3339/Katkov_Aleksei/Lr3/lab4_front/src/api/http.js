import axios from "axios";

export const http = axios.create({
  baseURL: "http://127.0.0.1:8000",
});

http.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) {
    config.headers.Authorization = `Token ${token}`;
  }
  return config;
});
