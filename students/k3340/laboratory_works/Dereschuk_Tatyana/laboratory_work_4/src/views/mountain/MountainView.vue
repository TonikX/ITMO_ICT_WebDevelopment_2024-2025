<script setup>
import {onMounted, ref} from "vue";
import axios from "axios";
import MountainList from "@/components/mountain/MountainList.vue";
import MountainModal from "@/components/mountain/MountainModal.vue";

const mountains = ref([]);
const isLoading = ref(false);
const isError = ref(false);
const isAddModalVisible = ref(false);

async function fetchMountains() {
  isLoading.value = true;
  await axios
      .get('club/mountains')
      .then(response => {
        mountains.value = response.data;
      })
      .catch(error => {
        console.error("Ошибка загрузки альпинистов", error);
        isError.value = true;
      })
      .finally(() => {
        isLoading.value = false;
      });
}

async function addMountain(mountain) {
  await axios.post(`club/mountains`, mountain).then(fetchMountains).catch(error => {
    isError.value = true;
    console.error(`Ошибка добавления вершины: ${error}`);
  })
}

async function deleteMountain(id) {
  await axios.delete(`club/mountains/${id}`).then(() => {
    mountains.value = mountains.value.filter(item => item.id !== id);
  }).catch(error => {
    isError.value = true;
    console.error(`Ошибка удаления альпиниста: ${error}`);
  })
}

async function updateMountain(mountain) {
  await axios.put(`club/mountains/${mountain.id}`, mountain).then(fetchMountains).catch(error => {
    isError.value = true;
    console.error(`Ошибка обновления альпиниста: ${error}`);
  })
}

onMounted(fetchMountains);

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
        <h2>Список вершин</h2>
        <v-btn color="primary" @click="isAddModalVisible = true">Добавить вершину</v-btn>
        <MountainList :mountains="mountains" @delete-mountain="deleteMountain" @update-mountain="updateMountain"/>
        <MountainModal
            v-model="isAddModalVisible"
            mode="add"
            @submit-mountain="addMountain"
        />
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
