<template>
    <v-dialog
      :model-value="dialog"
      @update:model-value="emitDialogUpdate"
      max-width="600px"
    >
      <v-card>
        <v-card-title>Добавить новый договор</v-card-title>
        <v-card-text>
          <v-form ref="form">
            <!-- Поля для ввода данных -->
            <v-text-field
              v-model="newContract.order_date"
              label="Дата заказа"
              type="date"
              :error-messages="errors.order_date || []"
              @input="clearFieldError('order_date')"
              required
            ></v-text-field>
            <v-select
              v-model="newContract.client"
              :items="choices.clients"
              label="Клиент"
              item-value="id"
              item-title="full_name"
              :error-messages="errors.client || []"
              @update:model-value="clearFieldError('client')"
              required
            ></v-select>
            <v-select
              v-model="newContract.auto"
              :items="choices.automobiles"
              label="Автомобиль"
              item-value="id"
              item-title="state_number"
              :error-messages="errors.auto || []"
              @update:model-value="clearFieldError('auto')"
              required
            ></v-select>
            <v-select
              v-model="newContract.employee"
              :items="choices.employees"
              label="Мастер"
              item-value="id"
              item-title="full_name"
              :error-messages="errors.employee || []"
              @update:model-value="clearFieldError('employee')"
              required
            ></v-select>
            <v-text-field
              v-model="newContract.total_payment"
              label="Стоимость"
              type="number"
              :error-messages="errors.total_payment || []"
              @input="clearFieldError('total_payment')"
              required
            ></v-text-field>
            <v-select
              v-model="newContract.order_status"
              :items="statuses"
              label="Статус"
              :error-messages="errors.order_status || []"
              @update:model-value="clearFieldError('order_status')"
              required
            ></v-select>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn text @click="closeDialog">Отмена</v-btn>
          <v-btn color="primary" @click="createContract">Создать</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </template>
  
  <script>
  export default {
    props: {
      dialog: { type: Boolean, required: true },
    },
    emits: ["update:dialog", "contract-created"],
    data() {
      return {
        newContract: {
          order_date: "",
          client: null,
          auto: null,
          employee: null,
          total_payment: "",
          order_status: "Pending",
        },
        choices: {
          clients: [],
          automobiles: [],
          employees: [],
        },
        statuses: ["Pending", "In Progress", "Completed"],
        errors: {},
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
          this.choices.clients = clientsResponse.data;
          this.choices.automobiles = autosResponse.data;
          this.choices.employees = employeesResponse.data;
        } catch (error) {
          console.error("Ошибка загрузки данных для выбора:", error.response?.data || error.message);
        }
      },
      emitDialogUpdate(value) {
        this.$emit("update:dialog", value);
      },
      closeDialog() {
        this.emitDialogUpdate(false);
        this.resetForm();
      },
      resetForm() {
        this.newContract = {
          order_date: "",
          client: null,
          auto: null,
          employee: null,
          total_payment: "",
          order_status: "Pending",
        };
        this.errors = {};
      },
      clearFieldError(fieldName) {
        if (this.errors[fieldName]) {
          delete this.errors[fieldName];
        }
      },
      async createContract() {
        try {
          const response = await apiClient.post("/contracts/", this.newContract);
          console.log("Договор создан:", response.data); // Отладка
          this.$emit("contract-created", response.data);
          this.closeDialog();
        } catch (error) {
          if (error.response?.status === 400) {
            this.errors = error.response.data;
            console.error("Ошибка создания договора:", error.response.data);
          } else {
            console.error("Ошибка создания договора:", error.message);
          }
        }
      },
    },
    mounted() {
      this.fetchChoices();
    },
  };
  </script>
  
  <style scoped>
  </style>
  