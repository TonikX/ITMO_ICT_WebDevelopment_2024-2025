<script setup>
import {onMounted, ref} from "vue";
import axios from "axios";
import {tokenStore} from "@/stores/token.js";

const token = tokenStore();
const orders = ref([]);
const isAddModalVisible = ref(false);
const isLoading = ref(true);

async function fetchOrders() {
  await axios
      .get("broker/")
      .then((response) => {
        if (response.status === 200) {
          orders.value = response.data;
          isLoading.value = false
        }
      })
      .catch((error) => {
        console.log(error);
      });
}

onMounted(fetchOrders);
</script>

<template>
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

      <ClientList :clients="orders" @delete-client="deleteClient" @update-clients="fetchOrders"/>

      <v-btn color="primary" @click="isAddModalVisible = true">Добавить клиента</v-btn>
      <ClientModal
          v-model="isAddModalVisible"
          mode="add"
          @submit-client="handleAddOrder"
      />
    </template>
  </div>
</template>
