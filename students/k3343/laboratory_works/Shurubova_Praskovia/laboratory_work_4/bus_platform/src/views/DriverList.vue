<template>
  <div>
    <h1>Список водителей</h1>

    <div class="actions-container">
      <div class="filter-container">
        <label for="class-filter" style="font-size: 16px;">Класс вождения:</label>
        <select id="class-filter" class="filter-select" v-model="selectedClass" @change="filterByClass">
          <option value="">Все классы</option>
          <option v-for="classType in driverClasses" :key="classType">
            {{ classType }}
          </option>
        </select>
      </div>
      <button @click="showModal = true" class="add">Добавить водителя</button>
    </div>

    <table v-if="drivers.length > 0">
      <thead>
        <tr>
          <th>Водитель</th>
          <th>Класс</th>
          <th>Статус</th>
          <th>Маршруты</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="driver in filteredDrivers" :key="driver.id">
          <td>
            <router-link :to="`/drivers/${driver.id}`" class="driver-link">
              {{ driver.name }} {{ driver.surname }}
            </router-link>
          </td>
          <td>{{ driver.driver_class }}</td>
          <td>{{ driver.status }}</td>
          <td>
            <span v-for="(route, index) in driver.routes" :key="route.id">
              {{ route.start_point }} - {{ route.end_point }}<span v-if="index < driver.routes.length - 1">, </span>
            </span>
          </td>
          <td>
            <button @click="deleteDriver(driver.id)" class="delete-btn">Удалить</button>
          </td>
        </tr>
      </tbody>
    </table>

    <p v-else>Данных нет</p>

    <div v-if="showModal" class="modal-overlay">
      <div class="modal-content">
        <button class="modal-close" @click="showModal = false">×</button>
        <!-- Вставляем компонент DriverModal -->
        <DriverModal @close="showModal = false" @driver-added="fetchDrivers" />
      </div>
    </div>
  </div>
</template>


<script>
import axios from 'axios';
import DriverModal from "@/components/DriverModal.vue";
import apiClient from "@/api/axios";

export default {
  components: {
      DriverModal
    },
  data() {
    return {
      drivers: [],
      routes: [],
      selectedRoute: "",
      selectedClass: "",
      showModal: false,
      driverClasses: ["A", "B", "D1", "D"],
    };
  },
  computed: {
    filteredDrivers() {
      return this.drivers.filter(driver => {
        const matchesRoute =
          !this.selectedRoute || driver.routes.some(route => route.id == this.selectedRoute);
        const matchesClass = !this.selectedClass || driver.driver_class === this.selectedClass;
        return matchesRoute && matchesClass;
      });
    },
  },
  methods: {
    async fetchDrivers() {
        try {
            const response = await apiClient.get('/drivers/');
            console.log(response.data);
            this.drivers = response.data;
        } catch (error) {
            console.error('Fetch error:', error.response || error.message);
        }
    },
    async deleteDriver(driverId) {
      // Запрос подтверждения удаления
      const confirmDelete = window.confirm('Вы уверены, что хотите удалить этого водителя?');
      if (!confirmDelete) return;

      try {

        await apiClient.delete(`/drivers/${driverId}/delete/`);

        this.drivers = this.drivers.filter(driver => driver.id !== driverId);

        alert('Водитель успешно удалён!');
      } catch (error) {
        console.error('Ошибка при удалении водителя:', error.response || error.message);
        alert('Не удалось удалить водителя. Попробуйте позже.');
      }
    },
    filterByRoute() {

    },
    filterByClass() {

    },
  },
  async created() {
    await this.fetchDrivers();
  },
};
</script>

<style scoped>

h1 {
  display: flex;
  justify-content: center;
}

.actions-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

label {
  font-size: 16px;
  white-space: nowrap;
}

.filter-container {
  display: flex;
  align-items: center;
  flex-direction: row;
  white-space: nowrap;
  gap: 20px;
}

.filter-select {
  appearance: none;
  width: 100%;
  max-width: 400px;
  padding: 5px 35px 5px 10px;
  border-radius: 6px;
  border: 2px solid #2C3643;
  background-color: white;
  font-size: 16px;
  color: #333;
  cursor: pointer;
  position: relative;
  background-image: url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 20 20'%3E%3Cpath fill='%232C3643' d='M5.5 7l4.5 4.5L14.5 7H5.5z'/%3E%3C/svg%3E");
  background-repeat: no-repeat;
  background-position: right 10px center;
  background-size: 16px 16px;
}

.filter-select:hover {
  border-color: #2C3643;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

table th, table td {
  padding: 8px;
  border: 1px solid #ddd;
  text-align: left;
}

table th {
  background-color: #f4f4f4;
}

.actions-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  margin-right: 10px;
}

.add {
  padding: 5px 10px;
  margin-bottom: 20px;
  border-radius: 6px;
  border: 2px solid #2C3643;
  background-color: transparent;
  color: black;
  cursor: pointer;
}

.add:hover {
  background-color: #2C3643;
  color: white;
}

.delete-btn {
  background-color: transparent;
  border: none;
  cursor: pointer;
  color: red;
}

.btn-text {
  position: absolute;
  width: 1px;
  height: 1px;
  margin: -1px;
  padding: 0;
  overflow: hidden;
  clip: rect(0, 0, 0, 0);
  white-space: nowrap;
  border: 0;
}

.edit-btn, .delete-btn {
  display: flex;
  align-items: center;
  gap: 5px;
}

.edit-btn .btn-text, .delete-btn .btn-text {
  font-size: 14px;
  color: #333;
}

.delete-btn:hover {
  color: darkred;
}

.delete-btn i {
  font-size: 18px;
}


select {
  margin-top: 10px;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100vw;
  height: 100vh;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
}

.modal-content {
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  max-width: 5px;
  width: 10%;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  animation: fadeIn 0.3s ease-in-out;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.modal-close {
  position: absolute;
  top: 10px;
  right: 10px;
  background: transparent;
  border: none;
  font-size: 20px;
  cursor: pointer;
}

</style>

