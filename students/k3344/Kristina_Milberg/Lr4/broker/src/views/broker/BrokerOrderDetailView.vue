<script setup>
import {useRoute} from "vue-router";
import {onMounted, ref} from "vue";
import axios from "axios";
import OrderProductsTable from "@/components/broker/OrderProductsTable.vue";
import {getOrderPaid, getOrderStatus} from "@/utils/functions.js";

const route = useRoute()
const order = ref({})
const isLoading = ref(true);

async function fetchOrder() {
  await axios.get(`broker/${route.params.id}`).then((response) => {
    if (response.status === 200) {
      order.value = response.data
      isLoading.value = false
    }
  }).catch((error) => {
    console.log(error);
  })
}

async function editBatch(batch) {
  const batches = order.value.batches;
  const batchIndex = batches.findIndex((b) => b.id === batch.id);
  if (batchIndex !== -1) {

    batches[batchIndex].quantity = batch.quantity;
    batches[batchIndex].price_per_unit = batch.price_per_unit;

    await axios.patch(`broker/${route.params.id}/`, {batches: batches}).then((response) => {
      if (response.status === 200) {
        fetchOrder()
      }
    }).catch(error => {
      console.log(error)
    })
  }
}

async function deleteBatch(id) {
  await axios.patch(`broker/${route.params.id}/`, {batches: order.value.batches.filter(b => b.id !== id)}).then((response) => {
    if (response.status === 200) {
      fetchOrder()
    }
  }).catch(error => {
    console.log(error);
  })
}

onMounted(fetchOrder)

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
      <div v-if="order">
        <h2>Заказ №{{ order.id }}</h2>
        <p>Дата доставки: {{ order.delivery_date ?? "Не назначена" }}</p>
        <p>Статус: {{ getOrderStatus(order.status) }}</p>
        <p>Предоплата: {{ getOrderPaid(order.prepaid) }}</p>
        <p>Полная стоимость заказа: {{ order.total_cost }} рублей</p>
        <p>Оплачено: {{ order.total_paid ?? 0 }} рублей</p>
      </div>
      <div v-else>
        <p>Загрузка информации...</p>
      </div>
      <OrderProductsTable
          :batches="order.batches"
          :is-opened="order.status === 'Opened'"
          @edit-batch="editBatch"
          @delete-batch="deleteBatch"
      />
    </template>
  </v-container>
</template>

<style scoped>

</style>