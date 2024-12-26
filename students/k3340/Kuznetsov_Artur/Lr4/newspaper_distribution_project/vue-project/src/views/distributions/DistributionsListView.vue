<script setup>
import {ref, onMounted, computed} from 'vue'
import axiosClient from '@/services/axiosClient'
import {userStore} from '@/stores/userStore'
import CreateDistributionDialog from '@/components/distributions/CreateDistributionDialog.vue'

const store = userStore()

const distributions = ref([])
const createDialog = ref(false)

const isAdmin = computed(() => store.user?.role === 'admin')

async function fetchDistributions() {
  try {
    const response = await axiosClient.get('/distributions/')
    distributions.value = response.data
  } catch (error) {
    console.error('Ошибка загрузки поставок:', error)
  }
}

function openCreateDialog() {
  createDialog.value = true
}

function onDistributionCreated() {
  fetchDistributions()
}

onMounted(fetchDistributions)
</script>

<template>
  <v-container>
    <v-card class="pa-4">
      <v-card-title class="d-flex justify-space-between">
        <span>Список поставок</span>
        <v-btn color="primary" v-if="isAdmin" @click="openCreateDialog">
          Добавить поставку
        </v-btn>
      </v-card-title>
      <v-card-text>
        <v-list>
          <v-list-item
            v-for="distribution in distributions"
            :key="distribution.id"
            :to="`/distributions/${distribution.id}`"
          >
            <v-list-item-content>
              <v-list-item-title>
                Поставка №{{ distribution.id }} | {{ distribution.printing_house_name }} → Почтовое отделение по адресу
                {{ distribution.post_office_address }}
              </v-list-item-title>
              <v-list-item-subtitle>{{ distribution.quantity }} экз. из {{ distribution.printing_house_name }}
              </v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-card-text>
    </v-card>

    <CreateDistributionDialog
      v-model="createDialog"
      @distribution-created="onDistributionCreated"
    />
  </v-container>
</template>
