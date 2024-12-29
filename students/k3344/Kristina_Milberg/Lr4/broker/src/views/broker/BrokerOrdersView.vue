<script setup>
import {onMounted, ref} from "vue";
import axios from "axios";
import BrokerOrdersList from "@/components/broker/BrokerOrdersList.vue";

const orders = ref([]);
ref(false);
const isLoading = ref(true);

async function fetchOrders() {
  await axios
      .get("broker/")
      .then((response) => {
        if (response.status === 200) {
          orders.value = response.data;
          console.log(orders.value);
          isLoading.value = false
        }
      })
      .catch((error) => {
        console.log(error);
      });
}

async function confirmOrder(id) {
  await axios.post(`/broker/${id}/approve/`, null)
  await fetchOrders()
}


async function deleteOrder(id) {
  await axios.delete(`/broker/${id}/`, null)
  await fetchOrders()
}

onMounted(fetchOrders);
</script>

<template>
  <v-container>
    <template v-if="isLoading">
      <v-skeleton-loader
          type="card"
          class="mt-4"
          max-width="500"
      ></v-skeleton-loader>
    </template>
    <template v-else>
      <h2>Список заказов</h2>

      <BrokerOrdersList
          :orders="orders"
          @delete-order="deleteOrder"
          @confirm-order="confirmOrder"
      />
    </template>
  </v-container>
</template>
