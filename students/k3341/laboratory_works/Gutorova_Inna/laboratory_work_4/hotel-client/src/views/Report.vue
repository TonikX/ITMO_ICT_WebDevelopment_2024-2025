<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { tokenStore } from "@/stores/token.js";

const tokenStorage = tokenStore();

const quarters = [1, 2, 3, 4];
const currentYear = new Date().getFullYear();
const years = ref([currentYear, currentYear - 1, currentYear - 2, currentYear - 3, currentYear - 4]);

const selectedQuarter = ref(1);
const selectedYear = ref(currentYear);
const report = ref({});

async function fetchReport() {
  try {
    const response = await axios.get("/api/hotel-report/", {
      params: {
        quarter: selectedQuarter.value,
        year: selectedYear.value,
      },
      headers: {
        Authorization: `Token ${tokenStorage.token}`,
      },
    });
    report.value = response.data;
  } catch (error) {
    console.error("Ошибка загрузки отчёта:", error);
  }
}

function formatRoomsData(data) {
  return Object.entries(data).map(([roomId, clientCount]) => {
    return { roomId, clientCount };
  });
}

function formatIncomeData(data) {
  return Object.entries(data).map(([roomId, income]) => {
    return { roomId, income };
  });
}

function formatFloorData(data) {
  return data.map((floor) => {
    return { floorNumber: floor.floor__number, roomCount: floor.room_count };
  });
}

function formatTotalIncome(data) {
  return data.toFixed(2);
}
</script>

<template>
  <v-container>
    <h1>Отчёты</h1>
    <v-row>
      <v-col cols="6" sm="3">
        <v-select
          v-model="selectedQuarter"
          :items="quarters"
          label="Выберите квартал"
          outlined
        />
      </v-col>
      <v-col cols="6" sm="3">
        <v-select
          v-model="selectedYear"
          :items="years"
          label="Выберите год"
          outlined
        />
      </v-col>
      <v-col cols="12" sm="6">
        <v-btn color="primary" @click="fetchReport">Показать отчёт</v-btn>
      </v-col>
    </v-row>


    <v-row>

      <v-col v-if="report.income_per_room" cols="12" sm="6" md="3">
        <v-card class="report-card">
          <v-card-title>Доходы по комнатам</v-card-title>
          <v-card-text>
            <v-list>
              <v-list-item v-for="(income, index) in formatIncomeData(report.income_per_room)" :key="index">
                <v-list-item-content>
                  <v-list-item-title>Комната {{ income.roomId }}</v-list-item-title>
                  <v-list-item-subtitle>Доход: {{ income.income }} ₽</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col v-if="report.clients_in_rooms" cols="12" sm="6" md="3">
        <v-card class="report-card">
          <v-card-title>Количество клиентов на комнату</v-card-title>
          <v-card-text>
            <v-list>
              <v-list-item v-for="(clientCount, index) in formatRoomsData(report.clients_in_rooms)" :key="index">
                <v-list-item-content>
                  <v-list-item-title>Комната {{ clientCount.roomId }}</v-list-item-title>
                  <v-list-item-subtitle>Клиентов: {{ clientCount.clientCount }}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col v-if="report.rooms_per_floor" cols="12" sm="6" md="3">
        <v-card class="report-card">
          <v-card-title>Занятость по этажам</v-card-title>
          <v-card-text>
            <v-list>
              <v-list-item v-for="(floor, index) in formatFloorData(report.rooms_per_floor)" :key="index">
                <v-list-item-content>
                  <v-list-item-title>Этаж {{ floor.floorNumber }}</v-list-item-title>
                  <v-list-item-subtitle>Комнат: {{ floor.roomCount }}</v-list-item-subtitle>
                </v-list-item-content>
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col v-if="report.total_income" cols="12" sm="6" md="3">
        <v-card class="report-card">
            <v-card-title>Общий доход</v-card-title>
            <v-card-subtitle class="total-income">
            {{ formatTotalIncome(report.total_income) }} ₽
            </v-card-subtitle>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>
.report-card {
  display: flex;
  flex-direction: column;
  height: 100%;
  justify-content: space-between;
}

.total-income {
  display: flex;
  justify-content: center;
  align-items: center;
  flex-grow: 1; 
  font-size: 1.5rem;
  font-weight: bold;
}
</style>
