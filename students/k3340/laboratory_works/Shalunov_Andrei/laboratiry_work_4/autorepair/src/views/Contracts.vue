<template>
    <v-container>
      <v-row>
        <v-col cols="12">
          <h1 class="text-center">Список договоров</h1>
        </v-col>
      </v-row>
  
      <v-row>
        <v-col cols="12" md="3">
          <v-select
            v-model="filters.client"
            label="Фильтр по клиенту"
            :items="clients"
            item-value="id"
            item-title="full_name"
            clearable
          ></v-select>
        </v-col>
  
        <v-col cols="12" md="3">
          <v-select
            v-model="filters.status"
            label="Фильтр по статусу"
            :items="statuses"
            clearable
          ></v-select>
        </v-col>
  
        <v-col cols="12" md="3">
          <v-select
            v-model="filters.payment_status"
            label="Фильтр по статусу оплаты"
            :items="['Paid', 'Unpaid']"
            clearable
          ></v-select>
        </v-col>
  
        <v-col cols="12" md="3">
          <v-text-field
            v-model="filters.date"
            label="Фильтр по дате"
            type="date"
            clearable
          ></v-text-field>
        </v-col>
      </v-row>
  
      <v-row>
        <v-col cols="12" class="d-flex justify-end">
          <v-btn color="primary" @click="navigateToCreate">Добавить договор</v-btn>
        </v-col>
      </v-row>
  
      <v-row>
        <v-col
          cols="12"
          md="6"
          v-for="contract in filteredAndPaginatedContracts"
          :key="contract.id"
        >
          <v-card class="mb-6" elevation="2">
            <v-card-title>Договор №{{ contract.id }}</v-card-title>
            <v-card-subtitle>
              Клиент: {{ contract.client.full_name }}
            </v-card-subtitle>
            <v-card-text>
              <p><strong>Статус:</strong> {{ contract.order_status }}</p>
              <p><strong>Стоимость:</strong> {{ contract.total_payment }} руб.</p>
              <p><strong>Статус оплаты:</strong> {{ contract.payment_status }}</p>
            </v-card-text>
            <v-card-actions class="justify-center">
              <v-btn color="primary" @click="navigateToDetails(contract.id)">Детали</v-btn>
              <v-btn color="primary" @click="navigateToEdit(contract.id)">Редактировать</v-btn>
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
        contracts: [],
        clients: [],
        statuses: ["Pending", "In Progress", "Completed"],
        paymentStatuses: ["Paid", "Unpaid"],
        currentPage: 1,
        itemsPerPage: 5,
        filters: {
          client: null,
          status: null,
          payment_status: null,
          date: null,
        },
      };
    },
    computed: {
      filteredContracts() {
        return this.contracts.filter((contract) => {
          const matchesClient =
            !this.filters.client || contract.client.id === this.filters.client;
          const matchesStatus =
            !this.filters.status || contract.order_status === this.filters.status;
          const matchesPaymentStatus =
            !this.filters.payment_status || contract.payment_status === this.filters.payment_status;
          const matchesDate =
            !this.filters.date || contract.order_date.startsWith(this.filters.date);
          return matchesClient && matchesStatus && matchesPaymentStatus && matchesDate;
        });
      },
      filteredAndPaginatedContracts() {
        const start = (this.currentPage - 1) * this.itemsPerPage;
        const end = start + this.itemsPerPage;
        return this.filteredContracts.slice(start, end);
      },
      totalPages() {
        return Math.ceil(this.filteredContracts.length / this.itemsPerPage);
      },
    },
    methods: {
      async fetchContracts() {
        try {
          const response = await apiClient.get("/contracts/");
          this.contracts = response.data;
        } catch (error) {
          console.error("Ошибка загрузки договоров:", error.response?.data || error.message);
        }
      },
      async fetchClients() {
        try {
          const response = await apiClient.get("/clients/");
          this.clients = response.data;
        } catch (error) {
          console.error("Ошибка загрузки клиентов:", error.response?.data || error.message);
        }
      },
      navigateToCreate() {
        this.$router.push("/contracts/create");
      },
      navigateToEdit(contractId) {
        this.$router.push(`/contracts/${contractId}/edit`);
      },
      navigateToDetails(contractId) {
        this.$router.push(`/contracts/${contractId}`);
      },
    },
    async created() {
      await Promise.all([this.fetchContracts(), this.fetchClients()]);
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
  