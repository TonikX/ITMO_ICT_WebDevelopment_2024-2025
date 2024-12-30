<script setup>

import {onMounted, ref} from "vue";
import axios from "axios";
import StudentList from "@/components/student/StudentList.vue";
import StudentModal from "@/components/student/StudentModal.vue";

const students = ref([])
const groups = ref([])
const isLoading = ref(true)
const isError = ref(false)
const isAddModalVisible = ref(false)

async function fetchStudents() {
  return await axios.get('/school/students').then(response => {
    students.value = response.data
    isLoading.value = false
  }).catch(error => {
    isError.value = true
    console.log(error);
  })
}

async function fetchGroups() {
  return await axios.get(`/school/groups`).then(response => {
    if (response.status === 200) {
      groups.value = response.data
    }
  }).catch(error => {
    isError.value = true
    console.log(error);
  })
}


async function addStudent(student) {
  await axios.post('/school/students/', student).then(response => {
        if (response.status === 201) {
          students.value.push(student)
        }
      }
  ).catch(error => console.log(error))
}

async function updateStudent(student) {
  await axios.put(`/school/students/${student.id}/update`, student)
  await fetchStudents()
}

async function deleteStudent(id) {
  await axios.delete(`/school/students/${id}/delete`).then(response => {
    students.value = students.value.filter(student => student.id !== id)
  })
}
onMounted(async () => {
  await fetchStudents()
  await fetchGroups()
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
      <h2>Ученики</h2>
      <v-btn color="primary" @click="isAddModalVisible = true">Добавить ученика</v-btn>
      <StudentList :students="students" :groups="groups" @delete-student="deleteStudent" @update-student="updateStudent"/>
      <StudentModal
          v-model="isAddModalVisible"
          :groups="groups"
          mode="add"
          @submit-student="addStudent"
      />
    </template>
  </div>
</template>

<style scoped>

</style>