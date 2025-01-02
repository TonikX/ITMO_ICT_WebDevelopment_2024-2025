<script setup>
import {onMounted, ref} from 'vue';
import {useRoute} from 'vue-router';
import axios from "axios";

const alpinistId = ref(null);
const alpinistData = ref();
const isLoading = ref(true);
const isError = ref(false);
const route = useRoute();
alpinistId.value = route.params.id;


async function fetchAlpinistAscending() {
  await axios.get(`club/alpinists/${alpinistId.value}/mountain_ascendings`).then(response => {
    alpinistData.value = response.data
    isLoading.value = false;
  }).catch(error => {
    console.error("Ошибка загрузки альпиниста", error);
    isError.value = true;
  })
}

onMounted(fetchAlpinistAscending)
</script>

<template>
  <div v-if="isLoading">Загрузка...</div>
  <div v-else-if="isError" class="error">Произошла ошибка при загрузке данных.</div>
  <div v-else>
    <v-card class="alpinist-details-card" width="800">
      <v-card-title>
        {{ alpinistData.alpinist.last_name }} {{ alpinistData.alpinist.first_name }}
        {{ alpinistData.alpinist.patronymic }}
      </v-card-title>
      <v-card-subtitle>
        Клуб: {{ alpinistData.alpinist.club.name }} <br/>
        Город: {{ alpinistData.alpinist.club.city }}, {{ alpinistData.alpinist.club.country }} <br/>
        Контактное лицо: {{ alpinistData.alpinist.club.contact_person }} <br/>
        Email: {{ alpinistData.alpinist.club.e_mail }} <br/>
        Телефон: {{ alpinistData.alpinist.club.phone }}
      </v-card-subtitle>
      <v-divider></v-divider>
      <v-card-text>
        <h3>Горы и количество восхождений:</h3>
        <v-list>
          <v-list-item
              v-for="(detail, index) in alpinistData.mountains"
              :key="index"
          >
            <v-list-item-content>
              <v-list-item-title>{{ detail.mountain }}</v-list-item-title>
              <v-list-item-subtitle>
                Количество восхождений: {{ detail.total_ascendings }}
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-card-text>
    </v-card>
  </div>
</template>

<style scoped>
.alpinist-details-card {
  margin: 0 auto;
  padding: 16px;
}

.error {
  color: red;
  font-weight: bold;
  margin-top: 16px;
}
</style>