<template>
    <v-container>
      <v-row>
        <v-col cols="12">
          <h1 class="text-center">Редактировать клиента</h1>
        </v-col>
      </v-row>
  
      <v-form ref="form">
        <v-row>
          <v-col cols="12" md="6">
            <v-text-field v-model="client.full_name" label="ФИО" required></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field v-model="client.phone" label="Телефон" required></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <v-text-field v-model="client.email" label="Email" required></v-text-field>
          </v-col>
          <v-col cols="12" md="6">
            <v-select
              v-model="client.user_id"
              :items="users"
              label="Пользователь"
              item-value="id"
              item-title="username"
              required
            ></v-select>
          </v-col>
        </v-row>
  
        <v-btn color="primary" @click="updateClient">Сохранить изменения</v-btn>
        <v-btn color="secondary" @click="navigateBack">Назад</v-btn>
      </v-form>
    </v-container>
  </template>
  
  <script>
  import apiClient from "@/services/api";
  
  export default {
    data() {
      return {
        client: {
          full_name: "",
          phone: "",
          email: "",
          user_id: null,
        },
        users: [],
      };
    },
    methods: {
      async fetchClientDetails() {
        try {
          const response = await apiClient.get(`/clients/${this.$route.params.id}`);
          this.client = response.data;
        } catch (error) {
          console.error("Ошибка загрузки клиента:", error.response?.data || error.message);
        }
      },
      async fetchUsers() {
        try {
          const response = await apiClient.get("/users/");
          this.users = response.data;
        } catch (error) {
          console.error("Ошибка загрузки пользователей:", error.response?.data || error.message);
        }
      },
      async updateClient() {
        try {
          const response = await apiClient.put(`/clients/${this.$route.params.id}/`, this.client);
          this.$router.push(`/clients/${this.$route.params.id}`);
          console.log("Успешно обновлен клиент:", response.data);
        } catch (error) {
          console.error("Ошибка при обновлении клиента:", error.response?.data || error.message);
        }
      },
      navigateBack() {
        this.$router.push("/clients");
      },
    },
    async created() {
      await Promise.all([this.fetchClientDetails(), this.fetchUsers()]);
    },
  };
  </script>
  
  <style scoped>
  .text-center {
    text-align: center;
  }
  </style>
  