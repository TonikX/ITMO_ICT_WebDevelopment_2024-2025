<script setup>
import { ref, onMounted, computed } from 'vue'
import axiosClient from '@/services/axiosClient'
import { userStore } from '@/stores/userStore'
import CreateNewspaperDialog from '@/components/newspapers/CreateNewspaperDialog.vue'

const store = userStore()

const newspapers = ref([])
const createDialog = ref(false)

const isAdmin = computed(() => store.user?.role === 'admin')

async function fetchNewspapers() {
  try {
    const response = await axiosClient.get('/newspapers/')
    newspapers.value = response.data
  } catch (error) {
    console.error('Ошибка загрузки газет:', error)
  }
}

function openCreateDialog() {
  createDialog.value = true
}

function onNewspaperCreated() {
  fetchNewspapers()
}

onMounted(fetchNewspapers)
</script>

<template>
  <v-container>
    <v-card class="pa-4">
      <v-card-title class="d-flex justify-space-between">
        <span>Список газет</span>
        <v-btn color="primary" v-if="isAdmin" @click="openCreateDialog">
          Добавить газету
        </v-btn>
      </v-card-title>
      <v-card-text>
        <v-list>
          <v-list-item
            v-for="newspaper in newspapers"
            :key="newspaper.id"
            :to="`/newspapers/${newspaper.id}`"
          >
            <v-list-item-content>
              <v-list-item-title>{{ newspaper.name }}</v-list-item-title>
              <v-list-item-subtitle>
                Индекс: {{ newspaper.index }} | Цена: {{ newspaper.price }} | Редактор: {{ newspaper.editor }}
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-card-text>
    </v-card>

    <CreateNewspaperDialog
      v-model="createDialog"
      @newspaper-created="onNewspaperCreated"
    />
  </v-container>
</template>

<style scoped>
</style>
