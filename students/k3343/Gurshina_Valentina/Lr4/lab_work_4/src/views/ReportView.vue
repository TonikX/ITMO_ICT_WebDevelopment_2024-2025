<script setup>
import {onMounted, ref, watch} from "vue";
import axios from "axios";
import {tokenStore} from "@/stores/token.js";

const token = tokenStore();
const isLoading = ref(true);
const reportData = ref(null);
const selectedQuarter = ref(1);

async function fetchReport() {
  isLoading.value = true;
  await axios.get("/hotel/report", {
    headers: {Authorization: `Token ${token.token}`},
    params: {quarter: selectedQuarter.value},
  }).then(response => {
    reportData.value = response.data;
    isLoading.value = false;
    console.log(response.data);
  }).catch(error => {
    console.log(error);
  });
}

watch(selectedQuarter, () => {
      fetchReport();
    }
)

onMounted(fetchReport);
</script>

<template>
  <v-container>
    <h2>Отчёт за квартал</h2>
    <v-select
        v-model="selectedQuarter"
        :items="[1, 2, 3, 4]"
        label="Выберите квартал"
        class="mb-4"
    ></v-select>
    <div v-if="isLoading">
      <v-skeleton-loader type="table"></v-skeleton-loader>
    </div>
    <div v-else-if="reportData">
      <h3>Количество клиентов по комнатам</h3>
      <v-data-table
          :headers="[
          { text: 'Комната', value: 'room' },
          { text: 'Количество клиентов', value: 'count_of_clients' },
        ]"
          :items="reportData.clients_per_room"
          class="mb-4"
      ></v-data-table>

      <h3>Количество комнат на этажах</h3>
      <v-data-table
          :headers="[
          { text: 'Этаж', value: 'floor' },
          { text: 'Количество комнат', value: 'rooms_count' },
        ]"
          :items="reportData.rooms_per_floor"
          class="mb-4"
      ></v-data-table>

      <h3>Прибыль по комнатам</h3>
      <v-data-table
          :headers="[
          { text: 'Комната', value: 'room' },
          { text: 'Прибыль', value: 'profit' },
        ]"
          :items="reportData.profit_per_room"
          class="mb-4"
      ></v-data-table>

      <h3>Общая прибыль</h3>
      <p>{{ reportData.total_profit }} ₽</p>
    </div>
    <div v-else>
      <p>Нет данных для отображения.</p>
    </div>
  </v-container>
</template>
