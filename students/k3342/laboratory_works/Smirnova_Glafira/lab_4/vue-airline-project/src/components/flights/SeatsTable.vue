<template>
  <v-container>

    <v-row>
      <v-col cols="12" md="6">
        <v-select
          v-model="filter"
          :items="statusOptions"
          label="Фильтр по статусу"
          clearable
        ></v-select>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12">
        <v-data-table
          :headers="headers"
          :items="filteredSeats"
          class="elevation-1"
        >
          <template v-slot:top>
            <v-toolbar flat>
              <v-toolbar-title class="text-center w-100">Места на рейс</v-toolbar-title>
            </v-toolbar>
          </template>

          <template v-slot:item.is_sold="{ item }">
            <span :style="{ color: item.is_sold ? 'blue' : 'green' }">
                {{ item.is_sold ? "Занято" : "Свободно" }}
            </span>
          </template>
        </v-data-table>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import apiClient from "@/services/api.js";

export default {
  props: {
    flightId: {
      type: String,
      required: true,
    },
  },
  data() {
    return {
      seats: [],
      filter: null,
      statusOptions: ["Занято", "Свободно"],
      headers: [
        { title: "Номер места", key: "number" },
        { title: "Статус", key: "is_sold" },
      ],
    };
  },
  computed: {
    filteredSeats() {
      if (!this.filter) {
        return this.seats;
      }
      const isSold = this.filter === "Занято";
      return this.seats.filter((seat) => seat.is_sold === isSold);
    },
  },
  methods: {
    async fetchSeats() {
      try {
        const response = await apiClient.get(`/flights/${this.flightId}/seats/`);
        this.seats = response.data.map((seat) => ({
          ...seat,
          is_sold: seat.is_sold,
        }));
      } catch (error) {
        console.error("Ошибка загрузки мест:", error.response?.data || error.message);
        alert("Ошибка загрузки мест");
      }
    },
  },
  async created() {
    await this.fetchSeats();
  },
};
</script>

<style>
.text-center {
  text-align: center;
}
</style>
