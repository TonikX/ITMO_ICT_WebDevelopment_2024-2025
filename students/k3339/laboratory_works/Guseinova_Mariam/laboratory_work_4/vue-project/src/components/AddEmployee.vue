<template>
  <div>
    <header class="header">
      <h1 class="header-title">Autoservice</h1>
    </header>
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
        await apiClient.post('/workers/', this.form);
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
/* General Styles */
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
  background-color: #f2f2f2;
}

/* Header Styles */
.header {
  background-color: darkslategray;
  color: white;
  padding: 20px;
  text-align: center;
}

.header-title {
  margin: 0;
  font-size: 24px;
}

/* Content Styles */
.content {
  margin: 20px auto;
  max-width: 600px;
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Buttons */
.back-button,
.submit-button {
  background-color: darkslategray;
  color: white;
  padding: 10px 15px;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  margin-top: 10px;
}

.back-button:hover,
.submit-button:hover {
  background-color: darkslategray;
}

/* Form Styles */
.form-container {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 14px;
}

/* Message Styles */
.message {
  margin-top: 15px;
  color: green;
  font-weight: bold;
}

.message.error {
  color: red;
}
</style>
