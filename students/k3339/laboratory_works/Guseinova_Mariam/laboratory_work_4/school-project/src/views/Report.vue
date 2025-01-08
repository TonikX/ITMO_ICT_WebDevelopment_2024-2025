<template>
  <div>
    <Header />
    <div class="page-container">
      <h1>Генерация отчёта</h1>
      <div class="form-container">
        <label for="class-select" class="form-label-inline">Выберите класс:</label>
        <div class="select-container-inline">
          <select v-model="selectedClass" id="class-select" @change="fetchReportData" class="custom-select">
            <option value="" disabled selected>Выберите класс...</option>
            <option v-for="className in classOptions" :key="className" :value="className">
              {{ className }}
            </option>
          </select>
        </div>
      </div>

      <div v-if="selectedClass && reportData" class="report-content">
        <h2>{{ selectedClass }} Класс</h2>

        <div class="gender-count">
          <p>Количество мальчиков: {{ reportData.genderCount.boys }}</p>
          <p>Количество девочек: {{ reportData.genderCount.girls }}</p>
        </div>

        <h3>Список учеников:</h3>
        <table class="students-table">
          <thead>
            <tr>
              <th>Фамилия</th>
              <th>Имя</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="student in reportData.students" :key="student.id_student">
              <td>{{ student.surname }}</td>
              <td>{{ student.name }}</td>
            </tr>
          </tbody>
        </table>

        <h3>Список уроков:</h3>
        <table class="lessons-table">
          <thead>
            <tr>
              <th>День</th>
              <th>Номер урока</th>
              <th>Предмет</th>
              <th>Кабинет</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="lesson in enrichedLessons" :key="lesson.id_lesson">
              <td>{{ lesson.day }}</td>
              <td>{{ lesson.lesson_number }}</td>
              <td>{{ lesson.subject }}</td>
              <td>{{ lesson.room_number }}</td>
            </tr>
          </tbody>
        </table>
      </div>

      <div v-else-if="selectedClass" class="loading-message">
        <p>Загружаем данные для класса {{ selectedClass }}...</p>
      </div>
    </div>
  </div>
</template>

<script>
import Header from "@/components/Header.vue";
import apiClient from "@/api/axios";

export default {
  components: { Header },
  data() {
    return {
      classOptions: [],
      selectedClass: null,
      reportData: null,
      rooms: [],
    };
  },
  computed: {
    enrichedLessons() {
      if (!this.reportData || !this.reportData.lessons) return [];
      const daysOfWeek = ["Понедельник", "Вторник", "Среда", "Четверг", "Пятница", "Суббота"];
      return this.reportData.lessons
        .map((lesson) => {
          const room = this.rooms.find((room) => room.id_room === lesson.room);
          return {
            ...lesson,
            room_number: room ? room.number : "Неизвестно",
          };
        })
        .sort((a, b) => {
          const dayA = daysOfWeek.indexOf(a.day);
          const dayB = daysOfWeek.indexOf(b.day);
          if (dayA !== dayB) {
            return dayA - dayB;
          }
          return a.lesson_number - b.lesson_number;
        });
    },
  },
  created() {
    this.fetchClasses();
    this.fetchRooms();
  },
  methods: {
    async fetchClasses() {
      try {
        const response = await apiClient.get("students/");
        const uniqueClasses = [
          ...new Set(response.data.map((student) => student.class_name)),
        ];
        this.classOptions = uniqueClasses;
      } catch (error) {
        console.error("Ошибка при загрузке классов:", error);
      }
    },
    async fetchRooms() {
      try {
        const response = await apiClient.get("rooms/");
        this.rooms = response.data;
      } catch (error) {
        console.error("Ошибка при загрузке данных кабинетов:", error);
      }
    },
    async fetchReportData() {
      if (!this.selectedClass) return;

      try {
        const studentsResponse = await apiClient.get("students/");
        const students = studentsResponse.data.filter(
          (student) => student.class_name === this.selectedClass
        );

        const genderCount = {
          boys: students.filter((student) => student.gender === "М").length,
          girls: students.filter((student) => student.gender === "Ж").length,
        };

        const lessonsResponse = await apiClient.get("lessons/");
        const lessons = lessonsResponse.data.filter(
          (lesson) => lesson.class_label === this.selectedClass
        );

        this.reportData = {
          students,
          genderCount,
          lessons,
        };
      } catch (error) {
        console.error("Ошибка при загрузке данных отчёта:", error);
      }
    },
  },
};
</script>
