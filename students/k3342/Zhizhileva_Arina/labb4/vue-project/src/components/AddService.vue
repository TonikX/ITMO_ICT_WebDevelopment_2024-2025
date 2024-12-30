<template>
  <div>
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
/* Стили для формы и кнопок */
.form-container {
  max-width: 500px;
  margin: 0 auto;
}

.form-group {
  margin-bottom: 15px;
}

input[type="text"],
input[type="number"],
textarea {
  width: 100%;
  padding: 10px;
  margin-top: 5px;
  border: 1px solid #ccc;
  border-radius: 5px;
}

textarea {
  resize: vertical;
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
