<script setup>
import {onMounted, ref} from "vue";
import instance from "@/AxiosInstance";
import router from "@/router/index.js";

const bookings = ref([])

function getBookings() {
  instance.get('/hotel/bookings/').then(
    response => {
      if (response.status === 200) {
        bookings.value = response.data
      }
    }
  ).catch(error => console.log(error))
}

function deleteBooking(id) {
  if (confirm("Are you sure you want to delete this booking?")) {
    instance.delete(`/hotel/bookings/${id}/`).then(response => {
        if (response.status === 204) {
          getBookings()
        }
      }
    ).catch(error => console.log(error))
  } else {
    console.log("Booking deletion cancelled.");
  }
}

onMounted(() => {
  getBookings()
})
</script>

<template>
  <div class="d-flex align-center flex-column ga-10">
    <div align="center">
      <h1>Hotel Bookings</h1>
      <div class="button-group">
        <v-btn class="styled-btn" color="green" @click="router.push('/bookings/add')" block>
          Add
        </v-btn>
        <v-btn class="styled-btn" color="blue" @click="router.push('/bookings/sort')" block>
          Sort
        </v-btn>
      </div>
    </div>

    <div v-if="bookings.length === 0">Loading bookings...</div>

    <v-container min-width="1000">
      <v-row>
        <v-col
          v-for="booking in bookings"
          :key="booking.id"
          cols="12"
          md="6"
        >
          <v-card width="100%">
            <v-card-title class="wrapped-title">
              Booking for {{ booking.client.first_name }} {{ booking.client.last_name }}
              in Room {{ booking.room.room_type }} on Floor {{ booking.room.floor_num }}
            </v-card-title>
            <v-card-item>Start Date: {{ booking.start_date }}</v-card-item>
            <v-card-item>End Date: {{ booking.end_date }}</v-card-item>
            <v-card-item v-if="booking.is_verified">
              <p style="color: green">Is verified</p></v-card-item>
            <v-card-item v-if="!booking.is_verified">
              <p style="color: red">Is not verified</p>
            </v-card-item>
            <v-card-actions>
              <v-btn color="blue" @click="router.push('/bookings/' + booking.id)">
                Edit
              </v-btn>
              <v-btn color="red" @click="deleteBooking(booking.id)">
                Terminate
              </v-btn>
            </v-card-actions>
          </v-card>
        </v-col>
      </v-row>
    </v-container>
  </div>
</template>

<style scoped>
h1 {
  margin-top: 50px;
}

.button-group {
  display: flex;
  gap: 20px;
  justify-content: center;
  margin-top: 10px;
}

.styled-btn {
  width: 50px;
  height: 50px;
  font-size: 15px;
  font-weight: bold;
  border-radius: 8px;
  text-transform: uppercase;
}

.wrapped-title {
  white-space: normal; /* Allows text to wrap */
  word-wrap: break-word; /* Ensures words break properly */
  overflow-wrap: anywhere; /* Modern approach for breaking long words */
}
</style>
