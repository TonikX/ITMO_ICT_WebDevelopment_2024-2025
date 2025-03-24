<template>
  <div class="payments-page">
    <h2 class="page-title">Платежи</h2>

    <div v-if="isStaff" class="create-payment-button">
      <button @click="showCreateForm = !showCreateForm">{{ showCreateForm ? 'Отменить' : 'Создать новый платеж' }}</button>
    </div>

    <div v-if="isStaff && showCreateForm" class="create-payment-form">
      <h3>Создать новый платеж</h3>
      <form @submit.prevent="createPayment">
        <label for="order">ID заявки:</label>
        <select v-model="newPayment.order" required>
          <option v-for="order in orders" :key="order.id" :value="order.id">
            {{ order.id }} - {{ order.client_name }}
          </option>
        </select>

        <label for="payment_order_date">Дата поручения:</label>
        <input type="datetime-local" v-model="newPayment.payment_order_date" required />

        <label for="payment_date">Дата оплаты:</label>
        <input type="datetime-local" v-model="newPayment.payment_date" required />

        <label for="payment_status">Статус:</label>
        <select v-model="newPayment.payment_status" required>
          <option value="waiting">Ожидает</option>
          <option value="paid">Оплачено</option>
        </select>

        <button type="submit">Создать платеж</button>
      </form>
    </div>

    <div v-if="editingPayment" class="edit-payment-form">
      <h3>Редактировать платеж</h3>
      <form @submit.prevent="updatePayment">
        <label for="order">ID заявки:</label>
        <select v-model="editedPayment.order" required>
          <option v-for="order in orders" :key="order.id" :value="order.id">
            {{ order.id }} - {{ order.client_name }}
          </option>
        </select>

        <label for="payment_order_date">Дата поручения:</label>
        <input type="datetime-local" v-model="editedPayment.payment_order_date" required />

        <label for="payment_date">Дата оплаты:</label>
        <input type="datetime-local" v-model="editedPayment.payment_date" required />

        <label for="payment_status">Статус:</label>
        <select v-model="editedPayment.payment_status" required>
          <option value="waiting">Ожидает</option>
          <option value="paid">Оплачено</option>
        </select>

        <button type="submit">Сохранить изменения</button>
      </form>
      <button @click="cancelEdit">Отменить</button>
    </div>

    <table class="payments-table">
      <thead>
        <tr>
          <th>ID поручения</th>
          <th>ID заявки</th>
          <th>Статус поручения</th>
          <th>Дата поручения</th>
          <th>Дата оплаты</th>
          <th v-if="isStaff">Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="payment in payments" :key="payment.id">
          <td>{{ payment.id }}</td>
          <td>{{ payment.order }}</td>
          <td>{{ payment.payment_status }}</td>
          <td>{{ payment.payment_order_date }}</td>
          <td>{{ payment.payment_date }}</td>
          <td v-if="isStaff">
            <button @click="editPayment(payment)">Редактировать</button>
            <button @click="deletePayment(payment.id)">Удалить</button>
          </td>
        </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import api from '@/api';

export default {
  name: "PaymentsPage",
  setup() {
    const payments = ref([]);
    const orders = ref([]);
    const isStaff = ref(false);
    const showCreateForm = ref(false);
    const editingPayment = ref(false);
    const newPayment = ref({
      order: null,
      payment_order_date: '',
      payment_date: '',
      payment_status: 'waiting'
    });
    const editedPayment = ref({
      id: null,
      order: null,
      payment_order_date: '',
      payment_date: '',
      payment_status: 'waiting'
    });

    const fetchUserInfo = async () => {
      try {
        const { data } = await api.get("auth/users/me/");
        isStaff.value = data.is_staff;
      } catch (error) {
        console.error("Ошибка загрузки информации о пользователе:", error.response.data);
      }
    };

    const fetchOrders = async () => {
      try {
        const { data } = await api.get("orders/");
        orders.value = data;
      } catch (error) {
        console.error("Ошибка загрузки заказов:", error.response.data);
      }
    };

    const fetchPayments = async () => {
      try {
        const { data } = await api.get("/payment-orders/");
        payments.value = data;
      } catch (error) {
        console.error("Ошибка загрузки платежей:", error.response.data);
      }
    };

    const createPayment = async () => {
      try {
        const { data } = await api.post("/payment-orders/", newPayment.value);
        payments.value.push(data);
        newPayment.value = { order: null, payment_order_date: '', payment_date: '', payment_status: 'waiting' };
        showCreateForm.value = false;
      } catch (error) {
        console.error("Ошибка создания платежа:", error.response.data);
      }
    };

    const editPayment = (payment) => {
      editingPayment.value = true;
      editedPayment.value = { ...payment };
    };

    const cancelEdit = () => {
      editingPayment.value = false;
      editedPayment.value = { id: null, order: null, payment_order_date: '', payment_date: '', payment_status: 'waiting' };
    };

    const updatePayment = async () => {
      try {
        const { data } = await api.put(`payment-orders/${editedPayment.value.id}/`, editedPayment.value);
        const index = payments.value.findIndex(payment => payment.id === data.id);
        if (index !== -1) {
          payments.value[index] = data;
        }
        editingPayment.value = false;
      } catch (error) {
        console.error("Ошибка обновления платежа:", error.response.data);
      }
    };

    const deletePayment = async (paymentId) => {
      try {
        await api.delete(`payment-orders/${paymentId}/`);
        payments.value = payments.value.filter(payment => payment.id !== paymentId);
      } catch (error) {
        console.error("Ошибка удаления платежа:", error.response.data);
      }
    };

    onMounted(async () => {
      await fetchUserInfo();
      await fetchOrders();
      await fetchPayments();
    });

    return { payments, orders, isStaff, showCreateForm, editingPayment, newPayment, editedPayment, createPayment, editPayment, cancelEdit, updatePayment, deletePayment };
  }
};
</script>


<style scoped>

.payments-page {
  background-color: #f4f6f9;
  padding: 20px;
  font-family: Arial, sans-serif;
}

.page-title {
  color: #333;
  font-size: 24px;
  margin-bottom: 20px;
}


.payments-table {
  width: 100%;
  border-collapse: collapse;
  background-color: #fff;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  margin-top: 20px;
}

.payments-table th,
.payments-table td {
  padding: 12px;
  text-align: left;
  border-bottom: 1px solid #ddd;
}


.payments-table tr:nth-child(even) {
  background-color: #f9f9f9;
}

.payments-table th {
  background-color: #4CAF50;
  color: white;
  font-weight: bold;
}


.payments-table tr:hover {
  background-color: #f1f1f1;
  cursor: pointer;
}


@media (max-width: 768px) {
  .payments-table th, .payments-table td {
    font-size: 14px;
    padding: 8px;
  }
}


.create-payment-button {
  margin-bottom: 20px;
}

.create-payment-form {
  margin-bottom: 20px;
}

.create-payment-form label {
  display: block;
  margin: 10px 0 5px;
}

.create-payment-form input, .create-payment-form select {
  width: 100%;
  padding: 8px;
  margin-bottom: 15px;
  border: 1px solid #ddd;
}

.create-payment-form button {
  padding: 10px 20px;
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
}

.create-payment-form button:hover {
  background-color: #45a049;
}
</style>
