<template>
  <div>
    <button @click="$router.push('/employees')" class="back-button">Назад к списку сотрудников</button>
    <h1>Добавление нового сотрудника</h1>
    <form @submit.prevent="addEmployee" class="form-container">
      <div class="form-group">
        <label for="name">Имя:</label>
        <input type="text" id="name" v-model="form.name" required />
      </div>
      <div class="form-group">
        <label for="position">Должность:</label>
        <input type="text" id="position" v-model="form.position" required />
      </div>
      <div class="form-group">
        <label for="phone">Телефон:</label>
        <input type="text" id="phone" v-model="form.phone" required />
      </div>
      <div class="form-group">
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="form.email" required />
      </div>
      <button type="submit" class="submit-button">Добавить сотрудника</button>
    </form>
    <p v-if="message" class="message">{{ message }}</p>
  </div>
</template>

<script>
import apiClient from '@/services/axios';

export default {
  data() {
    return {
      form: {
        name: '',
        position: '',
        phone: '',
        email: '',
      },
      message: '',
    };
  },
  methods: {
    async addEmployee() {
      try {
        await apiClient.post('/employees/', this.form);
        this.message = 'Сотрудник успешно добавлен!';
        this.form = {name: '', position: '', phone: '', email: ''}; // Очистить форму
      } catch (error) {
        console.error('Ошибка при добавлении сотрудника:', error);
        this.message = 'Ошибка при добавлении сотрудника.';
      }
    },
  },
};
</script>

<style scoped>
/* Стили для формы и кнопок */
.form-container {
  max-width: 500px;
  margin: 0 auto;
}

.form-group {
  margin-bottom: 15px;
}

input[type="text"],
input[type="email"] {
  width: 100%;
  padding: 10px;
  margin-top: 5px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

.submit-button {
  background-color: #4CAF50;
  color: white;
  padding: 10px 15px;
  border: none;
  cursor: pointer;
  width: 100%;
  font-size: 16px;
}

.submit-button:hover {
  background-color: #45a049;
}

.message {
  margin-top: 20px;
  color: green;
  font-weight: bold;
}
</style>
