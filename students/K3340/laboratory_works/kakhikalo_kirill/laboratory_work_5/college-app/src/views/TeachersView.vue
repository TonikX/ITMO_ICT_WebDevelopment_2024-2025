<template>
  <div class="teachers-container">
    <h1>Teachers</h1>
    <table class="teachers-table">
      <thead>
        <tr>
          <th>ID</th>
          <th>Имя</th>
          <th>Должность</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="teacher in teachers" :key="teacher.teacher_id">
          <td>{{ teacher.teacher_id }}</td>
          <td>
            <router-link :to="{ name: 'TeacherDetail', params: { id: teacher.teacher_id } }">
              {{ teacher.name }}
            </router-link>
          </td>
          <td>{{ teacher.job_title }}</td>
        </tr>
      </tbody>
    </table>

    <button @click="showAddTeacherForm = true">Add Teacher</button>

    <div v-if="showAddTeacherForm" class="modal-overlay">
      <div class="modal">
        <h2>Add Teacher</h2>
        <form @submit.prevent="submitTeacherForm">
          <div class="form-group">
            <label for="teacher_id">Teacher ID:</label>
            <input v-model="newTeacher.teacher_id" type="text" id="teacher_id" required />
          </div>
          <div class="form-group">
            <label for="name">Name:</label>
            <input v-model="newTeacher.name" type="text" id="name" required />
          </div>
          <div class="form-group">
            <label for="job_title">Job Title:</label>
            <input v-model="newTeacher.job_title" type="text" id="job_title" required />
          </div>
          <div class="form-buttons">
            <button type="submit">Save</button>
            <button type="button" @click="cancelAddTeacher">Cancel</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/api'

export default {
  name: 'TeachersView',
  data() {
    return {
      teachers: [],
      showAddTeacherForm: false,
      newTeacher: {
        teacher_id: '',
        name: '',
        job_title: ''
      }
    }
  },
  created() {
    this.fetchTeachers()
  },
  methods: {
    fetchTeachers() {
      api.get('http://localhost:8000/api/teachers/')
        .then(response => {
          this.teachers = response.data
        })
        .catch(error => {
          console.error('Error fetching teachers:', error)
        })
    },
    submitTeacherForm() {
      api.post('http://localhost:8000/api/teachers/', this.newTeacher)
        .then(response => {
          this.fetchTeachers()
          this.cancelAddTeacher()
        })
        .catch(error => {
          console.error('Error adding teacher:', error)
        })
    },
    cancelAddTeacher() {
      this.showAddTeacherForm = false
      this.newTeacher = { teacher_id: '', name: '', job_title: '' }
    }
  }
}
</script>

<style scoped>
.teachers-container {
  padding: 20px;
}

.teachers-table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

.teachers-table th,
.teachers-table td {
  border: 1px solid #ccc;
  padding: 8px 12px;
  text-align: left;
}

.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal {
  background: #fff;
  padding: 20px;
  width: 400px;
  border-radius: 5px;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
}

.form-group input {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}

.form-buttons {
  display: flex;
  gap: 10px;
  justify-content: flex-end;
}
</style>
