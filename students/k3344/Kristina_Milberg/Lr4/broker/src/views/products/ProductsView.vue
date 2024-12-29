<script setup>
import {tokenStore} from "@/stores/token.js";
import {onMounted, ref, watch} from "vue";
import axios from "axios";
import ProductsList from "@/components/ProductsList.vue";

const products = ref([]);
const isLoading = ref(true);
const searchQuery = ref("");

async function fetchProducts(query = "") {
  console.log(query);
  return axios
      .get("/product/", {
        params: {
          search: query,
        },
      })
      .then((response) => {
        if (response.status === 200) {
          products.value = response.data;
        }
      })
      .catch((error) => {
        console.log(error);
      })
}

onMounted(async () => {
  isLoading.value = true;
  await fetchProducts()
  isLoading.value = false;
});

watch(searchQuery, /**@param {string} newQuery*/(newQuery) => {
  fetchProducts(newQuery);
});
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
      <h2>Список товаров</h2>
      <v-text-field
          v-model="searchQuery"
          label="Поиск товаров"
          class="mb-4"
          clearable
      ></v-text-field>
      <ProductsList :products="products"/>
    </template>
  </v-container>
</template>

<style scoped>
</style>
