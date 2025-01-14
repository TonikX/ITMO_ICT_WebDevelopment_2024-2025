<template>
  <div class="employee-list-container">
    <HeaderComponent />
    <h1 class="title">Список сотрудников</h1>
    <v-btn color="primary" class="add-employee-btn" @click="openCreateModal">Добавить сотрудника</v-btn>
    <v-text-field
      v-model="searchQuery"
      label="Поиск сотрудника по имени или фамилии"
      append-icon="mdi-magnify"
      @input="filterEmployees"
      class="search-field"
    />


    <div v-if="filteredEmployees.length" class="employee-cards">
      <div v-for="employee in filteredEmployees" :key="employee.id" class="employee-card">
        <h2>{{ employee.first_name }} {{ employee.last_name }}</h2>
        <p>Специальность: {{ employee.specialization }}</p>
        <p>Дата рождения: {{ employee.birth_date || 'Не указано' }}</p>

        <div class="action-buttons">
          <v-btn color="yellow" @click="openEditModal(employee)" class="action-btn">Ред.</v-btn>
          <v-btn color="red" @click="deleteEmployee(employee.id)" class="action-btn">Удалить</v-btn>
        </div>
      </div>
    </div>

    <p v-else class="no-data">Нет данных о сотрудниках</p>

    <v-dialog v-model="dialog" max-width="500">
      <v-card>
        <v-card-title>
          <span class="headline">{{ isEditing ? 'Редактировать' : 'Добавить' }} сотрудника</span>
        </v-card-title>
        <v-card-text>
          <v-form ref="form">
            <v-text-field
              v-model="formData.first_name"
              label="Имя"
              required
            ></v-text-field>
            <v-text-field
              v-model="formData.last_name"
              label="Фамилия"
              required
            ></v-text-field>
            <v-text-field
              v-model="formData.specialization"
              label="Специальность"
              required
            ></v-text-field>
            <v-text-field
              v-model="formData.birth_date"
              label="Дата рождения"
              type="date"
            ></v-text-field>
            <v-select
              v-model="formData.gender"
              :items="['Male', 'Female']"
              label="Пол"
              required
            ></v-select>
            <v-textarea
              v-model="formData.education"
              label="Образование"
              required
            ></v-textarea>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-btn color="blue darken-1" text @click="saveEmployee">Сохранить</v-btn>
          <v-btn color="blue darken-1" text @click="closeDialog">Отмена</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
</template>

<script>
import HeaderComponent from "@/components/Visual/Header.vue";
import axios from 'axios';

export default {
  components: {
    HeaderComponent,
  },
  data() {
    return {
      employees: [],
      dialog: false,
      isEditing: false,
      formData: {
        id: null,
        first_name: "",
        last_name: "",
        specialization: "",
        education: "",
        birth_date: "",
        gender: ""
      },
      searchQuery: "",
      filteredEmployees: []
    };
  },
  async created() {
    await this.fetchEmployees();
  },
  methods: {
    async fetchEmployees() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/clinic/employees/");
        this.employees = response.data;
        this.filteredEmployees = this.employees;
      } catch (error) {
        console.error("Ошибка при получении данных сотрудников:", error);
      }
    },
    filterEmployees() {
      const query = this.searchQuery.toLowerCase();
      this.filteredEmployees = this.employees.filter(employee => {
        const fullName = `${employee.first_name} ${employee.last_name}`.toLowerCase();
        return fullName.includes(query);
      });
    },
    openCreateModal() {
      this.isEditing = false;
      this.formData = {
        id: null,
        first_name: "",
        last_name: "",
        specialization: "",
        education: "",
        birth_date: "",
        gender: ""
      };
      this.dialog = true;
    },
    openEditModal(employee) {
      this.isEditing = true;
      this.formData = { ...employee };
      this.dialog = true;
    },
    async saveEmployee() {
      try {
        if (this.isEditing) {
          await axios.put(
            `http://127.0.0.1:8000/clinic/employees/${this.formData.id}/`,
            this.formData
          );
        } else {
          await axios.post("http://127.0.0.1:8000/clinic/employees/", this.formData);
        }
        this.dialog = false;
        await this.fetchEmployees();
      } catch (error) {
        console.error("Ошибка при сохранении данных сотрудника:", error);
      }
    },
    async deleteEmployee(employeeId) {
      try {
        await axios.delete(`http://127.0.0.1:8000/clinic/employees/${employeeId}/`);
        await this.fetchEmployees();
      } catch (error) {
        console.error("Ошибка при удалении сотрудника:", error);
      }
    },
    closeDialog() {
      this.dialog = false;
    }
  }
};
</script>

<style scoped>
.employee-list-container {
  padding: 20px;
  text-align: center;
}

.title {
  text-align: center;
}

.add-employee-btn {
  margin-bottom: 20px;
  margin-left: auto;
  margin-right: auto;
  display: block;
}

.search-field {
  width: 100%;
  max-width: 500px;
  margin-left: auto;
  margin-right: auto;
  display: block;
}

.employee-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 30px;
  justify-items: center;
}

.employee-card {
  border: 1px solid #ccc;
  padding: 30px;
  width: 300px;
  box-sizing: border-box;
  text-align: left;
}

.action-buttons {
  display: flex;
  justify-content: space-between;
}

.action-btn {
  width: 90px;
  margin-top: 10px;
  font-size: 12px;
}

.no-data {
  text-align: center;
  font-size: 18px;
}

v-btn {
  margin-top: 10px;
}
</style>

