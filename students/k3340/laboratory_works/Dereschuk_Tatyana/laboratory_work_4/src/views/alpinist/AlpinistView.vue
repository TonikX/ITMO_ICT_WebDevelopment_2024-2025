<script setup>
import {onMounted, ref} from "vue";
import axios from "axios";
import AlpinistList from "@/components/alpinist/AlpinistList.vue";
import AlpinistModal from "@/components/alpinist/AlpinistModal.vue";

const alpinists = ref([]);
const clubs = ref([]);
const isLoading = ref(false);
const isError = ref(false);
const isAddModalVisible = ref(false);

async function fetchAlpinists() {
  isLoading.value = true;
  await axios
      .get('club/alpinists')
      .then(response => {
        alpinists.value = response.data;
      })
      .catch(error => {
        console.error("Ошибка загрузки альпинистов", error);
        isError.value = true;
      })
      .finally(() => {
        isLoading.value = false;
      });
}

async function fetchClubs() {
  isLoading.value = true;
  await axios
      .get('club/clubs')
      .then(response => {
        clubs.value = response.data;
      })
      .catch(error => {
        console.error("Ошибка загрузки клубов", error);
        isError.value = true;
      })
      .finally(() => {
        isLoading.value = false;
      });
}

async function addAlpinist(alpinist) {
  await axios.post(`club/alpinists`, alpinist).then(fetchAlpinists).catch(error => {
    isError.value = true;
    console.error(`Ошибка добавления альпиниста: ${error}`);
  })
}

async function deleteAlpinist(id) {
  await axios.delete(`club/alpinists/${id}`).then(() => {
    alpinists.value = alpinists.value.filter(item => item.id !== id);
  }).catch(error => {
    isError.value = true;
    console.error(`Ошибка удаления альпиниста: ${error}`);
  })
}

async function updateAlpinist(alpinist) {
  await axios.put(`club/alpinists/${alpinist.id}`, alpinist).then(fetchAlpinists).catch(error => {
    isError.value = true;
    console.error(`Ошибка обновления альпиниста: ${error}`);
  })
}

onMounted(async () => {
  await fetchAlpinists()
  await fetchClubs()
});

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
      <h2>Список альпинистов</h2>
      <v-btn color="primary" @click="isAddModalVisible = true">Добавить альпиниста</v-btn>
      <AlpinistList :alpinists="alpinists" :clubs="clubs" @delete-alpinist="deleteAlpinist" @update-alpinist="updateAlpinist"/>
      <AlpinistModal
          v-model="isAddModalVisible"
          :clubs="clubs"
          mode="add"
          @submit-alpinist="addAlpinist"
      />
    </template>
  </div>
</template>

<style scoped>
.alpinists-list {
  max-width: 600px;
  margin: 0 auto;
  font-family: Arial, sans-serif;
}

.alpinist-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px 0;
}

.info {
  flex-grow: 1;
  margin-right: 10px;
}

.actions {
  display: flex;
  gap: 5px;
}

.actions > .v-btn {
  min-width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.error {
  color: red;
  font-weight: bold;
  margin-top: 10px;
}
</style>
