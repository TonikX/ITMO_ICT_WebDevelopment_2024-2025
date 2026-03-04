import { defineStore } from "pinia";
import { ref, computed } from "vue";
import { authApi } from "../api/auth";

export const useAuthStore = defineStore("auth", () => {
  const token = ref(localStorage.getItem("token") || null);
  const user = ref(null);

  const isAuthenticated = computed(() => !!token.value);

  async function login(username, password) {
    const response = await authApi.login(username, password);

    token.value = response.data.auth_token;
    localStorage.setItem("token", token.value);

    await fetchUser();
  }

  async function register(username, password) {
    return await authApi.register(username, password);
  }

  async function logout() {
    try {
      await authApi.logout();
    } catch (e) {}

    token.value = null;
    user.value = null;
    localStorage.removeItem("token");
  }

  async function fetchUser() {
    if (!token.value) return;
    const response = await authApi.me();
    user.value = response.data;
  }

  async function changePassword(current_password, new_password) {
    // Djoser: /auth/users/set_password/
    await authApi.setPassword(current_password, new_password);
  }

  async function changeUsername(new_username, current_password) {
    // Djoser: /auth/users/set_username/
    await authApi.setUsername(new_username, current_password);
    await fetchUser();
  }

  return {
    token,
    user,
    isAuthenticated,
    login,
    register,
    logout,
    fetchUser,
    changePassword,
    changeUsername,
  };
});