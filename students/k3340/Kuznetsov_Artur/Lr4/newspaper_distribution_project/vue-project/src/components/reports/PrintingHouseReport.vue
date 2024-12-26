<script setup>
import {ref} from 'vue'
import axiosClient from '@/services/axiosClient'

const formData = ref({printing_house_id: null})
const report = ref(null)

async function fetchReport() {
  try {
    const response = await axiosClient.post('/reports/printinghouses/', formData.value)
    report.value = response.data
  } catch (error) {
    console.error('Ошибка загрузки отчёта:', error)
  }
}
</script>

<template>
  <v-card>
    <v-card-title>Отчёт по типографии</v-card-title>
    <v-card-text>
      <v-form @submit.prevent="fetchReport">
        <v-text-field v-model="formData.printing_house_id" label="ID типографии" type="number" required/>
        <v-btn color="primary" type="submit">Получить</v-btn>
      </v-form>
      <div v-if="report">
        <p><strong>Типография:</strong> {{ report.printing_house.name }}</p>
        <p><strong>Адрес:</strong> {{ report.printing_house.address }}</p>
        <p><strong>Общее количество газет:</strong> {{ report.total_newspapers }}</p>
        <p><strong>Газеты и тиражи:</strong></p>
        <ul>
          <li v-for="newspaper in report.newspaper_counts" :key="newspaper.newspaper_name">
            {{ newspaper.newspaper_name }}: {{ newspaper.quantity }}
          </li>
        </ul>
        <p><strong>Поставки:</strong></p>
        <ul>
          <li v-for="distribution in report.distributions" :key="distribution.post_office_address">
            {{ distribution.newspaper_name }} → {{ distribution.post_office_address }}: {{ distribution.quantity }}
          </li>
        </ul>
      </div>
    </v-card-text>
  </v-card>
</template>
