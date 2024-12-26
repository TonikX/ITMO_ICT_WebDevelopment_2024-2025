<template>
  <Header />
  <div class="page-container">
    <div class="header-container">
      <h1 class="page-title">Список учеников</h1>
      <button @click="showAddStudentModal = true" class="add-button">Добавить ученика</button>
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
      <table class="student-table">
        <thead>
          <tr>
            <th>Фамилия Имя</th>
            <th>Класс</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="student in filteredStudents" :key="student.id">
            <td>
              <router-link :to="`/students/${student.id_student}`" class="student-link">
                {{ student.surname }} {{ student.name }}
              </router-link>
            </td>
            <td>{{ student.class_name }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
  <div v-if="showAddStudentModal" class="modal-overlay">
    <div class="modal-content">
      <form @submit.prevent="addStudent">
        <input v-model="newStudent.surname" type="text" placeholder="Фамилия" required />
        <input v-model="newStudent.name" type="text" placeholder="Имя" required />
        <input v-model="newStudent.class_name" type="text" placeholder="Класс" required />
        <div class="gender-select">
          <span>Выберите пол:</span>
          <button
            type="button"
            class="gender-option"
            :class="{ active: newStudent.gender === 'М' }"
            @click="selectGender('М')"
          >
            М
          </button>
          <button
            type="button"
            class="gender-option"
            :class="{ active: newStudent.gender === 'Ж' }"
            @click="selectGender('Ж')"
          >
            Ж
          </button>
        </div>
        <div class="modal-actions">
          <button type="submit" class="save-button">Сохранить</button>
          <button @click="closeModal" type="button" class="cancel-button">Отмена</button>
        </div>
      </form>
    </div>
  </div>
</template>


<script>
import Header from '@/components/Header.vue';
import apiClient from '@/api/axios';

export default {
  components: {
    Header,
  },
  data() {
    return {
      students: [],
      searchQuery: '',
      newStudent: {
        surname: '',
        name: '',
        class_name: '',
        gender: '',
      },
      showAddStudentModal: false,
    };
  },
  computed: {
    filteredStudents() {
      if (!this.searchQuery) {
        return this.students;
      }
      return this.students.filter((student) =>
        student.surname.toLowerCase().includes(this.searchQuery.toLowerCase())
      );
    },
  },
  created() {
    this.fetchStudents();
  },
  methods: {
    selectGender(gender) {
      this.newStudent.gender = gender;
    },
    async fetchStudents() {
      try {
        const response = await apiClient.get('students/');
        this.students = response.data;
      } catch (error) {
        console.error('Ошибка при получении списка учеников:', error);
      }
    },
    async addStudent() {
      try {
        const response = await apiClient.post('students/', this.newStudent);
        this.students.push(response.data);
        this.closeModal();
      } catch (error) {
        console.error('Ошибка при добавлении ученика:', error);
      }
    },
    closeModal() {
      this.showAddStudentModal = false;
    },
  },
};
</script>
