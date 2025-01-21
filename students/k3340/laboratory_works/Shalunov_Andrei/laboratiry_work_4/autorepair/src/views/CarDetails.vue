<template>
    <v-container class="car-details" v-if="car">
      <v-row>
        <v-col cols="12" class="text-center">
          <h1>Детали автомобиля {{ car.state_number }}</h1>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" md="6">
          <v-card outlined class="mb-4">
            <v-card-title>Автомобиль</v-card-title>
            <v-card-text>
              <p><strong>Гос. номер:</strong> {{ car.state_number }}</p>
              <p><strong>Марка:</strong> {{ car.brand }}</p>
              <p><strong>Модель:</strong> {{ car.model }}</p>
              <p><strong>Год выпуска:</strong> {{ car.year_of_vehicle }}</p>
              <p><strong>Цвет:</strong> {{ car.colour }}</p>
            </v-card-text>
          </v-card>
        </v-col>
        <v-col cols="12" md="6">
          <v-card outlined class="mb-4">
            <v-card-title>Владелец</v-card-title>
            <v-card-text>
              <p><strong>Имя владельца:</strong> {{ car.client.full_name }}</p>
              <p><strong>Телефон:</strong> {{ car.client.phone }}</p>
              <p><strong>Email:</strong> {{ car.client.email || "Нет информации" }}</p>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12" class="d-flex justify-center">
          <v-btn color="primary" @click="navigateToEdit">Редактировать</v-btn>
          <v-btn color="secondary" @click="navigateBack">Назад</v-btn>
          <v-btn color="red" @click="deleteCar">Удалить</v-btn>
        </v-col>
      </v-row>
    </v-container>
  </template>
  
  <script>
  import apiClient from "@/services/api";
  
  export default {
    data() {
      return {
        car: {},
      };
    },
    methods: {
      async fetchCarDetails() {
        try {
          const response = await apiClient.get(`/automobiles/${this.$route.params.id}`);
          this.car = response.data;
        } catch (error) {
          console.error("Ошибка загрузки деталей автомобиля:", error.response?.data || error.message);
        }
      },
      navigateToEdit() {
        this.$router.push(`/cars/edit/${this.$route.params.id}`);
      },
      navigateBack() {
        this.$router.push("/cars");
      },
      async deleteCar() {
      const confirmDelete = confirm("Вы уверены, что хотите удалить этот автомобиль?");
      if (confirmDelete) {
        try {
          await apiClient.delete(`/automobiles/${this.car.id}/`);
          this.$router.push("/cars");
        } catch (error) {
          console.error("Ошибка удаления автомобиля:", error.response?.data || error.message);
        }
      }
    }
    },
    async created() {
      await this.fetchCarDetails();
    },
  };
  </script>
  
  <style scoped>
  .car-details {
    margin-top: 50px;
  }
  .mb-4 {
    margin-bottom: 20px;
  }
  .text-center {
    text-align: center;
  }
  </style>
  