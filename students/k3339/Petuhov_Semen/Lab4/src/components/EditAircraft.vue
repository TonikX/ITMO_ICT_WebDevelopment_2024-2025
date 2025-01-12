<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <h2>Редактировать рейс</h2>

      <form @submit.prevent="saveAircraft">
        <label for="onBoard_number">Бортовой номер:</label>
        <input type="text" v-model="aircraftData.onBoard_number" id="onBoard_number" required />


        <label for="flight_hours">Налёт в часах:</label>
        <input type="number" v-model="aircraftData.flight_hours" id="flight_hours" required />


        <label for="last_maintenance_date">Дата последнего обслуживания:</label>
        <input type="date" v-model="aircraftData.last_maintenance_date" id="last_maintenance_date" required />


        <label for="manufacture_date">Дата производства:</label>
        <input type="date" v-model="aircraftData.manufacture_date" id="manufacture_date" required />


        <label for="company_name">Название компании:</label>
        <select v-model="aircraftData.company_name" id="company_name" required>
          <option v-for="company in companyNames" :key="company" :value="company">
            {{ company }}
          </option>
        </select>


        <label for="model_number">Модель самолёта:</label>
        <select v-model="aircraftData.model_number" id="model_number" required>
          <option v-for="model in modelNumbers" :key="model" :value="model">
            {{ model }}
          </option>
        </select>

        <button type="submit">Сохранить самолёт</button>
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
    aircraft: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      aircraftData: {
        onBoard_number: this.aircraft.onBoard_number,
        flight_hours: this.aircraft.flight_hours,
        last_maintenance_date: this.aircraft.last_maintenance_date,
        manufacture_date: this.aircraft.manufacture_date,
        company_name: this.aircraft.company_name.company_name,
        model_number: this.aircraft.model_details.manufacturer + "-" + this.aircraft.model_details.model_number,
      },
      modelNumbers: [],
      companyNames: [],
      token: localStorage.getItem("auth_token"),
    };
  },
  methods: {
    async saveAircraft() {
      const aircraftDataToSend = {
        onBoard_number: this.aircraftData.onBoard_number,
        flight_hours: this.aircraftData.flight_hours,
        last_maintenance_date: this.aircraftData.last_maintenance_date,
        manufacture_date: this.aircraftData.manufacture_date,
        company_name: this.aircraftData.company_name,
        model_number: this.aircraftData.model_number.split('-')[1],
      };
      const url = `/api/aircraft/${this.aircraftData.onBoard_number}/`;
      const method = 'put';
      try {
        console.log(aircraftDataToSend);
        const response = await axios({
          method: method,
          url: url,
          data: aircraftDataToSend,
          headers: {
            Authorization: `Token ${this.token}`,
          },
        });
        this.$emit("save", response.data);
      } catch (error) {
        console.error("Ошибка при редактировании самолёта:", error);
      }
    },
    async loadData() {
      try {
        const [modelsResponse, companiesResponse] = await Promise.all([
          axios.get("api/aircrafts/models", {
            headers: {Authorization: `Token ${this.token}`},
          }),
          axios.get("api/companies/names", {
            headers: {Authorization: `Token ${this.token}`},
          }),
        ]);
        this.modelNumbers = modelsResponse.data; // Номера самолетов
        this.companyNames = companiesResponse.data;  // Расписания
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