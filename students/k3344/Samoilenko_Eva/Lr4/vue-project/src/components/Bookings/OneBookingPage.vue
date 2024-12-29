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

function getPage() {
  instance.get(`/hotel/bookings/${router.currentRoute.value.params.id}/`)
    .then(response => {
        if (response.status === 200) {
          form.value = response.data
        }
      }
    ).catch(error => console.log(error))

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

function savePage() {
  instance.patch(`/hotel/bookings/${router.currentRoute.value.params.id}/`,
    {client: form.value.client.id, room: form.value.room.id, start_date: form.value.start_date,
      end_date: form.value.end_date, is_verified: form.value.is_verified})
    .then(response => {
        if (response.status === 200) {
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
  getPage()
})

</script>

<template>
  <div v-if="router.currentRoute.value.params.id === 'undefined'">No such booking exists.</div>
  <div v-else class="container">
    <div class="form-container">
      <h1>Hotel Booking</h1>
      <v-select label="Room" :items="room_select"
                :item-title="getCustomRoomTitle" item-value="id"
                v-model="form.room"></v-select>
      <v-select label="Client" :items="client_select"
                :item-title="getCustomClientTitle" item-value="id"
                v-model="form.client"></v-select>
      <v-text-field label="Start Date" v-model="form.start_date"></v-text-field>
      <v-text-field label="End Date" v-model="form.end_date"></v-text-field>
      <v-switch v-model="form.is_verified" :label="`Verified: ${form.is_verified}`"></v-switch>
      <v-btn @click="savePage" color="green">Save</v-btn>
    </div>
  </div>
</template>

<style scoped>

</style>
