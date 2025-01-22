<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';
const organizationDetails = ref({});
const isLoading = ref(true);
const isError = ref(false);
const route = useRoute();
const organizationId = route.params.id;
async function fetchOrganizationDetails() {
    isLoading.value = true;
    await axios.get(`/insurance/organizations/${organizationId}`).then(response => {
      organizationDetails.value = response.data;
    }).catch(error => {
      console.error("Ошибка загрузки данных", error);
      isError.value = true;
    }).finally( isLoading.value = false);
}

onMounted(fetchOrganizationDetails);
</script>

<template>
  <div>
    <div v-if="isLoading">Загрузка...</div>
    <div v-if="isError" class="error">Произошла ошибка при загрузке данных.</div>
    <div v-if="!isLoading && !isError">
      <h2>Организация №{{ organizationDetails.id }}</h2>
      <hr />
      <p><strong>Полное имя:</strong> {{ organizationDetails.full_name }} {{ organizationDetails.second_name }} {{ organizationDetails.patronymic }}</p>
      <p><strong>Краткое имя:</strong> {{ organizationDetails.short_name }}</p>
      <p><strong>Адрес:</strong> {{ organizationDetails.address }}</p>
      <p><strong>Банковский код:</strong> {{ organizationDetails.bank_code }}</p>
      <p><strong>Специализация:</strong> {{ organizationDetails.specialization }}</p>
      <router-link to="/organizations/"class="end-link">
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
