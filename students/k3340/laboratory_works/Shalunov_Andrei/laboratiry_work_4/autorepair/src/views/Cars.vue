<template>
    <v-container>
      <v-row>
        <v-col cols="12">
          <h1 class="text-center">Список автомобилей</h1>
        </v-col>
      </v-row>
  
      <v-row>
        <v-col cols="12" md="3">
          <v-text-field
            v-model="filters.brand"
            label="Фильтр по марке"
            clearable
          ></v-text-field>
        </v-col>
        <v-col cols="12" md="3">
          <v-text-field
            v-model="filters.model"
            label="Фильтр по модели"
            clearable
          ></v-text-field>
        </v-col>
        <v-col cols="12" md="3">
          <v-text-field
            v-model="filters.year"
            label="Фильтр по году"
            type="number"
            clearable
          ></v-text-field>
        </v-col>
        <v-col cols="12" md="3">
          <v-text-field
            v-model="filters.state_number"
            label="Фильтр по гос. номеру"
            clearable
          ></v-text-field>
        </v-col>
      </v-row>
  
      <v-row>
        <v-col cols="12" class="d-flex justify-end">
          <v-btn color="primary" @click="navigateToCreate">Добавить автомобиль</v-btn>
        </v-col>
      </v-row>
  
      <v-row>
        <v-col
          cols="12"
          md="6"
          v-for="car in filteredAndPaginatedCars"
          :key="car.id"
        >
          <v-card class="mb-6" elevation="2">
            <v-card-title>Автомобиль №{{ car.state_number }}</v-card-title>
            <v-card-text>
              <p><strong>Гос. номер:</strong> {{ car.state_number }}</p>
              <p><strong>Год выпуска:</strong> {{ car.year }}</p>
            </v-card-text>
            <v-card-actions class="justify-center">
              <v-btn color="primary" @click="navigateToCarDetails(car.id)">Детали</v-btn>
              <v-btn color="primary" @click="navigateToEdit(car.id)">Редактировать</v-btn>
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
        cars: [],
        filters: {
          brand: "",
          model: "",
          year: "",
          state_number: "",
        },
        currentPage: 1,
        itemsPerPage: 5,
      };
    },
    computed: {
      filteredCars() {
        return this.cars.filter((car) => {
          const matchesBrand =
            !this.filters.brand || car.brand.includes(this.filters.brand);
          const matchesModel =
            !this.filters.model || car.model.includes(this.filters.model);
          const matchesYear =
            !this.filters.year || car.year.toString().includes(this.filters.year);
          const matchesStateNumber =
            !this.filters.state_number ||
            car.state_number.includes(this.filters.state_number);
          return matchesBrand && matchesModel && matchesYear && matchesStateNumber;
        });
      },
      filteredAndPaginatedCars() {
        const start = (this.currentPage - 1) * this.itemsPerPage;
        const end = start + this.itemsPerPage;
        return this.filteredCars.slice(start, end);
      },
      totalPages() {
        return Math.ceil(this.filteredCars.length / this.itemsPerPage);
      },
    },
    methods: {
      async fetchCars() {
        try {
          const response = await apiClient.get("/automobiles/");
          this.cars = response.data;
        } catch (error) {
          console.error("Ошибка загрузки автомобилей:", error.response?.data || error.message);
        }
      },
      navigateToCreate() {
        this.$router.push("/cars/create");
      },
      navigateToEdit(carId) {
        this.$router.push(`/cars/edit/${carId}`);
      },
      navigateToCarDetails(carId) {
        this.$router.push(`/cars/${carId}`);
      },
    },
    async created() {
      await this.fetchCars();
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
  