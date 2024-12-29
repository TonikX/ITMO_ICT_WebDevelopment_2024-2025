<script setup>
import {onMounted, ref} from "vue";
import instance from "@/AxiosInstance";
import router from "@/router/index.js";

const form = ref({
  client: "",
  room: "",
  start_date: "",
  end_date: "",
  is_verified: ""
})

const room_select = ref([])
const client_select = ref([])

function createForm() {
  instance.get('hotel/rooms/').then(response => {
      if (response.status === 200) {
        room_select.value = response.data
      }
    }
  ).catch(error => console.log(error))

  instance.get('hotel/clients/').then(response => {
      if (response.status === 200) {
        client_select.value = response.data
      }
    }
  ).catch(error => console.log(error))
}

function createBooking() {
  instance.post('/hotel/bookings/', form.value)
    .then(response => {
        if (response.status === 201) {
          router.push('/bookings')
        }
      }
    ).catch(error => console.log(error))
}

const getCustomRoomTitle = (room) => {
  return `${room.room_type} on Floor ${room.floor_num}`;
};

const getCustomClientTitle = (client) => {
  return `${client.first_name} ${client.last_name}`;
};

onMounted(() => {
  createForm()
})

</script>

<template>
  <div class="container">
    <div class="form-container">
      <h1>Create Hotel Booking</h1>
      <v-select label="Room" :items="room_select"
                :item-title="getCustomRoomTitle" item-value="id"
                v-model="form.room"></v-select>
      <v-select label="Client" :items="client_select"
                :item-title="getCustomClientTitle" item-value="id"
                v-model="form.client"></v-select>
      <v-text-field label="Start Date" v-model="form.start_date"></v-text-field>
      <v-text-field label="End Date" v-model="form.end_date"></v-text-field>
      <v-switch v-model="form.is_verified" :label="`Verified: ${form.is_verified}`"></v-switch>
      <v-btn @click="createBooking" color="green">Create</v-btn>
    </div>
  </div>
</template>

<style>

</style>
