<template>
  <div>

    <h1>Список автобусов</h1>

    <div class="actions-container">

      <div class="filter-container">
        <label for="status-filter" style="font-size: 16px;">Статус автобуса:</label>
        <select id="status-filter" class="filter-select" v-model="selectedStatus" @change="filterByStatus">
          <option value="">Все статусы</option>
          <option v-for="status in busStatuses" :key="status" :value="status">
            {{ status }}
          </option>
        </select>
      </div>

      <div class="filter-container">
        <label for="date-filter" style="font-size: 16px;">Выберите дату:</label>
        <input
          type="date"
          id="date-filter"
          class="date-filter-input"
          v-model="selectedDate"
          @change="fetchMissingBuses"
        />
      </div>

      <button @click="showModal = true" class="add">Добавить автобус</button>
    </div>

    <table v-if="buses.length > 0">
      <thead>
        <tr>
          <th>Рег. номер</th>
          <th>Тип</th>
          <th>Вместимость</th>
          <th>Статус</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>

        <tr v-for="bus in processedBuses" :key="bus.id">
          <td>
            <router-link :to="`/buses/${bus.id}`" class="bus-link">
              {{ bus.registration_num }}
            </router-link>
          </td>
          <td>{{ bus.type }}</td>
          <td>{{ bus.capacity }}</td>
          <td>{{ bus.processedStatus }}</td>
          <td>
            <button @click="deleteBus(bus.id)" class="delete-btn">Удалить</button>
          </td>
        </tr>
      </tbody>
    </table>

    <p v-else>Данных нет</p>

    <div v-if="showModal" class="modal-overlay">
      <div class="modal-content">
        <button class="modal-close" @click="showModal = false">×</button>
        <BusModal @close="showModal = false" @bus-added="fetchBuses" />
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import Header from "@/components/Header.vue";
import BusModal from "@/components/BusModal.vue";
import apiClient from "@/api/axios";

export default {
  components: {
    Header,
    BusModal
  },
  data() {
    return {
      buses: [],
      busStatuses: ['Свободен', 'В ремонте', 'Занят'],
      selectedStatus: '',
      selectedDate: '',
      showModal: false,
      missingBuses: []
    };
  },
  computed: {

    filteredBuses() {
      let filtered = this.buses;

      if (this.selectedStatus) {
        filtered = filtered.filter(bus => bus.status === this.selectedStatus);
      }

      if (this.selectedDate) {
        const missingBusIds = this.missingBuses.map(bus => bus.bus);
        filtered = filtered.filter(bus => missingBusIds.includes(bus.registration_num));
      }

      return filtered;
    },

    processedBuses() {
      return this.filteredBuses.map(bus => {

        const processedStatus =
          this.selectedDate && bus.status === "Свободен" ? "Нет водителя" : bus.status;

        return {
          ...bus,
          processedStatus
        };
      });
    }
  },
  methods: {

    async fetchBuses() {
      try {
        const response = await apiClient.get('/buses/');
        this.buses = response.data;
      } catch (error) {
        console.error('Ошибка при загрузке автобусов:', error.response || error.message);
      }
    },

    async fetchMissingBuses() {
      if (!this.selectedDate) return;

      try {
        const response = await apiClient.get('/missing-buses/', {
          params: { date: this.selectedDate },
        });
        this.missingBuses = response.data;
      } catch (error) {
        console.error('Ошибка при загрузке данных о не вышедших на линию автобусах:', error.response || error.message);
        alert('Не удалось загрузить данные о не вышедших на линию автобусах. Попробуйте позже.');
      }
    },

    async deleteBus(busId) {
      const confirmDelete = window.confirm('Вы уверены, что хотите удалить этот автобус?');
      if (!confirmDelete) return;

      try {
        await apiClient.delete(`/buses/${busId}/delete/`);
        this.fetchBuses();
      } catch (error) {
        console.error('Ошибка при удалении автобуса:', error.response || error.message);
        alert('Не удалось удалить автобус. Попробуйте позже.');
      }
    },

    filterByStatus() {

    },
  },
  async created() {
    await this.fetchBuses();
  },
};
</script>

<style scoped>
h1 {
  text-align: center;
}

.filter-container {
  display: flex;
  align-items: center;
  flex-direction: row;
  white-space: nowrap;
  gap: 20px;
}

.actions-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

button {
  padding: 10px;
  background-color: #2c3643;
  color: white;
  border: none;
  cursor: pointer;
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

.delete-btn {
  background-color: transparent;
  border: none;
  cursor: pointer;
  color: red;
}

.delete-btn:hover {
  color: darkred;
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

.date-filter-input {
  appearance: none;
  padding: 5px 10px;
  border-radius: 6px;
  border: 2px solid #2C3643;
  font-size: 16px;
  color: #333;
  background-color: white;
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
