<template>
  <div class="delivery-page">
    <Header />
    <h2>Доставки</h2>
    <div>
      <button v-if="isAdminOrEmployee" class="add-button" @click="openForm">Добавить доставку</button>
    </div>
    <table class="delivery-table">
      <thead>
        <tr>
          <th>Газета</th>
          <th>Типография</th>
          <th>Почтовое отделение</th>
          <th>Количество</th>
          <th>Дата доставки</th>
          <th>Статус</th>
          <th v-if="isAdminOrEmployee">Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="delivery in deliveries" :key="delivery.id">
          <td>{{ delivery.newspaper_name || delivery.newspaper }}</td>
          <td>{{ delivery.printshop_name || delivery.printshop }}</td>
          <td>{{ delivery.post_office_name || delivery.post_office }}</td>
          <td>{{ delivery.quantity }}</td>
          <td>{{ delivery.delivery_date }}</td>
          <td>{{ delivery.status }}</td>
          <td v-if="isAdminOrEmployee">
            <button @click="openEditForm(delivery)">Редактировать</button>
            <button @click="deleteDelivery(delivery.id)">Удалить</button>
          </td>
        </tr>
      </tbody>
    </table>
    <DeliveryForm
      v-if="isFormVisible"
      :delivery="selectedDelivery"
      @save="saveDelivery"
      @cancel="closeForm"
    />
  </div>
</template>

<script>
import Header from "../components/Header.vue";
import DeliveryForm from "../components/DeliveryForm.vue";
import { getDeliveries, addDelivery, updateDelivery, deleteDelivery } from "../api/api";

export default {
  components: {
    Header,
    DeliveryForm,
  },
  data() {
    return {
      deliveries: [],
      isFormVisible: false,
      selectedDelivery: null,
    };
  },
  computed: {
    isAdminOrEmployee() {
      const role = localStorage.getItem("role");
      return role === "admin" || role === "employee";
    },
  },
  methods: {
    async fetchDeliveries() {
      try {
        const response = await getDeliveries();
        this.deliveries = response.data;
      } catch (error) {
        console.error("Ошибка загрузки доставок:", error);
      }
    },
    openForm() {
      this.selectedDelivery = null;
      this.isFormVisible = true;
    },
    openEditForm(delivery) {
      this.selectedDelivery = { ...delivery };
      this.isFormVisible = true;
    },
    closeForm() {
      this.isFormVisible = false;
      this.selectedDelivery = null;
    },
    saveDelivery(delivery) {
  if (delivery.id) {
    this.editDelivery(delivery); // Редактирование доставки
  } else {
    this.createDelivery(delivery); // Добавление новой доставки
  }
  this.closeForm();
},
    async deleteDelivery(id) {
      try {
        if (confirm("Вы уверены, что хотите удалить эту доставку?")) {
          await deleteDelivery(id);
          this.fetchDeliveries();
        }
      } catch (error) {
        console.error("Ошибка удаления доставки:", error);
      }
    },
  },
  mounted() {
    this.fetchDeliveries();
  },
};
</script>

<style scoped>
.delivery-page {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px;
}

.delivery-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.delivery-table th,
.delivery-table td {
  border: 1px solid #ddd;
  padding: 10px;
  text-align: center;
}

.delivery-table th {
  background-color: #f4f4f4;
}

.add-button {
  background-color: #4caf50;
  color: white;
  border: none;
  padding: 10px 15px;
  cursor: pointer;
  font-size: 16px;
  border-radius: 5px;
}

.add-button:hover {
  background-color: #45a049;
}
</style>
