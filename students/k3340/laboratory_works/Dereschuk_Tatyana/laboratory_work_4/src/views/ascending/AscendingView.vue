<script setup>
import {onMounted, ref} from 'vue';
import axios from 'axios';
import router from "@/utils/router.js";
import AscendingModal from "@/components/ascending/AscendingModal.vue";

const ascendings = ref([]);
const mountains = ref([]);
const isLoading = ref(true);
const isError = ref(false);
const isAddAscendingModalOpen = ref(false);

async function fetchAscendings() {
    isLoading.value = true;
    await axios.get('/club/ascendings').then(response => {
      ascendings.value = response.data;
    }).catch(error => {
      console.error("Ошибка загрузки данных", error);
      isError.value = true;
    }).finally( isLoading.value = false);
}

async function fetchMountains() {
  await axios.get(`club/mountains`).then(response => {
    mountains.value = response.data;
  }).catch(error => {
    console.error("Ошибка загрузки данных", error);
    isError.value = true;
  })
}

async function addAscending(ascending) {
  await axios.post(`club/ascendings`, ascending).then(fetchAscendings).catch(error => {
    console.error("Ошибка загрузки данных", error);
    isError.value = true;
  })
}

onMounted(async () => {
  await fetchAscendings()
  await fetchMountains()
});
</script>

<template>
  <v-container class="pa-4">
    <v-card outlined class="pa-4">
      <h1 class="text-center">Список восхождений</h1>
      <div v-if="isLoading" class="text-center">Загрузка...</div>
      <div v-if="isError" class="text-center text-danger">Произошла ошибка при загрузке данных.</div>
      <v-list v-if="!isLoading && !isError">
        <div class="d-flex justify-center mb-4">
          <v-btn color="primary" @click="isAddAscendingModalOpen = true">Добавить восхождение</v-btn>
        </div>
        <v-list-item v-for="ascending in ascendings" :key="ascending.id" @click="router.push(`ascendings/${ascending.id}`)" class="mb-2 ascending-item">
          <v-card outlined>
            <v-card-title>
              {{ ascending.description }}
            </v-card-title>
            <v-card-subtitle>
              С {{ ascending.planned_start_date }} по {{ ascending.planned_end_date }}
            </v-card-subtitle>
          </v-card>
        </v-list-item>
        <AscendingModal
            :mountains="mountains"
            v-model="isAddAscendingModalOpen"
            @submit="addAscending"
        />
      </v-list>
    </v-card>
  </v-container>
</template>

<style scoped>
.pa-4 {
  padding: 16px;
}
.text-center {
  text-align: center;
}
.text-danger {
  color: #f44336;
}
.ascending-item {
  cursor: pointer;
}
.ascending-item:hover {
  background-color: #f5f5f5;
}
.mb-2 {
  margin-bottom: 16px;
}
</style>
