<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <h2>Добавить рейс</h2>

      <form @submit.prevent="saveFlight">
        <!-- Выбор самолета -->
        <label for="aircraft">Самолет (номер):</label>
        <select v-model="newFlight.onBoard_number" id="aircraft" required>
          <option v-for="number in aircraftNumbers" :key="number" :value="number">
            {{ number }}
          </option>
        </select>

        <!-- Выбор расписания -->
        <label for="schedule">Расписание:</label>
        <select v-model="newFlight.schedule_number" id="schedule" required>
          <option v-for="schedule in schedules" :key="schedule.schedule_number" :value="schedule.schedule_number">
            {{ schedule.schedule_number }}
          </option>
        </select>

        <!-- Дата вылета -->
        <label for="departure_date">Дата вылета:</label>
        <input type="date" v-model="newFlight.departure_date" id="departure_date" required />

        <!-- Дата прилета -->
        <label for="arrival_date">Дата прилета:</label>
        <input type="date" v-model="newFlight.arrival_date" id="arrival_date" required />

        <!-- Статус рейса -->
        <label for="status">Состояние рейса:</label>
        <select v-model="newFlight.status" id="status" required>
          <option value="scheduled">Запланирован</option>
          <option value="delayed">Задержан</option>
          <option value="completed">Завершен</option>
          <option value="waiting">Ожидание</option>
        </select>

        <button type="submit">Сохранить рейс</button>
      </form>

      <div class="modal-footer">
        <button @click="$emit('close')" class="close-btn">Закрыть</button>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return {
      newFlight: {
        schedule_number: "",  // Вставляем правильное значение
        onBoard_number: "",  // Новое поле для самолета
        departure_date: "",
        arrival_date: "",
        status: "waiting",
      },
      aircraftNumbers: [],
      schedules: [],
      token: localStorage.getItem("auth_token"),
    };
  },
  methods: {
    async saveFlight() {
      // Преобразуем поля в числовой формат, если нужно
      const flightData = {
        schedule_number: Number(this.newFlight.schedule_number), // Убедимся, что это число
        onBoard_number: Number(this.newFlight.onBoard_number),  // Преобразуем это поле в число
        departure_date: this.newFlight.departure_date,          // Только дата
        arrival_date: this.newFlight.arrival_date,              // Только дата
        status: this.newFlight.status,
      };
      try {
        console.log(flightData);  // Проверка отправляемых данных
        const response = await axios.post(
            "/api/flights/create/",
            flightData,
            {
              headers: {
                Authorization: `Token ${this.token}`,
              },
            }
        );
        this.$emit("save", response.data);
      } catch (error) {
        console.error("Ошибка при сохранении рейса:", error);
      }
    },
    async loadData() {
      try {
        const [aircraftsResponse, schedulesResponse] = await Promise.all([
          axios.get("/api/aircrafts/numbers", {
            headers: {Authorization: `Token ${this.token}`},
          }),
          axios.get("/api/schedules/", {
            headers: {Authorization: `Token ${this.token}`},
          }),
        ]);
        this.aircraftNumbers = aircraftsResponse.data.onBoard_numbers; // Номера самолетов
        this.schedules = schedulesResponse.data;  // Расписания
      } catch (error) {
        console.error("Ошибка при загрузке данных:", error);
      }
    },
  },
  created() {
    this.loadData();
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