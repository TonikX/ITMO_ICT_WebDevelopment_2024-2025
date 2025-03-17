<template>
  <div>
    <h2>Выход</h2>
    <p>Вы действительно хотите выйти?</p>
    <button @click="logout">Выйти</button>
  </div>
</template>

<script>
import api from "@/api"; // Axios instance

export default {
  methods: {
    async logout() {
      try {
        await api.post("auth/token/logout/"); // Отправляем запрос на logout
      } catch (error) {
        console.error("Ошибка при выходе:", error.response.data);
      }

      // Удаляем токены из локального хранилища
      localStorage.removeItem("accessToken");
      localStorage.removeItem("refreshToken");

      // Перенаправляем на страницу входа
      this.$router.push("/login");
    },
  },
};
</script>
