<template>
  <v-container>
   <v-row class="align-center mb-4">
      <v-col cols="12" md="6">
        <h1>Сотрудники авиалинии</h1>
      </v-col>
      <v-col cols="12" md="3" class="text-md-right">
        <span>Всего сотрудников: {{ totalEmployees }}</span>
      </v-col>
      <v-col cols="12" md="3" class="text-md-right">
        <v-btn color="primary" @click="openAddEmployeeDialog">Добавить сотрудника</v-btn>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" md="4">
        <v-select
          v-model="filters.role"
          :items="roles"
          label="Фильтр по должности"
          item-value="value"
          item-title="label"
          clearable
        ></v-select>
      </v-col>
      <v-col cols="12" md="4">
        <v-text-field
          v-model="filters.experience"
          label="Фильтр по опыту работы (лет)"
          type="number"
          clearable
        ></v-text-field>
      </v-col>
      <v-col cols="12" md="4">
        <v-text-field
          v-model="filters.search"
          label="Поиск по ФИО"
          clearable
        ></v-text-field>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" md="6" v-for="employee in filteredAndPaginatedEmployees" :key="employee.id">
        <v-card class="mb-6" elevation="2">
          <v-card-title>
            {{ employee.first_name }} {{ employee.last_name }}
          </v-card-title>
          <v-card-subtitle>
            Возраст: {{ employee.age }}
          </v-card-subtitle>
          <v-card-text>
            <p><strong>Образование:</strong> {{ employee.education }}</p>
            <v-divider class="my-2"></v-divider>
            <p><strong>Опыт работы:</strong> {{ employee.work_experience_years }} лет</p>
            <v-divider class="my-2"></v-divider>
            <p><strong>Паспортные данные:</strong> {{ employee.passport_data }}</p>
            <v-divider class="my-2"></v-divider>
            <p v-if="employee.roles.length > 0"><strong>Роли:</strong> {{ employee.roles.join(', ') }}</p>
            <p v-else><strong>Роли:</strong> Нет ролей</p>
          </v-card-text>

          <v-card-actions class="justify-center">
            <v-btn color="primary" @click="openAddRoleDialog(employee)">Добавить роль</v-btn>
            <v-btn color="warning" @click="openEditEmployeeDialog(employee)">Редактировать</v-btn>
            <v-btn color="error" @click="openDeleteDialog(employee)">Уволить</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="12" class="d-flex justify-center">
        <v-pagination v-model="currentPage" :length="totalPages" :total-visible="5"></v-pagination>
      </v-col>
    </v-row>

    <AddEmployeeDialog
      :dialog="addDialog"
      @update:dialog="addDialog = $event"
      @employee-added="addEmployee"
    />

    <EditEmployeeDialog
      ref="editEmployeeDialog"
      :dialog="editEmployeeDialog"
      :employee="currentEmployee"
      @update:dialog="editEmployeeDialog = $event"
      @employee-updated="updateEmployee"
    />

     <DeleteEmployeeDialog
      :dialog="deleteDialog"
      :employee="currentEmployee"
      @update:dialog="deleteDialog = $event"
      @employee-deleted="deleteEmployee"
    />

    <AddRoleDialog
      ref="addRoleDialog"
      :dialog="addRoleDialog"
      :employee-id="currentEmployee?.id"
      :available-roles="roles"
      :existing-roles="currentEmployee?.roles || []"
      @update:dialog="addRoleDialog = $event"
      @role-added="addRoleToEmployee"
    />
  </v-container>
</template>

<script>
import apiClient from "@/services/api";
import AddEmployeeDialog from "@/components/employees/AddEmployeeDialog.vue";
import AddRoleDialog from "@/components/employees/AddRoleDialog.vue";
import EditEmployeeDialog from "@/components/employees/EditEmployeeDialog.vue";
import DeleteEmployeeDialog from "@/components/employees/DeleteEmployeeDialog.vue";

