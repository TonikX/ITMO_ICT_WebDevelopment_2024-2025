<script setup>
import { ref } from 'vue'
const dialogRef = ref(null)
const showDialog = () => dialogRef.value?.showModal()
const closeDialog = () => dialogRef.value?.close()
</script>

<template>
  <h2>Schedule</h2>
  <table>
    <thead>
      <tr>
        <th>Day of week</th>
        <th>Number</th>
        <th>Grade</th>
        <th>Subject</th>
        <th>Teacher</th>
        <th></th>
      </tr>
    </thead>
    <tbody>
      <tr v-for="schedule in schedules" :key="schedule.id">
        <td>{{ {1: 'Monday', 2: 'Tuesday', 3: 'Wednesday', 4: 'Thursday', 5: 'Friday', 6: 'Saturday'}[schedule.day_of_week] }}</td>
        <td>{{ schedule.number }}</td>
        <td>{{ `${grades.find(i => i.id == schedule.grade)['number']}${grades.find(i => i.id == schedule.grade)['letter']}` }}</td>
        <td>{{ subjects.find(i => i.id == schedule.subject)['name'] }}</td>
        <td>{{ `${teachers.find(i => i.id == schedule.teacher)['first_name']} ${teachers.find(i => i.id == schedule.teacher)['last_name']}` }}</td>
        <td style="text-align: right;">
          <a href="javascript:void(0)" @click="this.schedule = Object.assign({}, schedule); update = 1; showDialog()">edit</a> / <a href="javascript:void(0)" @click="deleteSchedule(schedule.id)">delete</a>
        </td>
      </tr>
    </tbody>
  </table>
  <button @click="fetchSchedules">Update list of schedules</button>
  <button @click="Object.keys(schedule).forEach(i => schedule[i] = ''); update = 0; showDialog()">Create schedule</button>
  <dialog ref="dialogRef">
    <h2 v-if="update">Update schedule</h2>
    <h2 v-else>Create schedule</h2>
    <form @submit.prevent>
      <label>Day of week</label>
      <select v-model.number="schedule.day_of_week">
        <option value="1">Monday</option>
        <option value="2">Tuesday</option>
        <option value="3">Wednesday</option>
        <option value="4">Thursday</option>
        <option value="5">Friday</option>
        <option value="6">Saturday</option>
      </select>
      <label>Number</label>
      <input
        v-model="schedule.number"
        type="number"
      >
      <label>Grade</label>
      <select v-model="schedule.grade">
        <option v-for="grade in grades" :value="grade.id" :key="grade.id">{{ `${grade.number}${grade.letter}` }}</option>
      </select>
      <label>Subject</label>
      <select v-model="schedule.subject">
        <option v-for="subject in subjects" :value="subject.id" :key="subject.id">{{ subject.name }}</option>
      </select>
      <label>Teacher</label>
      <select v-model="schedule.teacher">
        <option v-for="teacher in teachers" :value="teacher.id" :key="teacher.id">{{ `${teacher.first_name} ${teacher.last_name}` }}</option>
      </select>
      <div style="display: flex; justify-content: space-between;">
        <button v-if="update" @click="updateSchedule(); closeDialog()">Update</button>
        <button v-else @click="createSchedule(); closeDialog()">Create</button>
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
      schedules: [],
      schedule: {},
      grades: [],
      subjects: [],
      teachers: [],
      update: 0
    }
  },
  methods: {
    async fetchSchedules() {
      const response = await axios.get('/api/lesson/')
      this.schedules = response.data
    },
    async fetchGrades() {
      const response = await axios.get('/api/grade/')
      this.grades = response.data
    },
    async fetchSubjects() {
      const response = await axios.get('/api/subject/')
      this.subjects = response.data
    },
    async fetchTeachers() {
      const response = await axios.get('/api/teacher/')
      this.teachers = response.data
    },
    async createSchedule() {
      await axios.post('/api/lesson/', {
        day_of_week: this.schedule.day_of_week,
        number: this.schedule.number,
        grade: this.schedule.grade,
        subject: this.schedule.subject,
        teacher: this.schedule.teacher,
      })
      this.fetchSchedules()
    },
    async deleteSchedule(scheduleId){
      await axios.delete(`/api/lesson/${scheduleId}/`)
      this.fetchSchedules()
    },
    async updateSchedule(){
      console.log(this.schedule.id, this.schedule.name)
      await axios.put(`/api/lesson/${this.schedule.id}/`, { 
        id: this.schedule.id,
        day_of_week: this.schedule.day_of_week,
        number: this.schedule.number,
        grade: this.schedule.grade,
        subject: this.schedule.subject,
        teacher: this.schedule.teacher,
      })
      this.fetchSchedules()
    }
  },
  mounted() {
    this.fetchSchedules()
    this.fetchGrades()
    this.fetchSubjects()
    this.fetchTeachers()
  }
}
</script>

<style scoped>

</style>