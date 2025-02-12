<template>
  <div class="container mt-5">
    <div class="row justify-content-center">
      <div class="col-md-6">
        <h2 class="text-center mb-4">Профиль</h2>
        <form @submit.prevent="updateProfile" class="card p-4 shadow">
          <div class="form-group mb-3">
            <label for="username">Имя пользователя:</label>
            <input
              id="username"
              v-model="form.username"
              type="text"
              class="form-control"
              placeholder="Введите имя пользователя"
              required
            />
          </div>
          <div class="form-group mb-3">
            <label for="email">Email:</label>
            <input
              id="email"
              v-model="form.email"
              type="email"
              class="form-control"
              placeholder="Введите email"
              required
            />
          </div>
          <button type="submit" class="btn btn-primary w-100">
            Обновить профиль
          </button>
        </form>
        <button
          @click="logout"
          class="btn btn-danger w-100 mt-3"
        >
          Выйти
        </button>
      </div>
    </div>
  </div>
</template>

<script>
import apiClient from "@/api/axios";

export default {
  data() {
    return {
      form: {
        username: "",
        email: "",
      },
    };
  },
  async created() {
    try {
      const token = localStorage.getItem("authToken");
      const response = await apiClient.get("/auth/users/me/", {
        headers: { Authorization: `Token ${token}` },
      });
      this.form = response.data;
    } catch (error) {
      console.error(error.response?.data || error.message);
      alert("Ошибка при загрузке профиля.");
    }
  },
  methods: {
    async updateProfile() {
      try {
        const token = localStorage.getItem("authToken");
        await apiClient.put("/auth/users/me/", this.form, {
          headers: { Authorization: `Token ${token}` },
        });
        alert("Профиль обновлен!");
      } catch (error) {
        console.error(error.response?.data || error.message);
        alert("Ошибка при обновлении профиля.");
      }
    },
    logout() {
      // Удаление токена из localStorage
      localStorage.removeItem("authToken");

      // Перенаправление на страницу входа
      this.$router.push("/login");
    },
  },
};
</script>

<style scoped>
h2 {
  margin-top: 90px;
}

</style>

