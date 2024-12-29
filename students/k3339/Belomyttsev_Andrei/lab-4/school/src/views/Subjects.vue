<script setup>
import { ref } from 'vue'
const dialogRef = ref(null)
const showDialog = () => dialogRef.value?.showModal()
const closeDialog = () => dialogRef.value?.close()
</script>

<template>
  <h2>Subjects</h2>
  <table>
    <thead>
      <tr>
        <th>Name</th>
        <th></th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="subject in subjects" :key="subject.id">
        <td>{{ subject.name }}</td>
        <td style="text-align: right;">
          <a href="javascript:void(0)" @click="this.subject = Object.assign({}, subject); update = 1; showDialog()">edit</a> / <a href="javascript:void(0)" @click="deleteSubject(subject.id)">delete</a>
        </td>
      </tr>
    </tbody>
  </table>
  <button @click="fetchSubjects">Update list of subjects</button>
  <button @click="Object.keys(subject).forEach(i => subject[i] = ''); update = 0; showDialog()">Create subject</button>
  <dialog ref="dialogRef">
    <h2 v-if="update">Update subject</h2>
    <h2 v-else>Create subject</h2>
    <form @submit.prevent>
      <label>Name</label>
      <input
        v-model="subject.name"
        type="text"
      >
      <div style="display: flex; justify-content: space-between;">
        <button v-if="update" @click="updateSubject(); closeDialog()">Update</button>
        <button v-else @click="createSubject(); closeDialog()">Create</button>
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
      subjects: [],
      subject: {},
      update: 0
    }
  },
  methods: {
    async fetchSubjects() {
      const response = await axios.get('/api/subject/')
      this.subjects = response.data
    },
    async createSubject() {
      await axios.post('/api/subject/', {
        name: this.subject.name,
      })
      this.fetchSubjects()
    },
    async deleteSubject(subjectId){
      await axios.delete(`/api/subject/${subjectId}/`)
      this.fetchSubjects()
    },
    async updateSubject(){
      console.log(this.subject.id, this.subject.name)
      await axios.put(`/api/subject/${this.subject.id}/`, { 
        id: this.subject.id,
        name: this.subject.name,
      })
      this.fetchSubjects()
    }
  },
  mounted() {
    this.fetchSubjects()
  }
}
</script>

<style scoped>

</style>