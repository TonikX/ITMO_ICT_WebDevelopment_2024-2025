<script setup>
import {onMounted, ref} from "vue";
import axios from "axios";
import ClientList from "@/components/client/ClientList.vue";
import ClientModal from "@/components/client/ClientModal.vue";
const clients = ref([]);
const isLoading = ref(false);
const isError = ref(false);
const isAddModalVisible = ref(false);
let token; // Объявляем переменную на уровне, доступном для обеих функций

async function fetchClients() {
  isLoading.value = true;
  await axios
      .get('http://127.0.0.1:8000/insurance/clients/')
      .then(response => {
        clients.value = response.data;
        console.log(response.data);
      })
      .catch(error => {
        console.error("Ошибка загрузки", error);
        isError.value = true;
      })
      .finally(() => {
        isLoading.value = false;
      });
}


async function addClient(client) {
  await axios.post(`insurance/clients/`, client).then(fetchClients).catch(error => {
    isError.value = true;
    console.error(`Ошибка добавления клиента: ${error}`);
  })
}
async function deleteClient(id) {
  await axios.delete(`http://127.0.0.1:8000/insurance/clients/${id}`).then(() => {
    clients.value = clients.value.filter(item => item.id !== id);
  }).catch(error => {
    isError.value = true;
    console.error(`Ошибка удаления клиента: ${error}`);
  })
}
async function updateClient(client) {
  try {
    await axios.put(`http://127.0.0.1:8000/insurance/clients/${client.id}`, client);
    await fetchClients();
  } catch (error) {
    isError.value = true;
    console.error('Ошибка обновления клиента: ${error}');
  }
}



onMounted(fetchClients);
</script>

<template>
  <div class="d-flex align-center flex-column ga-10">
    <template v-if="isLoading">
      <v-skeleton-loader type="card" class="mt-4" max-width="500"></v-skeleton-loader>
    </template>
    <template v-else>
      <h2>Список индивидуальных клиентов</h2>
      <v-btn color="#4CAF50" @click="isAddModalVisible = true">Добавить клиента</v-btn>
      <ClientList :clients="clients" @delete-client="deleteClient" @update-client="updateClient"/>
      <ClientModal v-model="isAddModalVisible" mode="add" @submit-client="addClient" />
      <div v-if="isError" class="error-message">
        Произошла ошибка при загрузке данных. Пожалуйста, попробуйте позже.
      </div>
    </template>
  </div>
</template>

<style scoped>
.actions > .v-btn {
  min-width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>
