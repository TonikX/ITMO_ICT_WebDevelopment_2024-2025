<template>
  <v-container>
    <h1>Пустые вольеры</h1>
    <v-table>
      <thead>
        <tr>
          <th>Номер вольера</th>
          <th>Отдел</th>
          <th>Здание</th>
          <th>Вместимость</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="enc in enclosures" :key="enc.id">
          <td>{{ enc.number }}</td>
          <td>{{ enc.department_name }}</td>
          <td>{{ enc.building_name }}</td>
          <td>{{ enc.capacity }}</td>
        </tr>
      </tbody>
    </v-table>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { api } from '@/services/api'

const enclosures = ref([])

onMounted(async () => {
  const response = await api.get('enclosures/empty/')
  enclosures.value = response.data
})
</script>