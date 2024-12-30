<template>
  <div>
    <button @click="$router.push('/customers')" class="back-button">Назад к списку клиентов</button>
    <h1>Добавление нового клиента</h1>
    <form @submit.prevent="addCustomer" class="form-container">
      <div class="form-group">
        <label for="name">Имя:</label>
        <input type="text" id="name" v-model="form.name" required />
      </div>
      <div class="form-group">
        <label for="phone">Телефон:</label>
        <input type="text" id="phone" v-model="form.phone" required />
      </div>
      <div class="form-group">
        <label for="email">Email:</label>
        <input type="email" id="email" v-model="form.email" required />
      </div>
      <div class="form-group">
        <label for="address">Адрес:</label>
        <textarea id="address" v-model="form.address"></textarea>
      </div>
      <button type="submit" class="submit-button">Добавить клиента</button>
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
        phone: '',
        email: '',
        address: '',
      },
      message: '',
    };
  },
  methods: {
    async addCustomer() {
      try {
        await apiClient.post('/customers/', this.form);
        this.message = 'Клиент успешно добавлен!';
        this.form = { name: '', phone: '', email: '', address: '' }; // Очистить форму
      } catch (error) {
        console.error('Ошибка при добавлении клиента:', error);
        this.message = 'Ошибка при добавлении клиента.';
      }
    },
  },
};
</script>

<style scoped>
.form-container {
  max-width: 500px;
  margin: 0 auto;
}

.form-group {
  margin-bottom: 15px;
}

input[type="text"],
input[type="email"],
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
