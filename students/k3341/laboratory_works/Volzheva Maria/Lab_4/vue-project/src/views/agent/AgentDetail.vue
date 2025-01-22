<script setup>
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import axios from 'axios';
const agentDetails = ref({});
const isLoading = ref(true);
const isError = ref(false);
const route = useRoute();
const agentId = route.params.id;
async function fetchAgentDetails() {
    isLoading.value = true;
    await axios.get(`/insurance/agents/${agentId}`).then(response => {
      agentDetails.value = response.data;
    }).catch(error => {
      console.error("Ошибка загрузки данных", error);
      isError.value = true;
    }).finally( isLoading.value = false);
}

onMounted(fetchAgentDetails);
</script>

<template>
  <div>
    <div v-if="isLoading">Загрузка...</div>
    <div v-if="isError" class="error">Произошла ошибка при загрузке данных.</div>
    <div v-if="!isLoading && !isError">
      <div class="container">
        <h2>Агент №{{ agentDetails.id }}</h2>
        <hr />
        <p><strong>ФИО:</strong> {{ agentDetails.first_name }} {{ agentDetails.second_name }} {{ agentDetails.patronymic }}</p>
        <p><strong>Номер телефона:</strong> {{ agentDetails.phone_number }}</p>
        <p><strong>Номер паспорта:</strong> {{ agentDetails.passport }}</p>
        <router-link to="/agents/" class="end-link" >
            <button class="btn">Назад</button>
        </router-link>
      </div>
    </div>
  </div>
</template>


<style scoped>
.end-link {
  color: green; /* Цвет ссылок в меню */
}
.actions > .v-btn {
  min-width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>



