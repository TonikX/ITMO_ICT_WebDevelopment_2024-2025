<template>
  <Header />
  <div class="page-container">
    <div class="header-container">
      <h1 class="page-title">Список оценок</h1>
      <button @click="showAddGradeModal = true" class="add-button">Добавить оценку</button>
    </div>

    <div class="search-container">
      <input
        v-model="searchQuery"
        type="text"
        placeholder="Поиск по фамилии"
        class="search-input"
      />
    </div>

    <div class="table-wrapper">
      <table class="grades-table">
        <thead>
          <tr>
            <th>Ученик</th>
            <th>Предмет</th>
            <th>Оценка</th>
            <th>Четверть</th>
            <th>Действия</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="grade in filteredGrades" :key="grade.id_grade">
            <td>{{ getStudentName(grade.student) }}</td>
            <td>{{ grade.subject }}</td>
            <td>{{ grade.grade }}</td>
            <td>{{ grade.quarter }}</td>
            <td>
              <button @click="editGrade(grade)" class="edit-button">Редактировать</button>
              <button @click="deleteGrade(grade.id_grade)" class="delete-button">Удалить</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="showAddGradeModal" class="modal-overlay">
      <div class="modal-content">
        <form @submit.prevent="editableGrade ? updateGrade() : addGrade()">
          <div class="form-group">
            <label for="subject" class="form-label">Предмет:</label>
            <input v-model="form.subject" id="subject" type="text" class="form-input" required />
          </div>

          <div class="form-group">
            <label for="grade" class="form-label">Оценка:</label>
            <input v-model="form.grade" id="grade" type="number" class="form-input" min="1" max="5" required />
          </div>

          <div class="form-group">
            <label for="quarter" class="form-label">Четверть:</label>
            <input v-model="form.quarter" id="quarter" type="number" class="form-input" min="1" max="4" required />
          </div>

          <div class="form-group">
            <label for="student" class="form-label">Ученик:</label>
            <select v-model="form.student" id="student" class="form-select" required>
              <option value="">Выберите ученика</option>
              <option v-for="student in students" :key="student.id_student" :value="student.id_student">
                {{ student.surname }} {{ student.name }} {{ student.class_name }}
              </option>
            </select>
          </div>

          <div class="modal-actions">
            <button type="submit" class="save-button">{{ editableGrade ? 'Обновить' : 'Добавить' }}</button>
            <button @click="closeModal" type="button" class="cancel-button">Отмена</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import Header from "@/components/Header.vue";
import apiClient from "@/api/axios";

export default {
  components: {
    Header,
  },
  data() {
    return {
      grades: [],
      students: [],
      searchQuery: "",
      form: {
        student: "",
        subject: "",
        grade: "",
        quarter: "",
      },
      showAddGradeModal: false,
      editableGrade: null,
    };
  },
  computed: {
    filteredGrades() {
      if (!this.searchQuery) {
        return this.grades;
      }
      return this.grades.filter((grade) => {
        const studentName = this.getStudentName(grade.student).toLowerCase();
        return studentName.includes(this.searchQuery.toLowerCase());
      });
    },
  },
  created() {
    this.fetchGrades();
    this.fetchStudents();
  },
  methods: {
    async fetchGrades() {
      try {
        const response = await apiClient.get("grades/");
        this.grades = response.data;
      } catch (error) {
        console.error("Ошибка при загрузке оценок:", error);
      }
    },
    async fetchStudents() {
      try {
        const response = await apiClient.get("students/");
        this.students = response.data;
      } catch (error) {
        console.error("Ошибка при загрузке списка учеников:", error);
      }
    },
    getStudentName(studentId) {
      const student = this.students.find((s) => String(s.id_student) === String(studentId));
      return student ? `${student.surname} ${student.name}` : "Неизвестно";
    },
    async addGrade() {
      try {
        const gradeData = {
          student: Number(this.form.student),
          subject: this.form.subject,
          grade: Number(this.form.grade),
          quarter: Number(this.form.quarter),
        };
        const response = await apiClient.post("grades/", gradeData);
        this.grades.push(response.data);
        this.resetForm();
        this.closeModal();
      } catch (error) {
        console.error("Ошибка при добавлении оценки:", error);
      }
    },
    async updateGrade() {
      try {
        const gradeData = {
          student: Number(this.form.student),
          subject: this.form.subject,
          grade: Number(this.form.grade),
          quarter: Number(this.form.quarter),
        };
        await apiClient.put(`grades/${this.editableGrade.id_grade}/`, gradeData);
        this.fetchGrades();
        this.resetForm();
        this.closeModal();
      } catch (error) {
        console.error("Ошибка при обновлении оценки:", error);
      }
    },
    editGrade(grade) {
      this.editableGrade = grade;
      this.form = { ...grade };
      this.showAddGradeModal = true;
    },
    async deleteGrade(id) {
      try {
        await apiClient.delete(`grades/${id}/`);
        this.fetchGrades();
      } catch (error) {
        console.error("Ошибка при удалении оценки:", error);
      }
    },
    closeModal() {
      this.showAddGradeModal = false;
      this.editableGrade = null;
      this.resetForm();
    },
    resetForm() {
      this.form = {
        student: "",
        subject: "",
        grade: "",
        quarter: "",
      };
    },
  },
};
</script>
