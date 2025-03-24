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

      <button type="submit" class="submit-button">Обновить пароль</button>
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

<style scoped>

label {
  font-size: 16px;
  color: #555;
  margin-bottom: 5px;
}

input {
  padding: 10px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-sizing: border-box;
  width: 100%;
}

input:focus {
  border-color: #007bff;
  outline: none;
}

.submit-button {
  padding: 12px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  font-size: 18px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.submit-button:hover {
  background-color: #0056b3;
}

.success-message {
  color: green;
  margin-top: 15px;
  font-size: 16px;
}

.error-message {
  color: red;
  margin-top: 15px;
  font-size: 16px;
}
</style>
