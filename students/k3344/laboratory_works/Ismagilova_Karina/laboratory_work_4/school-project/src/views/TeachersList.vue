<template>
  <div>
    <Header />
    <div class="page-container">
      <div class="header-container">
        <h1 class="page-title">Список учителей</h1>
        <button @click="showAddTeacherModal = true" class="add-button">Добавить учителя</button>
      </div>

      <div class="table-wrapper">
        <table class="teacher-table" v-if="teachers.length > 0">
          <thead>
            <tr>
              <th>Фамилия Имя</th>
              <th>Предметы</th>
              <th>Кабинет</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="teacher in teachers" :key="teacher.id_teacher">
              <td>
                <router-link :to="`/teachers/${teacher.id_teacher}`" class="teacher-link">
                  {{ teacher.surname }} {{ teacher.name }}
                </router-link>
              </td>
              <td>{{ getSubjects(teacher.id_teacher) }}</td>
              <td>{{ teacher.room_assigned?.number || 'Не назначен' }}</td>
            </tr>
          </tbody>
        </table>
        <p v-else>Список учителей пуст.</p>
      </div>

      <div v-if="showAddTeacherModal" class="modal-overlay">
        <div class="modal-content">
          <form @submit.prevent="addTeacher">
            <input v-model="newTeacher.surname" type="text" placeholder="Фамилия" required />
            <input v-model="newTeacher.name" type="text" placeholder="Имя" required />

            <div class="form-group">
              <label for="room" class="form-label">Назначить комнату (опционально):</label>
              <select v-model="newTeacher.room_assigned_id" id="room" class="form-select">
                <option value="">Выберите комнату</option>
                <option v-for="room in rooms" :key="room.id_room" :value="room.id_room">
                  №{{ room.number }} - {{ room.status }}
                </option>
              </select>
              <small class="form-hint">Вы можете оставить это поле пустым.</small>
            </div>

            <div class="modal-actions">
              <button type="submit" class="save-button">Сохранить</button>
              <button @click="closeModal" type="button" class="cancel-button">Отмена</button>
            </div>
          </form>
        </div>
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
  data() {
    return {
      teachers: [],
      rooms: [],
      lessons: [],
      newTeacher: {
        surname: '',
        name: '',
        room_assigned_id: null,
      },
      showAddTeacherModal: false,
    };
  },
  created() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      try {
        const [teachersResponse, roomsResponse, lessonsResponse] = await Promise.all([
          apiClient.get('teachers/'),
          apiClient.get('rooms/'),
          apiClient.get('lessons/'),
        ]);

        this.teachers = teachersResponse.data;
        this.rooms = roomsResponse.data;
        this.lessons = lessonsResponse.data;
      } catch (error) {
        console.error('Ошибка при загрузке данных:', error);
      }
    },

    getSubjects(teacherId) {
      const teacherLessons = this.lessons.filter(lesson => lesson.teacher === teacherId);
      if (teacherLessons.length > 0) {
        const uniqueSubjects = [...new Set(teacherLessons.map(lesson => lesson.subject))];
        return uniqueSubjects.join(', ') || 'Нет данных';
      }
      return 'Нет предметов';
    },

    async addTeacher() {
      try {
        const teacherData = { ...this.newTeacher };
        if (!teacherData.room_assigned_id) {
          teacherData.room_assigned_id = null;
        }

        const response = await apiClient.post('teachers/', teacherData);
        this.teachers.push(response.data);
        this.closeModal();
        this.resetNewTeacher();
      } catch (error) {
        console.error('Ошибка при добавлении учителя:', error);
      }
    },
    closeModal() {
      this.showAddTeacherModal = false;
    },
    resetNewTeacher() {
      this.newTeacher = {
        surname: '',
        name: '',
        room_assigned_id: null,
      };
    },
  },
};
</script>
