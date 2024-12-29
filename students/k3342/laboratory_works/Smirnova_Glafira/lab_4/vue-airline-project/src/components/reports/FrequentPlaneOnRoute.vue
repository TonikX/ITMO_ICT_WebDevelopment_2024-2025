<template>
  <v-container>
    <h1>Самый частый самолет на маршруте</h1>

    <v-select
      v-model="selectedRoute"
      :items="routes"
      item-title="route_str"
      item-value="id"
      label="Выберите маршрут"
      @update:model-value="fetchMostFrequentPlane"
    ></v-select>

    <v-card v-if="mostFrequentPlane" class="mt-4">
      <v-card-title>
        Модель самолета: {{ mostFrequentPlane.plane_model.name }}
      </v-card-title>
      <v-card-subtitle>
        Вместимость: {{ mostFrequentPlane.plane_model.seats_capacity }} мест
      </v-card-subtitle>
      <v-card-subtitle>
        Скорость: {{ mostFrequentPlane.plane_model.speed }} км/ч
      </v-card-subtitle>
      <v-card-text>
        Количество перелетов: {{ mostFrequentPlane.flight_count }}
      </v-card-text>
    </v-card>

    <v-alert v-else-if="noFlights" class="mt-4 custom-warning">
      По данному маршруту не было перелетов.
    </v-alert>

    <v-alert v-else-if="loading" type="info" class="mt-4">Загрузка...</v-alert>
    <v-alert v-else class="mt-4 custom-warning">Пожалуйста, выберите маршрут.</v-alert>
  </v-container>
</template>

<script>
import apiClient from "@/services/api.js";

export default {
  data() {
    return {
      routes: [],
      selectedRoute: null,
      mostFrequentPlane: null,
      loading: false,
      noFlights: false,
    };
  },
  created() {
    this.fetchRoutes();
  },
  methods: {
    async fetchRoutes() {
      try {
        const response = await apiClient.get('/routes/');
        this.routes = response.data;
      } catch (error) {
        console.error('Ошибка при получении маршрутов:', error);
      }
    },
    async fetchMostFrequentPlane() {
      if (!this.selectedRoute) return;

      this.loading = true;
      this.noFlights = false;
      try {
        const response = await apiClient.get(`/routes/${this.selectedRoute}/most-frequent-plane/`);

        if (response.data.most_frequent_plane) {
          this.mostFrequentPlane = response.data.most_frequent_plane;
        } else {
          this.noFlights = true;
          this.mostFrequentPlane = null;
        }

      } catch (error) {
        console.error('Ошибка при получении информации о самолете:', error);
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
</style>
