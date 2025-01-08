<template>
  <v-container>
    <h1>Незаполненные маршруты</h1>

    <v-text-field
      v-model="threshold"
      label="Процент заполненности (по умолчанию 50%)"
      type="number"
      min="0"
      max="100"
      dense
      style="max-width: 700px;"
    >

    <template #append>
        <v-btn @click="fetchUnderFilledRoutes" color="primary">Показать маршруты</v-btn>
      </template>
    </v-text-field>

     <div v-if="underFilledRoutes.length > 0" class="mt-4">
      <v-card v-for="route in underFilledRoutes" :key="route.id" class="mb-3">
        <v-card-title>
          Маршрут: {{ route.id }}<br>
          {{ route.departure_airport }}<br>
          - {{ route.destination_airport }})
        </v-card-title>
        <v-card-subtitle>
          Время вылета: {{ route.route.departure_time }}<br>
          Время прибытия: {{ route.route.arrival_time }}<br>
          <p v-if="route.stops.length > 0">Остановки: {{ route.stops.join(', ') }}</p>
          <p v-else>Остановки: Нет остановок</p>
          Расстояние: {{ route.route.distance_km }} км<br>
          Регулярность: {{ route.route.regularity }}<br>
        </v-card-subtitle>
        <v-card-text>
          Количество незаполненных перелетов:<p><strong>{{ route.under_filled_count }} ({{ route.under_filled_percentage }}%)</strong></p>
        </v-card-text>
      </v-card>
    </div>

    <v-alert v-else-if="loading" type="info" class="mt-4">Загрузка...</v-alert>
    <v-alert v-else-if="error" type="error" class="mt-4">{{ error }}</v-alert>
    <v-alert v-else class="mt-4 custom-warning">Нет маршрутов, соответствующих критериям.</v-alert>
  </v-container>
</template>

<script>
import apiClient from "@/services/api.js";

export default {
  data() {
    return {
      threshold: 50,
      underFilledRoutes: [],
      loading: false,
      error: null,
    };
  },
  methods: {
    async fetchUnderFilledRoutes() {
      this.loading = true;
      this.error = null;
      try {
        const response = await apiClient.get('routes/under-filled/', {
          params: { threshold: this.threshold },
        });

        this.underFilledRoutes = response.data.map(route => {
          return {
            ...route,
            stops: route.route.stops.map(stop => stop.airport)
          };
        });
      } catch (error) {
        console.error('Ошибка при получении незаполненных маршрутов:', error);
        this.error = 'Не удалось загрузить данные.';
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style>
.custom-warning {
  background-color: #b09af4;
  color: #ffffff;
}
</style>
