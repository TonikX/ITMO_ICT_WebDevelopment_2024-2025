<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h1 class="text-center">Список перелетов</h1>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" md="4">
        <v-select
          v-model="filters.route"
          :items="choices.route_choices"
          label="Фильтр по маршруту"
          item-value="name"
          item-title="name"
          clearable
        ></v-select>
      </v-col>
      <v-col cols="12" md="4">
        <v-select
          v-model="filters.status"
          :items="choices.status_choices"
          label="Фильтр по статусу"
          item-value="name"
          item-title="name"
          clearable
        ></v-select>
      </v-col>
      <v-col cols="12" md="4">
        <v-text-field
          v-model="filters.date"
          label="Фильтр по дате вылета"
          type="date"
          clearable
        ></v-text-field>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" class="d-flex justify-end">
        <v-btn color="primary" @click="openCreateDialog">Добавить перелет</v-btn>
      </v-col>
    </v-row>

    <v-row>
      <v-col
        cols="12"
        md="6"
        v-for="flight in filteredAndPaginatedFlights"
        :key="flight.id"
      >
        <v-card class="mb-6" elevation="2">
          <v-card-title>
            Номер: {{ flight.number }}
          </v-card-title>
          <v-card-subtitle>
            Самолет: {{ flight.plane }}
          </v-card-subtitle>
          <v-card-text>
            <p><strong>Маршрут: </strong>{{ flight.route }}</p>
            <v-divider class="my-2"></v-divider>
            <p v-if="flight.stops.length > 0"><strong>Остановки:</strong> {{ flight.stops.join(', ') }}</p>
            <p v-else><strong>Остановки:</strong> Нет остановок</p>
            <v-divider class="my-2"></v-divider>
            <p><strong>Вылет:</strong> {{ flight.departure_time }}</p>
            <v-divider class="my-2"></v-divider>
            <p><strong>Прибытие:</strong> {{ flight.arrival_time }}</p>
            <v-divider class="my-2"></v-divider>
            <p><strong>Статус:</strong> {{ flight.status }}</p>
          </v-card-text>
          <v-card-actions class="justify-center">
            <v-btn color="primary" @click="navigateToFlight(flight.id)">Детали</v-btn>
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

    <CreateFlightDialog
      ref="createFlightDialog"
      :dialog="createDialog"
      @update:dialog="createDialog = $event"
      :choices="choices"
      @flight-created="addFlight"
    />
  </v-container>
</template>

<script>
import apiClient from "@/services/api";
import CreateFlightDialog from "@/components/flights/CreateFlightDialog.vue";

export default {
  components: { CreateFlightDialog: CreateFlightDialog },
  data() {
    return {
      flights: [],
      currentPage: 1,
      itemsPerPage: 4,
      filters: {
        route: null,
        status: null,
        date: null,
      },
      createDialog: false,
      choices: {
        route_choices: [],
        plane_choices: [],
        crew_choices: [],
        status_choices: [],
      },
    };
  },
  computed: {
    filteredFlights() {
      console.log(this.filters)
      let flights = this.flights;
      if (!this.filters.route && !this.filters.status && !this.filters.date) {
        return flights;
      }
      return flights.filter((flight) => {
        const matchesRoute =
          !this.filters.route || flight.route === this.filters.route;
        const matchesStatus =
          !this.filters.status || flight.status === this.filters.status;
        const matchesDate =
          !this.filters.date || flight.departure_time.startsWith(this.filters.date);
        return matchesRoute && matchesStatus && matchesDate;
      });
    },
    filteredAndPaginatedFlights() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.filteredFlights.slice(start, end);
    },
    totalPages() {
      return Math.ceil(this.filteredFlights.length / this.itemsPerPage);
    },
  },
  methods: {
    async fetchFlights() {
      try {
        const response = await apiClient.get("/flights/");
        this.flights = response.data.map((flight) => ({
          ...flight,
          departure_time: `${flight.departure_date} ${flight.departure_time}`,
          arrival_time: `${flight.arrival_date} ${flight.arrival_time}`,
        }));
      } catch (error) {
        console.error("Ошибка загрузки перелетов:", error.response?.data || error.message);
      }
    },
    async fetchChoices() {
      try {
        const response = await apiClient.get("/flights/choices/");
        this.choices = response.data;
      } catch (error) {
        console.error("Ошибка загрузки данных для выбора:", error.response?.data || error.message);
      }
    },
    openCreateDialog() {
      this.createDialog = true;
    },
    async addFlight(newFlight) {
      try {
        await apiClient.post("/flights/", newFlight);
        await this.fetchFlights();
        this.$refs.createFlightDialog.closeDialog();
      } catch (error) {
        if (error.response && error.response.status === 400) {
          this.$refs.createFlightDialog.setErrors(error.response.data);
        } else {
          console.error("Ошибка создания перелета:", error.response?.data || error.message);
          alert("Ошибка создания перелета");
        }
      }
    },

    navigateToFlight(flightId) {
      this.$router.push(`/flights/${flightId}`);
    },
  },
  async created() {
    await Promise.all([this.fetchFlights(), this.fetchChoices()]);
  },
};
</script>
