<script setup>
import {ref, onMounted, computed} from 'vue'
import axiosClient from '@/services/axiosClient'
import {userStore} from '@/stores/userStore'
import CreateEditionDialog from '@/components/editions/CreateEditionDialog.vue'

const store = userStore()

const editions = ref([])
const createDialog = ref(false)

const isAdmin = computed(() => store.user?.role === 'admin')

async function fetchEditions() {
  try {
    const response = await axiosClient.get('/editions/')
    editions.value = response.data
  } catch (error) {
    console.error('Ошибка загрузки тиражей:', error)
  }
}

function openCreateDialog() {
  createDialog.value = true
}

function onEditionCreated() {
  fetchEditions()
}

onMounted(fetchEditions)
</script>

<template>
  <v-container>
    <v-card class="pa-4">
      <v-card-title class="d-flex justify-space-between">
        <span>Список тиражей</span>
        <v-btn color="primary" v-if="isAdmin" @click="openCreateDialog">
          Добавить тираж
        </v-btn>
      </v-card-title>
      <v-card-text>
        <v-list>
          <v-list-item
            v-for="edition in editions"
            :key="edition.id"
            :to="`/editions/${edition.id}`"
          >
            <v-list-item-content>
              <v-list-item-title>
                Тираж №{{ edition.id }} | {{ edition.printing_house_name }} → {{ edition.newspaper_name }}
              </v-list-item-title>
              <v-list-item-subtitle>
                Количество экземпляров: {{ edition.quantity }}
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-card-text>
    </v-card>

    <CreateEditionDialog
      v-model="createDialog"
      @edition-created="onEditionCreated"
    />
  </v-container>
</template>

<style scoped>
</style>
