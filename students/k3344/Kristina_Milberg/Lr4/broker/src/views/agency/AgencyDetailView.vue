<script setup>
import {useRoute} from "vue-router";
import {onMounted, ref} from "vue";
import axios from "axios";

const route = useRoute()
const agency = ref({})
const isLoading = ref(true);
const isEditModalVisible = ref(false);

async function fetchAgency() {
  await axios.get(`manage/agency/${route.params.id}/`).then((response) => {
    if (response.status === 200) {
      agency.value = response.data
      isLoading.value = false
    }
  }).catch((error) => {
    console.log(error);
  })
}

onMounted(fetchAgency)

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
      <div v-if="agency">
        <h2>{{ agency.name }}</h2>
        <p>Страна: {{ agency.country }}</p>
        <p>Контактный номер: {{ agency.contact_number }}</p>
        <p>Адрес: {{ agency.address }}</p>
        <p>Юридический адрес: {{ agency.legal_address }}</p>
        <p>Менеджер: {{ agency.manager.username }}</p>
      </div>
      <div v-else>
        <p>Загрузка информации...</p>
      </div>
    </template>
  </v-container>
</template>

