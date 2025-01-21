<template> 
    <v-container>
      <v-row>
        <v-col cols="12">
          <h1 class="text-center">Добавить нового работника</h1>
        </v-col>
      </v-row>
  
      <v-form ref="form">
        <v-text-field
          v-model="employee.full_name"
          label="Полное имя"
          required
        ></v-text-field>
  
        <v-text-field
          v-model="employee.phone"
          label="Телефон"
          required
        ></v-text-field>
  
        <v-text-field
          v-model="employee.email"
          label="Email"
          type="email"
        ></v-text-field>
  
        <v-select
          v-model="employee.job_position_id"
          :items="jobPositions"
          label="Должность"
          item-value="id"
          item-title="name"
          required
        ></v-select>
  
        <v-select
          v-model="employee.car_workshop_id"
          :items="carWorkshops"
          label="Мастерская"
          item-value="id"
          item-title="city"
          required
        ></v-select>
  
        <v-select
          v-model="employee.user_id"
          :items="users"
          label="Выбрать пользователя"
          item-value="id"
          item-title="username"
          required
        ></v-select>
  
        <v-text-field
          v-model="employee.rank"
          label="Ранг"
          type="number"
          required
        ></v-text-field>
  
        <v-text-field
          v-model="employee.bonus"
          label="Бонус"
          type="number"
        ></v-text-field>
  
        <v-btn color="primary" @click="createEmployee">Создать</v-btn>
      </v-form>
    </v-container>
  </template>
  
  <script>
  import apiClient from "@/services/api";
  
  export default {
    data() {
      return {
        employee: {
          full_name: "",
          phone: "",
          email: "",
          job_position_id: null,
          car_workshop_id: null,
          user_id: null,
          rank: null,
          bonus: null,
        },
        jobPositions: [],
        carWorkshops: [],
        users: [],
      };
    },
    methods: {
      async fetchChoices() {
        try {
          const [jobPositionsResponse, carWorkshopsResponse, usersResponse] = await Promise.all([
            apiClient.get("/positions/"),
            apiClient.get("/workshops/"),
            apiClient.get("/users/"),
          ]);
          this.jobPositions = jobPositionsResponse.data;
          this.carWorkshops = carWorkshopsResponse.data;
          this.users = usersResponse.data;
        } catch (error) {
          console.error("Ошибка загрузки данных для выбора:", error.response?.data || error.message);
        }
      },
      async createEmployee() {
        try {
          const response = await apiClient.post("/employees/", this.employee);
          console.log("Успешно создан работник:", response.data);
          this.$router.push("/employees");
        } catch (error) {
          console.error("Ошибка создания работника:", error.response?.data || error.message);
        }
      },
    },
    mounted() {
      this.fetchChoices();
    },
  };
  </script>
  
  <style scoped>
  .text-center {
    text-align: center;
  }
  </style>
  