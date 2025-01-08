<template>
  <div>
    <header class="header">
      <h1 class="header-title">Autoservice</h1>
    </header>
    <button @click="$router.push('/services')" class="back-button">Назад к списку услуг</button>
    <h1>Добавление услуги</h1>
    <form @submit.prevent="addService" class="form-container">
      <div class="form-group">
        <label for="service_name">Название услуги:</label>
        <input type="text" id="service_name" v-model="form.service_name" required />
      </div>
      <div class="form-group">
        <label for="description">Описание:</label>
        <textarea id="description" v-model="form.description"></textarea>
      </div>
      <div class="form-group">
        <label for="price">Цена:</label>
        <input type="number" id="price" v-model="form.price" required />
      </div>
      <button type="submit" class="submit-button">Добавить услугу</button>
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
        service_name: '',
        description: '',
        price: '',
      },
      message: '',
    };
  },
  methods: {
    async addService() {
      try {
        await apiClient.post('/services/', this.form);
        this.message = 'Услуга успешно добавлена!';
        this.form = { service_name: '', description: '', price: '' }; // Очистка формы
      } catch (error) {
        console.error('Ошибка при добавлении услуги:', error);
        this.message = 'Ошибка при добавлении услуги.';
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
.custom-button {
  background-color: darkslategray !important; /* Зеленый цвет кнопок */
  color: white !important;
  margin-bottom: 10px;
  text-transform: none !important; /* Отключение заглавных букв */
  font-size: 16px;
}
</style>