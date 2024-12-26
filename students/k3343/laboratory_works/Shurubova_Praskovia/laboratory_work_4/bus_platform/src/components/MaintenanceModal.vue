<template>
  <div class="modal-overlay" @click="handleOverlayClick">
    <div class="form-container" @click.stop>
      <h1>Добавить новое обслуживание</h1>
      <form @submit.prevent="addMaintenance">

        <div class="form-group">
          <label for="bus">Автобус:</label>
          <select v-model="maintenance.bus" id="bus" required>
            <option v-for="bus in buses" :key="bus.id" :value="bus.id">{{ bus.registration_num }}</option>
          </select>
        </div>

        <div class="form-group">
          <label for="date">Дата обслуживания:</label>
          <input v-model="maintenance.date" id="date" type="date" required />
        </div>

        <div class="form-group">
          <label for="reason">Причина обслуживания:</label>
          <input v-model="maintenance.reason" id="reason" type="text" placeholder="Введите причину обслуживания" required />
        </div>

        <div class="form-group">
          <label for="status">Статус:</label>
          <select v-model="maintenance.status" id="status" required>
            <option value="В процессе">В процессе</option>
            <option value="Починен">Починен</option>
          </select>
        </div>

        <div class="form-buttons">
          <button type="submit">Добавить</button>
          <button type="button" @click="closeModal">Закрыть</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import apiClient from "@/api/axios";

export default {
  data() {
    return {
      maintenance: {
        bus: '',
        date: '',
        reason: '',
        status: '',
      },
      buses: [],
    };
  },
  methods: {

    closeModal() {
      this.$emit('close');
    },

    formatDataForSubmission() {
      return {
        bus: this.maintenance.bus,
        maintenance_date: this.maintenance.date,
        reason: this.maintenance.reason,
        status: this.maintenance.status,
      };
    },

    async addMaintenance() {
      try {

        const formattedData = this.formatDataForSubmission();

        await apiClient.post('/maintenance/create/', formattedData);

        this.$emit('maintenance-added');
        this.closeModal();
      } catch (error) {
        console.error('Ошибка при добавлении обслуживания:', error.response?.data || error.message);
        alert(`Не удалось добавить обслуживание. Ошибка: ${error.response?.data || error.message}`);
      }
    },

    handleOverlayClick() {
      this.closeModal();
    },
  },
  async created() {
    try {

      const response = await apiClient.get('/buses/');
      this.buses = response.data;
    } catch (error) {
      console.error('Ошибка при загрузке автобусов:', error.response?.data || error.message);
    }
  },
};

</script>


<style scoped>

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

.form-container {
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  max-width: 600px;
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

form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

label {
  font-size: 16px;
  margin-bottom: 5px;
}

input, select {
  padding: 8px;
  font-size: 16px;
  border: 1px solid #ccc;
  border-radius: 6px;
}

.form-buttons {
  display: flex;
  justify-content: space-between;
  gap: 10px;
}

button {
  padding: 8px 15px;
  border-radius: 6px;
  cursor: pointer;
  border: 1px solid #2C3643;
}

button[type="submit"] {
  background-color: #2C3643;
  color: white;
}

button[type="submit"]:hover {
  background-color: #1d2a35;
}

button[type="button"] {
  background-color: transparent;
  color: #2C3643;
  border: 1px solid #2C3643;
}

button[type="button"]:hover {
  background-color: #f1f1f1;
}
</style>
