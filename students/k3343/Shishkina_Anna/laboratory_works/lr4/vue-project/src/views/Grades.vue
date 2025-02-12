<template>
  <div>
    <Header />
    <h3 class="mb-4">Список оценок</h3>
    <button @click="showAddForm = true" class="btn btn-primary mb-4">Добавить запись</button>

    <table class="table table-bordered">
      <thead class="thead-dark">
        <tr>
          <th>Ученик</th>
          <th>Предмет</th>
          <th>Год</th>
          <th>Четверть</th>
          <th>Оценка</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="grade in grades" :key="grade.id">
          <td v-if="grade.student">{{ grade.student.first_name }} {{ grade.student.last_name }}</td><td v-else>Нет данных</td>
          <td>{{ grade.subject.title }}</td>
          <td>{{ grade.year }}</td>
          <td>{{ grade.quarter }}</td>
          <td>{{ grade.grade }}</td>
          <td>
            <button @click="editGrade(grade)" class="btn btn-warning btn-sm">Редактировать</button>
            <button @click="deleteGrade(grade.id)" class="btn btn-danger btn-sm">Удалить</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Форма добавления/редактирования -->
    <div v-if="showAddForm || isEditing" class="form-modal">
      <div class="modal-overlay">
        <div class="modal-content">
          <h2>{{ isEditing ? 'Редактировать запись' : 'Добавить запись' }}</h2>
          <form @submit.prevent="saveGrade">
            <div class="mb-3">
              <label for="student" class="form-label">Имя ученика:</label>
              <input v-model="form.studentName" type="text" id="student" class="form-control" @input="searchStudents" required />
              <ul v-if="filteredStudents.length > 0">
                <li v-for="student in filteredStudents" :key="student.id" @click="selectStudents(student)">
                  {{ student.full_name }}
                </li>
              </ul>
            </div>

            <div class="mb-3">
              <label for="subject" class="form-label">Предмет:</label>
              <input v-model="form.subjectTitle" type="text" id="subject" class="form-control" @input="searchSubjects" required />
              <ul v-if="filteredSubjects.length > 0">
                <li v-for="subject in filteredSubjects" :key="subject.id" @click="selectSubject(subject)">
                  {{ subject.title }}
                </li>
              </ul>
            </div>

            <div class="mb-3">
              <label for="year" class="form-label">Год:</label>
              <input v-model="form.year" type="number" id="year" class="form-control" required />
            </div>

            <div class="mb-3">
              <label for="quarter" class="form-label">Четверть:</label>
              <input v-model="form.quarter" type="number" id="quarter" class="form-control" required />
            </div>

            <div class="mb-3">
              <label for="grade" class="form-label">Оценка:</label>
              <input v-model="form.grade" type="number" id="grade" class="form-control" required />
            </div>

            <div class="d-flex justify-content-between">
              <button type="submit" class="btn btn-primary">
                {{ isEditing ? 'Сохранить изменения' : 'Добавить' }}
              </button>
              <button type="button" @click="cancelEdit" class="btn btn-secondary">Отмена</button>
            </div>
          </form>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Header from '@/components/Header.vue';
import axios from "axios";

export default {
  name: "TeacherTable",
  data() {
    return {
      grades: [],
      students: [],
      subjects: [],
      filteredStudents: [],
      filteredSubjects: [],
      form: {
        id: null,
        studentName: "",
        subjectTitle: "",
        year: "",
        quarter: "",
        grade: null,
        student: null,
        subject: null,
      },
      isEditing: false,
      showAddForm: false,
    };
  },
  methods: {
    async fetchGrades() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/school/grades/");
        this.grades = response.data;
      } catch (error) {
        console.error("Ошибка загрузки данных", error);
      }
    },
    async fetchStudents() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/school/studentsfull/");
        this.students = response.data;
      } catch (error) {
        console.error("Ошибка загрузки учителей", error);
      }
    },
    async fetchSubjects() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/school/subjects/");
        this.subjects = response.data;
      } catch (error) {
        console.error("Ошибка загрузки предметов", error);
      }
    },
    searchStudents() {
      this.filteredStudents = this.students.filter(student =>
        student.full_name.toLowerCase().includes(this.form.studentName.toLowerCase())
      );
    },
    searchSubjects() {
      this.filteredSubjects = this.subjects.filter(subject =>
        subject.title.toLowerCase().includes(this.form.subjectTitle.toLowerCase())
      );
    },
    selectStudents(student) {
      this.form.studentName = student.full_name;
      this.form.student = student.id;
      this.filteredStudents = [];
    },
    selectSubject(subject) {
      this.form.subjectTitle = subject.title;
      this.form.subject = subject.id;
      this.filteredSubjects = [];
    },
    async saveGrade() {
        try {
            const payload = {
                subject: this.form.subject,
                student: this.form.student,
                year: this.form.year,
                quarter: this.form.quarter,
                grade: this.form.grade,
            };
            console.log(payload)
            if (this.isEditing) {
            await axios.put(`http://127.0.0.1:8000/school/update_grade/${this.form.id}/`, payload);
            } else {
            await axios.post("http://127.0.0.1:8000/school/add_grades/", payload);
            }

            this.resetForm();
            this.fetchGrades();
        } catch (error) {
            console.error("Ошибка сохранения данных", error);
        }
    },
    editGrade(grade) {
      this.form = {
        id: grade.id,
        studentName: grade.student.first_name + ' ' + grade.student.last_name,
        subjectTitle: grade.subject.title,
        year: grade.year,
        quarter: grade.quarter,
        grade: grade.grade,
        student: grade.student.id,
        subject: grade.subject.id,
      };
      this.isEditing = true;
      this.showAddForm = true;
    },
    async deleteGrade(id) {
      try {
        await axios.delete(
          `http://127.0.0.1:8000/school/delete_grade/${id}/`
        );
        this.teacherSubjects = this.teacherSubjects.filter(
          (item) => item.id !== id
        );
      } catch (error) {
        console.error("Ошибка удаления записи", error);
      }
    },
    cancelEdit() {
      this.resetForm();
    },
    resetForm() {
      this.form = {
        id: null,
        studentName: "",
        subjectTitle: "",
        year: "",
        quarter: "",
        grade: "",
        student: null,
        subject: null,
      };
      this.isEditing = false;
      this.showAddForm = false;
    },
  },
  mounted() {
    this.fetchGrades();
    this.fetchStudents();
    this.fetchSubjects();
  },
};
</script>

<style>
h3 {
    margin-top: 90px;
    margin-left: 20px;
}
button {
  margin-left: 20px;
  margin-top: 20px;
}
.table {
  margin-top: 20px;
  margin-left: 20px;
  margin-right: 0px;
}
.thead-dark {
  background-color: #343a40;
  color: white;
}
.form-modal {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  justify-content: center;
  align-items: center;
  background: rgba(0, 0, 0, 0.5);
  z-index: 1000;
}
.modal-overlay {
  background: white;
  padding: 20px;
  border-radius: 10px;
  width: 400px;
}
ul {
  list-style-type: none;
  padding: 0;
  max-height: 150px;
  overflow-y: auto;
}
li {
  padding: 5px;
  cursor: pointer;
}
li:hover {
  background-color: #f0f0f0;
}
</style>
