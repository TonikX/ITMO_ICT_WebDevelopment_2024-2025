<template>
  <v-container>
    <v-row justify="center" align="center">
      <v-col cols="14" md="10">
        <h1 class="text-center">Добро пожаловать в систему управления гостиницей</h1>
        <v-divider class="my-4"></v-divider>
        <v-row>
          <v-col cols="12" md="4">
            <v-card height="150">
              <v-card-title>Сотрудники</v-card-title>
              <v-card-subtitle>Всего сотрудников: {{ staffCount }}</v-card-subtitle>
              <v-card-actions>
                <v-btn color="primary" @click="navigateTo('staff')">Перейти</v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
          <v-col cols="12" md="4">
            <v-card height="150">
              <v-card-title>Клиенты</v-card-title>
              <v-card-subtitle>Всего клиентов: {{ clientCount }}</v-card-subtitle>
              <v-card-actions>
                <v-btn color="primary" @click="navigateTo('clients')">Перейти</v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
          <v-col cols="12" md="4">
            <v-card height="150">
              <v-card-title>Комнаты</v-card-title>
              <v-card-subtitle>Всего комнат: {{ roomCount }}</v-card-subtitle>

              <v-card-subtitle>Свободно комнат: {{ freeRoomCount }}</v-card-subtitle>
              <v-card-actions>
                <v-btn color="primary" @click="navigateTo('rooms')">Перейти</v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
          <v-col cols="12" md="4">
            <v-card height="150">
              <v-card-title>Расписание уборки</v-card-title>
              <v-card-actions>
                <v-btn color="primary" @click="navigateTo('cleaning-schedule')">Перейти</v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
          <v-col cols="12" md="4">
            <v-card height="150">
              <v-card-title>История бронирований</v-card-title>
              <v-card-actions>
                <v-btn color="primary" @click="navigateTo('reservations')">Перейти</v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
          <v-col cols="12" md="4">
            <v-card height="150">
              <v-card-title>Отчёт об отеле</v-card-title>
              <v-card-actions>
                <v-btn color="primary" @click="navigateTo('report')">Перейти</v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import type Room from "@/models/room";
import axiosApi from "@/plugins/axios";
import { defineComponent, ref, onMounted } from "vue";

export default defineComponent({
  name: "HomePage",
  setup() {
    const staffCount = ref(0);
    const clientCount = ref(0);
    const freeRoomCount = ref(0);
    const roomCount = ref(0);

    const fetchData = async () => {
      try {
        const [staffRes, clientRes, roomRes] = await Promise.all([
          axiosApi.get("staff/"),
          axiosApi.get("clients/"),
          axiosApi.get("rooms/"),
        ]);
        staffCount.value = staffRes.data.length;
        clientCount.value = clientRes.data.length;
        roomCount.value = roomRes.data.length;
        freeRoomCount.value = roomRes.data.filter((room: Room) => !room.is_occupied).length;
      } catch (error) {
        console.error("Ошибка при загрузке данных:", error);
      }
    };

    onMounted(fetchData);

    const navigateTo = (route: string) => {
      window.location.href = `/${route}`;
    };

    return {
      staffCount,
      clientCount,
      roomCount,
      freeRoomCount,
      navigateTo,
    };
  },
});
</script>

<style scoped>
.text-center {
  text-align: center;
}
</style>
