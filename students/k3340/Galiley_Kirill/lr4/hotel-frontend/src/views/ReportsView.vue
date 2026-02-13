<template>
  <v-container>
    <v-row>
      <v-col>
        <h1>Отчеты</h1>
      </v-col>
    </v-row>

    <v-row>
      <v-col>
        <v-card>
          <v-card-title>Свободные номера</v-card-title>
          <v-card-text>
            <v-btn @click="loadFreeRooms" color="primary">Проверить</v-btn>
            <p v-if="freeRooms !== null" class="mt-3">Свободных номеров: {{ freeRooms }}</p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row>
      <v-col>
        <v-card>
          <v-card-title>Квартальный отчет</v-card-title>
          <v-card-text>
            <v-select
              v-model="selectedQuarter"
              :items="[1, 2, 3, 4]"
              label="Выберите квартал"
            ></v-select>
            <v-btn @click="loadQuarterReport" color="primary">Получить отчет</v-btn>

            <div v-if="quarterReport" class="mt-3">
              <p><strong>Период:</strong> {{ quarterReport.period }}</p>
              <p><strong>Общий доход:</strong> {{ quarterReport.total_income }} ₽</p>

              <h3 class="mt-4">Доход по номерам</h3>
              <v-list>
                <v-list-item v-for="(income, room) in quarterReport.income_per_room" :key="room">
                  Номер {{ room }}: {{ income }} ₽
                </v-list-item>
              </v-list>
            </div>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import api from '@/services/api'

const freeRooms = ref(null)
const selectedQuarter = ref(1)
const quarterReport = ref(null)

const loadFreeRooms = async () => {
  try {
    const response = await api.getFreeRooms()
    freeRooms.value = response.data.free_rooms
  } catch (error) {
    console.error(error)
  }
}

const loadQuarterReport = async () => {
  try {
    const response = await api.getQuarterReport(selectedQuarter.value)
    quarterReport.value = response.data
  } catch (error) {
    console.error(error)
  }
}
</script>