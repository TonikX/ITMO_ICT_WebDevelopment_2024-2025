<template>
  <div>
    <Header />
    <div class="page-container">
      <h1 class="page-title">Детальная информация об учителе</h1>

      <div v-if="teacher" class="teacher-info">
        <p><strong>Фамилия:</strong> {{ teacher.surname }}</p>
        <p><strong>Имя:</strong> {{ teacher.name }}</p>
        <p><strong>Закреплённая комната:</strong>
          {{ teacher.room_assigned ? `${teacher.room_assigned.number}  ${teacher.room_assigned.status}` : 'Не назначена' }}
        </p>
        <div class="button-group">
          <button @click="toggleEditForm" class="edit-button">Редактировать</button>
          <button @click="deleteTeacher" class="delete-button">Удалить</button>
        </div>
      </div>
      <div v-if="schedule.length > 0" class="schedule-container">
        <h2>Расписание уроков</h2>
        <table class="schedule-table">
          <thead>
            <tr>
              <th>День недели</th>
              <th>Номер урока</th>
              <th>Предмет</th>
              <th>Класс</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="lesson in schedule" :key="lesson.id_lesson">
              <td>{{ lesson.day }}</td>
              <td>{{ lesson.lesson_number }}</td>
              <td>{{ lesson.subject }}</td>
              <td>{{ lesson.class_label }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-if="showEditForm" class="edit-form">
        <h2>Редактировать данные учителя</h2>
        <form @submit.prevent="updateTeacher">
          <input v-model="editedTeacher.surname" type="text" placeholder="Фамилия" required />
          <input v-model="editedTeacher.name" type="text" placeholder="Имя" required />
          <div class="form-group">
            <label for="room" class="form-label">Комната (опционально):</label>
            <select v-model="editedTeacher.room_assigned_id" id="room" class="form-select">
              <option value="">Выберите комнату</option>
              <option v-for="room in rooms" :key="room.id_room" :value="room.id_room">
               №{{ room.number }} - {{ room.status }}
              </option>
            </select>
          </div>

          <div class="form-actions">
            <button type="submit" class="save-button">Сохранить</button>
            <button @click="cancelEdit" type="button" class="cancel-button">Отмена</button>
          </div>
        </form>
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
      teacher: null,
      schedule: [],
      rooms: [],
      showEditForm: false,
      editedTeacher: {
        surname: '',
        name: '',
        room_assigned_id: null,
      },
    };
  },
  created() {
    this.fetchTeacher();
    this.fetchRooms();
    this.fetchSchedule();
  },
  methods: {
    async fetchTeacher() {
      try {
        const response = await apiClient.get(`teachers/${this.id}/`);
        this.teacher = response.data;
        this.editedTeacher = {
          ...response.data,
          room_assigned_id: response.data.room_assigned?.id_room || null,
        };
      } catch (error) {
        console.error('Ошибка при загрузке данных учителя:', error);
      }
    },
    async fetchSchedule() {
      try {
        const response = await apiClient.get('lessons/');
        const allLessons = response.data;
        this.schedule = allLessons.filter(lesson => lesson.teacher === Number(this.id));
      } catch (error) {
        console.error('Ошибка при загрузке расписания уроков:', error);
      }
    },

    async fetchRooms() {
      try {
        const response = await apiClient.get('rooms/');
        this.rooms = response.data;
      } catch (error) {
        console.error('Ошибка при загрузке списка кабинетов:', error);
      }
    },

    toggleEditForm() {
      this.showEditForm = true;
    },

    async updateTeacher() {
      try {
        const updatedData = { ...this.editedTeacher };
        if (!updatedData.room_assigned_id) {
          updatedData.room_assigned_id = null;
        }

        const response = await apiClient.put(`teachers/${this.id}/`, updatedData);
        this.teacher = response.data;
        this.showEditForm = false;
      } catch (error) {
        console.error('Ошибка при обновлении данных учителя:', error);
      }
    },

    async deleteTeacher() {
      if (confirm('Вы уверены, что хотите удалить этого учителя?')) {
        try {
          await apiClient.delete(`teachers/${this.id}/`);
          alert('Учитель успешно удалён.');
          this.$router.push('/teachers');
        } catch (error) {
          console.error('Ошибка при удалении учителя:', error);
        }
      }
    },
    cancelEdit() {
      this.showEditForm = false;
      this.editedTeacher = { ...this.teacher };
    },
  },
};
</script>
