import { http } from "./http";

export async function register(username, password) {
  return http.post("/auth/users/", {
    username,
    password,
    re_password: password,
  });
}

export async function login(username, password) {
  const res = await http.post("/auth/token/login/", { username, password });
  localStorage.setItem("token", res.data.auth_token);
  return res.data;
}

export async function me() {
  return http.get("/auth/users/me/");
}

export function logout() {
  localStorage.removeItem("token");
}
