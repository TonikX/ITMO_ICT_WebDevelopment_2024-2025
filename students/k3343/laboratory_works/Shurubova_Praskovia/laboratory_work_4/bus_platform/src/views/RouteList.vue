<template>
  <div>
    <h1>Список маршрутов</h1>

    <div class="actions-container">

      <div class="total-duration">
        Общая протяжённость: <strong>{{ totalDuration }} мин</strong>
      </div>

      <button @click="showModal = true" class="add">Добавить маршрут</button>
    </div>

    <table v-if="routes.length > 0">
      <thead>
        <tr>
          <th>Номер маршрута</th>
          <th>Начальный пункт</th>
          <th>Конечный пункт</th>
          <th>Длительность</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="route in routes" :key="route.id">
          <td>
            <router-link :to="`/routes/${route.id}`" class="route-link">
            {{ route.route_num }}
            </router-link>
          </td>
          <td>{{ route.start_point }}</td>
          <td>{{ route.end_point }}</td>
          <td>{{ route.duration }} мин</td>
          <td>
            <button @click="deleteRoute(route.id)" class="delete-btn">Удалить</button>
          </td>
        </tr>
      </tbody>
    </table>

    <p v-else>Данных нет</p>

    <div v-if="showModal" class="modal-overlay">
      <div class="modal-content">
        <button class="modal-close" @click="showModal = false">×</button>

        <RouteModal @close="showModal = false" @route-added="fetchRoutes" />
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import apiClient from "@/api/axios";
import RouteModal from "@/components/RouteModal.vue";

export default {
  components: {
    RouteModal
  },
  data() {
    return {
      routes: [],
      selectedRoute: "",
      showModal: false,
      totalDuration: 0,
    };
  },
  methods: {
    async fetchRoutes() {
      try {
        const response = await apiClient.get('/routes/');
        this.routes = response.data;

        await this.fetchTotalDuration();
      } catch (error) {
        console.error('Ошибка при загрузке маршрутов:', error);
      }
    },
    async fetchTotalDuration() {
      try {
        const response = await apiClient.get('/total-duration/');
        this.totalDuration = response.data.total_duration || 0;
      } catch (error) {
        console.error('Ошибка при получении общей протяжённости маршрутов:', error);
      }
    },
    async deleteRoute(routeId) {
      const confirmDelete = window.confirm('Вы уверены, что хотите удалить этот маршрут?');
      if (!confirmDelete) return;

      try {
        await apiClient.delete(`/routes/${routeId}/delete/`);
        this.routes = this.routes.filter(route => route.id !== routeId);

        await this.fetchTotalDuration();

        alert('Маршрут успешно удалён!');
      } catch (error) {
        console.error('Ошибка при удалении маршрута:', error);
        alert('Не удалось удалить маршрут. Попробуйте позже.');
      }
    },
  },
  async created() {
    await this.fetchRoutes();
  },
};

</script>

<style>
h1 {
  display: flex;
  justify-content: center;
}

.filter-container {
  display: flex;
  flex-direction: column;
  gap: 5px;
  margin-bottom: 20px;
}

.actions-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

label {
  font-size: 16px;
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

.delete-btn {
  background-color: transparent;
  border: none;
  cursor: pointer;
  color: red;
}

.edit-btn {
  background-color: transparent;
  border: none;
  cursor: pointer;
  color: blue;
}

.actions-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
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
  max-width: 50px;
  width: 100%;
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
