<template>
  <div class="form-container">
    <h1>Информация о техническом обслуживании</h1>
    <form @submit.prevent="updateMaintenance">
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
        <label for="work_type">Тип работы:</label>
        <input v-model="maintenance.work_type" id="work_type" type="text" placeholder="Введите тип работы" required />
      </div>

      <div class="form-group">
        <label for="status">Статус:</label>
        <select v-model="maintenance.status" id="status" required>
          <option value="В процессе">В процессе</option>
          <option value="Починен">Починен</option>
        </select>
      </div>

      <div class="form-buttons">
        <button type="submit">Сохранить</button>
        <router-link to="/maintenances" class="back-to-list-btn">Вернуться к списку</router-link>
      </div>
    </form>
  </div>
</template>

<script>
import apiClient from "@/api/axios";

export default {
  data() {
    return {
      maintenance: null,
      buses: [],
    };
  },
  async created() {
    try {
      const maintenanceId = this.$route.params.id;
      const response = await apiClient.get(`/maintenance/${maintenanceId}/update/`);
      this.maintenance = response.data;

      const busesResponse = await apiClient.get('/buses/');
      this.buses = busesResponse.data;
    } catch (error) {
      console.error("Ошибка при загрузке данных обслуживания:", error);
    }
  },
  methods: {
    async updateMaintenance() {
      try {
        const maintenanceId = this.$route.params.id;
        await apiClient.put(`/maintenance/${maintenanceId}/update/`, this.maintenance);
        alert("Обслуживание обновлено!");
      } catch (error) {
        console.error("Ошибка при обновлении обслуживания:", error);
        alert("Не удалось обновить обслуживание.");
      }
    },
  },
};
</script>

<style scoped>

html, body {
  height: 100%;
  margin: 0;
  display: flex;
  justify-content: center;
  align-items: center;
}


.form-container {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  max-width: 1500px;
  width: 100%;
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  text-align: left;
}

h1 {
  font-size: 24px;
  color: #2C3643;
  margin-bottom: 30px;
  text-align: center;
}

.form-group {
  margin-bottom: 20px;
  width: 100%;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-size: 16px;
  color: #333;
}

.form-group input,
.form-group select {
  width: 100%;
  padding: 10px;
  border-radius: 5px;
  border: 2px solid #2C3643;
  font-size: 14px;
  color: #2C3643;
  box-sizing: border-box;
}

.form-group input::placeholder,
.form-group select::placeholder {
  color: #aaa;
}

.form-group input[type="number"],
.form-group input[type="date"] {
  -moz-appearance: textfield;
}

button, .back-to-list-btn {
  padding: 10px 20px;
  border-radius: 6px;
  background-color: #8ABEE5;
  color: black;
  border: none;
  cursor: pointer;
  font-size: 16px;

  max-width: 300px;
  margin-top: 20px;
  text-align: center;
}

button:hover, .back-to-list-btn:hover {
  background-color: #2C3643;
  color: white;
}


.form-buttons {
  display: flex;
  justify-content: center;
  gap: 20px;
  margin-top: 20px;
}


.back-to-list-btn {
  text-decoration: none;
  display: inline-block;
}
</style>
