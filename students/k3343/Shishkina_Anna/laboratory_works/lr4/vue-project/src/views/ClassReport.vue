<template>
  <div class="container my-4">
  <div class="content-wrapper">
    <h3 class="mb-4">Отчёт об успеваемости класса</h3>

    <div class="mb-4">
      <select v-model="selectedClass" id="className" class="form-select w-50" @change="fetchStudentsPerClassGender">
        <option disabled value="">Выберите класс</option>
        <option v-for="classItem in classList" :key="classItem.id" :value="classItem.name">
          {{ classItem.name }} (id {{ classItem.id }})
        </option>
      </select>
    </div>

    <div v-if="studentsPerClassGender" class="mt-4">
      <h4>Количество учеников в классе {{ selectedClass }}:</h4>
      <table class="table table-striped">
        <thead>
          <tr>
            <th>Пол</th>
            <th>Количество учеников</th>
          </tr>
        </thead>
        <tbody>
          <tr>
            <td>Мальчики</td>
            <td>{{ studentsPerClassGender.male }}</td>
          </tr>
          <tr>
            <td>Девочки</td>
            <td>{{ studentsPerClassGender.female }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <!-- Форма для ввода ID класса и отчёт об успеваемости -->
    <div class="mb-4">
    <label for="classId" class="form-label me-3" style="margin-bottom: 0;">Введите ID класса:</label>
    <div class="d-flex align-items-center">
        <input
            v-model="classId"
            type="number"
            id="classId"
            class="form-control"
            placeholder="ID класса"
            style="width: 150px; height: 40px; margin-right: 10px; vertical-align: middle;"
            required
        />
        <button
            @click="fetchClassReport"
            class="btn"
            style="width: 150px; height: 40px; background-color: #0D6EFD; color: white; border-radius: 10px; display: flex; justify-content: center; align-items: center; vertical-align: middle; margin-top: -3px;"
        >
            Получить отчёт
        </button>
    </div>
    </div>

    <!-- Отчёт об успеваемости -->
    <div v-if="report" class="mt-4">
      <h4>Отчёт для класса: {{ report.name }}</h4>
      <p><strong>Классный руководитель:</strong> {{ report.class_teacher }}</p>
      <p><strong>Средняя оценка класса:</strong> {{ report.average_class_grade.toFixed(2) }}</p>
      <p><strong>Количество студентов:</strong> {{ report.total_students }}</p>

      <!-- Таблица с оценками по предметам -->
      <h4>Оценки по предметам:</h4>
      <table class="table table-bordered">
        <thead>
          <tr>
            <th>Предмет</th>
            <th>Оценка</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(grade, subject) in report.subject_grades" :key="subject">
            <td>{{ subject }}</td>
            <td>{{ grade.toFixed(2) }}</td>
          </tr>
        </tbody>
      </table>
    </div>

    <div v-if="error" class="alert alert-danger mt-4">
      <p>{{ error }}</p>
    </div>

    <!-- Отчёт по количеству учителей на предметах -->
    <div v-if="teachersPerSubject.length > 0" class="row mt-4">
      <div class="col-md-6">
        <h3>Количество учителей на предметах:</h3>
        <table class="table table-hover">
          <thead>
            <tr>
              <th>Предмет</th>
              <th>Количество учителей</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="(subject, index) in teachersPerSubject" :key="index">
              <td>{{ subject.title }}</td>
              <td>{{ subject.num_teachers }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Таблица с количеством профильных и базовых классов -->
      <div class="col-md-6">
        <h3>Количество профильных и базовых классов:</h3>
        <table class="table table-light">
          <thead>
            <tr>
              <th>Тип класса</th>
              <th>Количество</th>
            </tr>
          </thead>
          <tbody>
            <tr v-if="profileClassCount">
              <td>Профильные</td>
              <td>{{ profileClassCount.count }}</td>
            </tr>
            <tr v-if="basicClassCount">
              <td>Непрофильные</td>
              <td>{{ basicClassCount.count }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
  </div>
</template>


<script>
import apiClient from "@/api/axios";

export default {
  data() {
    return {
      selectedClass: "",
      classList: [],
      studentsPerClassGender: null,
      report: null,
      teachersPerSubject: [],
      profileClassCount: null, // Данные по профильным классам
      basicClassCount: null, // Данные по базовым классам
      classId: "", // ID класса, который вводит пользователь
      error: null,
    };
  },
  mounted() {
    this.fetchClassList();
    this.fetchTeachersPerSubject();
    this.fetchClassroomCounts();
  },
  methods: {
    async fetchClassList() {
      try {
        const response = await apiClient.get("/school/classes/");
        this.classList = response.data;
      } catch (error) {
        console.error("Ошибка при загрузке списка классов:", error);
      }
    },

    async fetchStudentsPerClassGender() {
        if (!this.selectedClass) {
            return;
        }

        try {
            const maleResponse = await apiClient.get(`/school/students-per-class/${this.selectedClass}/m/`);
            const maleCount = maleResponse.data.students_count;

            const femaleResponse = await apiClient.get(`/school/students-per-class/${this.selectedClass}/f/`);
            const femaleCount = femaleResponse.data.students_count;

            this.studentsPerClassGender = {
            male: maleCount,
            female: femaleCount,
            };
        } catch (error) {
            console.error("Ошибка при загрузке отчета по ученикам:", error);
            this.studentsPerClassGender = null;
        }
    },

    // Метод для загрузки отчета по количеству учителей на предметах
    async fetchTeachersPerSubject() {
      try {
        const response = await apiClient.get(`/school/teachers-per-subject/`);
        this.teachersPerSubject = response.data;
      } catch (error) {
        console.error("Ошибка при загрузке отчета по учителям:", error);
      }
    },

    // Метод для загрузки отчетов по профильным и базовым классам
    async fetchClassroomCounts() {
      try {
        const profileResponse = await apiClient.get(`/school/classrooms/profile/`);
        this.profileClassCount = profileResponse.data;

        const basicResponse = await apiClient.get(`/school/classrooms/basic/`);
        this.basicClassCount = basicResponse.data;
      } catch (error) {
        console.error("Ошибка при загрузке отчетов по классам:", error);
      }
    },

    // Метод для загрузки отчета по классу
    async fetchClassReport() {
      if (!this.classId) {
        this.error = "Пожалуйста, введите ID класса.";
        return;
      }

      try {
        const classResponse = await apiClient.get(`/school/class-report/${this.classId}/`);
        const reportData = classResponse.data;
        reportData.class_teacher = reportData.class_teacher.toString();
        this.report = reportData; 
        this.error = null; 
      } catch (error) {
        this.report = null; 
        this.error = "Не удалось загрузить отчёт. Проверьте правильность ID класса.";
        console.error("Ошибка при загрузке отчета:", error);
      }
    },
  },
};
</script>

<style scoped>
.content-wrapper {
  margin-left: 20px; 
}
h3 {
    margin-top: 90px;
    margin-left: 1px;
}
div {
  margin-bottom: 20px;
}
button {
  padding: 10px;
  background-color: #4CAF50;
  color: white;
  border: none;
  cursor: pointer;
}
button:hover {
  background-color: #45a049;
}
table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}
table th, table td {
  padding: 10px;
  border: 1px solid #ddd;
  text-align: left;
}
</style>
