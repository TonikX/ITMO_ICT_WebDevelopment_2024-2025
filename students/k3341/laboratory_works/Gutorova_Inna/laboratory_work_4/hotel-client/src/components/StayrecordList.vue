<script setup>
import { ref, onMounted } from "vue";
import axios from "axios";
import { tokenStore } from "@/stores/token.js";

const tokenStorage = tokenStore();

const stayRecords = ref([]); // Список ID записей о проживании
const bookingDetails = ref([]); // Детали бронирований

async function fetchStayRecords() {
  try {
    // Запрос списка ID StayRecord
    const response = await axios.get("/api/stayrecords/", {
      headers: { Authorization: `Token ${tokenStorage.token}` },
    });
    stayRecords.value = response.data;

    // По каждому ID StayRecord запрашиваем детали бронирования
    const detailsPromises = stayRecords.value.map((record) =>
      axios
        .get(`/api/booking/${record.id}/`, {
          headers: { Authorization: `Token ${tokenStorage.token}` },
        })
        .then((res) => res.data) // Берем только данные из ответа
        .catch((err) => {
          console.error(`Ошибка загрузки данных для записи ${record.id}:`, err);
          return null; // Игнорируем ошибочные записи
        })
    );

    // Ждем завершения всех запросов
    const detailsResponses = await Promise.all(detailsPromises);

    // Фильтруем только успешные результаты
    bookingDetails.value = detailsResponses.filter((data) => data !== null);
  } catch (error) {
    console.error("Ошибка при загрузке данных:", error);
  }
}

onMounted(() => {
  fetchStayRecords();
});
</script>

<template>
  <h3>Бронирования</h3>
  <div v-if="bookingDetails.length">
    <v-card
      v-for="booking in bookingDetails"
      :key="booking.id"
      class="mb-4 booking-card"
    >
      <v-card-title>
        Бронирование №{{ booking.id }}
      </v-card-title>
      <v-card-text>
        Клиент: {{ booking.client_full_name }}<br />
        Комната: {{ booking.room_number }}<br />
        Даты: {{ booking.check_in_date }} - {{ booking.check_out_date }}<br />
      </v-card-text>
      <v-card-actions>
        <v-btn color="primary" @click="$emit('edit-booking', booking)">Редактировать</v-btn>
        <v-btn color="error" @click="$emit('delete-booking', booking.id)">Удалить</v-btn>
      </v-card-actions>
    </v-card>
  </div>
  <div v-else>
    <p>Нет бронирований.</p>
  </div>
</template>

<style scoped>
.booking-card {
  margin-bottom: 16px;
  background-color: #f8f9fa;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}
</style>
