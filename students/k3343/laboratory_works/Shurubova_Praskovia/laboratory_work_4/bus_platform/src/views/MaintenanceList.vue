<template>
  <div>
    <h1>Список технических обслуживаний</h1>

    <div class="button-container">
      <button @click="showModal = true" class="add">Добавить обслуживание</button>
    </div>

    <table v-if="maintenances.length > 0">
      <thead>
        <tr>
          <th>ID</th>
          <th>Автобус</th>
          <th>Дата обслуживания</th>
          <th>Тип работы</th>
          <th>Статус</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="maintenance in maintenances" :key="maintenance.id">
          <td>{{ maintenance.id }}</td>
          <td>{{ maintenance.bus.registration_num }}</td>
          <td>{{ maintenance.maintenance_date }}</td>
          <td>{{ maintenance.reason }}</td>
          <td>{{ maintenance.status }}</td>
          <td>
            <router-link :to="`/maintenance/${maintenance.id}/update/`" class="edit-btn">
              Редактировать
            </router-link>
            <button @click="deleteMaintenance(maintenance.id)" class="delete-btn">Удалить</button>
          </td>
        </tr>
      </tbody>
    </table>

    <p v-else>Данных нет</p>

    <div v-if="showModal" class="modal-overlay">
      <div class="modal-content">
        <button class="modal-close" @click="showModal = false">×</button>
        <MaintenanceModal @close="showModal = false" @maintenance-added="fetchMaintenances" />
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import MaintenanceModal from "@/components/MaintenanceModal.vue";
import apiClient from "@/api/axios";

export default {
  components: {
    MaintenanceModal,
  },
  data() {
    return {
      maintenances: [],
      showModal: false,
    };
  },
  methods: {

    async fetchMaintenances() {
      try {
        const response = await apiClient.get('/maintenances/');
        this.maintenances = response.data;
      } catch (error) {
        console.error('Ошибка при загрузке обслуживаний:', error.response || error.message);
      }
    },

    async deleteMaintenance(maintenanceId) {
      const confirmDelete = window.confirm('Вы уверены, что хотите удалить это обслуживание?');
      if (!confirmDelete) return;

      try {
        await apiClient.delete(`/maintenances/${maintenanceId}/delete/`);
        this.fetchMaintenances();
      } catch (error) {
        console.error('Ошибка при удалении обслуживания:', error.response || error.message);
        alert('Не удалось удалить обслуживание. Попробуйте позже.');
      }
    },
  },
  async created() {
    await this.fetchMaintenances();
  },
};
</script>

<style scoped>
h1 {
  text-align: center;
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

button {
  padding: 10px;
  background-color: #2c3643;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #1f2c3d;
}

.button-container {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 20px;
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
  font-weight: bold;
  font-size: 14px;
  transition: color 0.2s ease;
}

.delete-btn:hover {
  color: darkred;
  background: white;
}

.edit-btn {
  margin-left: 10px;
  color: #2c3643;
  text-decoration: none;
  font-weight: bold;
  font-size: 14px;
  border: 1px solid #2c3643;
  border-radius: 4px;
  padding: 4px 8px;
  transition: background-color 0.3s ease, color 0.3s ease;
}

.edit-btn:hover {
  background-color: #2c3643;
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
