<script setup>
import {onMounted, ref} from "vue";
import axios from "axios";
import ManufacturerList from "@/components/manufacturer/ManufacturerList.vue";
import ManufacturerModal from "@/components/manufacturer/ManufacturerModal.vue";

const manufacturers = ref([]);
const isAddModalVisible = ref(false);
const isLoading = ref(true);
const isError = ref(false)

async function fetchManufacturers() {
  await axios
      .get("manage/manufacturer/")
      .then((response) => {
        if (response.status === 200) {
          manufacturers.value = response.data;
          console.log(manufacturers.value);
          isLoading.value = false
        }
      })
      .catch((error) => {
        isLoading.value = false
        isError.value = true
        console.log(error);
      });
}

async function handleAddManufacturer(manufacturer) {
  await axios
      .post("manage/manufacturer/", manufacturer)
      .then(() => {
        fetchManufacturers();
        isAddModalVisible.value = false;
      })
      .catch((error) => {
        console.log(error);
      });
}

onMounted(fetchManufacturers);
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
      <template v-if="isError">
        <p>Доступ запрещен</p>
        <p>Обратитесь к администратору</p>
      </template>
      <template v-else>

        <h2>Производители</h2>

        <ManufacturerList :manufacturers="manufacturers"/>

        <v-btn color="primary" @click="isAddModalVisible = true">Добавить производителя</v-btn>
        <ManufacturerModal
            v-model="isAddModalVisible"
            mode="add"
            @submit-manufacturer="handleAddManufacturer"
        />
      </template>
    </template>
  </div>
</template>
