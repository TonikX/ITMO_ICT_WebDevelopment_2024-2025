<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';
const clientDetails = ref({});
const isLoading = ref(true);
const isError = ref(false);
const route = useRoute();
const clientId = route.params.id;
async function fetchClientDetails() {
    isLoading.value = true;
    await axios.get(`/insurance/clients/${clientId}`).then(response => {
      clientDetails.value = response.data;
    }).catch(error => {
      console.error("Ошибка загрузки данных", error);
      isError.value = true;
    }).finally( isLoading.value = false);
}

onMounted(fetchClientDetails);
</script>

<template>
  <div>
    <div v-if="isLoading">Загрузка...</div>
    <div v-if="isError" class="error">Произошла ошибка при загрузке данных.</div>
    <div v-if="!isLoading && !isError">
      <h2>Клиент №{{ clientDetails.id }}</h2>
      <hr />
      <p><strong>ФИО:</strong> {{ clientDetails.first_name }} {{ clientDetails.second_name }} {{ clientDetails.patronymic }}</p>
      <p><strong>Возраст (лет):</strong> {{ clientDetails.age }}</p>
      <p><strong>Номер паспорта:</strong> {{ clientDetails.passport }}</p>
      <router-link to="/clients/"class="end-link">
        <button class="btn">Назад</button>
      </router-link>
    </div>
  </div>
</template>


<style scoped>
.end-link {
  color: green; /* Цвет ссылок в меню */
}
.error {
  color: red;
  font-weight: bold;
}
</style>
