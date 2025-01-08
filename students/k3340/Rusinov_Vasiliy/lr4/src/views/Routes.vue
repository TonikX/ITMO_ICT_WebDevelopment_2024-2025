<template>
  <v-container>

    <v-row>
      <v-col cols="12">
        <h1 class="text-center">Маршруты</h1>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" md="3">
        <v-text-field
          v-model="filters.number"
          label="Поиск по номеру"
          clearable
        ></v-text-field>
      </v-col>
      <v-col cols="12" md="3">
        <v-select
          v-model="filters.departure_airport"
          :items="choices.airports"
          label="Аэропорт вылета"
          item-value="name"
          item-title="name"
          clearable
        ></v-select>
      </v-col>
      <v-col cols="12" md="3">
        <v-select
          v-model="filters.destination_airport"
          :items="choices.airports"
          label="Аэропорт прилета"
          item-value="name"
          item-title="name"
          clearable
        ></v-select>
      </v-col>
      <v-col cols="12" md="3">
        <v-select
          v-model="filters.regularity"
          :items="choices.regularity"
          label="Регулярность"
          clearable
        ></v-select>
      </v-col>
    </v-row>

    <v-row>
      <v-col
        cols="12"
        md="6"
        v-for="route in filteredRoutes"
        :key="route.id"
      >
        <v-card class="compact-card mb-6" elevation="2">
          <v-card-title>
            <strong>Маршрут:</strong> {{ route.number }}
          </v-card-title>
          <v-card-text>
            <p><strong>Аэропорт вылета:</strong> {{ route.departure_airport }}</p>
            <v-divider class="my-2"></v-divider>
            <p><strong>Аэропорт прибытия:</strong> {{ route.destination_airport }}</p>
            <v-divider class="my-2"></v-divider>
            <p><strong>Время вылета:</strong> {{ route.departure_time }}</p>
            <v-divider class="my-2"></v-divider>
            <p><strong>Время прибытия:</strong> {{ route.arrival_time }}</p>
            <v-divider class="my-2"></v-divider>
            <p><strong>Регулярность:</strong> {{ route.regularity }}</p>
            <v-divider class="my-2"></v-divider>
            <p><strong>Расстояние:</strong> {{ route.distance_km }} км</p>
            <v-divider class="my-2"></v-divider>

            <template v-if="route.stops.length > 0">
              <p><strong>Остановки:</strong></p>
              <ul class="stops-list">
                <li v-for="stop in route.stops" :key="stop.airport">
                  <strong>{{ stop.airport }}</strong>:
                  Прибытие: {{ stop.arrival_time || 'неизвестно' }},
                  Отправление: {{ stop.departure_time || 'неизвестно' }}
                </li>
              </ul>
            </template>
            <template v-else>
              <p><strong>Остановки:</strong> Нет остановок</p>
            </template>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import apiClient from "@/services/api";

export default {
  data() {
    return {
      routes: [],
      filters: {
        number: null,
        departure_airport: null,
        destination_airport: null,
        regularity: null,
      },
      choices: {
        airports: [],
        regularity: [],
      },
    };
  },
  computed: {
    filteredRoutes() {
      let filtered = this.routes;

      if (this.filters.number) {
        filtered = filtered.filter(route =>
          route.number.toLowerCase().includes(this.filters.number.toLowerCase())
        );
      }
      if (this.filters.departure_airport) {
        filtered = filtered.filter(
          route =>
            route.departure_airport === this.filters.departure_airport
        );
      }
      if (this.filters.destination_airport) {
        filtered = filtered.filter(
          route =>
            route.destination_airport === this.filters.destination_airport
        );
      }
      if (this.filters.regularity) {
        filtered = filtered.filter(
          route => route.regularity === this.filters.regularity
        );
      }

      return filtered;
    },
  },
  methods: {
    async fetchRoutes() {
      try {
        const response = await apiClient.get("/routes/");
        this.routes = response.data;
        this.choices.regularity = [...new Set(this.routes.map(route => route.regularity))];
      } catch (error) {
        console.error("Ошибка загрузки маршрутов:", error.response?.data || error.message);
      }
    },
    async fetchChoices() {
      try {
        const response = await apiClient.get("/airports/");
        this.choices.airports = response.data.airports.map(airport => ({
          name: airport.name,
        }));
      } catch (error) {
        console.error("Ошибка загрузки аэропортов:", error.response?.data || error.message);
      }
    },
  },
  async created() {
    await Promise.all([this.fetchRoutes(), this.fetchChoices()]);
  },
};
</script>

<style>
.text-center {
  text-align: center;
}
.stops-list {
  padding-left: 0;
  margin: 0 auto;
  text-align: center;
  list-style-position: inside;
}
.stops-list li {
  margin: 5px 0;
}
.compact-card {
  max-width: 700px;
  margin: 0 auto;
}
</style>

