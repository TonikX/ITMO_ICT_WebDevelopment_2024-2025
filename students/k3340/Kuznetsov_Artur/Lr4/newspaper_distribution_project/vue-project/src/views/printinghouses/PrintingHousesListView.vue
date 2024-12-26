<script setup>
import { ref, onMounted, computed } from 'vue'
import axiosClient from '@/services/axiosClient'
import { userStore } from '@/stores/userStore'
import CreatePrintingHouseDialog from '@/components/printinghouses/CreatePrintingHouseDialog.vue'

const store = userStore()

const printingHouses = ref([])
const createDialog = ref(false)

const isAdmin = computed(() => store.user?.role === 'admin')

async function fetchPrintingHouses() {
  try {
    const response = await axiosClient.get('/printinghouses/')
    printingHouses.value = response.data
  } catch (error) {
    console.error('Ошибка загрузки типографий:', error)
  }
}

function openCreateDialog() {
  createDialog.value = true
}

function onPrintingHouseCreated() {
  fetchPrintingHouses()
}

onMounted(fetchPrintingHouses)
</script>

<template>
  <v-container>
    <v-card class="pa-4">
      <v-card-title class="d-flex justify-space-between">
        <span>Список типографий</span>
        <v-btn color="primary" v-if="isAdmin" @click="openCreateDialog">
          Добавить типографию
        </v-btn>
      </v-card-title>
      <v-card-text>
        <v-list>
          <v-list-item
            v-for="printingHouse in printingHouses"
            :key="printingHouse.id"
            :to="`/printinghouses/${printingHouse.id}`"
          >
            <v-list-item-content>
              <v-list-item-title>{{ printingHouse.name }}</v-list-item-title>
              <v-list-item-subtitle>
                Адрес: {{ printingHouse.address }} | Статус: {{ printingHouse.is_active ? 'Активна' : 'Закрыта' }}
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-card-text>
    </v-card>

    <CreatePrintingHouseDialog
      v-model="createDialog"
      @printinghouse-created="onPrintingHouseCreated"
    />
  </v-container>
</template>

<style scoped>
</style>
