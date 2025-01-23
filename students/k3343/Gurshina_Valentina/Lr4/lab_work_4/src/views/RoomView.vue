<script setup>
import {computed, onMounted, ref} from "vue";
import {tokenStore} from "@/stores/token.js";
import axios from "axios";
import RoomList from "@/components/RoomList.vue";

const token = tokenStore()
const rooms = ref([])
const reservations = ref([])
const showOnlyFree = ref(false)
const isLoading = ref(true)

async function fetchRooms() {
  await axios.get('/hotel/rooms', {
    headers: {
      Authorization: `Token ${token.token}`
    }
  }).then(response => {
    rooms.value = response.data
  }).catch(error => {
    console.log(error);
  })
}

async function fetchReservations() {
  await axios.get('/hotel/reservations', {
    headers: {
      Authorization: `Token ${token.token}`
    }
  }).then(response => {
    reservations.value = response.data
  }).catch(error => {
    console.log(error);
  })
}

function isRoomFree(room) {
  const today = new Date().toISOString().split("T")[0];
  return !reservations.value.some((reservation) =>
      reservation.room.id === room.id &&
      reservation.admin &&
      today >= reservation.arrival_date &&
      today <= reservation.departure_date
  );
}


const filteredRooms = computed(() =>
    showOnlyFree.value ? rooms.value.filter((room) => isRoomFree(room))
        :
        rooms.value)

onMounted(async () => {
  isLoading.value = true
  await Promise.all([fetchRooms(), fetchReservations()])
  isLoading.value = false
})
</script>

<template>
  <v-app>
  <v-container>
    <template v-if="isLoading">
      <v-skeleton-loader
          type="card, card, card"
          class="mt-4"
          max-width="500"
      />
    </template>
    <template v-else>
      <h2>Список комнат</h2>
      <v-checkbox
          v-model="showOnlyFree"
          label="Только свободные комнаты"
      />
      <RoomList :rooms="filteredRooms" :isRoomFree="isRoomFree"/>
    </template>
  </v-container>
</v-app>
</template>

<style scoped>

</style>