<template>
  <v-container>
    <h1 class="text-center">История бронирований</h1>
    <v-divider class="my-4"></v-divider>
    <v-row v-if="reservations.length">
      <v-col cols="12">
        <v-data-table
          v-if="reservations.length"
          :headers="reservationHeaders"
          :items="reservations"
          item-key="id"
          class="elevation-1"
        >
        </v-data-table>
      </v-col>
    </v-row>
    <v-row v-else>
      <v-col cols="12">
        Нет бронирований для отображения.
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import type Reservation from '@/models/reservation';
import axiosApi from '@/plugins/axios';
import { defineComponent, ref, onMounted } from 'vue';

export default defineComponent({
  setup() {
    const reservations = ref([] as Reservation[]);
    const reservationHeaders = [
      { title: 'Имя клиента', value: 'client_name' },
      { title: 'Номер комнаты', value: 'room_number' },
      { title: 'Дата заезда', value: 'check_in_date' },
      { title: 'Дата выезда', value: 'check_out_date' },
    ];

    const fetchReservations = async () => {
      try {
        const response = await axiosApi.get('/reservations');
        reservations.value = response.data;
      } catch (error) {
        console.error('Ошибка при загрузке бронирований:', error);
      }
    };

    const formatDate = (date: string | null): string => {
      if (!date) return '';
      const d = new Date(date);
      return d.toLocaleDateString('ru-RU');
    };

    onMounted(() => {
      fetchReservations();
    });

    return {
      reservations,
      reservationHeaders,
      formatDate,
    };
  },
});
</script>

<style scoped>
.v-container {
  padding-top: 20px;
}
</style>
