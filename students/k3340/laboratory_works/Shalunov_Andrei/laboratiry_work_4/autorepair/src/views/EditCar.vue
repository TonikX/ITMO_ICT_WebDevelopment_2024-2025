<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="text-center">Редактировать автомобиль</h1>
      </v-col>
    </v-row>

    <v-form ref="form">
      <v-text-field v-model="car.brand" label="Марка" required></v-text-field>
      <v-text-field v-model="car.model" label="Модель" required></v-text-field>
      <v-text-field v-model="car.year_of_vehicle" label="Год выпуска" type="number" required></v-text-field>
      <v-text-field v-model="car.state_number" label="Гос. номер" required></v-text-field>

      <v-select
        v-model="car.client_id"
        :items="clients"
        label="Клиент"
        item-value="id"
        item-title="full_name"
        required
      ></v-select>

      <v-select
        v-model="car.auto_model_id"
        :items="models"
        label="Модель автомобиля"
        item-value="id"
        item-title="car_brand + ' ' + model" <!-- Отображение марки и модели -->
        required
      ></v-select>

      <v-btn color="primary" @click="updateCar">Сохранить</v-btn>
    </v-form>
  </v-container>
</template>

<script>
import apiClient from "@/services/api";

export default {
  data() {
    return {
      car: {
        id: null,
        brand: "",
        model: "",
        year_of_vehicle: "",
        state_number: "",
        client_id: null,
        auto_model_id: null,
      },
      clients: [],
      models: [],
    };
  },
  methods: {
    async fetchChoices() {
      try {
        const [clientsResponse, modelsResponse] = await Promise.all([
          apiClient.get("/clients/"),
          apiClient.get("/models/"),
        ]);
        this.clients = clientsResponse.data;
        this.models = modelsResponse.data;
      } catch (error) {
        console.error("Ошибка загрузки данных для выбора:", error.response?.data || error.message);
      }
    },
    async fetchCarData() {
      const carId = this.$route.params.id;
      try {
        const response = await apiClient.get(`/automobiles/${carId}/`);
        this.car = response.data;
      } catch (error) {
        console.error("Ошибка загрузки данных автомобиля:", error.response?.data || error.message);
      }
    },
    async updateCar() {
      try {
        const response = await apiClient.put(`/automobiles/${this.car.id}/`, this.car);
        this.$router.push("/cars");
        console.log("Успешно обновлен автомобиль:", response.data);
      } catch (error) {
        console.error("Ошибка при обновлении автомобиля:", error.response?.data || error.message);
      }
    },
  },
  mounted() {
    this.fetchChoices();
    this.fetchCarData();
  },
};
</script>

<style scoped>
.text-center {
  text-align: center;
}
</style>
