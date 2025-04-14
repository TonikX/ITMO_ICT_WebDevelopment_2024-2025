<template>
  <div class="container">
    <h1>Сотрудники</h1>

    <section>
      <h2>{{ editMode ? 'Редактировать сотрудника' : 'Добавить сотрудника' }}</h2>
      <form @submit.prevent="editMode ? updateEmployee() : addEmployee">
        <div>
          <label for="first_name">Имя:</label>
          <input v-model="newEmployee.first_name" id="first_name" type="text" required />
        </div>
        <div>
          <label for="last_name">Фамилия:</label>
          <input v-model="newEmployee.last_name" id="last_name" type="text" required />
        </div>
        <div>
          <label for="email">Email:</label>
          <input v-model="newEmployee.email" id="email" type="email" required />
        </div>
        <div>
          <label for="phone">Телефон:</label>
          <input v-model="newEmployee.phone" id="phone" type="tel" required />
        </div>

        <div>
          <label for="position">Должность:</label>
          <select v-model="newEmployee.position.id" id="position" required>
            <option v-for="position in positions" :key="position.id" :value="position.id">
              {{ position.position_title }}
            </option>
          </select>
        </div>

        <button type="submit">{{ editMode ? 'Обновить сотрудника' : 'Добавить сотрудника' }}</button>
      </form>
    </section>

    <section>
      <h2>Список сотрудников</h2>
      <table v-if="employees.length">
        <thead>
          <tr>
            <th>Фамилия</th>
            <th>Имя</th>
            <th>Должность</th>
            <th>Email</th>
            <th>Телефон</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="employee in employees" :key="employee.id">
            <td>{{ employee.last_name }}</td>
            <td>{{ employee.first_name }}</td>
            <td>{{ employee.position?.position_title || 'Не указано' }}</td>
            <td>{{ employee.email }}</td>
            <td>{{ employee.phone }}</td>
            <td>
              <button @click="editEmployee(employee)">Редактировать</button>
              <button @click="deleteEmployee(employee.id)">Удалить</button>
            </td>
          </tr>
        </tbody>
      </table>
      <p v-else>Нет данных</p>
    </section>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue';
import api from '@/api';

const employees = ref([]);
const positions = ref([]);
const newEmployee = ref({
  first_name: '',
  last_name: '',
  email: '',
  phone: '',
  position: { id: null }
});

const editMode = ref(false);
const editingEmployeeId = ref(null);

const loading = ref(false);

const fetchEmployees = async () => {
  loading.value = true;
  try {
    const { data } = await api.get('employees/');
    employees.value = data;
  } catch (error) {
    console.error("Ошибка загрузки списка сотрудников:", error);
  } finally {
    loading.value = false;
  }
};

const fetchPositions = async () => {
  try {
    const { data } = await api.get('positions/');
    positions.value = data;
  } catch (error) {
    console.error("Ошибка загрузки списка позиций:", error);
  }
};

const addEmployee = async () => {
  const newEmployeeData = {
    first_name: newEmployee.value.first_name,
    last_name: newEmployee.value.last_name,
    email: newEmployee.value.email,
    phone: newEmployee.value.phone,
    position_id: newEmployee.value.position.id
  };

  try {
    const response = await api.post('employees/', newEmployeeData);
    employees.value.push(response.data);
    resetForm();
  } catch (error) {
    console.error("Ошибка при добавлении сотрудника:", error);
  }
};

const editEmployee = (employee) => {
  editMode.value = true;
  editingEmployeeId.value = employee.id;

  newEmployee.value = {
    first_name: employee.first_name,
    last_name: employee.last_name,
    email: employee.email,
    phone: employee.phone,
    position: { id: employee.position.id }
  };
};

const updateEmployee = async () => {
  const updatedEmployeeData = {
    first_name: newEmployee.value.first_name,
    last_name: newEmployee.value.last_name,
    email: newEmployee.value.email,
    phone: newEmployee.value.phone,
    position_id: newEmployee.value.position.id
  };

  try {
    await api.put(`employees/${editingEmployeeId.value}/`, updatedEmployeeData);

    const employeeIndex = employees.value.findIndex(employee => employee.id === editingEmployeeId.value);
    employees.value[employeeIndex] = { ...employees.value[employeeIndex], ...updatedEmployeeData };

    resetForm();
  } catch (error) {
    console.error("Ошибка при обновлении сотрудника:", error);
  }
};

const deleteEmployee = async (employeeId) => {
  try {
    await api.delete(`employees/${employeeId}/`);
    employees.value = employees.value.filter(employee => employee.id !== employeeId);
  } catch (error) {
    console.error("Ошибка при удалении сотрудника:", error);
  }
};

const resetForm = () => {
  newEmployee.value = {
    first_name: '',
    last_name: '',
    email: '',
    phone: '',
    position: { id: null }
  };
  editMode.value = false;
  editingEmployeeId.value = null;
};

onMounted(() => {
  fetchEmployees();
  fetchPositions();
});
</script>

<style scoped>
.container {
  max-width: 900px;
  margin: auto;
  padding: 20px;
}

h1 {
  text-align: center;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 10px;
}

th, td {
  padding: 8px;
  border: 1px solid #ddd;
  text-align: left;
}

th {
  background: #f4f4f4;
}

form {
  display: flex;
  flex-direction: column;
  gap: 10px;
}

input, select {
  padding: 8px;
  border: 1px solid #ddd;
}

button {
  padding: 10px;
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
}

button:hover {
  background-color: #45a049;
}
</style>
