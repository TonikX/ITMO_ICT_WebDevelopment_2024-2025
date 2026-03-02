<template>
  <v-container fluid>
    <v-row>
      <v-col>
        <v-card class="mb-6">
          <v-card-title class="text-h5 primary--text">
            Отчёт за квартал
          </v-card-title>

          <v-card-text>
            <v-row class="mb-6">
              <v-col cols="12" sm="6" md="4">
                <v-text-field
                  v-model="selectedYear"
                  label="Год"
                  type="number"
                  min="2000"
                  max="2100"
                  variant="outlined"
                  @change="fetchReport"
                ></v-text-field>
              </v-col>

              <v-col cols="12" sm="6" md="4">
                <v-select
                  v-model="selectedQuarter"
                  :items="quarters"
                  label="Квартал"
                  variant="outlined"
                  @change="fetchReport"
                ></v-select>
              </v-col>
            </v-row>

            <v-alert v-if="loading" type="info" prominent>
              Загрузка отчёта...
            </v-alert>

            <v-alert v-else-if="error" type="error" prominent>
              {{ error }}
            </v-alert>

            <div v-else>
              <!-- Общая сводка -->
              <v-card class="mb-6 elevation-2">
                <v-card-title>Общая сводка за {{ selectedYear }} квартал {{ selectedQuarter }}</v-card-title>
                <v-card-text>
                  <p><strong>Период:</strong> {{ report.period?.start || '—' }} — {{ report.period?.end || '—' }}</p>
                  <p><strong>Всего номеров на этажах:</strong></p>
                  <ul>
                    <li v-for="floor in report.rooms_per_floor || []" :key="floor.floor">
                      Этаж {{ floor.floor }}: {{ floor.count }} номеров
                    </li>
                  </ul>
                  <p><strong>Общий доход за квартал:</strong> <strong class="primary--text">{{ formatCurrency(report.total_revenue) }}</strong></p>
                </v-card-text>
              </v-card>

              <!-- Доход по номерам -->
              <v-card class="mb-6 elevation-2">
                <v-card-title>Доход по номерам</v-card-title>
                <v-data-table
                  :headers="revenueHeaders"
                  :items="report.revenue_per_room || []"
                  :items-per-page="10"
                  class="elevation-1"
                  no-data-text="Нет данных по доходам"
                >
                  <template v-slot:item.room__number="{ item }">
                    {{ item.room__number || '—' }}
                  </template>

                  <template v-slot:item.revenue="{ item }">
                    {{ formatCurrency(item.revenue || 0) }}
                  </template>
                </v-data-table>
              </v-card>

              <!-- Клиенты по номерам -->
              <v-card elevation="2">
                <v-card-title>Клиенты по номерам за период</v-card-title>
                <v-data-table
                  :headers="clientsHeaders"
                  :items="report.clients_per_room || []"
                  :items-per-page="10"
                  class="elevation-1"
                  no-data-text="Нет данных по клиентам"
                >
                  <template v-slot:item.room__number="{ item }">
                    {{ item.room__number || '—' }}
                  </template>

                  <template v-slot:item.room__floor="{ item }">
                    {{ item.room__floor || '—' }}
                  </template>

                  <template v-slot:item.client_count="{ item }">
                    {{ item.client_count || 0 }}
                  </template>
                </v-data-table>
              </v-card>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const report = ref(null)
const loading = ref(true)
const error = ref(null)
const selectedYear = ref(new Date().getFullYear())
const selectedQuarter = ref(1)
const router = useRouter()
const auth = useAuthStore()

const quarters = [
  { text: '1 квартал (янв-мар)', value: 1 },
  { text: '2 квартал (апр-июн)', value: 2 },
  { text: '3 квартал (июл-сен)', value: 3 },
  { text: '4 квартал (окт-дек)', value: 4 }
]

const revenueHeaders = [
  { text: 'Номер', value: 'room__number' },
  { text: 'Доход', value: 'revenue' }
]

const clientsHeaders = [
  { text: 'Номер', value: 'room__number' },
  { text: 'Этаж', value: 'room__floor' },
  { text: 'Количество клиентов', value: 'client_count' }
]

function formatCurrency(value) {
  return new Intl.NumberFormat('ru-RU', { style: 'currency', currency: 'RUB' }).format(value || 0)
}

async function fetchReport() {
  loading.value = true
  error.value = null

  try {
    const url = `http://127.0.0.1:8000/api/reports/quarter/?year=${selectedYear.value}&quarter=${selectedQuarter.value}`

    const response = await fetch(url, {
      headers: {
        Authorization: `Token ${auth.token}`
      }
    })

    if (!response.ok) {
      const errText = await response.text()
      throw new Error(`Ошибка загрузки: ${response.status} - ${errText}`)
    }

    report.value = await response.json()
  } catch (e) {
    error.value = e.message || 'Не удалось загрузить отчёт'
    console.error('Ошибка отчёта:', e)
  } finally {
    loading.value = false
  }
}

onMounted(() => {
  if (!auth.isAuthenticated) {
    router.push('/login')
    return
  }
  fetchReport()
})
</script>

<style scoped>
.v-data-table {
  border-radius: 8px;
  overflow: hidden;
}
</style>
