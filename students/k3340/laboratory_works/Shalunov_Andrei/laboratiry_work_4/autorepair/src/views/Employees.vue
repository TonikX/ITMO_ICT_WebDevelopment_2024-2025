<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="text-center">Список работников</h1>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" md="3">
        <v-text-field
          v-model="filters.name"
          label="Фильтр по имени"
          clearable
        ></v-text-field>
      </v-col>

      <v-col cols="12" md="3">
        <v-select
          v-model="filters.job_position"
          label="Фильтр по должности"
          :items="jobPositions"
          item-value="id"
          item-title="name"
          clearable
        ></v-select>
      </v-col>

      <v-col cols="12" md="3">
        <v-select
          v-model="filters.car_workshop"
          label="Фильтр по месту работы"
          :items="carWorkshops"
          item-value="id"
          item-title="city"
          clearable
        ></v-select>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" class="d-flex justify-end">
        <v-btn color="primary" @click="navigateToCreate">Добавить работника</v-btn>
      </v-col>
    </v-row>

    <v-row>
      <v-col
        cols="12"
        md="6"
        v-for="employee in filteredAndPaginatedEmployees"
        :key="employee.id"
      >
        <v-card class="mb-6" elevation="2">
          <v-card-title>{{ employee.full_name }}</v-card-title>
          <v-card-subtitle>
            Должность: {{ employee.job_position ? employee.job_position.name : "Не указана" }}
          </v-card-subtitle>
          <v-card-text>
            <p><strong>Телефон:</strong> {{ employee.phone}}</p>
            <p><strong>Email:</strong> {{ employee.email || "Нет информации" }}</p>
          </v-card-text>
          <v-card-actions class="justify-center">
            <v-btn color="primary" @click="navigateToDetails(employee.id)">Детали</v-btn>
            <v-btn color="primary" @click="navigateToEdit(employee.id)">Редактировать</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" class="d-flex justify-center">
        <v-pagination
          v-model="currentPage"
          :length="totalPages"
          :total-visible="5"
        ></v-pagination>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import apiClient from "@/services/api";

export default {
  data() {
    return {
      employees: [],
      jobPositions: [],
      carWorkshops: [],
      currentPage: 1,
      itemsPerPage: 5,
      filters: {
        job_position: null,
        car_workshop: null,
        name: "",
      },
    };
  },
  computed: {
    filteredEmployees() {
      return this.employees.filter((employee) => {
        const matchesJobPosition =
          !this.filters.job_position ||
          employee.job_position.id === this.filters.job_position;
        const matchesCarWorkshop =
          !this.filters.car_workshop ||
          employee.car_workshop.id === this.filters.car_workshop;
        const matchesName =
          !this.filters.name || employee.full_name.includes(this.filters.name);
        return matchesJobPosition && matchesCarWorkshop && matchesName;
      });
    },
    filteredAndPaginatedEmployees() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.filteredEmployees.slice(start, end);
    },
    totalPages() {
      return Math.ceil(this.filteredEmployees.length / this.itemsPerPage);
    },
  },
  methods: {
    async fetchEmployees() {
      try {
        const response = await apiClient.get("/employees/");
        this.employees = response.data;
      } catch (error) {
        console.error("Ошибка загрузки работников:", error.response?.data || error.message);
      }
    },
    async fetchJobPositions() {
      try {
        const response = await apiClient.get("/positions/");
        this.jobPositions = response.data;
      } catch (error) {
        console.error("Ошибка загрузки должностей:", error.response?.data || error.message);
      }
    },
    async fetchCarWorkshops() {
      try {
        const response = await apiClient.get("/workshops/");
        this.carWorkshops = response.data;
      } catch (error) {
        console.error("Ошибка загрузки мастерских:", error.response?.data || error.message);
      }
    },
    navigateToCreate() {
      this.$router.push("/employees/create");
    },
    navigateToEdit(employeeId) {
      this.$router.push(`/employees/edit/${employeeId}`);
    },
    navigateToDetails(employeeId) {
      this.$router.push(`/employees/${employeeId}`);
    },
  },
  async created() {
    await Promise.all([this.fetchEmployees(), this.fetchJobPositions(), this.fetchCarWorkshops()]);
  },
};
</script>

<style scoped>
.text-center {
  text-align: center;
}
.mb-6 {
  margin-bottom: 1.5rem;
}
</style>
