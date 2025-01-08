<template>
  <div>
    <header class="header">
      <h1 class="header-title">Autoservice</h1>
    </header>
    <button @click="$router.push('/main')" class="custom-button">Назад на главную</button>
    <h1 class="page-title">Список услуг</h1>

    <div class="service-list-container">
      <ul class="service-list">
        <li v-for="service in services" :key="service.service_id" class="service-item">
          <div class="service-info">
            <strong>{{ service.service_name }}</strong>  {{ service.price }} руб.
            <p v-if="service.description" class="service-description">{{ service.description }}</p>
          </div>
        </li>
      </ul>
    </div>

    <router-link to="/add-service" class="add-service-link">Добавить услугу</router-link>
  </div>
</template>

<script>
import apiClient from '@/services/axios';

export default {
  data() {
    return {
      services: [],
    };
  },
  created() {
    this.fetchServices();
  },
  methods: {
    async fetchServices() {
      try {
        const response = await apiClient.get('/services/');
        this.services = response.data;
      } catch (error) {
        console.error('Ошибка при получении списка услуг:', error);
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

/* Page Title */
.page-title {
  text-align: center;
  margin-top: 20px;
  font-size: 28px;
  color: darkslategray;
}

/* Service List Styles */
.service-list-container {
  background-color: white;
  padding: 20px;
  margin: 20px auto;
  max-width: 600px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.service-list {
  list-style-type: none;
  padding: 0;
}

.service-item {
  margin-bottom: 15px;
  font-size: 18px;
}

.service-info {
  display: flex;
  justify-content: space-between;
}

.service-description {
  margin-top: 10px;
  font-size: 14px;
  color: #666;
}

/* Buttons and Links */
.custom-button,
.add-service-link {
  background-color: darkslategray !important;
  color: white !important;
  padding: 10px 20px;
  font-size: 16px;
  text-transform: none !important;
  border-radius: 5px;
  cursor: pointer;
  display: block;
  width: 100%;
  margin-top: 15px;
  text-align: center;
}

.custom-button:hover,
.add-service-link:hover {
  background-color: #2f4f4f;
}

.add-service-link {
  text-decoration: none;
}

strong {
  font-weight: bold;
}
</style>
