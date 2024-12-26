<script setup>
import {computed, onMounted, ref} from 'vue'
import {useRoute, useRouter} from 'vue-router'
import axiosClient from '@/services/axiosClient'
import {userStore} from '@/stores/userStore'
import UpdateUserDialog from '@/components/users/UpdateUserDialog.vue'
import DeleteUserDialog from '@/components/users/DeleteUserDialog.vue'

const route = useRoute()
const router = useRouter()
const store = userStore()

const user = ref({})
const editDialog = ref(false)
const deleteDialog = ref(false)

const isAdmin = computed(() => store.user?.role === 'admin');

async function fetchUser() {
  try {
    const response = await axiosClient.get(`/users/${route.params.id}/`)
    user.value = response.data
  } catch (error) {
    console.error('Ошибка загрузки пользователя:', error)
  }
}

async function updateUser(updatedData) {
  try {
    await axiosClient.put(`/users/update/${route.params.id}/`, updatedData);
    await fetchUser(); // Обновляем данные пользователя после успешного изменения
  } catch (error) {
    console.error('Ошибка обновления пользователя:', error);
  }
}

async function deleteUser() {
  try {
    await axiosClient.delete(`/users/delete/${route.params.id}/`);
    goToUsersList(); // После удаления переходим к списку пользователей
  } catch (error) {
    console.error('Ошибка удаления пользователя:', error);
  }
}

function openEditDialog() {
  editDialog.value = true
}

function openDeleteDialog() {
  deleteDialog.value = true
}

function goToUsersList() {
  router.push('/users')
}

onMounted(async () => {
  await Promise.all([store.fetchUser(), fetchUser()]);
});

</script>

<template>
  <v-container>
    <v-card class="pa-4">
      <v-card-title>
        {{ user.last_name }} {{ user.first_name }} {{ user.patronymic }} ({{ user.role }}) (ID: {{ user.id }})
      </v-card-title>
      <v-card-text>
        <p><strong>Имя пользователя:</strong> {{ user.username }}</p>
        <p><strong>Email:</strong> {{ user.email }}</p>
        <template v-if="user.role === 'editor' && user.newspapers">
          <p><strong>Газеты:</strong></p>
          <ul>
            <li v-for="newspaper in user.newspapers" :key="newspaper.id">
              {{ newspaper.name }}
            </li>
          </ul>
        </template>
      </v-card-text>
      <v-card-actions>
        <v-btn
          v-if="isAdmin"
          color="primary"
          @click="openEditDialog"
        >
          Редактировать
        </v-btn>
        <v-btn
          v-if="isAdmin"
          color="error"
          @click="openDeleteDialog"
        >
          Удалить
        </v-btn>
      </v-card-actions>
    </v-card>

    <UpdateUserDialog
      v-model="editDialog"
      :user-data="user"
      @submit-user="updateUser"
    />
    <DeleteUserDialog
      v-model="deleteDialog"
      @confirm-delete="deleteUser"
    />
  </v-container>
</template>

<style scoped>

</style>
