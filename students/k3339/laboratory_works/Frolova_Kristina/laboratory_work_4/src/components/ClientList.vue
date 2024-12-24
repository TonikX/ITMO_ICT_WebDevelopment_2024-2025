<script setup>
import {ref} from "vue";
import ClientModal from "@/components/ClientModal.vue";
import axios from "axios";
import {tokenStore} from "@/stores/token.js";

const token = tokenStore()
defineProps({
  clients: Array,
});
const emits = defineEmits(["delete-client", "update-clients"]);

const isEditModalVisible = ref(false);
const selectedClient = ref({});

function handleEdit(client) {
  selectedClient.value = {...client};
  isEditModalVisible.value = true;
}

function handleUpdateClient(client) {
  axios
      .put(`hotel/clients/${client.id}/update`, client, {
        headers: {
          Authorization: `Token ${token.token}`,
        },
      })
      .then(() => {
        emits("update-clients");
        isEditModalVisible.value = false;
      })
      .catch((error) => {
        console.log(error);
      });
}
</script>

<template>
  <div class="client-list">
    <template v-for="client in clients" :key="client.id">
      <v-card class="client-card" width="400">
        <template #title>{{ client.full_name }}</template>
        <template #text>
          Данные паспорта: {{ client.passport_number }}<br/>
          Город прибытия: {{ client.city_from }}
        </template>
        <v-card-actions>
          <v-btn @click="handleEdit(client)" color="primary">Редактировать</v-btn>
          <v-btn @click="$emit('delete-client', client.id)" color="secondary">Удалить</v-btn>
        </v-card-actions>
      </v-card>
    </template>

    <ClientModal
        v-model="isEditModalVisible"
        :clientData="selectedClient"
        mode="edit"
        @submit-client="handleUpdateClient"
    />
  </div>
</template>

<style scoped>
.client-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.client-card {
  background-color: #f8f9fa;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 16px;
}
</style>
