<template>
    <v-container>
      <v-row>
        <v-col cols="12">
          <h1 class="text-center">Список клиентов</h1>
        </v-col>
      </v-row>
  
      <v-row>
        <v-col cols="12" md="4">
          <v-text-field
            v-model="filters.full_name"
            label="Фильтр по имени"
            clearable
          ></v-text-field>
        </v-col>
        <v-col cols="12" md="4">
          <v-text-field
            v-model="filters.phone"
            label="Фильтр по телефону"
            clearable
          ></v-text-field>
        </v-col>
        <v-col cols="12" md="4">
          <v-text-field
            v-model="filters.email"
            label="Фильтр по email"
            clearable
          ></v-text-field>
        </v-col>
      </v-row>
  
      <v-row>
        <v-col cols="12" class="d-flex justify-end">
          <v-btn color="primary" @click="navigateToCreate">Добавить клиента</v-btn>
        </v-col>
      </v-row>
  
      <v-row>
        <v-col
          cols="12"
          md="6"
          v-for="client in filteredAndPaginatedClients"
          :key="client.id"
        >
          <v-card class="mb-6" elevation="2">
            <v-card-title>{{ client.full_name }}</v-card-title>
            <v-card-subtitle>{{ client.phone }}</v-card-subtitle>
            <v-card-text>
              <p><strong>Email:</strong> {{ client.email }}</p>
            </v-card-text>
            <v-card-actions class="justify-center">
              <v-btn color="primary" @click="navigateToDetails(client.id)">Детали</v-btn>
              <v-btn color="primary" @click="navigateToEdit(client.id)">Редактировать</v-btn>
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
    </v-container>
  </template>
  
  <script>
  import apiClient from "@/services/api";
  
  export default {
    data() {
      return {
        clients: [],
        filters: {
          full_name: "",
          phone: "",
          email: "",
        },
        currentPage: 1,
        itemsPerPage: 5,
      };
    },
    computed: {
      filteredClients() {
        return this.clients.filter((client) => {
          const matchesFullName =
            !this.filters.full_name || client.full_name.includes(this.filters.full_name);
          const matchesPhone =
            !this.filters.phone || client.phone.includes(this.filters.phone);
          const matchesEmail =
            !this.filters.email || client.email.includes(this.filters.email);
          return matchesFullName && matchesPhone && matchesEmail;
        });
      },
      filteredAndPaginatedClients() {
        const start = (this.currentPage - 1) * this.itemsPerPage;
        const end = start + this.itemsPerPage;
        return this.filteredClients.slice(start, end);
      },
      totalPages() {
        return Math.ceil(this.filteredClients.length / this.itemsPerPage);
      },
    },
    methods: {
      async fetchClients() {
        try {
          const response = await apiClient.get("/clients/");
          this.clients = response.data;
        } catch (error) {
          console.error("Ошибка загрузки клиентов:", error.response?.data || error.message);
        }
      },
      navigateToCreate() {
        this.$router.push("/clients/create");
      },
      navigateToEdit(clientId) {
        this.$router.push(`/clients/edit/${clientId}`);
      },
      navigateToDetails(clientId) {
        this.$router.push(`/clients/${clientId}`);
      },
    },
    async created() {
      await this.fetchClients();
    },
  };
  </script>
  
  <style scoped>
  .text-center {
    text-align: center;
  }
  .mb-6 {
    margin-bottom: 1.5rem;
  }
  </style>
  