<script setup>
import {onMounted, ref} from "vue";
import axios from "axios";
import BookingModal from "@/components/BookingModal.vue";
import BookingList from "@/components/BookingList.vue";
import {tokenStore} from "@/stores/token.js";

const token = tokenStore();
const bookings = ref([]);
const clients = ref([]);
const rooms = ref([]);
const isModalVisible = ref(false);
const selectedBooking = ref(null);
const isLoading = ref(true);

async function fetchBookings() {
  await axios.get("/hotel/reservations", {
    headers: {Authorization: `Token ${token.token}`},
  }).then((response) => {
    if (response.status === 200) {
      bookings.value = response.data;
      console.log(bookings.value)
      isLoading.value = false
    }
  }).catch((error) => {
    console.log(error);
  });
}

async function fetchClients() {
  await axios.get("/hotel/clients", {
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
  await axios.get("/hotel/rooms", {
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
    await axios.put(`/hotel/reservations/${booking.id}/update`, booking, {
      headers: {Authorization: `Token ${token.token}`},
    }).catch((error) => {
      console.log(error);
    });
  } else { 
    console.log(booking)
    await axios.post("/hotel/reservations", booking, {
      headers: {Authorization: `Token ${token.token}`},
    }).catch((error) => {
      console.log(error);
    });
  }
  await fetchBookings();
  isModalVisible.value = false;
}

async function deleteBooking(id) {
  try {
    await axios.delete(`/hotel/reservations/${id}`, {
      headers: {Authorization: `Token ${token.token}`},
    });
    await fetchBookings();
  } catch (error) {
    console.error("Ошибка при удалении бронирования:", error);
  }
}

async function confirmBooking(id) {
  const user = await getUser();
  await axios.patch(`/hotel/reservations/${id}/update`, {admin: user.id}, {
    headers: {Authorization: `Token ${token.token}`},
  })
  await fetchBookings()
}

async function getUser() {
  return axios.get('/auth/users/me/', {
    headers: {
      Authorization: `Token ${token.token}`
    }
  }).then(response => response.data);
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
          @confirm-booking="confirmBooking"
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
