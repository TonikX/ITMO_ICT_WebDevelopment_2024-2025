<script setup>
import axios from "axios";
import {computed, onMounted, ref} from "vue";
import RoomList from "@/components/RoomList.vue";

const rooms = ref([])
const showOnlySpecial = ref(false)
const isLoading = ref(true)

async function fetchRooms() {
  await axios.get('/school/rooms').then(response => {
    rooms.value = response.data
  }).catch(error => {
    console.log(error);
  })
}

function isRoomSpecial(room) {
  return room.subject
}

const filteredRooms = computed(() =>
    showOnlySpecial.value ? rooms.value.filter((room) => room.subject)
        :
        rooms.value)

onMounted(async () => {
  isLoading.value = true
  await fetchRooms()
  isLoading.value = false
})
</script>

<template>
  <v-container>
    <template v-if="isLoading">
      <v-skeleton-loader
          type="card, card, card"
          class="mt-4"
          max-width="500"
      />
    </template>
    <template v-else>
      <h2>Список кабинетов</h2>
      <v-checkbox
          v-model="showOnlySpecial"
          label="Только специализированные кабинеты"
      />
      <RoomList :rooms="filteredRooms" :isRoomSpecial="isRoomSpecial"/>
    </template>
  </v-container>
</template>

<style scoped>

</style>