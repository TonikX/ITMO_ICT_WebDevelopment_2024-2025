<template>
    <v-container>
      <v-row>
        <v-col cols="12">
          <h1 class="text-center">Добавить нового клиента</h1>
        </v-col>
      </v-row>
  
      <v-form ref="form">
        <v-text-field v-model="client.full_name" label="ФИО" required></v-text-field>
        <v-text-field v-model="client.phone" label="Телефон" required></v-text-field>
        <v-text-field v-model="client.email" label="Email" required></v-text-field>
        <v-select
          v-model="client.user_id"
          :items="users"
          label="Выберите пользователя"
          item-value="id"
          item-title="username"
          required
        ></v-select>
  
        <v-btn color="primary" @click="createClient">Создать</v-btn>
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
      async fetchUsers() {
        try {
          const response = await apiClient.get("/users/");
          this.users = response.data;
        } catch (error) {
          console.error("Ошибка загрузки пользователей:", error.response?.data || error.message);
        }
      },
  
      async createClient() {
        try {
          const response = await apiClient.post("/clients/", this.client);
          this.$router.push("/clients");
          console.log("Успешно добавлен клиент:", response.data);
        } catch (error) {
          console.error("Ошибка при добавлении клиента:", error.response?.data || error.message);
        }
      },
    },
    mounted() {
      this.fetchUsers();
    },
  };
  </script>
  
  <style scoped>
  .text-center {
    text-align: center;
  }
  </style>
  