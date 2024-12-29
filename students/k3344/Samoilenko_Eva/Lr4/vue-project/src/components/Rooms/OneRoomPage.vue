<script setup>
import {onMounted, ref} from "vue";
import instance from "@/AxiosInstance";
import router from "@/router/index.js";

const form = ref({
  room_type: "",
  price: "",
  floor_num: "",
  phone_num: "",
})

const room_type_choices = [
  'Single',
  'Double',
  'Triple'
]

function getPage() {
  instance.get(`/hotel/rooms/${router.currentRoute.value.params.id}/`)
    .then(response => {
        if (response.status === 200) {
          form.value = response.data
        }
      }
    ).catch(error => console.log(error))
}

function savePage() {
  const {id, ...rest} = form.value
  instance.patch(`/hotel/rooms/${router.currentRoute.value.params.id}/`, rest)
    .then(response => {
        if (response.status === 200) {
          router.push('/rooms')
        }
      }
    ).catch(error => console.log(error))
}

onMounted(() => {
  getPage()
})

</script>

<template>
  <div v-if="router.currentRoute.value.params.id === 'undefined'">No such room given.</div>
  <div v-else class="container">
    <div class="form-container">
      <h1>Hotel Room</h1>
      <v-select label="Room Type" :items="room_type_choices" v-model="form.room_type"></v-select>
      <v-text-field label="Price" v-model="form.price"></v-text-field>
      <v-text-field label="Phone Number" v-model="form.phone_num"></v-text-field>
      <v-radio-group
        v-model="form.floor_num"
        inline
        label="Floor Number"
      >
        <v-radio label="0" :value="0"></v-radio>
        <v-radio label="1" :value="1"></v-radio>
        <v-radio label="2" :value="2"></v-radio>
        <v-radio label="3" :value="3"></v-radio>
        <v-radio label="4" :value="4"></v-radio>
      </v-radio-group>
      <v-btn @click="savePage" color="green">Save</v-btn>
    </div>
  </div>
</template>

<style scoped>

</style>
