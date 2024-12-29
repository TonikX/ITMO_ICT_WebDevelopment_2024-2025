<script setup>
import { ref } from 'vue'
const dialogRef = ref(null)
const showDialog = () => dialogRef.value?.showModal()
const closeDialog = () => dialogRef.value?.close()
</script>

<template>
  <h2>Marks</h2>
  <table>
    <thead>
      <tr>
        <th>Mark</th>
        <th>Student</th>
        <th>Subject</th>
        <th></th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="mark in marks" :key="mark.id">
        <td>{{ mark.mark }}</td>
        <td>{{ `${students.find(i => i.id == mark.student)['first_name']} ${students.find(i => i.id == mark.student)['last_name']}` }}</td>
        <td>{{ subjects.find(i => i.id == mark.subject)['name'] }}</td>
        <td style="text-align: right;">
          <a href="javascript:void(0)" @click="this.mark = Object.assign({}, mark); update = 1; showDialog()">edit</a> / <a href="javascript:void(0)" @click="deleteMark(mark.id)">delete</a>
        </td>
      </tr>
    </tbody>
  </table>
  <button @click="fetchMarks">Update list of marks</button>
  <button @click="Object.keys(mark).forEach(i => mark[i] = ''); update = 0; showDialog()">Create mark</button>
  <dialog ref="dialogRef">
    <h2 v-if="update">Update mark</h2>
    <h2 v-else>Create mark</h2>
    <form @submit.prevent>
      <label>Mark</label>
      <input
        v-model="mark.mark"
        type="number"
      >
      <label>Student</label>
      <select v-model="mark.student">
        <option v-for="student in students" :value="student.id" :key="student.id">{{ `${student.first_name} ${student.last_name}` }}</option>
      </select>
      <label>Subject</label>
      <select v-model="mark.subject">
        <option v-for="subject in subjects" :value="subject.id" :key="subject.id">{{ subject.name }}</option>
      </select>
      <div style="display: flex; justify-content: space-between;">
        <button v-if="update" @click="updateMark(); closeDialog()">Update</button>
        <button v-else @click="createMark(); closeDialog()">Create</button>
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
      marks: [],
      mark: {},
      students: [],
      subjects: [],
      update: 0
    }
  },
  methods: {
    async fetchMarks() {
      const response = await axios.get('/api/mark/')
      this.marks = response.data
    },
    async fetchStudents() {
      const response = await axios.get('/api/student/')
      this.students = response.data
    },
    async fetchSubjects() {
      const response = await axios.get('/api/subject/')
      this.subjects = response.data
    },
    async createMark() {
      await axios.post('/api/mark/', {
        mark: this.mark.mark,
        student: this.mark.student,
        subject: this.mark.subject,
      })
      this.fetchMarks()
    },
    async deleteMark(markId){
      await axios.delete(`/api/mark/${markId}/`)
      this.fetchMarks()
    },
    async updateMark(){
      console.log(this.mark.id, this.mark.name)
      await axios.put(`/api/mark/${this.mark.id}/`, { 
        id: this.mark.id,
        mark: this.mark.mark,
        student: this.mark.student,
        subject: this.mark.subject,
      })
      this.fetchMarks()
    }
  },
  mounted() {
    this.fetchMarks()
    this.fetchStudents()
    this.fetchSubjects()
  }
}
</script>

<style scoped>

</style>