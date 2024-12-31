<script setup>

import {onMounted, ref} from "vue";
import axios from "axios";
import TeacherList from "@/components/teacher/TeacherList.vue";
import TeacherModal from "@/components/teacher/TeacherModal.vue";

const teachers = ref([])
const rooms = ref([])
const isLoading = ref(true)
const isError = ref(false)
const isAddModalVisible = ref(false)

async function fetchTeachers() {
  return await axios.get('/school/teachers').then(response => {
    if (response.status === 200) {
      teachers.value = response.data
      console.log(teachers.value)
      isLoading.value = false
    }
  }).catch(error => {
    isError.value = true
    console.log(error);
  })
}

async function fetchRooms() {
  return await axios.get('/school/rooms').then(response => {
    if (response.status === 200) {
      rooms.value = response.data
    }
  }).catch(error => {
    isError.value = true
    console.log(error);
  })
}

async function addTeacher(teacher) {
  await axios.post('/school/teachers/', teacher).then(response => {
        if (response.status === 201) {
          teachers.value.push(teacher)
        }
      }
  ).catch(error => console.log(error))
}

async function updateTeacher(teacher) {
  await axios.put(`/school/teachers/${teacher.id}/update`, teacher)
  await fetchTeachers()
}

async function deleteTeacher(id) {
  await axios.delete(`/school/teachers/${id}/delete`).then(response => {
    teachers.value = teachers.value.filter(teacher => teacher.id !== id)
    fetchTeachers()
  })
}

onMounted(async () => {
  await fetchTeachers()
  await fetchRooms()
})


</script>

<template>
  <div class="d-flex align-center flex-column ga-10">
    <template v-if="isLoading">
      <v-skeleton-loader
          type="card"
          class="mt-4"
          max-width="500"
      ></v-skeleton-loader>
    </template>
    <template v-else>
      <h2>Учители</h2>
      <v-btn color="primary" @click="isAddModalVisible = true">Добавить учителя</v-btn>
      <TeacherList :teachers="teachers" :rooms="rooms" @delete-teacher="deleteTeacher" @update-teacher="updateTeacher"/>
      <TeacherModal
          v-model="isAddModalVisible"
          :rooms="rooms"
          mode="add"
          @submit-teacher="addTeacher"
      />
    </template>
  </div>
</template>

<style scoped>

</style>