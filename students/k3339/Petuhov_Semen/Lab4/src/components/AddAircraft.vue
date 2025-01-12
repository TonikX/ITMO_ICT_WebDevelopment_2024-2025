<template>
  <div class="modal-overlay">
    <div class="modal-content">
      <h2>Добавить рейс</h2>

      <form @submit.prevent="saveAircraft">
        <label for="onBoard_number">Бортовой номер:</label>
        <input type="text" v-model="newAircraft.onBoard_number" id="onBoard_number" required />


        <label for="flight_hours">Налёт в часах:</label>
        <input type="number" v-model="newAircraft.flight_hours" id="flight_hours" required />


        <label for="last_maintenance_date">Дата последнего обслуживания:</label>
        <input type="date" v-model="newAircraft.last_maintenance_date" id="last_maintenance_date" required />


        <label for="manufacture_date">Дата производства:</label>
        <input type="date" v-model="newAircraft.manufacture_date" id="manufacture_date" required />


        <label for="company_name">Наименование компании:</label>
        <select v-model="newAircraft.company_name" id="company_name" required>
          <option v-for="company in companyNames" :key="company" :value="company">
            {{ company }}
          </option>
        </select>


        <label for="model_number">Модель самолёта:</label>
        <select v-model="newAircraft.model_number" id="model_number" required>
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
  data() {
    return {
      newAircraft: {
        onBoard_number: "",
        flight_hours: "",
        last_maintenance_date: "",
        manufacture_date: "",
        company_name: "",
        model_number: "",
      },
      modelNumbers: [],
      companyNames: [],
      token: localStorage.getItem("auth_token"),
    };
  },
  methods: {
    async saveAircraft() {
      const aircraftData = {
        onBoard_number: this.newAircraft.onBoard_number,
        flight_hours: this.newAircraft.flight_hours,
        last_maintenance_date: this.newAircraft.last_maintenance_date,
        manufacture_date: this.newAircraft.manufacture_date,
        company_name: this.newAircraft.company_name,
        model_number: this.newAircraft.model_number.split('-')[1],
      };
      try {
        console.log(aircraftData);
        const response = await axios.post(
            "/api/aircrafts/create/",
            aircraftData,
            {
              headers: {
                Authorization: `Token ${this.token}`,
              },
            }
        );
        this.$emit("save", response.data);
      } catch (error) {
        console.error("Ошибка при сохранении самолёта:", error);
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