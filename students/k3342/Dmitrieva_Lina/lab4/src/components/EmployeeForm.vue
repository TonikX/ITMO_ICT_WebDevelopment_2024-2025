<template>
  <div>
    <h2>{{ isEditMode ? "Редактировать сотрудника" : "Добавить сотрудника" }}</h2>
    <form @submit.prevent="submitForm">
      <label for="firstName">Имя:</label>
      <input v-model="employee.first_name" id="firstName" required />

      <label for="lastName">Фамилия:</label>
      <input v-model="employee.last_name" id="lastName" required />

      <label for="position">Должность:</label>
      <input v-model="employee.position" id="position" required />

      <label for="email">Email:</label>
      <input v-model="employee.email" id="email" type="email" required />

      <label for="phoneNumber">Телефон:</label>
      <input v-model="employee.phone_number" id="phoneNumber" />

      <label for="printshop">Типография:</label>
      <select v-model="employee.printshop" id="printshop" required>
        <option v-for="printshop in printshops" :value="printshop.id" :key="printshop.id">
          {{ printshop.name }}
        </option>
      </select>

      <button type="submit">{{ isEditMode ? "Сохранить" : "Добавить" }}</button>
    </form>
    <p v-if="errorMessage" class="error">{{ errorMessage }}</p>
  </div>
</template>

<script>
import { createEmployee, updateEmployee } from "../api/api";

export default {
  props: {
    isEditMode: { type: Boolean, default: false },
    initialData: { type: Object, default: () => ({}) },
    printshops: { type: Array, required: true },
  },
  data() {
    return {
      employee: { ...this.initialData },
      errorMessage: "",
    };
  },
  methods: {
    async submitForm() {
      try {
        if (this.isEditMode) {
          await updateEmployee(this.employee.id, this.employee);
        } else {
          await createEmployee(this.employee);
        }
        this.$emit("success");
      } catch (error) {
        this.errorMessage = error.response?.data?.error || "Ошибка сохранения";
      }
    },
  },
};
</script>
