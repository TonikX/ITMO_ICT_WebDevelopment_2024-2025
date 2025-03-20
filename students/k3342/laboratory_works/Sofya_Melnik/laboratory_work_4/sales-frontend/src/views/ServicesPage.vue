<template>
  <div class="services-page">
    <h2 class="page-title">Рекламные услуги и прайс-лист</h2>
    <table class="services-table">
      <thead>
        <tr>
          <th>Название услуги</th>
          <th>Цена</th>
          <th>Единица измерения</th>
          <th>Материалы</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="serviceItem in services" :key="serviceItem.id">
          <td>{{ serviceItem.service.name }}</td>
          <td>{{ serviceItem.price }}</td>
          <td>{{ serviceItem.service.unit }}</td>
          <td>{{ serviceItem.service.materials }}</td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/api';

const services = ref([]);

const fetchServices = async () => {
  try {
    const { data } = await api.get('price-list/');
    services.value = data;
  } catch (error) {
    console.error("Ошибка загрузки услуг:", error);
  }
};

onMounted(fetchServices);
</script>

<style scoped>
.services-page {
  max-width: 1000px;
  margin: 40px auto;
  padding: 30px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
  font-family: 'Arial', sans-serif;
}

.page-title {
  font-size: 28px;
  font-weight: bold;
  color: #333;
  margin-bottom: 20px;
  text-align: center;
}

.services-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

th, td {
  border: 1px solid #ddd;
  padding: 12px;
  text-align: left;
  font-size: 16px;
}

th {
  background-color: #4CAF50;
  color: white;
  font-weight: bold;
}

tbody tr:nth-child(even) {
  background-color: #f2f2f2;
}

tbody tr:hover {
  background-color: #e0e0e0;
  cursor: pointer;
}

@media (max-width: 768px) {
  .services-page {
    padding: 15px;
  }
  th, td {
    font-size: 14px;
    padding: 10px;
  }
}
</style>
