<script setup>
import { ref } from 'vue'
const dialogRef = ref(null)
const showDialog = () => dialogRef.value?.showModal()
const closeDialog = () => dialogRef.value?.close()
</script>

<template>
  <h2>Grades</h2>
  <table>
    <thead>
      <tr>
        <th>Number</th>
        <th>Letter</th>
        <th>Teacher</th>
        <th>Report</th>
        <th></th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="grade in grades" :key="grade.id">
        <td>{{ grade.number }}</td>
        <td>{{ grade.letter }}</td>
        <td>{{ `${teachers.find(i => i.id == grade.teacher)['first_name']} ${teachers.find(i => i.id == grade.teacher)['last_name']}` }}</td>
        <td><router-link :to="'/report/' + grade.id">report</router-link></td>
        <td style="text-align: right;">
          <a href="javascript:void(0)" @click="this.grade = Object.assign({}, grade); update = 1; showDialog()">edit</a> / <a href="javascript:void(0)" @click="deleteGrade(grade.id)">delete</a>
        </td>
      </tr>
    </tbody>
  </table>
  <button @click="fetchGrades">Update list of grades</button>
  <button @click="Object.keys(grade).forEach(i => grade[i] = ''); update = 0; showDialog()">Create grade</button>
  <dialog ref="dialogRef">
    <h2 v-if="update">Update grade</h2>
    <h2 v-else>Create grade</h2>
    <form @submit.prevent>
      <label>Number</label>
      <input
        v-model="grade.number"
        type="number"
      >
      <label>Letter</label>
      <input
        v-model="grade.letter"
        type="text"
      >
      <label>Teacher</label>
      <select v-model="grade.teacher">
        <option v-for="teacher in teachers" :value="teacher.id" :key="teacher.id">{{ `${teacher.first_name} ${teacher.last_name}` }}</option>
      </select>
      <div style="display: flex; justify-content: space-between;">
        <button v-if="update" @click="updateGrade(); closeDialog()">Update</button>
        <button v-else @click="createGrade(); closeDialog()">Create</button>
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
      grades: [],
      grade: {},
      teachers: [],
      update: 0
    }
  },
  methods: {
    async fetchGrades() {
      const response = await axios.get('/api/grade/')
      this.grades = response.data
    },
    async fetchTeachers() {
      const response = await axios.get('/api/teacher/')
      this.teachers = response.data
    },
    async createGrade() {
      await axios.post('/api/grade/', {
        number: this.grade.number,
        letter: this.grade.letter,
        teacher: this.grade.teacher,
      })
      this.fetchGrades()
    },
    async deleteGrade(gradeId){
      await axios.delete(`/api/grade/${gradeId}/`)
      this.fetchGrades()
    },
    async updateGrade(){
      console.log(this.grade.id, this.grade.name)
      await axios.put(`/api/grade/${this.grade.id}/`, { 
        id: this.grade.id,
        number: this.grade.number,
        letter: this.grade.letter,
        teacher: this.grade.teacher,
      })
      this.fetchGrades()
    }
  },
  mounted() {
    this.fetchGrades()
    this.fetchTeachers()
  }
}
</script>

<style scoped>

</style>