<template>
  <div>
    <h1>Расписание водителей</h1>

    <div class="filter-actions-container">
      <div class="filter-container">
        <label for="driverFilter">Выберите водителя:</label>
        <select v-model="selectedDriverId" id="driverFilter" class="filter-select">
          <option value="">Все водители</option>
          <option v-for="driver in drivers" :key="driver.id" :value="driver.id">
            {{ driver.name }} {{ driver.surname }}
          </option>
        </select>
      </div>
      <button @click="showModal = true" class="add">Добавить расписание</button>
    </div>

    <table v-if="filteredSchedules.length > 0">
      <thead>
        <tr>
          <th>Водитель</th>
          <th>Автобус</th>
          <th>Маршрут</th>
          <th>Дата работы</th>
          <th>Начало смены</th>
          <th>Конец смены</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="schedule in filteredSchedules" :key="schedule.id">
          <td>{{ schedule.driver.name }} {{ schedule.driver.surname }}</td>
          <td>{{ schedule.bus.registration_num }}</td>
          <td>{{ schedule.route.route_num }}</td>
          <td>{{ schedule.work_date }}</td>
          <td>{{ schedule.shift_start }}</td>
          <td>{{ schedule.shift_end }}</td>
          <td>
            <button @click="deleteSchedule(schedule.id)" class="delete-btn">Удалить</button>
            <router-link :to="`/driver-schedule/${schedule.id}/`" class="edit-btn">Редактировать</router-link>
          </td>
        </tr>
      </tbody>
    </table>

    <p v-else>Расписания нет</p>

    <div v-if="showModal" class="modal-overlay">
      <div class="modal-content">
        <button class="modal-close" @click="showModal = false">×</button>
        <ScheduleModal @close="showModal = false" @schedule-added="fetchSchedules" />
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import ScheduleModal from '@/components/ScheduleModal.vue';
import apiClient from '@/api/axios';

export default {
  components: {
    ScheduleModal
  },
  data() {
    return {
      schedules: [],
      drivers: [],
      selectedDriverId: '',
      showModal: false
    };
  },
  computed: {

    filteredSchedules() {
      if (this.selectedDriverId) {
        return this.schedules.filter(schedule => schedule.driver.id === this.selectedDriverId);
      }
      return this.schedules;
    }
  },
  methods: {

    async fetchDrivers() {
      try {
        const response = await apiClient.get('/drivers/');
        this.drivers = response.data;
      } catch (error) {
        console.error('Ошибка при загрузке водителей:', error);
      }
    },

    async fetchSchedules() {
      try {
        const response = await apiClient.get('/driver-schedules/');
        this.schedules = response.data;
      } catch (error) {
        console.error('Ошибка при загрузке расписаний:', error);
      }
    },

    async deleteSchedule(scheduleId) {
      const confirmDelete = window.confirm('Вы уверены, что хотите удалить это расписание?');
      if (!confirmDelete) return;

      try {
        await apiClient.delete(`/driver-schedule/${scheduleId}/delete/`);
        this.fetchSchedules();
      } catch (error) {
        console.error('Ошибка при удалении расписания:', error);
        alert('Не удалось удалить расписание. Попробуйте позже.');
      }
    },
  },
  async created() {
    await this.fetchDrivers();
    await this.fetchSchedules();
  }
};
</script>

<style scoped>
h1 {
  text-align: center;
}

.filter-actions-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.filter-container {
  display: flex;
  align-items: center;
  flex-direction: row;
  white-space: nowrap;
  gap: 20px;
}

label {
  font-size: 16px;
  white-space: nowrap;
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
</style>
