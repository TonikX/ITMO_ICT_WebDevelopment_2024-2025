<script setup>
import {onMounted, ref} from "vue";
import axios from "axios";
import {tokenStore} from "@/stores/token.js";
import ClientList from "@/components/ClientList.vue";
import ClientModal from "@/components/ClientModal.vue";

const token = tokenStore();
const clients = ref([]);
const isAddModalVisible = ref(false);
const isLoading = ref(true);

async function fetchClients() {
  await axios
      .get("hotel/clients", {
        headers: {
          Authorization: `Token ${token.token}`,
        },
      })
      .then((response) => {
        if (response.status === 200) {
          clients.value = response.data;
          isLoading.value = false
        }
      })
      .catch((error) => {
        console.log(error);
      });
}

async function handleAddClient(client) {
  await axios
      .post("hotel/clients", client, {
        headers: {
          Authorization: `Token ${token.token}`,
        },
      })
      .then(() => {
        fetchClients();
        isAddModalVisible.value = false;
      })
      .catch((error) => {
        console.log(error);
      });
}

async function deleteClient(id) {
  await axios
      .delete(`hotel/clients/${id}/delete`, {
        headers: {
          Authorization: `Token ${token.token}`,
        },
      })
      .then(() => {
        fetchClients();
      })
      .catch((error) => {
        console.log(error);
      });
}

onMounted(fetchClients);
</script>

<template>
  <v-app>
  <div class="d-flex align-center flex-column ga-10">
    <template v-if="isLoading">
      <v-skeleton-loader
          type="card"
          class="mt-4"
          max-width="500"
      ></v-skeleton-loader>
    </template>
    <template v-else>
      <h2>Клиенты</h2>

      <ClientList :clients="clients" @delete-client="deleteClient" @update-clients="fetchClients"/>

      <v-btn color="primary" @click="isAddModalVisible = true">Добавить клиента</v-btn>
      <ClientModal
          v-model="isAddModalVisible"
          mode="add"
          @submit-client="handleAddClient"
      />
    </template>
  </div>
</v-app>
</template>
