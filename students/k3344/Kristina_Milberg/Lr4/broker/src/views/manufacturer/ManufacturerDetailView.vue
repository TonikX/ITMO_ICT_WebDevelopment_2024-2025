<script setup>
import axios from "axios";
import {nextTick, onMounted, ref} from "vue";
import {useRoute} from "vue-router";
import ManufacturerProductsTable from "@/components/manufacturer/ManufacturerProductsTable.vue";
import ProductModal from "@/components/manufacturer/ProductModal.vue";

const route = useRoute()
const manufacturer = ref({})
const isLoading = ref(true);
const isAddProductModalVisible = ref(false);

async function fetchManufacturer() {
  await axios.get(`manage/manufacturer/${route.params.id}/`).then((response) => {
    if (response.status === 200) {
      manufacturer.value = response.data
      isLoading.value = false
    }
  }).catch((error) => {
    console.log(error);
  })
}

function handleAddProduct() {
  isAddProductModalVisible.value = true
}

async function saveProduct(product) {
  await axios.post(`manage/manufacturer/${route.params.id}/add_product/`, product).then(response => {
    if (response.status === 200) {
      fetchManufacturer().then(() => {
        nextTick(() => {
          manufacturer.value = { ...manufacturer.value };
        });
      });
    }
  }).catch(error => console.log(error))
}


onMounted(fetchManufacturer)
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
      <div v-if="manufacturer">
        <h2>{{ manufacturer.name }}</h2>
        <v-btn color="primary" text="Добавить продукт" @click="handleAddProduct"/>
      </div>
      <div v-else>
        <p>Загрузка информации...</p>
      </div>
      <ManufacturerProductsTable
          :key="manufacturer.products.length"
          :products="manufacturer.products"
      />
      <ProductModal
          v-model="isAddProductModalVisible"
          :manufacturer="manufacturer"
          @save-product="saveProduct"
      />
    </template>
  </v-container>
</template>

<style scoped>

</style>