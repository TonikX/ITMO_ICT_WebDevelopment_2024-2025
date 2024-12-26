<script setup>
import {ref, computed, onMounted} from 'vue'
import {useRoute, useRouter} from 'vue-router'
import axiosClient from '@/services/axiosClient'
import {userStore} from '@/stores/userStore'
import UpdateEditionDialog from '@/components/editions/UpdateEditionDialog.vue'
import DeleteEditionDialog from '@/components/editions/DeleteEditionDialog.vue'

const route = useRoute()
const router = useRouter()
const store = userStore()

const edition = ref(null)
const editDialog = ref(false)
const deleteDialog = ref(false)

const canEditDelete = computed(() => store.user?.role === 'admin')

async function fetchEdition() {
  try {
    const response = await axiosClient.get(`/editions/${route.params.id}/`)
    edition.value = response.data
  } catch (error) {
    console.error('Ошибка загрузки тиража:', error)
  }
}

function openEditDialog() {
  editDialog.value = true
}

function openDeleteDialog() {
  deleteDialog.value = true
}

async function onUpdated() {
  await fetchEdition()
}

async function onDeleted() {
  await router.push('/editions')
}

onMounted(fetchEdition)
</script>

<template>
  <v-container>
    <v-card class="pa-4">
      <v-card-title v-if="edition">
        Тираж №{{ edition?.id }} | {{ edition?.printing_house_name }} → {{ edition?.newspaper_name }}
      </v-card-title>
      <v-card-text v-if="edition">
        <p><strong>ID Газеты:</strong> {{ edition?.newspaper }}</p>
        <p><strong>ID Типографии:</strong> {{ edition?.printing_house }}</p>
        <p><strong>Количество экземпляров:</strong> {{ edition?.quantity }}</p>
      </v-card-text>
      <v-card-actions v-if="edition">
        <v-btn color="primary" v-if="canEditDelete" @click="openEditDialog">
          Изменить
        </v-btn>
        <v-btn color="error" v-if="canEditDelete" @click="openDeleteDialog">
          Удалить
        </v-btn>
      </v-card-actions>
      <p v-else>Загрузка данных тиража...</p>
    </v-card>

    <UpdateEditionDialog
      v-model="editDialog"
      :editionData="edition"
      @updated="onUpdated"
    />
    <DeleteEditionDialog
      v-model="deleteDialog"
      :editionId="edition?.id"
      @deleted="onDeleted"
    />
  </v-container>
</template>
