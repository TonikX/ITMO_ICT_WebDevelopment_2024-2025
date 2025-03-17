<template>
  <div class="quarterly-report-page">
    <h2 class="page-title">Отчёт о стоимости работ за последний квартал</h2>

    <!-- Показать сообщение о загрузке данных -->
    <div v-if="loading" class="loading-message">Загрузка данных...</div>

    <!-- Показать отчет о стоимости работ -->
    <div v-if="reportData" class="report-content">
      <h3>Общая стоимость выполненных работ:</h3>
      <p class="total-cost">{{ formattedTotalCost }}</p>
    </div>

    <!-- Показать ошибку, если не удалось загрузить данные -->
    <div v-if="error" class="error-message">
      Ошибка при загрузке данных. Пожалуйста, попробуйте снова.
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/api'; // Импортируем настроенный экземпляр Axios

const loading = ref(true); // Флаг для отслеживания загрузки данных
const error = ref(false); // Флаг для отслеживания ошибки при загрузке
const reportData = ref(null); // Для хранения данных отчета
const formattedTotalCost = ref(''); // Для форматирования общей стоимости

// Метод для загрузки данных с API
const fetchQuarterlyReport = async () => {
  try {
    const response = await api.get('/quarterly-report/'); // Замените на реальный эндпоинт
    reportData.value = response.data;
    formattedTotalCost.value = formatCost(response.data.total_cost); // Форматируем стоимость
  } catch (err) {
    error.value = true; // В случае ошибки загрузки
    console.error('Ошибка при загрузке данных:', err); // Дополнительная отладочная информация
  } finally {
    loading.value = false; // Загрузка завершена
  }
};

// Метод для форматирования стоимости с разделением на тысячи
const formatCost = (cost) => {
  if (!cost) return '0 ₽';
  return new Intl.NumberFormat('ru-RU', {
    style: 'currency',
    currency: 'RUB',
  }).format(cost);
};

// Загружаем данные при монтировании компонента
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
