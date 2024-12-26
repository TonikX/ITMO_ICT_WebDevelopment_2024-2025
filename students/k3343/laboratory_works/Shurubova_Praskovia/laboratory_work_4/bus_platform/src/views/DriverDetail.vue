<template>
  <div class="form-container">
    <h1>Информация о водителе</h1>
    <form @submit.prevent="updateDriver">
      <div class="form-group">
        <label for="name">Имя:</label>
        <input v-model="driver.name" class="colour" id="name" placeholder="Введите имя" required />
      </div>
      <div class="form-group">
        <label for="surname">Фамилия:</label>
        <input v-model="driver.surname" class="colour" id="surname" placeholder="Введите фамилию" required />
      </div>
      <div class="form-group">
        <label for="passport">Паспорт:</label>
        <input v-model="driver.passport" class="colour" id="passport" placeholder="Введите паспортные данные" required />
      </div>
      <div class="form-group">
        <label for="driverClass">Класс водителя:</label>
        <select v-model="driver.driver_class" class="colour" id="driverClass" required>
          <option v-for="classType in driverClasses" :key="classType" :value="classType">
            {{ classType }}
          </option>
        </select>
      </div>
      <div class="form-group">
        <label for="experience">Стаж работы (лет):</label>
        <input v-model.number="driver.experience" class="colour" id="experience" type="number" min="0" placeholder="Введите стаж" required />
      </div>
      <div class="form-group">
        <label for="salary">Оклад:</label>
        <input v-model.number="driver.salary" class="colour" id="salary" type="number" step="0.01" placeholder="Введите оклад" required />
      </div>
      <div class="form-group">
        <label for="dateOfBirth">Дата рождения:</label>
        <input v-model="driver.date_of_birth" class="colour" id="dateOfBirth" type="date" required />
      </div>
      <div class="form-group">
        <label for="status">Статус:</label>
        <select v-model="driver.status" class="colour" id="status" required>
          <option v-for="statusOption in driverStatuses" :key="statusOption.value" :value="statusOption.value">
            {{ statusOption.label }}
          </option>
        </select>
      </div>

      <div class="form-buttons">
        <button type="submit">Сохранить</button>
        <router-link to="/drivers" class="back-to-list-btn">
          Вернуться к списку водителей
        </router-link>
      </div>
    </form>
  </div>
</template>

<script>
import apiClient from "@/api/axios";
import Header from "@/components/Header.vue";

export default {
  components: {
    Header,
  },
  data() {
    return {
      driver: null,
      driverClasses: ["A", "B", "D1", "D"],
      driverStatuses: [
        { value: "На работе", label: "На работе" },
        { value: "Выходной", label: "Выходной" },
        { value: "В отпуске", label: "В отпуске" },
        { value: "На больничном", label: "На больничном" },
        { value: "В командировке", label: "В командировке" },
        { value: "Уволен", label: "Уволен" },
      ],
    };
  },
  async created() {
    try {
      const driverId = this.$route.params.id;
      const response = await apiClient.get(`/drivers/${driverId}/`);
      this.driver = response.data;
    } catch (error) {
      console.error("Ошибка при загрузке данных водителя:", error);
    }
  },
  methods: {
    async updateDriver() {
      try {
        const driverId = this.$route.params.id;
        await apiClient.put(`/drivers/${driverId}/update/`, this.driver);
        alert("Данные обновлены!");
      } catch (error) {
        console.error("Ошибка при обновлении данных:", error);
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
  background-color: white;
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
  justify-content: space-between;
  align-items: center;
  gap: 20px;
  margin-top: 20px;
}

.back-to-list-btn {
  text-decoration: none;
  display: inline-block;
}
</style>
