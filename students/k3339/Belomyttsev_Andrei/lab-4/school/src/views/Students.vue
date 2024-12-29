<script setup>
import { ref } from 'vue'
const dialogRef = ref(null)
const showDialog = () => dialogRef.value?.showModal()
const closeDialog = () => dialogRef.value?.close()
</script>

<template>
  <h2>Students</h2>
  <table>
    <thead>
      <tr>
        <th>First Name</th>
        <th>Last Name</th>
        <th>Gender</th>
        <th>Grade</th>
        <th></th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="student in students" :key="student.id">
        <td>{{ student.first_name }}</td>
        <td>{{ student.last_name }}</td>
        <td>{{ {'M': 'Male', 'F': 'Female'}[student.gender] }}</td>
        <td>{{ `${grades.find(i => i.id == student.grade)['number']}${grades.find(i => i.id == student.grade)['letter']}` }}</td>
        <td style="text-align: right;">
          <a href="javascript:void(0)" @click="this.student = Object.assign({}, student); update = 1; showDialog()">edit</a> / <a href="javascript:void(0)" @click="deleteStudent(student.id)">delete</a>
        </td>
      </tr>
    </tbody>
  </table>
  <button @click="fetchStudents">Update list of students</button>
  <button @click="Object.keys(student).forEach(i => student[i] = ''); update = 0; showDialog()">Create student</button>
  <dialog ref="dialogRef">
    <h2 v-if="update">Update student</h2>
    <h2 v-else>Create student</h2>
    <form @submit.prevent>
      <label>First Name</label>
      <input
        v-model="student.first_name"
        type="text"
      >
      <label>Last Name</label>
      <input
        v-model="student.last_name"
        type="text"
      >
      <label>Gender</label>
      <select v-model="student.gender">
        <option value="M">Male</option>
        <option value="F">Female</option>
      </select>
      <label>Grade</label>
      <select v-model="student.grade">
        <option v-for="grade in grades" :value="grade.id" :key="grade.id">{{ `${grade.number}${grade.letter}` }}</option>
      </select>
      <div style="display: flex; justify-content: space-between;">
        <button v-if="update" @click="updateStudent(); closeDialog()">Update</button>
        <button v-else @click="createStudent(); closeDialog()">Create</button>
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
      students: [],
      student: {},
      grades: [],
      update: 0
    }
  },
  methods: {
    async fetchStudents() {
      const response = await axios.get('/api/student/')
      this.students = response.data
    },
    async fetchGrades() {
      const response = await axios.get('/api/grade/')
      this.grades = response.data
    },
    async createStudent() {
      await axios.post('/api/student/', {
        marks: this.student.marks || [],
        first_name: this.student.first_name,
        last_name: this.student.last_name,
        gender: this.student.gender,
        grade: this.student.grade,
      })
      this.fetchStudents()
    },
    async deleteStudent(studentId){
      await axios.delete(`/api/student/${studentId}/`)
      this.fetchStudents()
    },
    async updateStudent(){
      console.log(this.student.id, this.student.name)
      await axios.put(`/api/student/${this.student.id}/`, { 
        id: this.student.id,
        marks: this.student.marks || [],
        first_name: this.student.first_name,
        last_name: this.student.last_name,
        gender: this.student.gender,
        grade: this.student.grade,
      })
      this.fetchStudents()
    }
  },
  mounted() {
    this.fetchStudents()
    this.fetchGrades()
  }
}
</script>

<style scoped>

</style>