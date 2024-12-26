<script setup>
import {tokenStore} from "@/stores/token.js";
import {useRoute} from "vue-router";
import {onMounted, ref} from "vue";
import axios from "axios";
import {getRoomType} from "../utils/functions.js";
import RoomEditModal from "@/components/RoomEditModal.vue";
import RoomBookModal from "@/components/RoomBookModal.vue";

const token = tokenStore()
const route = useRoute()
const room = ref({})
const clients = ref([])
const isLoading = ref(true);
const isEditModalVisible = ref(false);
const isBookingModalVisible = ref(false);

async function fetchRoom() {
  await axios.get(`hotel/rooms/${route.params.id}`, {
    headers: {'Authorization': `Token ${token.token}`}
  }).then((response) => {
    if (response.status === 200) {
      room.value = response.data
      isLoading.value = false
    }
  }).catch((error) => {
    console.log(error);
  })
}

async function fetchClients() {
  await axios.get(`hotel/clients`, {
    headers: {'Authorization': `Token ${token.token}`}
  }).then((response) => {
    if (response.status === 200) {
      clients.value = response.data
      isLoading.value = false
    }

  }).catch((error) => {
    console.log(error);
  })
}

async function handleBook(booking) {
  await axios.post(`hotel/reservations`, booking, {
    headers: {'Authorization': `Token ${token.token}`}
  })
}

async function handleEditRoom(room) {
  await axios.put(`hotel/rooms/${room.id}/update`, room, {
    headers: {'Authorization': `Token ${token.token}`}
  })
  await fetchRoom()
}

onMounted(async () => fetchRoom())

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
      <div v-if="room">
        <h2>Комната №{{ room.id }}</h2>
        <p>Тип: {{ getRoomType(room.type) }}</p>
        <p>Этаж: {{ room.floor }}</p>
        <p>Стоимость: {{ room.cost }}₽/сутки</p>
        <p>Телефон: {{ room.phone_number }}</p>
        <div class="button-group">
          <v-btn color="primary" @click="isEditModalVisible = true">Редактировать</v-btn>
          <v-btn color="success" @click="() => {
            isBookingModalVisible = true
            fetchClients()
          }">Забронировать
          </v-btn>
        </div>
      </div>
      <div v-else>
        <p>Загрузка информации...</p>
      </div>
      <RoomEditModal
          v-model="isEditModalVisible"
          :room="room"
          @save-room="handleEditRoom"
      />

      <RoomBookModal
          v-model="isBookingModalVisible"
          :room="room"
          :clients="clients"
          @save-booking="handleBook"
      />
    </template>
  </v-container>
</template>

<style scoped>
.button-group {
  display: flex;
  gap: 16px;
  margin-top: 16px;
}
</style>
