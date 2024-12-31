<script setup>
import { ref, onMounted } from 'vue';
import axios from 'axios';

const studentId = ref(null);
const grades = ref([]);
const isLoading = ref(true);
const error = ref(null);

import { useRoute } from 'vue-router';
const route = useRoute();
studentId.value = route.params.id;

async function fetchGrades() {
  isLoading.value = true;
  await axios.get(`/school/students/${studentId.value}/grades`).then(response => {
    if (response.status === 200) {
      grades.value = response.data
    }
  }).catch(err => {
    error.value = "Ошибка загрузки данных"
    console.log(err);
  }).finally(isLoading.value = false);
}

async function saveGrade(grade) {
    await axios.put(`/school/grades/${grade.id}`, {grade: Number(grade.grade)}).then(response => {
      fetchGrades()
    }).then(err => {
      console.error('Ошибка сохранения:', err);
    });
}

onMounted(fetchGrades);
</script>

<template>
  <div>
    <h1>Оценки ученика</h1>
    <v-alert v-if="error" type="error">{{ error }}</v-alert>
    <v-progress-circular v-if="isLoading" indeterminate />

    <v-table v-if="grades.length">
      <thead>
      <tr>
        <th>Предмет</th>
        <th>Оценка</th>
        <th>Действия</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="grade in grades" :key="grade.id">
        <td>{{ grade.subject.subject_name }}</td>
        <td>
          <v-text-field
              v-model="grade.grade"
              type="number"
              min="1"
              max="5"
              label="Оценка"
          />
        </td>
        <td>
          <v-btn @click="saveGrade(grade)" color="primary">Сохранить</v-btn>
        </td>
      </tr>
      </tbody>
    </v-table>
  </div>
</template>

<style scoped>
</style>
