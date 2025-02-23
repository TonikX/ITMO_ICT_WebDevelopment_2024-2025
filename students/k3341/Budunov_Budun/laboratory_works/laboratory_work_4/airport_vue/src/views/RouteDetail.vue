<template>
    <v-container>
      <v-row>
        <v-col cols="12">
          <h1>Route Detail</h1>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12">
          <v-card>
            <v-card-title>Route Information</v-card-title>
            <v-card-text>
              <p><strong>Airline:</strong> {{ route.airline ? route.airline.name : 'N/A' }}</p>
              <p><strong>Departure Airport:</strong> {{ route.departure_airport ? route.departure_airport.name : 'N/A' }}</p>
              <p><strong>Arrival Airport:</strong> {{ route.arrival_airport ? route.arrival_airport.name : 'N/A' }}</p>
              <p><strong>Distance:</strong> {{ route.distance }}</p>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12">
          <v-card>
            <v-card-title>Related flights</v-card-title>
            <v-card-text>
              <v-table v-if="flights && flights.length">
                <thead>
                <tr>
                  <th>Flight Number</th>
                  <th>Departure Time</th>
                  <th>Arrival Time</th>
                  <th>Airplane</th>
                </tr>
                </thead>
                <tbody>
                <tr v-for="flight in flights" :key="flight.id">
                  <td>{{ flight.flight_number }}</td>
                  <td>{{ flight.departure_time }}</td>
                  <td>{{ flight.arrival_time }}</td>
                  <td>{{ flight.airplane }}</td>
                </tr>
                </tbody>
              </v-table>
              <p v-else>There are no flights in this route</p>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <Loading v-if="isLoading" />
    </v-container>
  </template>
  
  <script>
  import api from "@/api";
  import Loading from "@/components/Loading.vue";
  
  export default {
    name: "RouteDetail",
    components: {
      Loading,
    },
    data() {
      return {
        route: {},
        flights: [],
        isLoading: true,
      };
    },
    created() {
      this.fetchRoute();
    },
    methods: {
      async fetchRoute() {
        try {
          const routeResponse = await api.get(`/route/${this.$route.params.id}/`);
          this.route = routeResponse.data;
          const flightsResponse = await api.get(`/route/${this.$route.params.id}/flights/`)
          this.flights = flightsResponse.data
        } catch (error) {
          console.error(error);
        } finally {
          this.isLoading = false;
        }
      },
    },
  };
  </script>
  