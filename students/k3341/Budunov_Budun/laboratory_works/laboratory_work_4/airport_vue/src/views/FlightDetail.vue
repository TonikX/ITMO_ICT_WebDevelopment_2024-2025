<template>
    <v-container>
      <v-row>
        <v-col cols="12">
          <h1>Flight Detail</h1>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12">
          <v-card>
            <v-card-title>
              Flight Information
            </v-card-title>
            <v-card-text>
              <p><strong>Flight Number:</strong> {{ flight.flight_number }}</p>
              <p><strong>Route:</strong> {{ flight.route }}</p>
              <p><strong>Departure Time:</strong> {{ flight.departure_time }}</p>
              <p><strong>Arrival Time:</strong> {{ flight.arrival_time }}</p>
              <p><strong>Airplane:</strong> {{ flight.airplane }}</p>
              <p><strong>Crews:</strong></p>
                <ul>
                  <li v-for="crew in flight.crews" :key="crew.id">{{ crew.employee }}</li>
                </ul>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
        <v-row v-if="transits && transits.length">
            <v-col cols="12">
              <v-card>
                <v-card-title>
                    Transits
                </v-card-title>
                  <v-card-text>
                    <v-table>
                      <thead>
                        <tr>
                          <th>Airport</th>
                          <th>Arrival</th>
                          <th>Departure</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="transit in transits" :key="transit.id">
                            <td>{{ transit.airport }}</td>
                            <td>{{ transit.arrival_time }}</td>
                            <td>{{ transit.departure_time }}</td>
                        </tr>
                      </tbody>
                    </v-table>
                  </v-card-text>
              </v-card>
            </v-col>
        </v-row>
      <Loading v-if="isLoading"/>
    </v-container>
  </template>
  
  <script>
  import api from "@/api";
  import Loading from '@/components/Loading.vue';
  
  export default {
    name: "FlightDetail",
    components: {
      Loading
    },
    data() {
      return {
        flight: {},
          transits: [],
        isLoading: true,
      };
    },
    created() {
      this.fetchFlight();
    },
    methods: {
      async fetchFlight() {
        try {
          const response = await api.get(`/flight/${this.$route.params.id}/full_info/`);
          this.flight = response.data.flight;
          this.transits = response.data.transits;
        } catch (error) {
          console.error(error);
        } finally {
          this.isLoading = false
        }
      },
    },
  };
  </script>
  