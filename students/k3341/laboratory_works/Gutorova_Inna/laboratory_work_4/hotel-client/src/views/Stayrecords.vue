<script setup>
import {onMounted, ref} from "vue";
import axios from "axios";
import BookingModal from "@/components/StayrecordModal.vue";
import BookingList from "@/components/StayrecordList.vue";
import {tokenStore} from "@/stores/token.js";

const token = tokenStore();
const bookings = ref([]);
const clients = ref([]);
const rooms = ref([]);
const isModalVisible = ref(false);
const selectedBooking = ref(null);
const isLoading = ref(true);

async function fetchBookings() {
  await axios.get("/api/stay-records/", {
    headers: {Authorization: `Token ${token.token}`},
  }).then((response) => {
    if (response.status === 200) {
      bookings.value = response.data;
      isLoading.value = false
    }
  }).catch((error) => {
    console.log(error);
  });
}

async function fetchClients() {
  await axios.get("/api/clients/", {
    headers: {Authorization: `Token ${token.token}`},
  }).then((response) => {
    if (response.status === 200) {
      clients.value = response.data;
    }
  }).catch((error) => {
    console.log(error);
  });
}

async function fetchRooms() {
  await axios.get("/api/rooms/", {
    headers: {Authorization: `Token ${token.token}`},
  }).then((response) => {
    if (response.status === 200) {
      rooms.value = response.data;
    }
  }).catch((error) => {
    console.log(error);
  });
}

async function saveBooking(booking) {
  if (booking.id) {
    await axios.patch(`/api/stay-records/${booking.id}/`, booking, {
      headers: {Authorization: `Token ${token.token}`},
    }).catch((error) => {
      console.log(error);
    });
  } else {
    await axios.post("/api/stay-records/", booking, {
      headers: {Authorization: `Token ${token.token}`},
    })
    .catch((error) => {
      console.log(error);
    });
  }
  await fetchBookings();
  isModalVisible.value = false;
}

async function deleteBooking(id) {
  try {
    await axios.delete(`/api/stay-records/${id}/`, {
      headers: {Authorization: `Token ${token.token}`},
    });
    await fetchBookings();
  } catch (error) {
    console.error("Ошибка при удалении бронирования:", error);
  }
}


function handleEditBooking(booking) {
  selectedBooking.value = {...booking};
  isModalVisible.value = true;
}

function handleAddBooking() {
  selectedBooking.value = null;
  isModalVisible.value = true;
}

onMounted(() => {
  fetchBookings()
  fetchClients()
  fetchRooms()
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
      <h2>Список бронирований</h2>
      <v-btn
          color="primary"
          class="mb-4"
          @click="handleAddBooking"
      >
        Добавить бронирование
      </v-btn>

      <BookingList
          :bookings="bookings"
          @edit-booking="handleEditBooking"
          @delete-booking="deleteBooking"
      />

      <BookingModal
          v-model="isModalVisible"
          :booking="selectedBooking"
          :rooms="rooms"
          :clients="clients"
          @save-booking="saveBooking"
      />
    </template>
  </v-container>
</template>