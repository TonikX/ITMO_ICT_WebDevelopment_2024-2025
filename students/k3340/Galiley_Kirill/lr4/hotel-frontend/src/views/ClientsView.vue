<template>
  <v-container>
    <v-row>
      <v-col>
        <h1>Клиенты</h1>
        <v-btn @click="dialogCreate = true" color="primary">Добавить клиента</v-btn>
      </v-col>
    </v-row>

    <v-row>
      <v-col>
        <v-text-field
          v-model="filterCity"
          label="Фильтр по городу"
          @input="loadClients"
          clearable
        ></v-text-field>
      </v-col>
    </v-row>

    <v-data-table
      :headers="headers"
      :items="clients"
      :loading="loading"
    >
    </v-data-table>

    <v-dialog v-model="dialogCreate" max-width="500">
      <v-card>
        <v-card-title>Новый клиент</v-card-title>
        <v-card-text>
          <v-form>
            <v-text-field v-model="newClient.passport" label="Паспорт"></v-text-field>
            <v-text-field v-model="newClient.last_name" label="Фамилия"></v-text-field>
            <v-text-field v-model="newClient.first_name" label="Имя"></v-text-field>
            <v-text-field v-model="newClient.patronymic" label="Отчество"></v-text-field>
            <v-text-field v-model="newClient.city" label="Город"></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-btn @click="createClient" color="primary">Создать</v-btn>
          <v-btn @click="dialogCreate = false">Отмена</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import api from '@/services/api'

const clients = ref([])
const loading = ref(false)
const dialogCreate = ref(false)
const filterCity = ref('')

const newClient = ref({
  passport: '',
  last_name: '',
  first_name: '',
  patronymic: '',
  city: ''
})

const headers = [
  { title: 'ID', key: 'id' },
  { title: 'Паспорт', key: 'passport' },
  { title: 'Фамилия', key: 'last_name' },
  { title: 'Имя', key: 'first_name' },
  { title: 'Отчество', key: 'patronymic' },
  { title: 'Город', key: 'city' },
]

const loadClients = async () => {
  loading.value = true
  try {
    const params = filterCity.value ? { city: filterCity.value } : {}
    const response = await api.getClients(params)
    clients.value = response.data
  } catch (error) {
    console.error(error)
  } finally {
    loading.value = false
  }
}

const createClient = async () => {
  try {
    await api.createClient(newClient.value)
    dialogCreate.value = false
    newClient.value = { passport: '', last_name: '', first_name: '', patronymic: '', city: '' }
    loadClients()
  } catch (error) {
    console.error(error)
  }
}

onMounted(() => {
  loadClients()
})
</script>