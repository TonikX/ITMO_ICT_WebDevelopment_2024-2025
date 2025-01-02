<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';

const mountainDetails = ref({});
const isLoading = ref(true);
const isError = ref(false);

const route = useRoute();
const mountainId = route.params.id;

async function fetchMountainDetails() {
    isLoading.value = true;
    await axios.get(`/club/mountains/${mountainId}`).then(response => {
      mountainDetails.value = response.data;
    }).catch(error => {
      console.error("Ошибка загрузки данных", error);
      isError.value = true;
    }).finally( isLoading.value = false);
}

onMounted(fetchMountainDetails);
</script>

<template>
  <div>
    <div v-if="isLoading">Загрузка...</div>
    <div v-if="isError" class="error">Произошла ошибка при загрузке данных.</div>
    <div v-if="!isLoading && !isError">
      <v-card>
        <v-card-title>{{ mountainDetails.name }}</v-card-title>
        <v-card-subtitle>
          Количество альпинистов: {{ mountainDetails.total_climbers }}
        </v-card-subtitle>
        <v-divider></v-divider>
        <v-card-text>
          <p>Высота: {{ mountainDetails.height }} метров</p>
          <p>Страна: {{ mountainDetails.country }}</p>
          <p>Район: {{ mountainDetails.district }}</p>
        </v-card-text>
      </v-card>
    </div>
  </div>
</template>

<style scoped>
.error {
  color: red;
  font-weight: bold;
}
</style>
