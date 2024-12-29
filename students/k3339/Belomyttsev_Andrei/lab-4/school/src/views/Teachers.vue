<script setup>
import { ref } from 'vue'
const dialogRef = ref(null)
const showDialog = () => dialogRef.value?.showModal()
const closeDialog = () => dialogRef.value?.close()
</script>

<template>
  <h2>Teachers</h2>
  <table>
    <thead>
      <tr>
        <th>First Name</th>
        <th>Last Name</th>
        <th>Classroom</th>
        <th></th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="teacher in teachers" :key="teacher.id">
        <td>{{ teacher.first_name }}</td>
        <td>{{ teacher.last_name }}</td>
        <td>{{ teacher.classroom }}</td>
        <td style="text-align: right;">
          <a href="javascript:void(0)" @click="this.teacher = Object.assign({}, teacher); update = 1; showDialog()">edit</a> / <a href="javascript:void(0)" @click="deleteTeacher(teacher.id)">delete</a>
        </td>
      </tr>
    </tbody>
  </table>
  <button @click="fetchTeachers">Update list of teachers</button>
  <button @click="Object.keys(teacher).forEach(i => teacher[i] = ''); update = 0; showDialog()">Create teacher</button>
  <dialog ref="dialogRef">
    <h2 v-if="update">Update teacher</h2>
    <h2 v-else>Create teacher</h2>
    <form @submit.prevent>
      <label>First name</label>
      <input
        v-model="teacher.first_name"
        type="text"
      >
      <label>Last name</label>
      <input
        v-model="teacher.last_name"
        type="text"
      >
      <label>Classroom</label>
      <input
        v-model="teacher.classroom"
        type="number"
      >
      <div style="display: flex; justify-content: space-between;">
        <button v-if="update" @click="updateTeacher(); closeDialog()">Update</button>
        <button v-else @click="createTeacher(); closeDialog()">Create</button>
        <button @click="closeDialog">Cancel</button>
      </div>
    </form>
  </dialog>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      teachers: [],
      teacher: {},
      update: 0
    }
  },
  methods: {
    async fetchTeachers() {
      const response = await axios.get('/api/teacher/')
      this.teachers = response.data
    },
    async createTeacher() {
      await axios.post('/api/teacher/', {
        first_name: this.teacher.first_name,
        last_name: this.teacher.last_name,
        classroom: this.teacher.classroom,
      })
      this.fetchTeachers()
    },
    async deleteTeacher(teacherId){
      await axios.delete(`/api/teacher/${teacherId}/`)
      this.fetchTeachers()
    },
    async updateTeacher(){
      console.log(this.teacher.id, this.teacher.name)
      await axios.put(`/api/teacher/${this.teacher.id}/`, { 
        id: this.teacher.id,
        first_name: this.teacher.first_name,
        last_name: this.teacher.last_name,
        classroom: this.teacher.classroom,
      })
      this.fetchTeachers()
    }
  },
  mounted() {
    this.fetchTeachers()
  }
}
</script>

<style scoped>

</style>