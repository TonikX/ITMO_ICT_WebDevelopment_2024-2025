<template>
  <v-container>
    <v-row>
      <v-col>
        <h1>Проживания</h1>
        <v-btn @click="openDialog" color="primary">Добавить проживание</v-btn>
      </v-col>
    </v-row>

    <v-data-table :headers="headers" :items="stays" :loading="loading"> </v-data-table>

    <v-dialog v-model="dialogCreate" max-width="500">
      <v-card>
        <v-card-title>Новое проживание</v-card-title>
        <v-card-text>
          <v-form>
            <v-select
              v-model="newStay.client"
              :items="clients"
              item-title="full_name"
              item-value="id"
              label="Клиент"
            ></v-select>
            <v-select
              v-model="newStay.room"
              :items="rooms"
              item-title="id"
              item-value="id"
              label="Номер"
              ><template v-slot:item="{ props, item }">
                <v-list-item v-bind="props" :title="`Комната ID: ${item.raw.id}`"></v-list-item>
              </template> </v-select
            ><v-text-field
              v-model="newStay.check_in"
              label="Дата заселения"
              type="date"
            ></v-text-field>
            <v-text-field
              v-model="newStay.check_out"
              label="Дата выселения"
              type="date"
            ></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-btn @click="createStay" color="primary">Создать</v-btn>
          <v-btn @click="dialogCreate = false">Отмена</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import api from '@/services/api'

const stays = ref([])
const clients = ref([])
const rooms = ref([])
const loading = ref(false)
const dialogCreate = ref(false)

const newStay = ref({
  client: null,
  room: null,
  check_in: '',
  check_out: '',
})

const headers = [
  { title: 'ID', key: 'id' },
  { title: 'Клиент', key: 'client_name' },
  { title: 'Номер', key: 'room_number' },
  { title: 'Заселение', key: 'check_in' },
  { title: 'Выселение', key: 'check_out' },
]

const loadStays = async () => {
  loading.value = true
  try {
    const response = await api.getStays()
    stays.value = response.data
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

const loadClients = async () => {
  try {
    const response = await api.getClients()
    console.log('Клиенты:', response.data)
    clients.value = response.data.map((c) => ({
      id: c.id,
      full_name: `${c.last_name} ${c.first_name} (ID: ${c.id})`,
    }))
  } catch (error) {
    console.error(error)
  }
}

const loadRooms = async () => {
  try {
    const response = await api.getRooms()
    console.log('Номера:', response.data)
    rooms.value = response.data
  } catch (error) {
    console.error(error)
  }
}

const openDialog = () => {
  loadClients()
  loadRooms()
  dialogCreate.value = true
}

const createStay = async () => {
  try {
    const data = {
      client: Number(newStay.value.client),
      room: Number(newStay.value.room),
      check_in: newStay.value.check_in,
      check_out: newStay.value.check_out,
    }
    await api.createStay(data)
    console.log('Отправляемые данные:', data)

    dialogCreate.value = false
    newStay.value = { client: null, room: null, check_in: '', check_out: '' }
    loadStays()
  } catch (error) {
    console.error(error)
    alert('Ошибка: ' + JSON.stringify(error.response?.data))
  }
}

onMounted(() => {
  loadStays()
})
</script>
