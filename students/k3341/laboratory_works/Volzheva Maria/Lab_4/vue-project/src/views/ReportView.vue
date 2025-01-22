<template>
  <div class="report-view">
    <h2>Отчет</h2>
    <v-skeleton-loader v-if="isLoading" type="card" class="mt-4" max-width="500"></v-skeleton-loader>

    <div v-else>
      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Имя</th>
            <th>Фамилия</th>
            <th>Активные индивидуальные контракты</th>
            <th>Активные коллективные контракты</th>
            <th>Общая сумма индивидуальных контрактов</th>
            <th>Общая сумма коллективных контрактов</th>
            <th>Общая сумма компании</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="client in clients" :key="client.id">
            <td>{{ client.id }}</td>
            <td>{{ client.first_name }}</td>
            <td>{{ client.second_name }}</td>
            <td>{{ client.active_individual_contracts }}</td>
            <td>{{ client.active_collective_contracts }}</td>
            <td>{{ client.total_individual_sum }}</td>
            <td>{{ client.total_collective_sum }}</td>
            <td>{{ client.company_total_sum }}</td>
          </tr>
        </tbody>
      </table>

      <div v-if="isError" class="error-message">
        Произошла ошибка при загрузке данных. Пожалуйста, попробуйте позже.
      </div>
    </div>
  </div>
</template>

<script setup>
import { onMounted, ref } from "vue";
import axios from "axios";

const clients = ref([]);
const isLoading = ref(false);
const isError = ref(false);

async function fetchReport() {
  isLoading.value = true;
  try {
    const response = await axios.get('http://localhost:8000/insurance/report/');
    clients.value = response.data;
  } catch (error) {
    console.error("Ошибка загрузки отчета", error);
    isError.value = true;
  } finally {
    isLoading.value = false;
  }
}

onMounted(fetchReport);
</script>

<style scoped>
.report-view {
  padding: 20px;
  background-color: #f9f9f9;
  border-radius: 8px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
}

h2 {
  color: #333;
  margin-bottom: 20px;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

th, td {
  border: 1px solid #ccc;
  padding: 12px;
  text-align: left;
}

th {
  background-color: #4CAF50;
  color: white;
}

tbody tr:nth-child(even) {
  background-color: #f2f2f2;
}

tbody tr:hover {
  background-color: #e0e0e0;
}

.error-message {
  color: red;
  margin-top: 20px;
}

@media (max-width: 600px) {
  table {
    font-size: 14px;
  }
}
</style>
