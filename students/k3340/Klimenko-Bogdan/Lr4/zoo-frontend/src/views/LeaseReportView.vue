<template>
  <v-container>
    <h1>Отчет по аренде животных</h1>
    <v-table>
      <thead>
        <tr>
          <th>Зоопарк</th>
          <th>Количество животных</th>
          <th>Общая стоимость аренды</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="item in report" :key="item.id">
          <td>{{ item.name }}</td>
          <td>{{ item.animal_count }}</td>
          <td>{{ item.total_cost }}</td>
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
  const response = await api.get('zoos/lease-report/')
  report.value = response.data
})
</script>