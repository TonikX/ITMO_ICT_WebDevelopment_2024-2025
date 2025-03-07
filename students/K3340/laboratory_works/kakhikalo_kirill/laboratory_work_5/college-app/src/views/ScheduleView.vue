<template>
  <div>
    <h2>Schedule</h2>
    
    <form @submit.prevent="applyFilters" class="filter-form">
      <div class="filter-group">
        <label for="filterGroup">Group:</label>
        <select id="filterGroup" v-model="filterGroup">
          <option value="">-- All Groups --</option>
          <option v-for="group in groups" :key="group.group_id" :value="group.group_id">
            {{ group.group_id }}
          </option>
        </select>
      </div>
      
      <div class="filter-group">
        <label for="filterTeacher">Teacher:</label>
        <select id="filterTeacher" v-model="filterTeacher">
          <option value="">-- All Teachers --</option>
          <option v-for="teacher in teachers" :key="teacher.teacher_id" :value="teacher.teacher_id">
            {{ teacher.name }}
          </option>
        </select>
      </div>
      
      <div class="filter-group">
        <label for="filterAuditorium">Auditorium:</label>
        <select id="filterAuditorium" v-model="filterAuditorium">
          <option value="">-- All Auditoriums --</option>
          <option v-for="classroom in classrooms" :key="classroom.classroom_id" :value="classroom.classroom_id">
            {{ classroom.number }} ({{ classroom.type }})
          </option>
        </select>
      </div>
      
      <div class="filter-buttons">
        <button type="submit">Apply Filters</button>
        <button type="button" @click="resetFilters">Reset</button>
      </div>
    </form>
    
    <div v-if="sessions.length">
      <table>
        <thead>
          <tr>
            <th>Date</th>
            <th>Start Hour</th>
            <th>Duration</th>
            <th>Group</th>
            <th>Teacher</th>
            <th>Discipline</th>
            <th>Auditorium</th>
            <th>Type</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="session in sessions" :key="session.class_id">
            <td>{{ session.date }}</td>
            <td>{{ getStartHour(session.classes_order_number) }}</td>
            <td>1:30</td>
            <td>{{ session.group_id }}</td>
            <td>{{ getTeacherName(session.teacher_id) }}</td>
            <td>{{ session.discipline_id }}</td>
            <td>{{ getAuditoriumNumber(session.classroom_id) }}</td>
            <td>{{ session.type }}</td>
          </tr>
        </tbody>
      </table>
    </div>
    <div v-else>
      <p>No schedule found.</p>
    </div>
  </div>
</template>

<script>
import api from '@/api';

export default {
  name: "ScheduleView",
  data() {
    return {
      sessions: [],
      filterGroup: "",
      filterTeacher: "",
      filterAuditorium: "",
      groups: [],
      teachers: [],
      classrooms: []
    };
  },
  created() {
    this.fetchFiltersData();
    this.fetchSchedule();
  },
  methods: {
    fetchSchedule() {
      const params = {};
      if (this.filterGroup) params.group_id = this.filterGroup;
      if (this.filterTeacher) params.teacher_id = this.filterTeacher;
      if (this.filterAuditorium) params.classroom_id = this.filterAuditorium;
      
      api.get("http://localhost:8000/api/classsessions/", { params })
        .then(response => {
          this.sessions = response.data;
        })
        .catch(error => {
          console.error("Error fetching schedule:", error);
        });
    },
    applyFilters() {
      this.fetchSchedule();
    },
    resetFilters() {
      this.filterGroup = "";
      this.filterTeacher = "";
      this.filterAuditorium = "";
      this.fetchSchedule();
    },
    fetchFiltersData() {
      api.get("http://localhost:8000/api/groups/")
        .then(response => {
          this.groups = response.data;
        })
        .catch(error => {
          console.error("Error fetching groups:", error);
        });
      
      api.get("http://localhost:8000/api/teachers/")
        .then(response => {
          this.teachers = response.data;
        })
        .catch(error => {
          console.error("Error fetching teachers:", error);
        });
      
      api.get("http://localhost:8000/api/classrooms/")
        .then(response => {
          this.classrooms = response.data;
        })
        .catch(error => {
          console.error("Error fetching classrooms:", error);
        });
    },
    getStartHour(orderNumber) {
      const mapping = {
        1: "8:20",
        2: "10:00",
        3: "11:20",
        4: "13:10",
        5: "15:20",
        6: "17:00"
      };
      return mapping[orderNumber] || "Unknown";
    },
    getAuditoriumNumber(classroom_id) {
      const classroom = this.classrooms.find(c => c.classroom_id === classroom_id);
      return classroom ? classroom.number : classroom_id;
    },
    getTeacherName(teacher_id) {
      const teacher = this.teachers.find(t => t.teacher_id === teacher_id);
      return teacher ? teacher.name : teacher_id;
    }
  }
}
</script>

<style scoped>
h2 {
  margin-top: 20px;
}

.filter-form {
  margin-bottom: 20px;
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
  align-items: flex-end;
}
.filter-group {
  display: flex;
  flex-direction: column;
}
.filter-group label {
  font-weight: bold;
  margin-bottom: 5px;
}
.filter-form select {
  padding: 5px;
  font-size: 14px;
}
.filter-buttons {
  display: flex;
  gap: 10px;
  align-items: center;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-bottom: 20px;
}
th, td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: left;
}
</style>
