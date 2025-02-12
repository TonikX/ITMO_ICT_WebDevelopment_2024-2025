<template>
  <div>
    <Header />
    <h3 class="mb-4">Список классов</h3>
    <div class="d-flex align-items-center mb-4">
      <button @click="showAddForm = true" class="btn btn-primary me-3">Добавить ученика</button>
    </div>

    <table class="table table-bordered">
      <thead class="thead-dark">
        <tr>
          <th>Ученик</th>
          <th>Класс</th>
          <th>Дата начала</th>
          <th>Дата окончания</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="studentClass in filteredStudentClasses" :key="studentClass.id">
          <td>{{ studentClass.student }}</td>
          <td>{{ studentClass.school_class }}</td>
          <td>{{ studentClass.start_date }}</td>
          <td>{{ studentClass.end_date }}</td>
          <td>
            <button @click="editStudentClass(studentClass)" class="btn btn-warning btn-sm">Редактировать</button>
            <button @click="deleteStudentClass(studentClass.id)" class="btn btn-danger btn-sm">Удалить</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Форма добавления/редактирования -->
    <div v-if="showAddForm || selectedStudentClass" class="form-modal">
      <div class="modal-overlay">
        <div class="modal-content">
          <h2>{{ selectedStudentClass ? 'Редактировать ученика' : 'Добавить ученика' }}</h2>
          <form @submit.prevent="saveStudentClass">
            <div class="mb-3">
              <label for="student" class="form-label">Ученик:</label>
              <input v-model="formData.student" type="text" id="student" class="form-control" @input="searchStudent" required />
            </div>

            <div class="mb-3">
              <label for="school_class" class="form-label">Класс:</label>
              <input v-model="formData.school_class" type="text" id="school_class" class="form-control" placeholder="Введите класс" @input="searchClass" required />
            </div>

            <div class="mb-3">
              <label for="start_date" class="form-label">Дата начала:</label>
              <input v-model="formData.start_date" type="date" id="start_date" class="form-control" required />
            </div>

            <div class="mb-3">
              <label for="end_date" class="form-label">Дата окончания:</label>
              <input v-model="formData.end_date" type="date" id="end_date" class="form-control" required />
            </div>

            <div class="d-flex justify-content-between">
              <button type="submit" class="btn btn-primary">
                {{ selectedStudentClass ? "Сохранить изменения" : "Добавить" }}
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
import apiClient from "@/api/axios";

export default {
  data() {
    return {
      studentClasses: [],
      filteredStudentClasses: [],
      showAddForm: false,
      selectedStudentClass: null, // Выбранный класс ученика для редактирования
      selectedFilterClass: "",
      formData: {
        student: "",
        school_class: "",
        start_date: "",
        end_date: "",
        studentId: null,
        schoolClassId: null,
      },
      classes: [],
      students: [],
    };
  },
  async created() {
    await this.loadStudentClasses();
    await this.loadClasses();
    await this.loadStudents();
    this.filteredStudentClasses = this.studentClasses;
  },
  methods: {
    async loadClasses() {
      try {
        const response = await apiClient.get("/school/classes/");
        this.classes = response.data;
        console.log(this.classes)
      } catch (error) {
        console.error("Ошибка при загрузке списка классов:", error);
        alert("Не удалось загрузить список классов.");
      }
    },
    async loadStudents() {
      try {
        const response = await apiClient.get("/school/studentsfull");
        this.studentsfull = response.data;
        console.log(this.studentsfull)
      } catch (error) {
        console.error("Ошибка при загрузке списка учеников:", error);
        alert("Не удалось загрузить список учеников.");
      }
    },
    async loadStudentClasses() {
      try {
        const response = await apiClient.get("/school/student_class/");
        this.studentClasses = response.data;
        console.log(response)
        console.log(response.data)
      } catch (error) {
        console.error("Ошибка при загрузке списка учеников:", error);
        alert("Не удалось загрузить список учеников.");
      }
    },
    filterByClass() {
      if (!this.selectedFilterClass) {
        this.filteredStudentClasses = this.studentClasses;
      } else {
        this.filteredStudentClasses = this.studentClasses.filter(
          (studentClass) =>
            studentClass.school_class_id === parseInt(this.selectedFilterClass)
        );
      }
    },
    async saveStudentClass() {
      try {
        const classObj = this.classes.find((cls) => cls.name === this.formData.school_class);
        console.log(classObj.id)
        const studentObj = this.studentsfull.find((st) => st.full_name === this.formData.student);
        console.log(studentObj)
        const StudentId = studentObj.id
        console.log(StudentId)
        const payload = {
          student: StudentId,
          school_class: classObj.id,
          start_date: this.formData.start_date,
          end_date: this.formData.end_date,
        };
        console.log(payload);
        if (this.selectedStudentClass) {
          await apiClient.put(
            `/school/update_student_class/${this.selectedStudentClass.id}/`,
            payload
          );
          alert("Изменения сохранены.");
        } else {
          await apiClient.post("/school/add_student_class/", payload);
          alert("Ученик добавлен в класс.");
        }
        await this.loadStudentClasses();
        this.cancelEdit();
      } catch (error) {
        console.error("Ошибка при сохранении:", error);
        alert("Не удалось сохранить изменения.");
      }
    },
    async deleteStudentClass(id) {
      try {
        console.log(id)
        if (confirm("Вы уверены, что хотите удалить этого ученика?")) {
          await apiClient.delete(`/school/delete_student_class/${id}/`);
          this.studentClasses = this.studentClasses.filter((studentClass) => studentClass.id !== id);
        }
      } catch (error) {
        console.error("Ошибка при удалении учителя:", error);
      }
    },
    editStudentClass(studentClass) {
      this.selectedStudentClass = studentClass;
      this.formData.student = studentClass.student;
      this.formData.school_class = studentClass.school_class;
      this.formData.start_date = studentClass.start_date;
      this.formData.end_date = studentClass.end_date;
    },
    cancelEdit() {
      this.selectedStudentClass = null;
      this.showAddForm = false;
      this.formData = {
        student: "",
        school_class: "",
        start_date: "",
        end_date: "",
        studentId: null,
        schoolClassId: null,
      };
    },
  },
};
</script>

<style scoped>
* {
  margin-left: 20px;
  margin-right: 40px;
}

h3 {
  margin-top: 90px;
}

.form-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background-color: rgba(0, 0, 0, 0.5);
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-overlay {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  max-width: 600px;
  width: 100%;
}

.btn {
  border-radius: 8px;
  padding: 6px 12px;
}

.td {
  overflow: hidden;
}
</style>