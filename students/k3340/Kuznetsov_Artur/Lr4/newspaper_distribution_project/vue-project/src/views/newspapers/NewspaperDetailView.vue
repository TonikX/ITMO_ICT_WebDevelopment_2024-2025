<script setup>
import {ref, computed, onMounted} from 'vue'
import {useRoute, useRouter} from 'vue-router'
import axiosClient from '@/services/axiosClient'
import {userStore} from '@/stores/userStore'
import UpdateNewspaperDialog from '@/components/newspapers/UpdateNewspaperDialog.vue'
import DeleteNewspaperDialog from '@/components/newspapers/DeleteNewspaperDialog.vue'

const route = useRoute()
const router = useRouter()
const store = userStore()

const newspaper = ref(null)
const editor = ref(null)
const editDialog = ref(false)
const deleteDialog = ref(false)

const canEdit = computed(() => {
  return store.user?.role === 'admin' || store.user?.role === 'editor'
})

const canDelete = computed(() => {
  return store.user?.role === 'admin'
})

async function fetchNewspaper() {
  try {
    const response = await axiosClient.get(`/newspapers/${route.params.id}/`)
    newspaper.value = response.data
    await fetchEditor(response.data.editor)
  } catch (error) {
    console.error('Ошибка загрузки газеты:', error)
  }
}

async function fetchEditor(editorId) {
  try {
    if (!editorId) return
    const response = await axiosClient.get(`/users/${editorId}/`)
    editor.value = response.data
  } catch (error) {
    console.error('Ошибка загрузки редактора:', error)
  }
}

function openEditDialog() {
  editDialog.value = true
}

function openDeleteDialog() {
  deleteDialog.value = true
}

async function onUpdated() {
  await fetchNewspaper()
}

async function onDeleted() {
  await router.push('/newspapers')
}

onMounted(fetchNewspaper)
</script>

<template>
  <v-container>
    <v-card class="pa-4">
      <v-card-title>
        {{ newspaper?.name }} ({{ newspaper?.index }})
      </v-card-title>
      <v-card-text>
        <p><strong>Цена:</strong> {{ newspaper?.price }}</p>
        <p v-if="editor">
          <strong>Редактор:</strong>
          {{ editor.last_name }} {{ editor.first_name }} {{ editor.patronymic }} (ID: {{ editor.id }})
        </p>
        <p v-else>
          <strong>Редактор:</strong> Загрузка...
        </p>
        <p><strong>Тиражи:</strong></p>
        <ul>
          <li v-for="edition in newspaper?.editions" :key="edition.id">
            {{ edition.printing_house_name }}: {{ edition.quantity }} экз.
          </li>
        </ul>
        <p><strong>Поставки:</strong></p>
        <ul>
          <li v-for="distribution in newspaper?.distributions" :key="distribution.id">
            {{ distribution.post_office_address }}: {{ distribution.quantity }} экз.
          </li>
        </ul>
      </v-card-text>
      <v-card-actions>
        <v-btn color="primary" v-if="canEdit" @click="openEditDialog">
          Изменить
        </v-btn>
        <v-btn color="error" v-if="canDelete" @click="openDeleteDialog">
          Удалить
        </v-btn>
      </v-card-actions>
    </v-card>

    <UpdateNewspaperDialog
      v-model="editDialog"
      :newspaperData="newspaper"
      @updated="onUpdated"
    />
    <DeleteNewspaperDialog
      v-model="deleteDialog"
      :newspaperId="newspaper?.id"
      @deleted="onDeleted"
    />
  </v-container>
</template>
