<template>
  <v-container>
    <h1 class="text-center">Список номеров</h1>
    <v-divider class="my-4"></v-divider>

    <v-data-table
      :headers="headers"
      :items="rooms"
      class="elevation-1"
      dense
    >
      <template v-slot:top>
        <v-toolbar flat>
          <v-toolbar-title>Номера</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="fetchRooms">Обновить</v-btn>
        </v-toolbar>
      </template>

      <template v-slot:item.is_occupied="{ item }">
        <v-chip :color="item.is_occupied ? 'red' : 'green'" dark>
          {{ item.is_occupied ? "Занят" : "Свободен" }}
        </v-chip>
      </template>
      <template #item.actions="{ item }">
        <v-btn variant="text" @click="navigateToRoomInfo(item.id)" icon="mdi-information-outline"/>
      </template>
    </v-data-table>
  </v-container>
</template>

<script lang="ts">
import type Room from "@/models/room";
import axiosApi from "@/plugins/axios";
import router from "@/router";
import { defineComponent, ref, onMounted } from "vue";

export default defineComponent({
  name: "RoomsPage",
  setup() {
    const rooms = ref([] as Room[]);
    const headers = ref([
      { title: "ID", value: "id" },
      { title: "Номер", value: "number" },
      { title: "Этаж", value: "floor" },
      { title: "Тип", value: "type" },
      { title: "Цена за день", value: "price_per_day" },
      { title: "Телефон", value: "phone" },
      { title: "Статус", value: "is_occupied" },
      { title: 'Действия', value: 'actions', sortable: false },
    ]);

    const fetchRooms = async () => {
      try {
        const response = await axiosApi.get("/rooms");
        rooms.value = response.data;
      } catch (error) {
        console.error("Ошибка при загрузке списка номеров:", error);
      }
    };

    const navigateToRoomInfo = (roomId: number) => {
      router.push(`/rooms/${roomId}`);
    };

    onMounted(fetchRooms);

    return {
      rooms,
      headers,
      fetchRooms,
      navigateToRoomInfo
    };
  },
});
</script>

<style scoped>
.text-center {
  text-align: center;
}
</style>
