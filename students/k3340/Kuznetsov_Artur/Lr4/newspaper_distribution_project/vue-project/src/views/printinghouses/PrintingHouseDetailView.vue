<script setup>
import {ref, computed, onMounted} from 'vue'
import {useRoute, useRouter} from 'vue-router'
import axiosClient from '@/services/axiosClient'
import {userStore} from '@/stores/userStore'
import UpdatePrintingHouseDialog from '@/components/printinghouses/UpdatePrintingHouseDialog.vue'
import DeletePrintingHouseDialog from '@/components/printinghouses/DeletePrintingHouseDialog.vue'

const route = useRoute()
const router = useRouter()
const store = userStore()

const printingHouse = ref(null)
const editDialog = ref(false)
const deleteDialog = ref(false)

const canManage = computed(() => store.user?.role === 'admin')

async function fetchPrintingHouse() {
  try {
    const response = await axiosClient.get(`/printinghouses/${route.params.id}/`)
    printingHouse.value = response.data
  } catch (error) {
    console.error('Ошибка загрузки типографии:', error)
  }
}

function openEditDialog() {
  editDialog.value = true
}

function openDeleteDialog() {
  deleteDialog.value = true
}

async function onUpdated() {
  await fetchPrintingHouse()
}

async function onDeleted() {
  await router.push('/printinghouses')
}

onMounted(fetchPrintingHouse)
</script>

<template>
  <v-container>
    <v-card class="pa-4">
      <v-card-title>
        {{ printingHouse?.name }}
      </v-card-title>
      <v-card-text>
        <p><strong>Адрес:</strong> {{ printingHouse?.address }}</p>
        <p><strong>Статус:</strong> {{ printingHouse?.is_active ? 'Активна' : 'Закрыта' }}</p>
        <p><strong>Тиражи:</strong></p>
        <ul>
          <li v-for="edition in printingHouse?.editions" :key="edition.id">
            Газета: {{ edition.newspaper_name }} (ID: {{ edition.newspaper }}) - {{ edition.quantity }} экз.
          </li>
        </ul>
        <p><strong>Поставки:</strong></p>
        <ul>
          <li v-for="distribution in printingHouse?.distributions" :key="distribution.id">
            Почтовое отделение: {{ distribution.post_office_address }} - {{ distribution.quantity }} экз.
          </li>
        </ul>
      </v-card-text>
      <v-card-actions>
        <v-btn color="primary" v-if="canManage" @click="openEditDialog">
          Редактировать
        </v-btn>
        <v-btn color="error" v-if="canManage" @click="openDeleteDialog">
          Удалить
        </v-btn>
      </v-card-actions>
    </v-card>

    <UpdatePrintingHouseDialog
      v-model="editDialog"
      :printingHouseData="printingHouse"
      @updated="onUpdated"
    />
    <DeletePrintingHouseDialog
      v-model="deleteDialog"
      :printingHouseId="printingHouse?.id"
      @deleted="onDeleted"
    />
  </v-container>
</template>
