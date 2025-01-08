<template>
  <v-container>
    <h1>Борты авиалинии</h1>

    <v-card>
      <v-card-title>
        Общее количество бортов: {{ totalPlanes }}
      </v-card-title>
    </v-card>

    <div class="mt-4">
      <v-card v-for="model in modelsStatistics" :key="model.model" class="mb-3">
        <v-card-title>
          Модель: {{ model.model }}
        </v-card-title>
        <v-card-subtitle>
          Количество бортов: {{ model.plane_amount }}<br>
          Количество посадочных мест: {{ model.seat_capacity }}<br>
          Скорость: {{ model.speed }} км/ч<br>
          Номера самолетов: {{ model.plane_numbers.join(', ') }}
        </v-card-subtitle>
      </v-card>
    </div>

    <v-alert v-if="loading" type="info" class="mt-4">Загрузка...</v-alert>
    <v-alert v-if="error" type="error" class="mt-4">{{ error }}</v-alert>
  </v-container>
</template>

<script>
import apiClient from "@/services/api.js";

export default {
  data() {
    return {
      totalPlanes: 0,
      modelsStatistics: [],
      loading: false,
      error: null,
    };
  },
  created() {
    this.fetchPlaneStatistics();
  },
  methods: {
    async fetchPlaneStatistics() {
      this.loading = true;
      this.error = null;
      try {
        const response = await apiClient.get('/plane-statistics/');
        this.totalPlanes = response.data.total_planes;
        this.modelsStatistics = response.data.models_statistics;
      } catch (error) {
        console.error('Ошибка при получении статистики по самолетам:', error);
        this.error = 'Не удалось загрузить данные.';
      } finally {
        this.loading = false;
      }
    },
  },
};
</script>

<style scoped>
</style>
