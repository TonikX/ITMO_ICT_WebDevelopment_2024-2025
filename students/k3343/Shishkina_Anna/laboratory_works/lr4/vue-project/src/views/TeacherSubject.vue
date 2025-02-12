<template>
  <div>
    <Header />
    <h3 class="mb-4">Список предметов и учителей, которые их ведут</h3>
    <button @click="showAddForm = true" class="btn btn-primary mb-4">Добавить запись</button>

    <table class="table table-bordered">
      <thead class="thead-dark">
        <tr>
          <th>Имя учителя</th>
          <th>Предмет</th>
          <th>Дата начала</th>
          <th>Дата окончания</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="teacherSubject in teacherSubjects" :key="teacherSubject.id">
          <td v-if="teacherSubject.teacher">{{ teacherSubject.teacher.first_name }} {{ teacherSubject.teacher.last_name }}</td><td v-else>Нет данных</td>
          <td>{{ teacherSubject.subject.title }}</td>
          <td>{{ teacherSubject.start_date }}</td>
          <td>{{ teacherSubject.end_date }}</td>
          <td>
            <button @click="editTeacherSubject(teacherSubject)" class="btn btn-warning btn-sm">Редактировать</button>
            <button @click="deleteTeacherSubject(teacherSubject.id)" class="btn btn-danger btn-sm">Удалить</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Форма добавления/редактирования -->
    <div v-if="showAddForm || isEditing" class="form-modal">
      <div class="modal-overlay">
        <div class="modal-content">
          <h2>{{ isEditing ? 'Редактировать запись' : 'Добавить запись' }}</h2>
          <form @submit.prevent="saveTeacherSubject">
            <div class="mb-3">
              <label for="teacher" class="form-label">Имя учителя:</label>
              <input v-model="form.teacherName" type="text" id="teacher" class="form-control" @input="searchTeachers" required />
              <ul v-if="filteredTeachers.length > 0">
                <li v-for="teacher in filteredTeachers" :key="teacher.id" @click="selectTeacher(teacher)">
                  {{ teacher.full_name }}
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
              <label for="start_date" class="form-label">Дата начала:</label>
              <input v-model="form.start_date" type="date" id="start_date" class="form-control" required />
            </div>

            <div class="mb-3">
              <label for="end_date" class="form-label">Дата окончания:</label>
              <input v-model="form.end_date" type="date" id="end_date" class="form-control" required />
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
      teacherSubjects: [],
      teachers: [],
      subjects: [],
      filteredTeachers: [],
      filteredSubjects: [],
      form: {
        id: null,
        teacherName: "",
        subjectTitle: "",
        start_date: "",
        end_date: "",
        teacher: null,
        subject: null,
      },
      isEditing: false,
      showAddForm: false,
    };
  },
  methods: {
    async fetchTeacherSubjects() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/school/teacher_subject/");
        this.teacherSubjects = response.data;
      } catch (error) {
        console.error("Ошибка загрузки данных", error);
      }
    },
    async fetchTeachers() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/school/teachersfull/");
        this.teachers = response.data;
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
    searchTeachers() {
      this.filteredTeachers = this.teachers.filter(teacher =>
        teacher.full_name.toLowerCase().includes(this.form.teacherName.toLowerCase())
      );
    },
    searchSubjects() {
      this.filteredSubjects = this.subjects.filter(subject =>
        subject.title.toLowerCase().includes(this.form.subjectTitle.toLowerCase())
      );
    },
    selectTeacher(teacher) {
      this.form.teacherName = teacher.full_name;
      this.form.teacher = teacher.id;
      this.filteredTeachers = [];
    },
    selectSubject(subject) {
      this.form.subjectTitle = subject.title;
      this.form.subject = subject.id;
      this.filteredSubjects = [];
    },
    async saveTeacherSubject() {
      try {
        if (this.isEditing) {
          await axios.put(
            `http://127.0.0.1:8000/school/update_teacher_subject/${this.form.id}/`,
            this.form
          );
        } else {
          const response = await axios.post(
            "http://127.0.0.1:8000/school/add_teacher_subject/",
            this.form
          );
          this.teacherSubjects.push(response.data);
        }
        this.resetForm();
        this.fetchTeacherSubjects();
      } catch (error) {
        console.error("Ошибка сохранения данных", error);
      }
    },
    editTeacherSubject(teacherSubject) {
      this.form = {
        id: teacherSubject.id,
        teacherName: teacherSubject.teacher.first_name + ' ' + teacherSubject.teacher.last_name,
        subjectTitle: teacherSubject.subject.title,
        start_date: teacherSubject.start_date,
        end_date: teacherSubject.end_date,
        teacher: teacherSubject.teacher.id,
        subject: teacherSubject.subject.id,
      };
      this.isEditing = true;
      this.showAddForm = true;
    },
    async deleteTeacherSubject(id) {
      try {
        await axios.delete(
          `http://127.0.0.1:8000/school/delete_teacher_subject/${id}/`
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
        teacherName: "",
        subjectTitle: "",
        start_date: "",
        end_date: "",
        teacher: null,
        subject: null,
      };
      this.isEditing = false;
      this.showAddForm = false;
    },
  },
  mounted() {
    this.fetchTeacherSubjects();
    this.fetchTeachers();
    this.fetchSubjects();
  },
};
</script>

<style>
button {
  margin-left: 20px;
  margin-top: 20px;
}
h3 {
    margin-top: 90px;
    margin-left: 20px;
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
