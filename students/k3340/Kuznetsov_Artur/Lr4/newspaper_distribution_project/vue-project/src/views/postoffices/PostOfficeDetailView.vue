<script setup>
import {ref, computed, onMounted} from 'vue'
import {useRoute, useRouter} from 'vue-router'
import axiosClient from '@/services/axiosClient'
import {userStore} from '@/stores/userStore'
import UpdatePostOfficeDialog from '@/components/postoffices/UpdatePostOfficeDialog.vue'
import DeletePostOfficeDialog from '@/components/postoffices/DeletePostOfficeDialog.vue'

const route = useRoute()
const router = useRouter()
const store = userStore()

const postOffice = ref(null)
const editDialog = ref(false)
const deleteDialog = ref(false)

const canEditOrDelete = computed(() => store.user?.role === 'admin')

async function fetchPostOffice() {
  try {
    const response = await axiosClient.get(`/postoffices/${route.params.id}/`)
    postOffice.value = response.data
  } catch (error) {
    console.error('Ошибка загрузки почтового отделения:', error)
  }
}

function openEditDialog() {
  editDialog.value = true
}

function openDeleteDialog() {
  deleteDialog.value = true
}

async function onUpdated() {
  await fetchPostOffice()
}

async function onDeleted() {
  await router.push('/postoffices')
}

onMounted(fetchPostOffice)
</script>

<template>
  <v-container>
    <v-card class="pa-4">
      <v-card-title>
        Почтовое отделение №{{ postOffice?.number }}
      </v-card-title>
      <v-card-text>
        <p><strong>Адрес:</strong> {{ postOffice?.address }}</p>
        <p><strong>Поставки:</strong></p>
        <ul>
          <li v-for="distribution in postOffice?.distributions" :key="distribution.id">
            Газета "{{ distribution.newspaper_name }}" из {{ distribution.printing_house_name }}:
            {{ distribution.quantity }} экз.
          </li>
        </ul>
      </v-card-text>
      <v-card-actions>
        <v-btn color="primary" v-if="canEditOrDelete" @click="openEditDialog">
          Изменить
        </v-btn>
        <v-btn color="error" v-if="canEditOrDelete" @click="openDeleteDialog">
          Удалить
        </v-btn>
      </v-card-actions>
    </v-card>

    <UpdatePostOfficeDialog
      v-model="editDialog"
      :postOfficeData="postOffice"
      @updated="onUpdated"
    />
    <DeletePostOfficeDialog
      v-model="deleteDialog"
      :postOfficeId="postOffice?.id"
      @deleted="onDeleted"
    />
  </v-container>
</template>
