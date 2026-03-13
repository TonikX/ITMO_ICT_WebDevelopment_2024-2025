<template>
  <v-container>
    <h1>Количество животных по отделам</h1>
    <v-table>
      <thead>
        <tr>
          <th>Отдел</th>
          <th>Количество животных</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in report" :key="item.id">
          <td>{{ item.name }}</td>
          <td>{{ item.animal_count }}</td>
        </tr>
      </tbody>
    </v-table>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '@/services/api'

const report = ref([])

onMounted(async () => {
  const response = await api.get('departments/animal-count/')
  report.value = response.data
})
</script>