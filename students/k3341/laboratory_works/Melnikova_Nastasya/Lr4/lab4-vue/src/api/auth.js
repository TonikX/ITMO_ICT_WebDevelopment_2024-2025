import axios from "axios";

const authHttp = axios.create({
  baseURL: "http://127.0.0.1:8000/auth/",
  headers: {
    "Content-Type": "application/json",
  },
});

authHttp.interceptors.request.use((config) => {
  const token = localStorage.getItem("token");
  if (token) config.headers.Authorization = `Token ${token}`;
  return config;
});

export const authApi = {
  register({ username, password }) {
    return authHttp.post("users/", { username, password });
  },
  login({ username, password }) {
    return authHttp.post("token/login/", { username, password });
  },
  logout() {
    return authHttp.post("token/logout/");
  },
  me() {
    return authHttp.get("users/me/");
  },
  setPassword({ current_password, new_password }) {
    return authHttp.post("users/set_password/", { current_password, new_password });
  },
  setUsername({ current_password, new_username }) {
    return authHttp.post("users/set_username/", { current_password, new_username });
  },
};