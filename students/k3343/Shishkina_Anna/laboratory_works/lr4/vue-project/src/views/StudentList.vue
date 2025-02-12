<template>
  <div>
    <Header />
    <h3 class="mb-4">Список учеников</h3>
    <button @click="showAddForm = true" class="btn btn-primary mb-4">Добавить ученика</button>

    <table class="table table-bordered">
      <thead class="thead-dark">
        <tr>
          <th>Имя</th>
          <th>Фамилия</th>
          <th>Пол</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="student in students" :key="student.id">
          <td>{{ student.first_name }}</td>
          <td>{{ student.last_name }}</td>
          <td>{{ student.gender === 'm' ? 'Мужской' : 'Женский' }}</td>
          <td>
            <button @click="editStudent(student)" class="btn btn-warning btn-sm">Редактировать</button>
            <button @click="deleteStudent(student.id)" class="btn btn-danger btn-sm">Удалить</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Форма добавления/редактирования -->
    <div v-if="showAddForm || selectedStudent" class="form-modal">
      <div class="modal-overlay">
        <div class="modal-content">
          <h2>{{ selectedStudent ? 'Редактировать ученика' : 'Добавить ученика' }}</h2>
          <form @submit.prevent="saveStudent">
            <div class="mb-3">
              <label for="first_name" class="form-label">Имя:</label>
              <input v-model="formData.first_name" type="text" id="first_name" class="form-control" required />
            </div>

            <div class="mb-3">
              <label for="last_name" class="form-label">Фамилия:</label>
              <input v-model="formData.last_name" type="text" id="last_name" class="form-control" required />
            </div>

            <div class="mb-3">
              <label for="gender" class="form-label">Пол:</label>
              <select v-model="formData.gender" id="gender" class="form-control" required>
                <option value="m">Мужской</option>
                <option value="f">Женский</option>
              </select>
            </div>

            <div class="d-flex justify-content-between">
              <button type="submit" class="btn btn-primary">
                {{ selectedStudent ? "Сохранить изменения" : "Добавить" }}
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
  data() {
    return {
      students: [],
      showAddForm: false, // Флаг отображения формы добавления
      selectedStudent: null, // Выбранный ученик для редактирования
      formData: {
        first_name: "",
        last_name: "",
        gender: "m",
      },
    };
  },
  async created() {
    this.fetchStudents();
  },
  methods: {
    async fetchStudents() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/school/students/");
        this.students = response.data;
      } catch (error) {
        console.error("Ошибка при загрузке списка учеников:", error);
        alert("Не удалось загрузить список учеников.");
      }
    },

    async deleteStudent(studentId) {
      try {
        if (confirm("Вы уверены, что хотите удалить этого ученика?")) {
          await axios.delete(`http://127.0.0.1:8000/school/delete_student/${studentId}/`);
          this.students = this.students.filter((student) => student.id !== studentId);
        }
      } catch (error) {
        console.error("Ошибка при удалении ученика:", error);
        alert("Не удалось удалить ученика.");
      }
    },

    editStudent(student) {
      this.selectedStudent = student;
      this.formData.first_name = student.first_name;
      this.formData.last_name = student.last_name;
      this.formData.gender = student.gender;
      this.showAddForm = true;
    },

    async saveStudent() {
        try {
            const studentData = {
            ...this.formData,
            school_classes: this.formData.school_classes || [],
            grades: this.formData.grades || [],
            };

            if (this.selectedStudent) {
                await axios.put(`http://127.0.0.1:8000/school/update_student/${this.selectedStudent.id}/`, studentData);
                Object.assign(this.selectedStudent, studentData);
            } else {
                const response = await axios.post("http://127.0.0.1:8000/school/add_student/", studentData);
                this.students.push(response.data);
            }

            this.cancelEdit();
            alert("Изменения успешно сохранены.");
        } catch (error) {
            console.error("Ошибка при сохранении ученика:", error);
            alert("Не удалось сохранить изменения.");
        }
    },

    cancelEdit() {
      this.showAddForm = false;
      this.selectedStudent = null;
      this.formData = { first_name: "", last_name: "", gender: "" };
    },
  },
};
</script>

<style scoped>
h3 {
    margin-top: 90px;
    margin-left: 20px;
}
.table {
  margin-top: 20px;
  margin-left: 20px;
  margin-right: 20px;
}
.table {
  table-layout: fixed;
  width: 80%;
}
.form-label {
  font-weight: bold;
}
.btn {
  margin-left: 20px;
  margin-top: 20px;
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
  background-color: rgba(0, 0, 0, 0.5);
}
.modal-overlay {
  background: #fff;
  padding: 20px;
  border-radius: 10px;
  width: 400px;
  box-shadow: 0 5px 15px rgba(0, 0, 0, 0.3);
}
</style>