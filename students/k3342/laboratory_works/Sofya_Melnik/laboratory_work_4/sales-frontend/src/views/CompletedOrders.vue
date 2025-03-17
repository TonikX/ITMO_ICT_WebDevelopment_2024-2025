<template>
  <div class="completed-orders-page">
    <h2 class="page-title">Список выполненных работ</h2>

    <!-- Показать сообщение о загрузке данных -->
    <div v-if="loading" class="loading-message">Загрузка данных...</div>

    <!-- Показать список выполненных работ -->
    <div v-if="orders && orders.length" class="orders-list">
      <ul>
        <li v-for="order in orders" :key="order.id" class="order-item">
          <div class="order-details">
            <p><strong>Номер заявки:</strong> {{ order.id }}</p>
            <!-- <p><strong>Клиент:</strong> {{ order.client.name }}</p> -->
            <p><strong>Услуга:</strong> {{ order.service.name }}</p>
            <!-- <p><strong>Сотрудник:</strong> {{ order.employee.name }}</p> -->
            <p><strong>Дата выполнения:</strong> {{ order.completion_date }}</p>
            <p><strong>Стоимость:</strong> {{ formatCost(order.total_cost) }}</p>
          </div>
        </li>
      </ul>
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
const orders = ref([]); // Для хранения данных о выполненных работах

// Метод для загрузки данных с API
const fetchCompletedOrders = async () => {
  try {
    const response = await api.get('/completed-orders/'); // Замените на реальный эндпоинт
    orders.value = response.data; // Сохраняем список заказов
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
  fetchCompletedOrders();
});
</script>

<style scoped>
.completed-orders-page {
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

.orders-list {
  margin-top: 30px;
}

.order-item {
  background-color: #f9f9f9;
  padding: 15px;
  margin: 10px 0;
  border-radius: 8px;
  box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}

.order-details p {
  margin: 8px 0;
}

.error-message {
  color: red;
}

</style>
