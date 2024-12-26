<template>
  <div class="modal-overlay" @click="handleOverlayClick">
    <div class="form-container" @click.stop>
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
      driver: {
        name: "",
        surname: "",
        passport: "",
        driver_class: "",
        experience: 0,
        salary: 0.0,
        date_of_birth: "",
        status: "",
      },
      driverClasses: ["A", "B", "D1", "D"],
      driverStatuses: [
        { value: "На работе", label: "На работе" },
        { value: "Выходной", label: "Выходной" },
        { value: "В отпуске", label: "В отпуске" },
        { value: "На больничном", label: "На больничном" },
        { value: "В командировке", label: "В командировке" },
      ],
    };
  },
  methods: {
    closeModal() {
      this.$emit('close');
    },

    formatDataForSubmission() {
      return {
        name: this.driver.name,
        surname: this.driver.surname,
        passport: this.driver.passport,
        driver_class: this.driver.driver_class,
        experience: this.driver.experience,
        salary: this.driver.salary,
        date_of_birth: this.driver.date_of_birth,
        status: this.driver.status,
      };
    },

    async updateDriver() {
      try {
        const formattedData = this.formatDataForSubmission();
        await apiClient.post("/drivers/create/", formattedData);
        this.$emit('driver-added');
        this.closeModal();
      } catch (error) {
        console.error("Ошибка при добавлении водителя:", error);
      }
    },
    handleOverlayClick() {
      this.closeModal();
    },
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
  max-width: 500px;
  max-height: 700px;
  width: 90%;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  animation: none;
  overflow-y: auto;
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

form {
  display: flex;
  flex-direction: column;
  gap: 15px;
}

h1 {
  font-size: 24px;
  color: #2C3643;
  margin-bottom: 20px;
  text-align: center;
}


.form-group {
  display: flex;
  flex-direction: column;
  margin-bottom: 0px;
}

label {
  font-size: 16px;
  color: #333;
  margin-bottom: 8px;
}

input, select {
  padding: 10px;
  font-size: 16px;
  border-radius: 6px;
  border: 1px solid #ccc;
  margin-top: 5px;
}

input::placeholder,
select::placeholder {
  color: #aaa;
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

.form-buttons {
  display: flex;
  justify-content: space-between;
  gap: 20px;
}
</style>

