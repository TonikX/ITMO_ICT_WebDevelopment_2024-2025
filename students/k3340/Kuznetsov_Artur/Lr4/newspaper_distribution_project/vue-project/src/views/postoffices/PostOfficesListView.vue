<script setup>
import {ref, onMounted, computed} from 'vue'
import axiosClient from '@/services/axiosClient'
import {userStore} from '@/stores/userStore'
import CreatePostOfficeDialog from '@/components/postoffices/CreatePostOfficeDialog.vue'

const store = userStore()

const postOffices = ref([])
const createDialog = ref(false)

const isAdmin = computed(() => store.user?.role === 'admin')

async function fetchPostOffices() {
  try {
    const response = await axiosClient.get('/postoffices/')
    postOffices.value = response.data
  } catch (error) {
    console.error('Ошибка загрузки почтовых отделений:', error)
  }
}

function openCreateDialog() {
  createDialog.value = true
}

function onPostOfficeCreated() {
  fetchPostOffices()
}

onMounted(fetchPostOffices)
</script>

<template>
  <v-container>
    <v-card class="pa-4">
      <v-card-title class="d-flex justify-space-between">
        <span>Список почтовых отделений</span>
        <v-btn color="primary" v-if="isAdmin" @click="openCreateDialog">
          Добавить отделение
        </v-btn>
      </v-card-title>
      <v-card-text>
        <v-list>
          <v-list-item
            v-for="office in postOffices"
            :key="office.id"
            :to="`/postoffices/${office.id}`"
          >
            <v-list-item-content>
              <v-list-item-title>Почтовое отделение №{{ office.number }}</v-list-item-title>
              <v-list-item-subtitle>{{ office.address }}</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-card-text>
    </v-card>

    <CreatePostOfficeDialog
      v-model="createDialog"
      @post-office-created="onPostOfficeCreated"
    />
  </v-container>
</template>
