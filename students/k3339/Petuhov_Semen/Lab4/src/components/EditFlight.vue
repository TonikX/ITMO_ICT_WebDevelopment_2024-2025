<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <h2>Редактировать рейс</h2>  <form @submit.prevent="saveFlight">
      <label for="flight_number">Номер рейса:</label>
      <input type="text" v-model="flightData.flight_number" id="flight_number" readonly />

      <label for="aircraft">Самолет (номер):</label>
      <select v-model="flightData.onBoard_number" id="aircraft" required>
        <option v-for="number in aircraftNumbers" :key="number" :value="number">
          {{ number }}
        </option>
      </select>

      <label for="schedule">Расписание:</label>
      <select v-model="flightData.schedule_number" id="schedule" required>
        <option v-for="schedule in schedules" :key="schedule.schedule_number" :value="schedule.schedule_number">
          {{ schedule.schedule_number }}
        </option>
      </select>

      <label for="departure_date">Дата вылета:</label>
      <input type="date" v-model="flightData.departure_date" id="departure_date" required />

      <label for="arrival_date">Дата прилета:</label>
      <input type="date" v-model="flightData.arrival_date" id="arrival_date" required />

      <label for="status">Состояние рейса:</label>
      <select v-model="flightData.status" id="status" required>
        <option value="scheduled">Запланирован</option>
        <option value="delayed">Задержан</option>
        <option value="completed">Завершен</option>
        <option value="waiting">Ожидание</option>
      </select>

      <button type="submit">Сохранить изменения</button>
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
  props: {
    flight: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      flightData: { // Object for flight data
        flight_number: this.flight.flight_number,
        schedule_number: this.flight.schedule.match(/\d+/)[0] || null,
        onBoard_number: this.flight.aircraft.onBoard_number,
        departure_date: this.flight.departure_date,
        arrival_date: this.flight.arrival_date,
        status: this.flight.status,
      },
      aircraftNumbers: [],
      schedules: [],
      token: localStorage.getItem("auth_token"),
    };
  },
  methods: {
    async saveFlight() {
      const flightDataToSend = {
        flight_number: this.flight.flight_number,
        schedule_number: this.flightData.schedule_number,
        onBoard_number: this.flightData.onBoard_number,
        departure_date: this.flightData.departure_date,
        arrival_date: this.flightData.arrival_date,
        status: this.flightData.status,
      };
      const url = `/api/flight/${this.flightData.flight_number}/`;
      const method = 'put';

      try {
        const response = await axios({
          method: method,
          url: url,
          data: flightDataToSend,
          headers: {
            Authorization: `Token ${this.token}`,
          },
        });
        this.$emit("save", response.data);
      } catch (error) {
        console.error("Ошибка при редактировании рейса:", error);
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

        this.aircraftNumbers = aircraftsResponse.data.onBoard_numbers;
        this.schedules = schedulesResponse.data;
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