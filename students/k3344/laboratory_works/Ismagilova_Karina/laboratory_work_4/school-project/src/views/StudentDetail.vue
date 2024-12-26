<template>
  <div>
    <Header />
    <div class="page-container">
      <h1 class="page-title">Детальная информация об ученике</h1>
      <div v-if="student" class="student-info">
        <p><strong>Фамилия:</strong> {{ student.surname }}</p>
        <p><strong>Имя:</strong> {{ student.name }}</p>
        <p><strong>Класс:</strong> {{ student.class_name }}</p>
        <p><strong>Пол:</strong> {{ student.gender }}</p>
        <div class="button-group">
          <button @click="toggleEditForm" class="edit-button">Редактировать</button>
          <button @click="deleteStudent" class="delete-button">Удалить</button>
        </div>
      </div>
      <div v-if="showEditForm" class="edit-form">
        <h2>Редактировать ученика</h2>
        <form @submit.prevent="updateStudent">
          <input v-model="editedStudent.surname" type="text" placeholder="Фамилия" required />
          <input v-model="editedStudent.name" type="text" placeholder="Имя" required />
          <input v-model="editedStudent.class_name" type="text" placeholder="Класс" required />
          <div class="gender-buttons">
            <button
              :class="{'active': editedStudent.gender === 'М'}"
              @click.prevent="setGender('М')"
              class="gender-button">
              М
            </button>
            <button
              :class="{'active': editedStudent.gender === 'Ж'}"
              @click.prevent="setGender('Ж')"
              class="gender-button">
              Ж
            </button>
          </div>

          <div class="form-actions">
            <button type="submit" class="save-button">Сохранить</button>
            <button @click="cancelEdit" type="button" class="cancel-button">Отмена</button>
          </div>
        </form>
      </div>
      <div v-else-if="grades.length > 0" class="grades-container">
        <h2>Оценки</h2>
        <table class="grades-table">
          <thead>
            <tr>
              <th>Предмет</th>
              <th>Оценка</th>
              <th>Четверть</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="grade in grades" :key="grade.id">
              <td>{{ grade.subject }}</td>
              <td>{{ grade.grade }}</td>
              <td>{{ grade.quarter }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else>
        <p>Нет данных об оценках.</p>
      </div>
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
  props: ['id'],
  data() {
    return {
      student: null,
      grades: [],
      showEditForm: false,
      isLoading: true,
      editedStudent: {
        surname: '',
        name: '',
        class_name: '',
        gender: '',
      },
    };
  },
  created() {
    if (this.id) {
      this.fetchStudent();
      this.fetchGrades();
    } else {
      console.error('Не передан ID ученика.');
    }
  },
  methods: {
    async fetchStudent() {
      try {
        const response = await apiClient.get(`students/${this.id}/`);
        this.student = response.data;
        this.editedStudent = { ...response.data };
      } catch (error) {
        console.error('Ошибка при загрузке данных ученика:', error.response || error.message);
      }
    },
    toggleEditForm() {
      this.showEditForm = true;
    },
    async fetchGrades() {
      this.isLoading = true;
      try {
        const response = await apiClient.get(`grades/student/${this.id}/`);
        this.grades = response.data.sort((a, b) => a.quarter - b.quarter);
      } catch (error) {
        console.error('Ошибка при загрузке оценок ученика:', error.response || error.message);
      } finally {
        this.isLoading = false;
      }
    },
    async updateStudent() {
      try {
        const response = await apiClient.put(`students/${this.id}/`, this.editedStudent);
        this.student = response.data;
        this.showEditForm = false;
      } catch (error) {
        console.error('Ошибка при обновлении данных ученика:', error.response || error.message);
      }
    },
    async deleteStudent() {
      if (confirm('Вы уверены, что хотите удалить этого ученика?')) {
        try {
          await apiClient.delete(`students/${this.id}/`);
          alert('Ученик удалён успешно.');
          this.$router.push('/students');
        } catch (error) {
          console.error('Ошибка при удалении ученика:', error.response || error.message);
        }
      }
    },
    cancelEdit() {
      this.showEditForm = false;
      this.editedStudent = { ...this.student };
    },
    setGender(gender) {
      this.editedStudent.gender = gender;
    },
  },
};
</script>
