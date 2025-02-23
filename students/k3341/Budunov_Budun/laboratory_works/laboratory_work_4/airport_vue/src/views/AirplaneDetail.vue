<template>
    <v-container>
      <v-row>
        <v-col cols="12">
          <h1>Airplane Detail</h1>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12">
          <v-card>
            <v-card-title>Airplane Information</v-card-title>
            <v-card-text>
              <p>
                <strong>Registration Number:</strong>
                {{ airplane.registration_number }}
              </p>
              <p>
                <strong>Model:</strong>
                {{ airplane.airplane_model ? airplane.airplane_model.name : "N/A" }}
              </p>
              <p>
                <strong>Airline:</strong>
                {{ airplane.airline ? airplane.airline.name : "N/A" }}
              </p>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <v-row>
          <v-col cols="12">
              <v-card>
                  <v-card-title>Maintenance history</v-card-title>
                  <v-card-text>
                    <v-table v-if="maintenance && maintenance.length">
                      <thead>
                        <tr>
                          <th>Date</th>
                          <th>Description</th>
                        </tr>
                      </thead>
                      <tbody>
                        <tr v-for="m in maintenance" :key="m.id">
                          <td>{{m.date}}</td>
                          <td>{{m.description}}</td>
                        </tr>
                      </tbody>
                    </v-table>
                    <p v-else>No maintenance records yet</p>
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
    name: "AirplaneDetail",
    components: {
      Loading,
    },
    data() {
      return {
        airplane: {},
        maintenance: [],
        isLoading: true,
      };
    },
    created() {
      this.fetchAirplane();
    },
    methods: {
      async fetchAirplane() {
        try {
          const airplaneResponse = await api.get(`/airplane/${this.$route.params.id}/`);
          this.airplane = airplaneResponse.data;
          const maintenanceResponse = await api.get(`/airplane/${this.$route.params.id}/maintenance/`);
          this.maintenance = maintenanceResponse.data
        } catch (error) {
          console.error(error);
        } finally {
          this.isLoading = false;
        }
      },
    },
  };
  </script>
  