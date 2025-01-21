<template>
  <v-container class="contract-details" v-if="contract">
    <v-row>
      <v-col cols="12" class="text-center">
        <h1>Детали договора №{{ contract.id }}</h1>
      </v-col>
    </v-row>
    
    <v-row>
      <v-col cols="12" md="6">
        <v-card outlined class="mb-4">
          <v-card-title>Клиент</v-card-title>
          <v-card-text>
            <p><strong>Имя:</strong> {{ contract.client.full_name }}</p>
            <p><strong>Email:</strong> {{ contract.client.email || "Нет информации" }}</p>
            <p><strong>Телефон:</strong> {{ contract.client.phone }}</p>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <v-card outlined class="mb-4">
          <v-card-title>Автомобиль</v-card-title>
          <v-card-text>
            <p><strong>Марка:</strong> {{ contract.auto.auto_model.car_brand }}</p>
            <p><strong>Модель:</strong> {{ contract.auto.auto_model.model }}</p>
            <p><strong>Цвет:</strong> {{ contract.auto.colour }}</p>
            <p><strong>Номер:</strong> {{ contract.auto.state_number }}</p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" md="6">
        <v-card outlined class="mb-4">
          <v-card-title>Мастер</v-card-title>
          <v-card-text>
            <p><strong>Имя:</strong> {{ contract.employee?.full_name || "Не назначен" }}</p>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <v-card outlined class="mb-4">
          <v-card-title>Детали заказа</v-card-title>
          <v-card-text>
            <p><strong>Стоимость:</strong> {{ contract.total_payment }} руб.</p>
            <p><strong>Статус:</strong> {{ contract.order_status }}</p>
            <p><strong>Дата заказа:</strong> {{ contract.order_date }}</p>
            <p><strong>Дата принятия на ремонт:</strong> {{ contract.date_of_acceptance_for_repair }}</p>
            <p><strong>Запланированная дата окончания ремонта:</strong> {{ contract.scheduled_date_end_of_repair || "Не указана" }}</p>
            <p><strong>Фактическая дата окончания ремонта:</strong> {{ contract.actual_date_end_of_repair || "Не указана" }}</p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" class="d-flex justify-center">
        <v-btn color="primary" @click="navigateToEdit">Редактировать</v-btn>
        <v-btn color="secondary" @click="navigateBack">Назад</v-btn>
        <v-btn color="red" @click="deleteContract">Удалить</v-btn>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import apiClient from "@/services/api";

export default {
  name: "ContractDetails",
  data() {
    return {
      contract: null,
    };
  },
  methods: {
    async fetchContractDetails() {
      const contractId = this.$route.params.id;
      try {
        const response = await apiClient.get(`/contracts/${contractId}/`);
        this.contract = response.data;
      } catch (error) {
        console.error("Ошибка загрузки деталей договора:", error.response?.data || error.message);
      }
    },
    navigateToEdit() {
      this.$router.push(`/contracts/${this.contract.id}/edit`);
    },
    navigateBack() {
      this.$router.push("/contracts");
    },
    async deleteContract() {
      const confirmDelete = confirm("Вы уверены, что хотите удалить этот договор?");
      if (confirmDelete) {
        try {
          await apiClient.delete(`/contracts/${this.contract.id}/`);
          this.$router.push("/contracts");
        } catch (error) {
          console.error("Ошибка удаления договора:", error.response?.data || error.message);
        }
      }
    }
  },
  mounted() {
    this.fetchContractDetails();
  },
};
</script>

<style scoped>
.contract-details {
  margin-top: 50px;
}
.mb-4 {
  margin-bottom: 20px;
}
.text-center {
  text-align: center;
}
</style>
