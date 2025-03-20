<template>
  <div class="services-list-page">
    <h2 class="page-title">Номенклатура услуг</h2>

    <div v-if="loading" class="loading-message">Загрузка данных...</div>

    <div v-if="services && services.length" class="services-list">
      <ul>
        <li v-for="service in services" :key="service.id" class="service-item">
          <div class="service-details">
            <p><strong>Название услуги:</strong> {{ service.name }}</p>
            <p><strong>Единица:</strong> {{ service.unit }}</p>
            <p><strong>Материалы:</strong> {{ service.materials }}</p>

            <p v-if="service.prices && service.prices.length">
              <strong>Цена:</strong>
              {{ formatCost(service.prices[0].price) }}
            </p>
            <p v-else>
              <strong>Цена:</strong> Не указана
            </p>

            <p v-if="service.prices && service.prices.length">
              <strong>Дата начала:</strong> {{ formatDate(service.prices[0].start_price) }}
            </p>
            <p v-if="service.prices && service.prices.length">
              <strong>Дата окончания:</strong> {{ formatDate(service.prices[0].end_price) }}
            </p>
          </div>
        </li>
      </ul>
    </div>

    <div v-if="error" class="error-message">
      Ошибка при загрузке данных. Пожалуйста, попробуйте снова.
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/api';

const loading = ref(true);
const error = ref(false);
const services = ref([]);


const fetchServicesList = async () => {
  try {
    const response = await api.get('/service-list/');
    services.value = response.data;
  } catch (err) {
    error.value = true;
    console.error('Ошибка при загрузке данных:', err);
  } finally {
    loading.value = false;
  }
};


const formatCost = (cost) => {
  if (!cost) return '0 ₽';
  return new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: 'RUB',
  }).format(cost);
};

const formatDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('ru-RU');
};

onMounted(() => {
  fetchServicesList();
});
</script>

<style scoped>
.services-list-page {
  max-width: 1200px;
  margin: 40px auto;
  padding: 20px;
  background-color: #ffffff;
  border-radius: 10px;
  box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
}

.page-title {
  font-size: 2.2rem;
  font-weight: 700;
  color: #333;
  text-align: center;
  margin-bottom: 30px;
  border-bottom: 2px solid #4CAF50;
  padding-bottom: 10px;
}

.loading-message,
.error-message {
  text-align: center;
  font-size: 18px;
  color: #888;
}

.services-list {
  margin-top: 30px;
}

.service-item {
  background-color: #f9f9f9;
  padding: 15px;
  margin: 10px 0;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.service-details p {
  margin: 8px 0;
}

.error-message {
  color: red;
}
</style>
