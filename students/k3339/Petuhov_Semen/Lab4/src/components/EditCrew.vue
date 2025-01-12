<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <h2>Редактировать члена экипажа</h2>
      <form @submit.prevent="saveCrew">

        <label for="medical_check_date">Дата медосмотра:</label>
        <input type="date" v-model="crewData.medical_check_date" required />

        <label for="clearance_status">Статус проверки:</label>
        <select v-model="crewData.clearance_status" required>
          <option value="1">Проверка пройдена</option>
          <option value="0">Проверка не пройдена</option>
        </select>

        <label for="flight_position">Роль в полете:</label>
        <input type="text" v-model="crewData.flight_position" required />

        <label for="flight_number">Номер рейса:</label>
        <input type="number" v-model="crewData.flight_number" required />

        <label for="employee_code">Код сотрудника:</label>
        <select v-model="crewData.employee_code" required>
          <option v-for="employee in employees" :key="employee.employee_code" :value="employee.employee_code">
            {{ employee.employee_code }}
          </option>
        </select>

        <button type="submit">Сохранить</button>
      </form>

      <button @click="$emit('close')" class="close-btn">Закрыть</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  props: {
    crew: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      crewData: {
        crew_number: this.crew.crew_number,
        medical_check_date: this.crew.medical_check_date,
        clearance_status: this.crew.clearance_status,
        flight_position: this.crew.flight_position,
        flight_number: this.crew.flight_number,
        employee_code: this.crew.employee_code.employee_code,
      },
      employees: [],
      token: localStorage.getItem('auth_token'), // Получение токена из localStorage
    };
  },
  created() {
    this.loadData();
  },
  methods: {
    // Метод для загрузки списка сотрудников с сервера
    async loadData() {
      try {
        // Проверяем наличие токена
        if (!this.token) {
          console.error('Токен не найден. Вы должны быть авторизованы.');
          return;
        }

        // Отправляем запрос на получение данных сотрудников с токеном в заголовке
        const response = await axios.get('/api/employees/', {
          headers: {
            Authorization: `Token ${this.token}`,
          },
        });

        // Присваиваем список сотрудников в переменную employees
        this.employees = response.data;
        console.log('Сотрудники:', this.employees);
      } catch (error) {
        console.error('Ошибка при загрузке сотрудников:', error);
      }
    },
    async saveCrew() {
      const crewDataToSend = {
        crew_number: this.crew.crew_number,
        medical_check_date: this.crewData.medical_check_date,
        clearance_status: this.crewData.clearance_status,
        flight_position: this.crewData.flight_position,
        flight_number: this.crewData.flight_number,
        employee_code: this.crewData.employee_code,
      };
      const url = `/api/crew/${this.crewData.crew_number}/`;
      const method = 'put';

      try {
        console.log(crewDataToSend);
        const response = await axios({
          method: method,
          url: url,
          data: crewDataToSend,
          headers: {
            Authorization: `Token ${this.token}`,
          },
        });
        this.$emit("save", response.data);
      } catch (error) {
        console.error("Ошибка при редактировании члена экипажа:", error);
      }
    },
  },
};
</script>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 10px;
  width: 500px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

form label {
  display: block;
  margin: 10px 0 5px;
  font-weight: bold;
}

input,
select {
  width: 100%;
  padding: 10px;
  margin-bottom: 15px;
  border: 1px solid #ccc;
  border-radius: 4px;
  box-sizing: border-box;
  font-size: 14px;
}

button {
  padding: 10px 20px;
  background-color: #007bff;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  font-size: 16px;
}

button:hover {
  background-color: #0056b3;
}

.modal-footer {
  margin-top: 20px;
  display: flex;
  justify-content: flex-end;
}

.close-btn {
  padding: 10px 20px;
  background-color: #ff4040;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.close-btn:hover {
  background-color: #cc3333;
}
</style>
