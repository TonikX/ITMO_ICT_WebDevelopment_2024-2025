<template>
  <div>
    <h2>Смена пароля</h2>
    <form @submit.prevent="changePassword">
      <label>Старый пароль:</label>
      <input v-model="currentPassword" type="password" required />

      <label>Новый пароль:</label>
      <input v-model="newPassword" type="password" required />

      <label>Подтвердите новый пароль:</label>
      <input v-model="confirmPassword" type="password" required />

      <button type="submit">Обновить пароль</button>
    </form>

    <p v-if="message" class="success-message">{{ message }}</p>
    <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
  </div>
</template>

<script>
import api from "@/api";

export default {
  data() {
    return {
      currentPassword: "",
      newPassword: "",
      confirmPassword: "",
      message: "",
      errorMessage: "",
    };
  },
  methods: {
    async changePassword() {
      if (this.newPassword !== this.confirmPassword) {
        this.errorMessage = "Новые пароли не совпадают!";
        return;
      }

      try {
        await api.post("auth/users/set_password/", {
          current_password: this.currentPassword,
          new_password: this.newPassword,
        });
        this.message = "Пароль успешно изменен!";
        this.errorMessage = "";
      } catch (error) {
        this.errorMessage = "Ошибка: " + JSON.stringify(error.response.data);
        this.message = "";
      }
    },
  },
};
</script>

<style>
.success-message {
  color: green;
}
.error-message {
  color: red;
}
</style>