export default {
  components: {DeleteEmployeeDialog, EditEmployeeDialog, AddRoleDialog, AddEmployeeDialog },
  data() {
    return {
      employees: [],
      roles: [],
      filters: {
        role: null,
        experience: null,
        search: "",
      },
      currentPage: 1,
      itemsPerPage: 6,
      addDialog: false,
      currentEmployee: null,
      addRoleDialog: false,
      editEmployeeDialog: false,
      deleteDialog: false,
    };
  },
  computed: {
    filteredEmployees() {
      let filtered = this.employees;

      if (this.filters.role) {
        filtered = filtered.filter(employee =>
          employee.roles.includes(this.filters.role)
        );
      }
      if (this.filters.experience) {
        filtered = filtered.filter(
          employee => employee.work_experience_years >= this.filters.experience
        );
      }
      if (this.filters.search) {
        const search = this.filters.search.toLowerCase();
        filtered = filtered.filter(
          employee =>
            `${employee.first_name} ${employee.last_name}`.toLowerCase().includes(search)
        );
      }

      return filtered;
    },
    filteredAndPaginatedEmployees() {
      const start = (this.currentPage - 1) * this.itemsPerPage;
      const end = start + this.itemsPerPage;
      return this.filteredEmployees.slice(start, end);
    },
    totalEmployees() {
      return this.filteredEmployees.length;
    },
    totalPages() {
      return Math.ceil(this.filteredEmployees.length / this.itemsPerPage);
    },
  },
  methods: {
    async fetchEmployees() {
      try {
        const response = await apiClient.get("/employees/");
        this.employees = await Promise.all(
          response.data.map(async employee => {
            const rolesResponse = await apiClient.get(
              `/employees/${employee.id}/crew-members/`
            );
            return {
              ...employee,
              roles: rolesResponse.data.map(role => role.role),
            };
          })
        );
      } catch (error) {
        console.error("Ошибка загрузки сотрудников:", error.response?.data || error.message);
      }
    },
    async fetchRoles() {
      try {
        const response = await apiClient.get("/crew-members/roles/");
        this.roles = response.data;
      } catch (error) {
        console.error("Ошибка загрузки ролей:", error.response?.data || error.message);
      }
    },
    openAddEmployeeDialog() {
      this.addDialog = true;
    },
    openEditEmployeeDialog(employee) {
      this.currentEmployee = { ...employee };
      this.editEmployeeDialog = true;
    },
    openDeleteDialog(employee) {
      this.currentEmployee = employee;
      this.deleteDialog = true;
    },
    openAddRoleDialog(employee) {
      this.currentEmployee = employee;
      this.addRoleDialog = true;
    },
    async updateEmployee(updatedEmployee) {
      try {
        await apiClient.put(`/employees/${updatedEmployee.id}/`, updatedEmployee);
        await this.fetchEmployees();
        this.editEmployeeDialog = false;
      } catch (error) {
        console.error("Ошибка обновления сотрудника:", error.response?.data || error.message);
        alert("Ошибка обновления сотрудника.");
      }
    },
    async deleteEmployee(employeeId) {
      try {
        await apiClient.delete(`/employees/${employeeId}/`);
        await this.fetchEmployees();
      } catch (error) {
        console.error("Ошибка увольнения сотрудника:", error.response?.data || error.message);
      }
    },
    async addRoleToEmployee(roleData) {
      try {
        await apiClient.post("/crew-members/", roleData);
        await this.fetchEmployees();
      } catch (error) {
        console.error("Ошибка добавления роли:", error.response?.data || error.message);
        alert("Ошибка добавления роли.");
      }
    },

    async addEmployee(employeeData) {
      try {
        await apiClient.post('/employees/', employeeData);
        await this.fetchEmployees();
      } catch (error) {
        console.error('Ошибка добавления сотрудника:', error.response?.data || error.message);
        alert('Ошибка добавления сотрудника');
      }
    },
  },
  async created() {
    await Promise.all([this.fetchEmployees(), this.fetchRoles()]);
  },
};
</script>

<style>
.mb-4 .v-col {
  margin-bottom: 10px;
}

.roles-list {
  padding-left: 0px;
  list-style-position: inside;
  margin: 0;
}

.roles-list li {
  margin-bottom: 4px;
}
</style>
