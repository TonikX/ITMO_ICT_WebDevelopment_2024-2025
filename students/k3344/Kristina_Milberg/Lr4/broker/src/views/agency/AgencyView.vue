<script setup>
import {onMounted, ref} from "vue";
import axios from "axios";
import AgencyList from "@/components/agency/AgencyList.vue";
import AgencyModal from "@/components/agency/AgencyModal.vue";

const agencies = ref([]);
const isAddModalVisible = ref(false);
const isLoading = ref(true);
const isError = ref(false)


async function fetchAgencies() {
  await axios
      .get("manage/agency/")
      .then((response) => {
        if (response.status === 200) {
          agencies.value = response.data;
          isLoading.value = false
        }
      })
      .catch((error) => {
        isLoading.value = false
        isError.value = true
        console.log(error);
      });
}

async function handleAddAgency(agency) {
  await axios
      .post("manage/agency/", agency)
      .then(() => {
        fetchAgencies();
        isAddModalVisible.value = false;
      })
      .catch((error) => {
        console.log(error);
      });
}

onMounted(fetchAgencies);
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


        <AgencyList :agencies="agencies"/>
        <v-btn color="primary" @click="isAddModalVisible = true">Добавить агенство</v-btn>
        <AgencyModal
            v-model="isAddModalVisible"
            mode="add"
            @submit-agency="handleAddAgency"
        />
      </template>
    </template>
  </div>
</template>
