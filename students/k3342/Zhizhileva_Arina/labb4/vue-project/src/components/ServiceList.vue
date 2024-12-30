<template>
  <div>
    <button @click="$router.push('/main')" class="back-button">Назад на главную</button>
    <h1>Список услуг</h1>
    <ul class="service-list">
      <li v-for="service in services" :key="service.service_id" class="service-item">
        <strong>{{ service.service_name }}</strong> - {{ service.price }} руб.
        <p v-if="service.description">{{ service.description }}</p>
      </li>
    </ul>
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
.service-list {
  list-style-type: none;
  padding: 0;
}

.service-item {
  margin: 15px 0;
  font-size: 18px;
}

.add-service-link {
  display: inline-block;
  margin-top: 20px;
  background-color: #4CAF50;
  color: white;
  padding: 10px 15px;
  text-decoration: none;
  text-align: center;
}

.add-service-link:hover {
  background-color: #45a049;
}

strong {
  font-weight: bold;
}
</style>
