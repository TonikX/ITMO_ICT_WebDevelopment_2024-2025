<template>
  <v-container>
    <h2 class="mb-4">Отчёт по гостинице</h2>
    <!-- Карточка для выбора квартала и кнопки формирования отчета -->
    <v-card variant="eleveated" :elevation="4" class="pa-4 mb-4">
      <v-select
        :items="[1,2,3,4]"
        v-model="selectedQuarter"
        label="Выберите квартал"
        variant="outlined"
      ></v-select>
      <v-btn
        variant="outlined"
        color="primary"
        class="mt-2"
        @click="fetchReport"
      >
        Сформировать отчёт
      </v-btn>
    </v-card>

    <!-- Карточка для отображения данных отчета -->
    <v-card
      v-if="reportData"
      variant="elevated"
      class="pa-4 mb-4"
      :elevation="4"
    >
      <div class="mb-2">
        <strong>Число клиентов по номерам:</strong>
      </div>
      <v-list density="compact" v-for="item in reportData.stays_per_room" :key="item.room__room_id">
        <v-list-item>
          Номер {{ item.room__room_id }} — Клиентов: {{ item.client_count }}
        </v-list-item>
      </v-list>

      <div class="mb-2 mt-3">
        <strong>Количество номеров на этажах:</strong>
      </div>
      <v-list density="compact" v-for="floorInfo in reportData.rooms_per_floor" :key="floorInfo.floor">
        <v-list-item>
          Этаж: {{ floorInfo.floor }} — Номеров: {{ floorInfo.room_count }}
        </v-list-item>
      </v-list>

      <div class="mb-2 mt-3">
        <strong>Доход по каждому номеру:</strong>
      </div>
      <v-list density="compact" v-for="roomIncome in reportData.income_per_room" :key="roomIncome.room_id">
        <v-list-item>
          Номер {{ roomIncome.room_id }} — Доход: {{ roomIncome.total_income }}
        </v-list-item>
      </v-list>

      <div class="mt-3">
        <strong>Суммарный доход:</strong> {{ reportData.total_income }}
      </div>
    </v-card>
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Report',
  data() {
    return {
      selectedQuarter: null, // Выбранный квартал
      reportData: null // Данные отчета
    }
  },
  methods: {
    async fetchReport() {
      if (!this.selectedQuarter) return
      const token = localStorage.getItem('token')
      try {
        const response = await axios.get(
          `http://127.0.0.1:8000/report/?quarter=${this.selectedQuarter}`, 
          { headers: { Authorization: `Token ${token}` } }
        )
        this.reportData = response.data
      } catch (error) {
        console.error(error)
      }
    }
  }
}
</script>

