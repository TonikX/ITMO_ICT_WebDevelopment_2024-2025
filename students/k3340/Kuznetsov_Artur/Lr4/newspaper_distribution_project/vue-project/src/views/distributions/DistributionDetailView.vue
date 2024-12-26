<script setup>
import {ref, computed, onMounted} from 'vue'
import {useRoute, useRouter} from 'vue-router'
import axiosClient from '@/services/axiosClient'
import {userStore} from '@/stores/userStore'
import UpdateDistributionDialog from '@/components/distributions/UpdateDistributionDialog.vue'
import DeleteDistributionDialog from '@/components/distributions/DeleteDistributionDialog.vue'

const route = useRoute()
const router = useRouter()
const store = userStore()

const distribution = ref(null)
const editDialog = ref(false)
const deleteDialog = ref(false)

const canEditOrDelete = computed(() => store.user?.role === 'admin')

async function fetchDistribution() {
  try {
    const response = await axiosClient.get(`/distributions/${route.params.id}/`)
    distribution.value = response.data
  } catch (error) {
    console.error('Ошибка загрузки поставки:', error)
  }
}

function openEditDialog() {
  editDialog.value = true
}

function openDeleteDialog() {
  deleteDialog.value = true
}

async function onUpdated() {
  await fetchDistribution()
}

async function onDeleted() {
  await router.push('/distributions')
}

onMounted(fetchDistribution)
</script>

<template>
  <v-container>
    <v-card class="pa-4" v-if="distribution">
      <v-card-title>
        Поставка №{{ distribution.id }} | {{ distribution.printing_house_name }} → Почтовое отделение по адресу
        {{ distribution.post_office_address }}
      </v-card-title>
      <v-card-text>
        <p><strong>Газета:</strong> {{ distribution?.newspaper_name }}</p>
        <p><strong>Типография:</strong> {{ distribution?.printing_house_name }}</p>
        <p><strong>Почтовое отделение:</strong> {{ distribution?.post_office_address }}</p>
        <p><strong>Количество экземпляров:</strong> {{ distribution?.quantity }}</p>
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

    <p v-else>Загрузка данных поставки...</p>

    <UpdateDistributionDialog
      v-model="editDialog"
      :distributionData="distribution"
      @updated="onUpdated"
    />
    <DeleteDistributionDialog
      v-model="deleteDialog"
      :distributionId="distribution?.id"
      @deleted="onDeleted"
    />
  </v-container>
</template>
