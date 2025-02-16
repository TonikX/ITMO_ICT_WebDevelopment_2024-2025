<template>
  <div v-if="teacher">
    <h1>Преподователь</h1>
    
    <div v-if="!editMode">
      <p><strong>ФИО:</strong> {{ teacher.name }}</p>
      <p><strong>Должность:</strong> {{ teacher.job_title }}</p>
      <button @click="toggleEdit">Edit Info</button>
    </div>
    <div v-else>
      <h2>Edit Teacher Info</h2>
      <form @submit.prevent="saveTeacher">
        <div class="form-group">
          <label for="name">ФИО:</label>
          <input id="name" v-model="editTeacher.name" type="text" required />
        </div>
        <div class="form-group">
          <label for="job_title">Должность:</label>
          <input id="job_title" v-model="editTeacher.job_title" type="text" required />
        </div>
        <div class="form-buttons">
          <button type="submit">Сохранить</button>
          <button type="button" @click="cancelEdit">Отменить</button>
        </div>
      </form>
    </div>

    <h2>Разрешения на преподование</h2>
    <div v-if="permits.length">
      <ul>
        <li v-for="permit in permits" :key="permit.id">
          Дисциплина: {{ permit.discipline.discipline_name }}
          <button @click="removePermit(permit.id)">Удалить</button>
        </li>
      </ul>
    </div>
    <div v-else>
      <p>Нет разрешений на преподования</p>
    </div>
    <h3>Добавить новое разрешение</h3>
    <form @submit.prevent="addPermit">
      <div class="form-group">
        <label for="new-discipline">ID дисциплины:</label>
        <input id="new-discipline" v-model="newPermit.discipline" type="text" required />
      </div>
      <button type="submit">Добавить разрешение</button>
    </form>

    <h2>Расписание</h2>
    <div v-if="schedule.length">
      <table>
        <thead>
          <tr>
            <th>Дата</th>
            <th>Номер пары</th>
            <th>Группа</th>
            <th>Дисциплина</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="session in schedule" :key="session.class_id">
            <td>{{ session.date }}</td>
            <td>{{ session.classes_order_number }}</td>
            <td>{{ session.group_id }}</td>
            <td>{{ session.discipline_id }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else>
      <p>Нет расписания для этого учителя</p>
    </div>
  </div>
  <div v-else>
    <p>Загрузка...</p>
  </div>
</template>

<script>
import api from '@/api';

export default {
  name: 'TeacherDetail',
  props: ['id'],
  data() {
    return {
      teacher: null,
      editMode: false,
      editTeacher: {},
      permits: [],
      newPermit: { discipline: '' },
      schedule: []
    }
  },
  created() {
    this.fetchTeacher();
    this.fetchPermits();
    this.fetchSchedule();
  },
  methods: {
    fetchTeacher() {
      api.get(`http://localhost:8000/api/teachers/${this.id}/`)
        .then(response => {
          this.teacher = response.data;
        })
        .catch(error => {
          console.error('Error fetching teacher:', error);
        });
    },
    toggleEdit() {
      this.editMode = true;
      this.editTeacher = { ...this.teacher };
    },
    cancelEdit() {
      this.editMode = false;
      this.editTeacher = {};
    },
    saveTeacher() {
      api.patch(`http://localhost:8000/api/teachers/${this.id}/`, this.editTeacher)
        .then(response => {
          this.teacher = response.data;
          this.editMode = false;
        })
        .catch(error => {
          console.error('Error updating teacher:', error);
        });
    },
    fetchPermits() {
      api.get(`http://localhost:8000/api/teachingpermits/?teacher=${this.id}`)
        .then(response => {
          this.permits = response.data;
        })
        .catch(error => {
          console.error('Error fetching permits:', error);
        });
    },
    addPermit() {
      const permitData = {
        teacher: this.id,
        discipline: this.newPermit.discipline
      };
      api.post(`http://localhost:8000/api/teachingpermits/`, permitData)
        .then(response => {
          this.fetchPermits();
          this.newPermit.discipline = '';
        })
        .catch(error => {
          console.error('Error adding permit:', error);
        });
    },
    removePermit(permitId) {
      api.delete(`http://localhost:8000/api/teachingpermits/${permitId}/`)
        .then(response => {
          this.fetchPermits();
        })
        .catch(error => {
          console.error('Error removing permit:', error);
        });
    },
    fetchSchedule() {
      api.get(`http://localhost:8000/api/classsessions/?teacher_id=${this.id}`)
        .then(response => {
          this.schedule = response.data;
        })
        .catch(error => {
          console.error('Error fetching schedule:', error);
        });
    }
  }
}
</script>

<style scoped>
h1, h2, h3 {
  margin-bottom: 10px;
}

p {
  margin-bottom: 10px;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}

table, th, td {
  border: 1px solid #ccc;
}

th, td {
  padding: 8px;
  text-align: left;
}

.form-group {
  margin-bottom: 10px;
}

.form-group label {
  display: block;
  font-weight: bold;
  margin-bottom: 5px;
}

.form-group input {
  width: 100%;
  padding: 8px;
  box-sizing: border-box;
}

.form-buttons {
  display: flex;
  gap: 10px;
}
</style>
