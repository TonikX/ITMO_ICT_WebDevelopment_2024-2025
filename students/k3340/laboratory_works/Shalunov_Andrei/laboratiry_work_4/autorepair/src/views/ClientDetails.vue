<template>
  <v-container class="client-details" v-if="client">
    <v-row>
      <v-col cols="12" class="text-center">
        <h1>Детали клиента {{ client.full_name }}</h1>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" md="6">
        <v-card outlined class="mb-4">
          <v-card-title>Клиент</v-card-title>
          <v-card-text>
            <p><strong>Имя:</strong> {{ client.full_name }}</p>
            <p><strong>Email:</strong> {{ client.email || "Нет информации" }}</p>
            <p><strong>Телефон:</strong> {{ client.phone }}</p>
            <p><strong>Пользователь:</strong> {{ client.user.username }}</p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="12" class="d-flex justify-center">
        <v-btn color="primary" @click="navigateToEdit">Редактировать</v-btn>
        <v-btn color="secondary" @click="navigateBack">Назад</v-btn>
        <v-btn color="red" @click="deleteClient">Удалить</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import apiClient from "@/services/api";

export default {
  data() {
    return {
      client: {},
    };
  },
  methods: {
    async fetchClientDetails() {
      try {
        const response = await apiClient.get(`/clients/${this.$route.params.id}`);
        this.client = response.data;
      } catch (error) {
        console.error("Ошибка загрузки деталей клиента:", error.response?.data || error.message);
      }
    },
    navigateToEdit() {
      this.$router.push(`/clients/edit/${this.$route.params.id}`);
    },
    navigateBack() {
      this.$router.push("/clients");
    },
    async deleteClient() {
      const confirmDelete = confirm("Вы уверены, что хотите удалить этого клиента?");
      if (confirmDelete) {
        try {
          await apiClient.delete(`/clients/${this.client.id}/`);
          this.$router.push("/clients");
        } catch (error) {
          console.error("Ошибка удаления клиента:", error.response?.data || error.message);
        }
      }
    }
  },
  async created() {
    await this.fetchClientDetails();
  },
};
</script>

<style scoped>
.client-details {
  margin-top: 50px;
}
.mb-4 {
  margin-bottom: 20px;
}
.text-center {
  text-align: center;
}
</style>
