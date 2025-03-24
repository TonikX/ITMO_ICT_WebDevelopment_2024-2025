<template>
  <div class="quarterly-report-page">
    <h2 class="page-title">Отчёт о стоимости работ за последний квартал</h2>

    <div v-if="loading" class="loading-message">Загрузка данных...</div>

    <div v-if="reportData" class="report-content">
      <h3>Общая стоимость выполненных работ:</h3>
      <p class="total-cost">{{ formattedTotalCost }}</p>
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
const reportData = ref(null);
const formattedTotalCost = ref('');

const fetchQuarterlyReport = async () => {
  try {
    const response = await api.get('/quarterly-report/');
    reportData.value = response.data;
    formattedTotalCost.value = formatCost(response.data.total_cost);
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

onMounted(() => {
  fetchQuarterlyReport();
});
</script>

<style scoped>
.quarterly-report-page {
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

.report-content {
  text-align: center;
  margin-top: 30px;
}

.report-content h3 {
  font-size: 1.5rem;
  font-weight: 600;
  color: #333;
}

.total-cost {
  font-size: 2rem;
  font-weight: 700;
  color: #4CAF50;
  margin-top: 15px;
}

.error-message {
  color: red;
}

</style>
