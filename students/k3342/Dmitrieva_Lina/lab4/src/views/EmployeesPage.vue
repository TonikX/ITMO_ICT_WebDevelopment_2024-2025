<template>
  <div>
    <h1>Сотрудники типографий</h1>
    <EmployeeForm
      v-if="showForm"
      :is-edit-mode="editMode"
      :initial-data="currentEmployee"
      :printshops="printshops"
      @success="fetchEmployees"
    />
    <button v-if="!showForm" @click="addEmployee">Добавить сотрудника</button>
    <EmployeeTable
      :employees="employees"
      @edit="editEmployee"
      @delete="deleteEmployee"
    />
  </div>
</template>

<script>
import { getEmployees, deleteEmployee } from "../api/api";
import EmployeeForm from "../components/EmployeeForm.vue";
import EmployeeTable from "../components/EmployeeTable.vue";
import Header from "@/components/Header.vue";

export default {
  components: { EmployeeForm, EmployeeTable, Header },
  data() {
    return {
      employees: [],
      printshops: [],
      showForm: false,
      editMode: false,
      currentEmployee: {},
    };
  },
  methods: {
    async fetchEmployees() {
      this.showForm = false;
      const response = await getEmployees();
      this.employees = response.data;
    },
    addEmployee() {
      this.editMode = false;
      this.currentEmployee = {};
      this.showForm = true;
    },
    editEmployee(employee) {
      this.editMode = true;
      this.currentEmployee = employee;
      this.showForm = true;
    },
    async deleteEmployee(id) {
      await deleteEmployee(id);
      this.fetchEmployees();
    },
  },
  mounted() {
    this.fetchEmployees();
  },
};
</script>
