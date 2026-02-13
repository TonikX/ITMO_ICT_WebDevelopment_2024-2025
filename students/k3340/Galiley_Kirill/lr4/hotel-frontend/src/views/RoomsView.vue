<template>
  <v-container>
    <h1>Номера</h1>
    <v-btn @click="dialogCreate = true" color="primary">Добавить номер</v-btn>

    <v-data-table :headers="headers" :items="rooms" :loading="loading" class="mt-4"> </v-data-table>

    <v-dialog v-model="dialogCreate" max-width="500">
      <v-card>
        <v-card-title>Новый номер</v-card-title>
        <v-card-text>
          <v-form>
            <v-text-field v-model="newRoom.number" label="Номер" type="number"></v-text-field>
            <v-select
              v-model="newRoom.type"
              :items="['single', 'double', 'triple']"
              label="Тип"
            ></v-select>
            <v-text-field v-model="newRoom.floor" label="Этаж" type="number"></v-text-field>
            <v-text-field v-model="newRoom.phone" label="Телефон"></v-text-field>
            <v-text-field
              v-model="newRoom.price_per_day"
              label="Цена за сутки"
              type="number"
            ></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-btn @click="createRoom" color="primary">Создать</v-btn>
          <v-btn @click="dialogCreate = false">Отмена</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'

const rooms = ref([])
const loading = ref(false)
const dialogCreate = ref(false)

const newRoom = ref({
  number: '',
  type: 'single',
  floor: '',
  phone: '',
  price_per_day: '',
})

const headers = [
  { title: 'ID', key: 'id' },
  { title: 'Номер', key: 'number' },
  { title: 'Тип', key: 'type' },
  { title: 'Этаж', key: 'floor' },
  { title: 'Телефон', key: 'phone' },
  { title: 'Цена', key: 'price_per_day' },
]

const loadRooms = async () => {
  loading.value = true
  try {
    const response = await api.getRooms()
    rooms.value = response.data
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

const createRoom = async () => {
  try {
    await api.createRoom(newRoom.value)
    dialogCreate.value = false
    loadRooms()
  } catch (error) {
    console.error(error)
  }
}

onMounted(() => {
  loadRooms()
})
</script>
