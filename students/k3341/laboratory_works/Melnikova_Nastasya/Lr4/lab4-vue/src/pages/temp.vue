<template>
  <v-container>
    <v-card class="pa-4">
      <v-card-title class="text-h5">
        Free Rooms
      </v-card-title>

      <v-card-actions>
        <v-btn color="success" @click="loadFreeRooms">
          Load Free Rooms
        </v-btn>
      </v-card-actions>

      <v-row class="mt-4">
        <v-col cols="12" md="4" v-for="room in rooms" :key="room.id">
          <v-card>
            <v-card-title>
              Room {{ room.number }}
            </v-card-title>

            <v-card-text>
              Floor: {{ room.floor }} <br>
              Type: {{ room.room_type }} <br>
              Price: {{ room.price_per_day }}
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref } from "vue"
import { roomsApi } from "../api/rooms"

const rooms = ref([])

async function loadFreeRooms() {
  const res = await roomsApi.free()
  rooms.value = res.data
}
</script>
