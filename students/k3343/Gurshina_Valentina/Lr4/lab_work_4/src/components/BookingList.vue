<script setup>
import {computed} from "vue";

const props = defineProps({
  bookings: Array,
});

defineEmits(["edit-booking", "delete-booking", "confirm-booking"]);

console.log(props.bookings)
const pendingBookings = computed(() => props.bookings.filter((b) => !b.admin));
const confirmedBookings = computed(() => props.bookings.filter((b) => b.admin));
</script>

<template>
  <h3>Требуют подтверждения</h3>
  <div v-if="pendingBookings.length">
    <v-card
        v-for="booking in pendingBookings"
        :key="booking.id"
        class="mb-4 pending-booking"
    >
      <v-card-title>
        Резервирование №{{ booking.id }} (Ожидается подтверждение)
      </v-card-title>
      <v-card-text>
        Гость: {{ booking.client.full_name }}<br />
        Комната: {{ booking.room.id }}<br />
        Даты: {{ booking.arrival_date }} - {{ booking.departure_date }}
      </v-card-text>
      <v-card-actions>
        <v-btn color="green" @click="$emit('confirm-booking', booking.id)">Подтвердить</v-btn>
        <v-btn color="primary" @click="$emit('edit-booking', booking)">Изменить</v-btn>
        <v-btn color="error" @click="$emit('delete-booking', booking.id)">Удалить</v-btn>
      </v-card-actions>
    </v-card>
  </div>
  <div v-else>
    <p>Нет бронирований, требующих подтверждения.</p>
  </div>

  <h3>Подтвержденные бронирования</h3>
  <div v-if="confirmedBookings.length">
    <v-card
        v-for="booking in confirmedBookings"
        :key="booking.id"
        class="mb-4 confirmed-booking"
    >
      <v-card-title>
        Резервирование №{{ booking.id }}
      </v-card-title>
      <v-card-text>
        Гость: {{ booking.client.full_name }}<br />
        Комната: {{ booking.room.id }}<br />
        Даты: {{ booking.arrival_date }} - {{ booking.departure_date }} <br />
        Работник: {{ booking.admin.username }}
      </v-card-text>
      <v-card-actions>
        <v-btn color="primary" @click="$emit('edit-booking', booking)">Изменить</v-btn>
        <v-btn color="error" @click="$emit('delete-booking', booking.id)">Удалить</v-btn>
      </v-card-actions>
    </v-card>
  </div>
  <div v-else>
    <p>Нет подтвержденных бронирований.</p>
  </div>
</template>

<style scoped>
.pending-booking {
  background-color: #fff3cd;
  border: 1px solid #ffeeba;
}

.confirmed-booking {
  background-color: #d4edda;
  border: 1px solid #c3e6cb;
}
</style>
