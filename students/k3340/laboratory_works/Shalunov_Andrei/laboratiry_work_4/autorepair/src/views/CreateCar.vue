<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="text-center">Добавить новый автомобиль</h1>
      </v-col>
    </v-row>

    <v-form ref="form">
      <v-text-field v-model="car.engine_number" label="Номер двигателя" required></v-text-field>
      <v-text-field v-model="car.year_of_vehicle" label="Год выпуска" type="number" required></v-text-field>
      <v-text-field v-model="car.colour" label="Цвет" required></v-text-field>
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
        item-title="model"
        required
      ></v-select>

      <v-btn color="primary" @click="createCar">Создать</v-btn>
    </v-form>
  </v-container>
</template>

<script>
import apiClient from "@/services/api";

export default {
  data() {
    return {
      car: {
        engine_number: "",
        year_of_vehicle: "",
        colour: "",
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

    async createCar() {
      try {
        const response = await apiClient.post("/automobiles/", {
          engine_number: this.car.engine_number,
          year_of_vehicle: this.car.year_of_vehicle,
          colour: this.car.colour,
          state_number: this.car.state_number,
          client: this.car.client_id,
          auto_model: this.car.auto_model_id,
        });
        
        this.$router.push("/cars");
        console.log("Успешно добавлен автомобиль:", response.data);
      } catch (error) {
        console.error("Ошибка при добавлении автомобиля:", error.response?.data || error.message);
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
