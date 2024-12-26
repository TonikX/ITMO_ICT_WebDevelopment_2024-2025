<script setup>
import {onMounted, ref} from 'vue'
import axiosClient from '@/services/axiosClient'
import {useRouter} from 'vue-router'

const users = ref([])
const router = useRouter()

async function fetchUsers() {
  try {
    const response = await axiosClient.get('/users/')
    users.value = response.data
  } catch (error) {
    console.error('Ошибка загрузки пользователей:', error)
  }
}

function navigateToUser(userId) {
  router.push(`/users/${userId}`)
}

onMounted(fetchUsers)
</script>

<template>
  <v-container>
    <v-card class="pa-4">
      <v-card-title>Список пользователей</v-card-title>
      <v-card-text>
        <v-list>
          <v-list-item
            v-for="user in users"
            :key="user.id"
            @click="navigateToUser(user.id)"
            class="cursor-pointer"
          >
            <v-list-item-content>
              <v-list-item-title>
                {{ user.last_name }} {{ user.first_name }} {{ user.patronymic }}
              </v-list-item-title>
              <v-list-item-subtitle>{{ user.role }}</v-list-item-subtitle>
            </v-list-item-content>
          </v-list-item>
        </v-list>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<style scoped>
.cursor-pointer {
  cursor: pointer;
}
</style>
