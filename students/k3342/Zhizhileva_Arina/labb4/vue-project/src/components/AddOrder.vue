<template>
  <div>
    <h1>Создание нового заказа</h1>
    <form @submit.prevent="createOrder">
      <div>
        <label for="customer">Клиент (ID):</label>
        <input type="text" v-model="form.customer" required placeholder="Введите ID клиента" />
      </div>

      <div>
        <label for="car">Автомобиль (ID):</label>
        <input type="text" v-model="form.car" required placeholder="Введите ID автомобиля" />
      </div>

      <div>
        <label for="employee">Сотрудник (ID):</label>
        <input type="text" v-model="form.employee" required placeholder="Введите ID сотрудника" />
      </div>

      <div>
        <label for="status">Статус:</label>
        <select v-model="form.status" required>
          <option value="in_progress">В процессе</option>
          <option value="completed">Завершен</option>
        </select>
      </div>

      <div>
        <label for="total_cost">Итоговая стоимость:</label>
        <input type="number" v-model="form.total_cost" required placeholder="Введите итоговую стоимость" />
      </div>

      <div>
        <label for="order_date">Дата заказа:</label>
        <input type="datetime-local" v-model="form.order_date" required />
      </div>

      <button type="submit">Создать заказ</button>
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
        customer: '',
        car: '',
        employee: '',
        status: 'in_progress',
        total_cost: 0.0,
        order_date: '',
      },
      message: '',
    };
  },
  methods: {
    async createOrder() {
      try {
        this.form.order_date = new Date(this.form.order_date).toISOString().slice(0, 16);
        const response = await apiClient.post('/orders/', this.form);

        if (response.status === 201) {
          this.message = 'Заказ успешно создан!';
          this.form = {customer: '', car: '', employee: '', status: 'in_progress', total_cost: 0.0, order_date: ''};
        }
      } catch (error) {
        console.error('Ошибка при создании заказа:', error);
        this.message = 'Ошибка при создании заказа.';
      }
    },
  },
};
</script>

<style scoped>
/* Добавьте стили по мере необходимости */
</style>
