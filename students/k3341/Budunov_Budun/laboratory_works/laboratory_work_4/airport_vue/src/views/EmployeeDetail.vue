<template>
    <v-container>
      <v-row>
        <v-col cols="12">
          <h1>Employee Detail</h1>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12">
          <v-card>
            <v-card-title>Employee Information</v-card-title>
            <v-card-text>
              <p><strong>Full Name:</strong> {{ employee.full_name }}</p>
              <p><strong>Position:</strong> {{ employee.position }}</p>
              <p><strong>Airline:</strong> {{ employee.airline ? employee.airline.name : "N/A" }}</p>
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
    name: "EmployeeDetail",
    components: {
      Loading,
    },
    data() {
      return {
        employee: {},
        isLoading: true,
      };
    },
    created() {
      this.fetchEmployee();
    },
    methods: {
      async fetchEmployee() {
        try {
          const response = await api.get(`/employee/${this.$route.params.id}/`);
          this.employee = response.data;
        } catch (error) {
          console.error(error);
        } finally {
          this.isLoading = false;
        }
      },
    },
  };
  </script>
  