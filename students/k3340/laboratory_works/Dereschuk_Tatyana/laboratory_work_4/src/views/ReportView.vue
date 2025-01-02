<script setup>
import axios from 'axios';
import {ref} from 'vue';

const startDate = ref(null);
const endDate = ref(null);
const isLoading = ref(false);
const isError = ref(false);
const reportData = ref([]);

async function fetchReport() {
  if (!startDate.value || !endDate.value) {
    alert('Пожалуйста, укажите начало и конец периода');
    return;
  }

  isLoading.value = true;
  isError.value = false;

  await axios.get('club/report', {
    params: {
      start_date: startDate.value,
      end_date: endDate.value,
    },
  }).then(response => {
    reportData.value = response.data;
  }).catch(error => {
    console.error('Error fetching report:', error);
    isError.value = true;
  }).finally(isLoading.value = false);

}
</script>

<template>
  <div class="date-range-report">
    <h1>Отчёт за период</h1>

    <div class="date-selectors">
      <v-text-field
          v-model="startDate"
          label="Начало периода"
          type="date"
          required
      ></v-text-field>
      <v-text-field
          v-model="endDate"
          label="Конец периода"
          type="date"
          required
      ></v-text-field>

      <v-btn @click="fetchReport">Сгенерировать отчёт</v-btn>
    </div>

    <div v-if="isLoading">Загрузка...</div>

    <div v-if="isError" class="error">Возникла ошибка при загрузке отчёта</div>

    <div v-if="reportData.length > 0">
      <h2>Отчёт</h2>
      <div v-for="mountain in reportData" :key="mountain.mountain.id" class="report-item">
        <v-card class="mt-3">
          <v-card-title>{{ mountain.mountain.name }}</v-card-title>
          <v-divider></v-divider>
          <v-card-text>
            <p><strong>Группы:</strong></p>
            <ul>
              <li v-for="group in mountain.groups" :key="group.group.id">
                Группа: {{ group.group.name }} - Участники: {{ group.member_count }}
                <ul>
                  <li>Успехов: {{ group.success_count }}</li>
                  <li>Неудач: {{ group.failure_count }}</li>
                  <li>ЧС: {{ group.emergency_count }}</li>
                </ul>
              </li>
            </ul>
          </v-card-text>
        </v-card>
      </div>
    </div>
  </div>
</template>

<style scoped>
.date-range-report {
  max-width: 600px;
  margin: 0 auto;
  font-family: Arial, sans-serif;
}

.date-selectors {
  margin-bottom: 20px;
}

.date-selectors label {
  display: block;
  margin-bottom: 5px;
}

.date-selectors input {
  margin-bottom: 10px;
  width: 100%;
  padding: 5px;
}

button {
  padding: 10px 20px;
  background-color: #007BFF;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

button:hover {
  background-color: #0056b3;
}

.error {
  color: red;
  font-weight: bold;
}

.report-item {
  border: 1px solid #ccc;
  padding: 10px;
  margin-bottom: 10px;
  border-radius: 5px;
}

.report-item h3 {
  margin-top: 0;
}
</style>
