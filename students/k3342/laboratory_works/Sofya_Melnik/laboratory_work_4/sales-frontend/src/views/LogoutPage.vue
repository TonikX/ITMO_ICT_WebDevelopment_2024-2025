<template>
  <div>
    <h2>Выход</h2>
    <p>Вы действительно хотите выйти?</p>
    <button @click="logout">Выйти</button>
  </div>
</template>

<script>
import api from "@/api";

export default {
  methods: {
    async logout() {
      try {
        await api.post("auth/token/logout/");
      } catch (error) {
        console.error("Ошибка при выходе:", error.response.data);
      }

      localStorage.removeItem("accessToken");
      localStorage.removeItem("refreshToken");

      this.$router.push("/login");
    },
  },
};
</script>
