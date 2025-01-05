<template>
  <v-container>
    <v-row>
      <v-col cols="12" md="6">
        <v-select
          v-model="selectedQuarter"
          :items="quarters"
          label="Выберите квартал"
          outlined
        />
      </v-col>

      <v-col cols="12" md="6">
        <v-btn @click="generateReport" color="primary" :disabled="!selectedQuarter">
          Получить отчет
        </v-btn>
      </v-col>
    </v-row>

    <v-divider></v-divider>

    <v-row class="mt-4" v-if="reportData">
      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>Общий доход</v-card-title>
          <v-card-text>{{ reportData.total_income+"$" || 'Нет данных' }}</v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12" md="6">
        <v-card>
          <v-card-title>Этажи</v-card-title>
          <v-card-text>
            <v-list>
              <v-list-item-group v-for="floor in reportData.floors" :key="floor.floor">
                <v-list-item>
                  <v-list-item-content>
                    <v-list-item-title>Этаж: {{ floor.floor }}</v-list-item-title>
                    <v-list-item-subtitle>Кол-во номеров: {{ floor.num_rooms }}</v-list-item-subtitle>
                  </v-list-item-content>
                </v-list-item>
              </v-list-item-group>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>

      <v-col cols="12">
        <v-data-table
          :headers="roomHeaders"
          :items="reportData.rooms"
          item-key="id"
          :items-per-page="5"
          class="elevation-1"
        >
        </v-data-table>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { defineComponent, ref } from 'vue';
import axiosApi from '@/plugins/axios';

interface Room {
  id: number;
  number: number;
  total_clients: number;
  total_income: number | null;
}

interface Floor {
  floor: number;
  num_rooms: number;
}

interface ReportData {
  year: number;
  quarter: number;
  rooms: Room[];
  floors: Floor[];
  total_income: number | null;
}

export default defineComponent({
  setup() {
    const selectedQuarter = ref<number | null>(null);
    const quarters = ref<number[]>([1, 2, 3, 4]);
    const reportData = ref<ReportData | null>(null);

    const roomHeaders = [
      { title: 'Номер', value: 'number' },
      { title: 'Клиенты', value: 'total_clients' },
      { title: 'Доход ($)', value: 'total_income' },
    ];

    const generateReport = async () => {
      if (selectedQuarter.value === null) return;
      reportData.value = null
      try {
        const response = await axiosApi.get<ReportData>(`/reports/generate-report/${selectedQuarter.value}`);
        var data = response.data;
        data.rooms.forEach((room) => {
          room.total_income = room.total_income === null ? 0 : room.total_income;
        });
        data.total_income = data.rooms.reduce((acc, curr) => acc + curr.total_income, 0);
        reportData.value = data;
        console.log(response)
      } catch (error) {
        console.error('Ошибка при получении отчета:', error);
      }
    };

    return {
      selectedQuarter,
      quarters,
      reportData,
      roomHeaders,
      generateReport,
    };
  },
});
</script>

<style scoped>
.v-container {
  padding-top: 20px;
}
</style>
