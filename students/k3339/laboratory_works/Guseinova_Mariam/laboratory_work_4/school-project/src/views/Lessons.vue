<template>
  <div>
    <Header />
    <div class="page-container">
      <div class="header-container">
        <h1 class="page-title">Уроки</h1>
        <button @click="openAddLessonModal" class="add-button">Добавить новый урок</button>
      </div>

      <div v-if="showAddLessonModal" class="lesson-modal">
        <div class="modal-content">
          <form @submit.prevent="addLesson">

            <div class="form-group">
              <label for="subject">Предмет</label>
              <input v-model="newLesson.subject" type="text" id="subject" required placeholder="Введите название предмета" />
            </div>

            <div class="form-group">
              <label for="teacher">Учитель</label>
              <select v-model="newLesson.id_teacher" id="teacher" required>
                <option v-for="teacher in teachers" :key="teacher.id_teacher" :value="teacher.id_teacher">
                  {{ teacher.surname }} {{ teacher.name }} {{ teacher.room_assigned?.number }}
                </option>
              </select>
            </div>

            <div class="form-group">
              <label for="room">Комната</label>
              <select v-model="newLesson.room_assigned_id" id="room" required>
                <option v-for="room in rooms" :key="room.id_room" :value="room.id_room">
                  Комната №{{ room.number }} - {{ room.status }}
                </option>
              </select>
            </div>

            <div class="form-group">
              <label for="class_label">Класс</label>
              <input v-model="newLesson.class_label" type="text" id="class_label" required placeholder="Введите класс" />
            </div>

            <div class="form-group">
              <label for="day">День недели</label>
              <select v-model="newLesson.day" id="day" required>
                <option value="Понедельник">Понедельник</option>
                <option value="Вторник">Вторник</option>
                <option value="Среда">Среда</option>
                <option value="Четверг">Четверг</option>
                <option value="Пятница">Пятница</option>
                <option value="Суббота">Суббота</option>
              </select>
            </div>

            <div class="form-group">
              <label for="lesson_number">Номер урока</label>
              <div class="lesson-number-buttons">
                <button
                  v-for="n in 8"
                  :key="n"
                  type="button"
                  :class="['lesson-number-button', { selected: newLesson.lesson_number === n }]"
                  @click="newLesson.lesson_number = n"
                >
                  {{ n }}
                </button>
              </div>
            </div>

            <button type="submit" class="save-button">Сохранить</button>
            <button @click="closeAddLessonModal" class="cancel-button">Отмена</button>

          </form>
        </div>
      </div>

      <div v-if="showEditLessonModal" class="lesson-modal">
        <div class="modal-content">
          <form @submit.prevent="updateLesson">
            <h2>Редактировать урок</h2>
            <div class="form-group">
              <label for="edit-subject">Предмет</label>
              <input v-model="editableLesson.subject" type="text" id="edit-subject" required placeholder="Введите название предмета" />
            </div>
            <div class="form-group">
              <label for="edit-teacher">Учитель</label>
              <select v-model="editableLesson.id_teacher" id="edit-teacher" required>
                <option v-for="teacher in teachers" :key="teacher.id_teacher" :value="teacher.id_teacher">
                  {{ teacher.surname }} {{ teacher.name }} {{ teacher.room_assigned?.number }}
                </option>
              </select>
            </div>

            <div class="form-group">
              <label for="room">Комната</label>
              <select v-model="editableLesson.room_assigned_id" id="room" required>
                <option v-for="room in rooms" :key="room.id_room" :value="room.id_room">
                  Комната №{{ room.number }} - {{ room.status }}
                </option>
              </select>
            </div>

            <div class="form-group">
              <label for="class_label">Класс</label>
              <input v-model="editableLesson.class_label" type="text" id="class_label" required placeholder="Введите класс" />
            </div>

            <div class="form-group">
              <label for="day">День недели</label>
              <select v-model="editableLesson.day" id="day" required>
                <option value="Понедельник">Понедельник</option>
                <option value="Вторник">Вторник</option>
                <option value="Среда">Среда</option>
                <option value="Четверг">Четверг</option>
                <option value="Пятница">Пятница</option>
                <option value="Суббота">Суббота</option>
              </select>
            </div>

            <div class="form-group">
              <label for="lesson_number">Номер урока</label>
              <div class="lesson-number-buttons">
                <button
                  v-for="n in 8"
                  :key="n"
                  type="button"
                  :class="['lesson-number-button', { selected: editableLesson.lesson_number === n }]"
                  @click="editableLesson.lesson_number = n"
                >
                  {{ n }}
                </button>
              </div>
            </div>
            <button type="submit" class="save-button">Сохранить</button>
            <button @click="closeEditLessonModal" class="cancel-button">Отмена</button>
          </form>
        </div>
      </div>

      <div v-if="teachers.length > 0 && rooms.length > 0">
        <div v-for="(lessons, day) in lessonsByDay" :key="day" class="lesson-day">
          <h2>{{ day }}</h2>
          <div v-for="lesson in lessons" :key="lesson.id_lesson" class="lesson-card">
            <p><strong> {{lesson.lesson_number }} {{ lesson.subject }}</strong></p>
            <p>Учитель: {{ lesson.teacher }}</p>
            <p>Комната: {{ lesson.room }}</p>
            <p>Класс: {{ lesson.class_label }}</p>

            <div class="lesson-card-actions">
              <button @click="openEditLessonModal(lesson)" class="edit-button">Редактировать</button>
              <button @click.stop="deleteLesson(lesson.id_lesson)" class="delete-button">Удалить</button>
            </div>
          </div>
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
      newLesson: {
        subject: '',
        id_teacher: null,
        room_assigned_id: null,
        class_label: '',
        day: '',
        lesson_number: null,
      },
      editableLesson: {},
      teachers: [],
      rooms: [],
      lessonsByDay: {},
      showModal: false,
      modalLesson: {},
      showAddLessonModal: false,
      showEditLessonModal: false,
    };
  },
  created() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      try {
        const [teachersResponse, roomsResponse] = await Promise.all([
          apiClient.get('teachers/'),
          apiClient.get('rooms/')
        ]);
        this.teachers = teachersResponse.data;
        this.rooms = roomsResponse.data;
        this.fetchLessons();
      } catch (error) {
        console.error('Ошибка при загрузке данных:', error);
      }
    },

    async fetchLessons() {
      try {
        const response = await apiClient.get('lessons/');
        const lessons = response.data;
        console.log('Загруженные уроки:', lessons);
        lessons.forEach(lesson => {
          const teacher = this.teachers.find(t => t.id_teacher === lesson.teacher);
          const room = this.rooms.find(r => r.id_room === lesson.room);

          lesson.teacher = teacher ? `${teacher.surname} ${teacher.name}` : 'Неизвестно';
          lesson.room = room ? `№${room.number}` : 'Не указан';
          lesson.class_label = lesson.class_label || 'Класс не указан';
        });
        this.lessonsByDay = this.organizeLessonsByDay(lessons);
      } catch (error) {
        console.error('Ошибка при загрузке данных уроков:', error);
      }
    },
    organizeLessonsByDay(lessons) {
      const lessonsByDay = {
        Понедельник: [],
        Вторник: [],
        Среда: [],
        Четверг: [],
        Пятница: [],
        Суббота: [],
      };

      lessons.forEach(lesson => {
        lessonsByDay[lesson.day].push(lesson);
      });

      for (const day in lessonsByDay) {
        lessonsByDay[day].sort((a, b) => a.lesson_number - b.lesson_number);
      }

      return lessonsByDay;
    },

    async addLesson() {
      try {
        if (!this.newLesson.id_teacher || !this.newLesson.room_assigned_id || !this.newLesson.class_label || !this.newLesson.subject) {
          alert('Пожалуйста, заполните все обязательные поля');
          return;
        }

        const newLesson = {
          subject: this.newLesson.subject,
          teacher: this.newLesson.id_teacher,
          room: this.newLesson.room_assigned_id,
          class_label: this.newLesson.class_label,
          day: this.newLesson.day,
          lesson_number: this.newLesson.lesson_number,
        };
        const response = await apiClient.post('lessons/', newLesson);
        this.lessonsByDay[response.data.day].push(response.data);
        this.resetNewLessonForm();
        this.closeAddLessonModal();
      } catch (error) {
        console.error('Ошибка при добавлении урока:', error);
        if (error.response) {
          console.error('Ответ от сервера:', error.response.data);
        }
      }
    },
    resetNewLessonForm() {
      this.newLesson = {
        subject: '',
        id_teacher: null,
        room_assigned_id: null,
        class_label: '',
        day: 'Понедельник',
        lesson_number: 1,
      };
    },
    openAddLessonModal() {
      this.showAddLessonModal = true;
    },
    closeAddLessonModal() {
      this.showAddLessonModal = false;
    },

    openEditLessonModal(lesson) {
      this.editableLesson = {
        id_lesson: lesson.id_lesson,
        subject: lesson.subject,
        id_teacher: lesson.id_teacher,
        room_assigned_id: lesson.room_assigned_id,
        class_label: lesson.class_label,
        day: lesson.day,
        lesson_number: lesson.lesson_number,
      };
      this.showEditLessonModal = true;
    },

    async updateLesson() {
      try {
        console.log('Данные для обновления:', this.editableLesson);
        await apiClient.put(`lessons/${this.editableLesson.id_lesson}/`, {
          subject: this.editableLesson.subject,
          teacher: this.editableLesson.id_teacher,
          room: this.editableLesson.room_assigned_id,
          class_label: this.editableLesson.class_label,
          day: this.editableLesson.day,
          lesson_number: this.editableLesson.lesson_number,
        });
        this.fetchLessons();
        this.closeEditLessonModal();
      } catch (error) {
        console.error('Ошибка при обновлении урока:', error.response?.data || error);
        alert(`Ошибка: ${JSON.stringify(error.response?.data || error)}`);
      }
    },

    closeEditLessonModal() {
      this.showEditLessonModal = false;
    },

    async deleteLesson(lessonId) {
      try {
        await apiClient.delete(`lessons/${lessonId}/`);
        this.fetchLessons();
        this.closeModal();
      } catch (error) {
        console.error('Ошибка при удалении урока:', error);
      }
    },
  },
};
</script>
