<template>
    <v-container>
      <v-row>
        <v-col cols="12">
          <h1>Profile</h1>
        </v-col>
      </v-row>
      <v-row v-if="user">
        <v-col cols="12">
          <v-card>
            <v-card-title>User Information</v-card-title>
            <v-card-text>
              <p><strong>Username:</strong> {{ user.username }}</p>
              <p><strong>Is admin:</strong> {{ user.is_admin }}</p>
              <p><strong>Full name:</strong> {{ user.employee.full_name }}</p>
              <p><strong>Position:</strong> {{ user.employee.position }}</p>
              <p><strong>Airline:</strong> {{ user.employee.airline ? user.employee.airline.name : 'N/A' }}</p>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <v-row>
        <v-col cols="12">
          <v-card>
            <v-card-title>Change profile</v-card-title>
            <v-card-text>
              <v-form v-model="valid" @submit.prevent="onSubmit">
                <v-text-field
                  v-model="requestData.full_name"
                  label="Full Name"
                  outlined
                  required
                ></v-text-field>
                  <v-text-field
                          v-model="requestData.position"
                          label="Position"
                          outlined
                          required
                  ></v-text-field>
                  <v-select
                          v-model="requestData.airline"
                          :items="airlines"
                          item-text="name"
                          item-value="id"
                          label="Airline"
                          outlined
                          required>
                  </v-select>
                <v-btn type="submit" :disabled="!valid">Send request</v-btn>
              </v-form>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
      <v-row>
          <v-col cols="12">
              <v-btn @click="logout" color="primary">Logout</v-btn>
          </v-col>
      </v-row>
      <Loading v-if="isLoading" />
    </v-container>
  </template>
  
  <script>
  import api from "@/api";
  import { mapState, mapActions } from "vuex";
  import Loading from "@/components/Loading.vue";
  
  export default {
    name: "Profile",
    components: {
      Loading,
    },
    data() {
      return {
        valid: false,
        requestData: {
          full_name: "",
          position: "",
          airline: null,
        },
        airlines: [],
        isLoading: true,
      };
    },
    computed: {
      ...mapState("auth", ["user"]),
    },
    created() {
      this.fetchData();
    },
    methods: {
      ...mapActions('auth', ['logout']),
      async fetchData() {
        try {
          const airlinesResponse = await api.get("/airline/");
          this.airlines = airlinesResponse.data;
          this.requestData.full_name = this.user.employee.full_name
          this.requestData.position = this.user.employee.position
          this.requestData.airline = this.user.employee.airline.id
        } catch (error) {
          console.error(error);
        } finally {
          this.isLoading = false;
        }
      },
      async onSubmit() {
        try {
          await api.post("/profile_change_request/", this.requestData);
          alert('Your request successfully sent!')
        } catch (error) {
          console.error(error);
        }
      },
      logout() {
        this.logout();
        this.$router.push('/login');
      }
    },
  };
  </script>
  