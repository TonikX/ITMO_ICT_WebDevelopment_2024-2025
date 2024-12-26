<script setup>
import {ref} from 'vue'
import axiosClient from '@/services/axiosClient'

const formData = ref({
  printing_house_id: ''
})

const reportData = ref(null)
const errorMessage = ref('')

async function fetchReport() {
  errorMessage.value = ''
  reportData.value = null

  try {
    const response = await axiosClient.post('/reports/printinghouses/', {
      printing_house_id: formData.value.printing_house_id
    })
    reportData.value = response.data
  } catch (error) {
    if (error.response?.status === 404) {
      errorMessage.value = 'Типография с указанным ID не найдена.'
    } else {
      errorMessage.value = 'Произошла ошибка при загрузке отчёта.'
    }
    console.error('Ошибка получения отчёта:', error)
  }
}
</script>

<template>
  <v-container>
    <v-card class="pa-4">
      <v-card-title>Отчёт по типографии</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="fetchReport">
          <v-text-field
            v-model="formData.printing_house_id" label="ID типографии" type="number" required
          ></v-text-field>
          <v-btn color="primary" @click="fetchReport">Получить отчёт</v-btn>
        </v-form>
        <p v-if="errorMessage" class="error-message">{{ errorMessage }}</p>
        <div v-if="reportData">
          <p><strong>Типография:</strong> {{ reportData.printing_house.name }}</p>
          <p><strong>Адрес:</strong> {{ reportData.printing_house.address }}</p>
          <p><strong>Всего газет:</strong> {{ reportData.total_newspapers }}</p>
          <p><strong>Газеты:</strong></p>
          <ul>
            <li v-for="item in reportData.newspaper_counts" :key="item.newspaper_name">
              {{ item.newspaper_name }}: {{ item.quantity }} экз.
            </li>
          </ul>
          <p><strong>Поставки:</strong></p>
          <ul>
            <li v-for="distribution in reportData.distributions" :key="distribution.post_office_address">
              {{ distribution.newspaper_name }} → {{ distribution.post_office_address }}: {{ distribution.quantity }}
              экз.
            </li>
          </ul>
        </div>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<style scoped>
.error-message {
  color: red;
  font-weight: bold;
  margin-top: 10px;
}
</style>
