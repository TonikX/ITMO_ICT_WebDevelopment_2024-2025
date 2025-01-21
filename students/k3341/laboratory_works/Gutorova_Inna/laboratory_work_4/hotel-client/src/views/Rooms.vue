<template>
  <v-container>
    <!-- Форма для выбора дат -->
    <v-row>
      <v-col>
        <v-text-field
          label="Дата заезда"
          type="date"
          v-model="checkInDate"
        ></v-text-field>
      </v-col>
      <v-col>
        <v-text-field
          label="Дата выезда"
          type="date"
          v-model="checkOutDate"
        ></v-text-field>
      </v-col>
    </v-row>

    <BookingModal
          v-model="isModalVisible"
          :booking="selectedBooking"
          :rooms="rooms"
          :clients="clients"
          @save-booking="saveBooking"
      />
    <!-- Список номеров -->
    <v-row>
      <v-col v-for="room in filteredRooms" :key="room.id" cols="12" md="4">
        <v-card>
          <v-card-title>{{ room.number }} - {{ getRoomType(room.room_type) }}</v-card-title>
          <v-card-subtitle>{{ room.price_per_day }} ₽/сутки</v-card-subtitle>
          <v-card-actions>
            <v-btn @click="handleAddBooking()">
              Забронировать
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup>
import { ref, computed, watchEffect } from "vue";
import axios from "axios";
import BookingModal from "@/components/StayrecordModal.vue";

const isModalVisible = ref(false);
const selectedBooking = ref(null);
const checkInDate = ref("");
const checkOutDate = ref("");
const onlyAvailable = ref(false);
const rooms = ref([]);
const clients = ref([]);
import {tokenStore} from "@/stores/token.js";

const token = tokenStore();

const filteredRooms = computed(() => {
  // Фильтрация номеров по доступности и выбранным датам
  return rooms.value.filter((room) => {
    // Если требуется только свободные номера, проверяем их на наличие бронирований
    const isAvailable =
      !onlyAvailable.value ||
      (room.stay_records && room.stay_records.every((record) => {
        // Проверяем, не перекрываются ли записи с выбранными датами
        return !(checkInDate.value && checkOutDate.value &&
          ((record.check_in_date < checkOutDate.value && record.check_out_date > checkInDate.value)));
      }));

    return isAvailable;
  });
});

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


function getRoomType(type) {
    const types = {
        single: "Одиночная",
        double: "Двухместная",
        triple: "Трёхместная"
    }
    return types[type] || "Unknown";
}

// Получение списка номеров
const fetchRooms = async () => {
  try {
    const response = await axios.get("/api/rooms/", {
    headers: {Authorization: `Token ${token.token}`},
  }); // Получаем все номера
    rooms.value = response.data;
  } catch (error) {
    console.error("Ошибка при загрузке номеров", error);
  }
};

// Получение списка свободных номеров для выбранных дат
const fetchAvailableRooms = async () => {
  if (checkInDate.value && checkOutDate.value) {
    try {
      const response = await axios.get("/api/available/", {
        params: {
          check_in_date: checkInDate.value,
          check_out_date: checkOutDate.value,
        },
      });
      rooms.value = response.data;
    } catch (error) {
      console.error("Ошибка при загрузке свободных номеров", error);
    }
  }
};

// Проверка изменений в датах и загрузка данных
watchEffect(() => {
  if (checkInDate.value && checkOutDate.value) {
    fetchAvailableRooms();
  } else {
    fetchRooms();
  }
});

function handleAddBooking() {
  selectedBooking.value = null;
  selectedBooking.value.room = room;
  isModalVisible.value = true;
  fetchClients();
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

fetchRooms(); // Загружаем номера при инициализации компонента
</script>

<style scoped>
.v-card {
  margin-bottom: 16px;
}
</style>
