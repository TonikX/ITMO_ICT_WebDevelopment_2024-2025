<script setup>
import axios from 'axios';
import {onMounted, ref} from "vue";

const groups = ref([])
const selectedClass = ref()
const isLoading = ref(false)
const isError = ref(false)
const report = ref()

async function fetchClasses() {
  const students = (await axios.get(`/school/students`)).data
  const groupsSets = new Set(students.map(student => `${student.group.group_grade}${student.group.group_name}`))
  groups.value = Array.from(groupsSets)
}

async function fetchReport() {
  if (!selectedClass.value) return
  isLoading.value = true
  return await axios.get('/school/report', {
    params: {
      group_name: selectedClass.value
    }
  }).then(response => {
    report.value = response.data
    isLoading.value = false
  }).catch(error => {
    isError.value = true
    console.log(error);
  })
}

onMounted(fetchClasses)
</script>


<template>
  <div class="report-selector">
    <h1>Отчет об успеваемости класса</h1>

    <label for="class-selector">Выберите класс:</label>
    <v-select
        v-model="selectedClass"
        id="class-selector"
        @update:modelValue="fetchReport"
        :items="groups"
    >
    </v-select>

    <div v-if="isLoading">Загрузка...</div>

    <div v-if="report">
      <h2>Отчет по классу {{ report.class_name }}</h2>
      <p>Классный руководитель: {{ report.class_teacher }}</p>
      <p>Общее количество учеников: {{ report.total_students }}</p>

      <h3>Предметы и средний балл</h3>
      <table>
        <thead>
        <tr>
          <th>Предмет</th>
          <th>Средний балл</th>
        </tr>
        </thead>
        <tbody>
        <tr v-for="subject in report.subjects" :key="subject.subject_name">
          <td>{{ subject.subject_name }}</td>
          <td>{{ subject.average_grade ? subject.average_grade.toFixed(2) : 'Нет данных' }}</td>
        </tr>
        </tbody>
      </table>
    </div>

    <div v-if="error" class="error">
      Ошибка: {{ error }}
    </div>
  </div>
</template>


<style setup>
.report-selector {
  max-width: 600px;
  margin: 0 auto;
  font-family: Arial, sans-serif;
}

label {
  display: block;
  margin-bottom: 0.5em;
}

select {
  width: 100%;
  padding: 0.5em;
  margin-bottom: 1em;
}

.error {
  color: red;
  font-weight: bold;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 1em;
}

table th, table td {
  border: 1px solid #ccc;
  padding: 0.5em;
  text-align: left;
}
</style>
