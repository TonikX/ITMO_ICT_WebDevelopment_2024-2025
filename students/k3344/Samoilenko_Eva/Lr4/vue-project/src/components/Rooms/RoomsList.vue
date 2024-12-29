<script setup>
import {onMounted, ref} from "vue";
import instance from "@/AxiosInstance";
import router from "@/router/index.js";

const rooms = ref([])

function getRooms() {
  instance.get('/hotel/rooms/').then(
    response => {
      if (response.status === 200) {
        rooms.value = response.data
      }
    }
  ).catch(error => console.log(error))
}

function deleteRoom(id) {
  if (confirm("Are you sure you want to delete this room?")) {
    instance.delete(`/hotel/rooms/${id}/`).then(response => {
        if (response.status === 204) {
          getRooms()
        }
      }
    ).catch(error => console.log(error))
  } else {
    console.log("Room deletion cancelled.")
  }
}

onMounted(() => {
  getRooms()
})
</script>

<template>
  <div class="d-flex align-center flex-column ga-10">
    <h1>Hotel Rooms</h1>
    <div v-if="rooms.length === 0">Loading rooms...</div>
    <v-container min-width="1000">
      <v-row>
        <v-col
          v-for="room in rooms"
          :key="room.id"
          cols="auto"
          md="6"
        >
          <v-card  width="100%">
            <v-card-title>{{ room.room_type }} Room on Floor {{ room.floor_num }}</v-card-title>
            <v-card-item> Price: {{room.price}}$ </v-card-item>
            <v-card-item> Floor Number: {{room.floor_num}} </v-card-item>
            <v-card-item> Phone Number: {{room.phone_num}}</v-card-item>
            <v-card-actions>
              <v-btn color="blue" @click="router.push('/rooms/' + room.id)">
                Edit
              </v-btn>
              <v-btn color="red" @click="deleteRoom(room.id)">
                Delete
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<style>
h1{
 margin-top: 50px;
 font-weight: bold;
}
</style>
