<template>
    <v-dialog :model-value="dialog" @update:model-value="updateDialog" max-width="600px">
      <v-card>
        <v-card-title>Редактировать договор</v-card-title>
        <v-card-text>
          <v-form ref="form">
            <v-text-field
              v-model="contract.order_date"
              label="Дата заказа"
              type="date"
              required
            ></v-text-field>
            <v-select
              v-model="contract.client"
              :items="clients"
              label="Клиент"
              item-value="id"
              item-title="full_name"
              required
            ></v-select>
            <v-select
              v-model="contract.auto"
              :items="automobiles"
              label="Автомобиль"
              item-value="id"
              item-title="state_number"
              required
            ></v-select>
            <v-select
              v-model="contract.employee"
              :items="employees"
              label="Мастер"
              item-value="id"
              item-title="full_name"
              required
            ></v-select>
            <v-text-field
              v-model="contract.total_payment"
              label="Стоимость"
              type="number"
              required
            ></v-text-field>
            <v-select
              v-model="contract.order_status"
              :items="statuses"
              label="Статус"
              required
            ></v-select>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-btn text @click="closeDialog">Отмена</v-btn>
          <v-btn color="primary" @click="saveContract">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </template>
  
  <script>
  import apiClient from "@/services/api";
  
  export default {
    props: {
      dialog: {
        type: Boolean,
        required: true,
      },
      contractData: {
        type: Object,
        required: true,
      },
    },
    emits: ["update:dialog", "contract-updated"],
    data() {
      return {
        contract: {}, // Переменная для работы с данными договора
        clients: [],
        automobiles: [],
        employees: [],
        statuses: ["Pending", "In Progress", "Completed"],
      };
    },
    methods: {
      async fetchChoices() {
        try {
          const [clientsResponse, autosResponse, employeesResponse] = await Promise.all([
            apiClient.get("/clients/"),
            apiClient.get("/automobiles/"),
            apiClient.get("/employees/"),
          ]);
          this.clients = clientsResponse.data;
          this.automobiles = autosResponse.data;
          this.employees = employeesResponse.data;
        } catch (error) {
          console.error("Ошибка загрузки данных для выбора:", error.response?.data || error.message);
        }
      },
      updateDialog(value) {
        this.$emit("update:dialog", value);
      },
      closeDialog() {
        this.updateDialog(false);
      },
      async saveContract() {
        console.log("Сохраняем договор:", this.contract); // Отладка: выводим контракт в консоль
        if (!this.contract.id) {
          console.error("ID договора отсутствует.");
          return;
        }
        try {
          const response = await apiClient.put(`/contracts/${this.contract.id}/`, this.contract);
          console.log("Данные успешно сохранены:", response.data); // Отладка
          this.$emit("contract-updated", response.data);
          this.closeDialog();
        } catch (error) {
          console.error("Ошибка сохранения договора:", error.response?.data || error.message);
        }
      },
    },
    watch: {
      contractData: {
        handler(newValue) {
          this.contract = { ...newValue };
          console.log("Данные обновлены в watch:", this.contract); // Отладка
        },
        immediate: true,
      },
    },
    mounted() {
      this.fetchChoices();
    },
  };
  </script>
  
  <style scoped>
  </style>
  