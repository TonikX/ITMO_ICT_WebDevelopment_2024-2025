<template>
  <div>
    <button @click="$router.push('/payments/')" class="back-button">Назад</button>
    <h1>Создание записи об оплате</h1>
    <form @submit.prevent="createPayment">
      <div>
        <label for="order_id">Номер заказа:</label>
        <input type="number" v-model="form.order_id" required />
      </div>

      <div v-if="order">
        <p>Заказ найден: {{ order.order_id }} - Статус: {{ order.status }}</p>
      </div>
      <div v-else>
        <p v-if="form.order_id">Заказ с таким номером не найден.</p>
      </div>

      <div>
        <label for="payment_method">Метод оплаты:</label>
        <input type="text" v-model="form.payment_method" required />
      </div>

      <div>
        <label for="payment_amount">Сумма оплаты:</label>
        <input type="number" v-model="form.payment_amount" required />
      </div>

      <button type="submit">Создать запись об оплате</button>
    </form>

    <p v-if="message">{{ message }}</p>
  </div>
</template>

<script>
import apiClient from '@/services/axios';

export default {
  data() {
    return {
      form: {
        order_id: '',
        payment_method: '',
        payment_amount: 0.0,
      },
      order: null,
      message: '',
    };
  },
  watch: {
    'form.order_id': 'fetchOrder',
  },
  methods: {
    async fetchOrder() {
      if (this.form.order_id) {
        try {
          // Проверяем URL и ID
          console.log(`Запрос к /orders/${this.form.order_id}/`);

          const response = await apiClient.get(`/orders/${this.form.order_id}/`);
          this.order = response.data;
          console.log('Информация о заказе:', this.order);
        } catch (error) {
          console.error('Ошибка при получении заказа:', error);
          this.order = null;
          if (error.response) {
            console.error('Ответ от сервера:', error.response.data);
            console.error('Статус ошибки:', error.response.status);
          }
        }
      } else {
        this.order = null;
      }
    },
    async createPayment() {
      if (!this.order) {
        this.message = 'Невозможно создать запись об оплате. Заказ не найден.';
        return;
      }

      try {
        const response = await apiClient.post('/payments/', {
          order: this.order.order_id,
          payment_method: this.form.payment_method,
          payment_amount: this.form.payment_amount,
        });
        if (response.status === 201) {
          this.message = 'Запись об оплате успешно создана!';
          this.form = {order_id: '', payment_method: '', payment_amount: 0.0}; // Очистка формы
        }
      } catch (error) {
        console.error('Ошибка при создании записи об оплате:', error);
        this.message = 'Ошибка при создании записи об оплате.';
      }
    },
  },
};
</script>

<style scoped>
/* Добавьте стили для кнопки и других элементов, если необходимо */
.back-button {
  background-color: #4CAF50;
  color: white;
  padding: 10px 15px;
  border: none;
  cursor: pointer;
  text-align: center;
  margin: 20px 0;
}

.back-button:hover {
  background-color: #45a049;
}
</style>
