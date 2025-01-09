import { defineStore } from "pinia";

export const TokenStore = defineStore("TokenStore", {
  state: () => ({
    token: localStorage.getItem("auth_token") || "",
    userId: localStorage.getItem("user_id") || "", // Добавлено поле userId
  }),
  actions: {
    setToken(newToken) {
      this.token = newToken;
      localStorage.setItem("auth_token", newToken);
    },
    clearToken() {
      this.token = "";
      localStorage.removeItem("auth_token");
    },
    setUserId(newUserId) { // Метод для установки userId
      this.userId = newUserId;
      localStorage.setItem("user_id", newUserId);
    },
    clearUserId() { // Метод для очистки userId
      this.userId = "";
      localStorage.removeItem("user_id");
    },
  },
});
