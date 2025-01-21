<template>
    <v-container>
      <v-row>
        <v-col cols="12">
          <h1 class="text-center">Добавить новый договор</h1>
        </v-col>
      </v-row>
  
      <v-form ref="form">
        <v-text-field
          v-model="contract.order_date"
          label="Дата заказа"
          type="date"
          required
        ></v-text-field>
  
        <v-select
          v-model="contract.client_id"
          :items="clients"
          label="Клиент"
          item-value="id"
          item-title="full_name"
          required
        ></v-select>
  
        <v-select
          v-model="contract.auto_id"
          :items="automobiles"
          label="Автомобиль"
          item-value="id"
          item-title="state_number"
          required
        ></v-select>
  
        <v-select
          v-model="contract.employee_id"
          :items="employees"
          label="Мастер"
          item-value="id"
          item-title="full_name"
          required
        ></v-select>
  
        <v-text-field
          v-model="contract.date_of_acceptance_for_repair"
          label="Дата принятия на ремонт"
          type="date"
          required
        ></v-text-field>
  
        <v-text-field
          v-model="contract.scheduled_date_end_of_repair"
          label="Запланированная дата окончания ремонта"
          type="date"
          required
        ></v-text-field>
  
        <v-text-field
          v-model="contract.actual_date_end_of_repair"
          label="Фактическая дата окончания ремонта"
          type="date"
        ></v-text-field>
  
        <v-text-field
          v-model.number="contract.total_payment"
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
  
        <v-select
          v-model="contract.payment_status"
          :items="['Paid', 'Unpaid']"
          label="Статус оплаты"
          required
        ></v-select>
  
        <v-btn color="primary" @click="createContract">Создать</v-btn>
      </v-form>
    </v-container>
  </template>
  
  <script>
  import apiClient from "@/services/api";
  
  export default {
    data() {
      return {
        contract: {
          order_date: "",
          order_status: "Pending",
          payment_status: "Unpaid",
          date_of_acceptance_for_repair: "",
          scheduled_date_end_of_repair: "",
          actual_date_end_of_repair: null,
          total_payment: null,
          client_id: null,
          auto_id: null,
          employee_id: null,
        },
        clients: [],
        automobiles: [],
        employees: [],
        statuses: ["Pending", "Closed", "In Progress"],
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
      async createContract() {
        try {
          const response = await apiClient.post("/contracts/", this.contract);
          console.log("Успешно создан договор:", response.data);
          this.$router.push("/contracts");
        } catch (error) {
          console.error("Ошибка создания договора:", error.response?.data || error.message);
        }
      },
    },
    mounted() {
      this.fetchChoices();
    },
  };
  </script>
  