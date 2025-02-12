<template>
  <div>
    <h3 class="mb-4">Расписание</h3>
    <table class="table table-bordered">
      <thead class="thead-dark">
        <tr>
          <th>Учитель</th>
          <th>Предмет</th>
          <th>Кабинет</th>
          <th>Время</th>
          <th>Действия</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="(lesson, index) in schedule" :key="index">
          <td>{{ lesson.teacher }}</td>
          <td>{{ lesson.subject }}</td>
          <td>{{ lesson.classroom }}</td>
          <td>{{ lesson.time }}</td>
          <td>
            <button @click="editLesson(lesson.id)" class="btn btn-primary btn-sm">Изменить</button>
            <button @click="deleteLesson(lesson.id)" class="btn btn-danger btn-sm">Удалить</button>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- Модальное окно для редактирования -->
    <div v-if="isEditing" class="modal-overlay">
      <div class="modal-content">
        <h3>Редактировать занятие</h3>
        <label for="time">Время:</label>
        <input v-model="editedLesson.time" type="time" id="time" class="form-control" />
        <button @click="saveEdit" class="btn btn-success">Сохранить изменения</button>
        <button @click="cancelEdit" class="btn btn-secondary">Отменить</button>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      schedule: [],
      isEditing: false,
      editedLesson: {},
    };
  },
  mounted() {
    this.fetchSchedule();
  },
  methods: {
    async fetchSchedule() {
      try {
        const response = await fetch('http://127.0.0.1:8000/school/schedule/');
        const data = await response.json();
        this.schedule = data;
      } catch (error) {
        console.error('Ошибка при загрузке расписания:', error);
      }
    },
    editLesson(id) {
      const lesson = this.schedule.find((lesson) => lesson.id === id);
      this.editedLesson = { ...lesson };
      this.isEditing = true;
    },
    async saveEdit() {
      try {
        const response = await fetch(`http://127.0.0.1:8000/school/schedule/${this.editedLesson.id}/`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            time: this.editedLesson.time,
          }),
        });
        if (response.ok) {
          this.fetchSchedule();
          this.isEditing = false;
        }
      } catch (error) {
        console.error('Ошибка при сохранении изменений:', error);
      }
    },
    cancelEdit() {
      this.isEditing = false;
    },
    async deleteLesson(id) {
      try {
        const response = await fetch(`http://127.0.0.1:8000/school/schedule/${id}/`, {
          method: 'DELETE',
        });
        if (response.ok) {
          this.fetchSchedule();
        } else {
          console.error('Ошибка при удалении занятия:', response.statusText);
        }
      } catch (error) {
        console.error('Ошибка при удалении занятия:', error);
      }
    }
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
  margin-left: 20px;
}

.modal-overlay {
  background-color: rgba(0, 0, 0, 0.5);
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  justify-content: center;
  align-items: center;
}

.modal-content {
  background-color: white;
  padding: 20px;
  border-radius: 8px;
  max-width: 600px;
  width: 100%;
}

.table {
  width: 100%;
  margin: 20px 0;
}

th, td {
  padding: 10px;
  text-align: left;
}

button {
  margin: 5px;
  border-radius: 8px;
}
</style>
