<script setup>
import {useRoute} from "vue-router";
import {onMounted, ref} from "vue";
import axios from "axios";

const route = useRoute()
const product = ref({})
const isLoading = ref(true);

async function fetchProduct() {
  await axios.get(`product/${route.params.id}/`).then((response) => {
    if (response.status === 200) {
      product.value = response.data
      isLoading.value = false
    }
  }).catch((error) => {
    console.log(error);
  })
}

onMounted(fetchProduct)

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
      <div v-if="product">
        <h2>{{ product.name }}</h2>
        <p>Производитель: {{ product.manufacturer.name }}</p>
        <p>Категория: {{ product.product_group}}</p>
        <p>Количество: {{ product.quantity }}</p>
        <p>Дата производства: {{ product.production_date }}</p>
        <p>Гарантийный срок хранения: {{ product.expiry_period ?? "Не назначен " }}</p>
      </div>
      <div v-else>
        <p>Загрузка информации...</p>
      </div>
    </template>
  </v-container>
</template>

<style scoped>
</style>
