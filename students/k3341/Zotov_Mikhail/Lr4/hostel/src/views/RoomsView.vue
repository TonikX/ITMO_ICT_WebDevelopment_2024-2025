<template>
  <v-container>
    <v-card>
      <v-card-title class="text-h5 font-weight-bold">Доступные комнаты</v-card-title>
      <v-card-text>
        <v-text-field
          label="Количество клиентов"
          v-model="countOfClients"
          type="number"
          class="mb-3"
        ></v-text-field>
        <v-btn color="primary" @click="fetchRooms">Найти</v-btn>
      </v-card-text>
    </v-card>

    <v-card class="mt-4">
      <v-data-table
        :headers="headers"
        :items="formattedRooms"
        class="elevation-1"
        dense
        item-value="number"
      >
        <template v-slot:top>
          <v-toolbar flat>
            <v-toolbar-title>Список комнат</v-toolbar-title>
          </v-toolbar>
        </template>

        <template v-slot:item.room_type="{ item }">
          {{ formatRoomType(item.room_type) }}
        </template>
      </v-data-table>
    </v-card>
  </v-container>
</template>

<script>
import axios from 'axios'

export default {
  name: 'Rooms',
  data() {
    return {
      rooms: [],
      countOfClients: 1,
      headers: [
        { title: 'Номер комнаты', value: 'number', sortable: true },
        { title: 'Этаж', value: 'floor', sortable: true },
        { title: 'Тип', value: 'room_type', sortable: true },
        { title: 'Цена за день', value: 'price_per_day', sortable: true },
        { title: 'Телефон', value: 'phone', sortable: false },
      ],
    }
  },
  computed: {
    formattedRooms() {
      if (!Array.isArray(this.rooms)) {
        console.error('Ошибка: rooms не является массивом', this.rooms);
        return [];
      }
      return this.rooms.map(room => ({
        id: room.id,
        number: room.number,
        floor: room.floor?.number || 'Неизвестно',
        room_type: room.room_type,
        price_per_day: room.price_per_day,
        phone: room.phone
      }));
    }
  },
  methods: {
    async fetchRooms() {
      try {
        const response = await axios.get(`http://localhost:8000/api/rooms/?count_of_clients=${this.countOfClients}`);
        console.log('Полученные комнаты:', response.data);
        if (!Array.isArray(response.data)) {
          console.error('Ошибка: API вернуло не массив', response.data);
          return;
        }
        this.rooms = response.data;
      } catch (error) {
        console.error('Ошибка при загрузке комнат:', error);
      }
    },
    formatRoomType(value) {
      const types = {
        double: 'Двухместный',
        triple: 'Трехместный',
        single: 'Одноместный'
      };
      return types[value] || 'Неизвестно';
    }
  },
  created() {
    this.fetchRooms();
  },
}
</script>
