<template>
  <div>
    <h2>Groups</h2>
    <div>
      <label for="group-select">Select Group:</label>
      <select id="group-select" v-model="selectedGroup" @change="onGroupChange">
        <option value="" disabled>Select a group</option>
        <option v-for="group in groups" :key="group.group_id" :value="group.group_id">
          {{ group.group_id }}
        </option>
      </select>
    </div>

    <div v-if="selectedGroup">
      <h3>Schedule for Group {{ selectedGroup }}</h3>
      <div v-if="schedule.length">
        <table>
          <thead>
            <tr>
              <th>Date</th>
              <th>Start Hour</th>
              <th>Duration</th>
              <th>Teacher</th>
              <th>Discipline</th>
              <th>Auditorium</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="session in schedule" :key="session.class_id">
              <td>{{ session.date }}</td>
              <td>{{ getStartHour(session.classes_order_number) }}</td>
              <td>1:30</td>
              <td>{{ getTeacherName(session.teacher_id) }}</td>
              <td>{{ session.discipline_id }}</td>
              <td>{{ getAuditoriumNumber(session.classroom_id) }}</td>
            </tr>
          </tbody>
        </table>
      </div>
      <div v-else>
        <p>No schedule available for this group.</p>
      </div>

      <h3>Students in Group {{ selectedGroup }}</h3>
      <div v-if="students.length">
        <ul>
          <li v-for="student in students" :key="student.student_id">
            {{ student.fio }}
          </li>
        </ul>
      </div>
      <div v-else>
        <p>No students found for this group.</p>
      </div>
    </div>
  </div>
</template>

<script>
import api from '@/api';

export default {
  name: "GroupsView",
  data() {
    return {
      groups: [],
      selectedGroup: '',
      schedule: [],
      students: [],
      teachers: [],
      classrooms: []
    }
  },
  created() {
    this.fetchGroups();
    this.fetchTeachers();
    this.fetchClassrooms();
  },
  methods: {
    fetchGroups() {
      api.get("http://localhost:8000/api/groups/")
        .then(response => {
          this.groups = response.data;
        })
        .catch(error => {
          console.error("Error fetching groups:", error);
        });
    },
    fetchTeachers() {
      api.get("http://localhost:8000/api/teachers/")
        .then(response => {
          this.teachers = response.data;
        })
        .catch(error => {
          console.error("Error fetching teachers:", error);
        });
    },
    fetchClassrooms() {
      api.get("http://localhost:8000/api/classrooms/")
        .then(response => {
          this.classrooms = response.data;
        })
        .catch(error => {
          console.error("Error fetching classrooms:", error);
        });
    },
    onGroupChange() {
      if (this.selectedGroup) {
        this.fetchSchedule();
        this.fetchStudents();
      } else {
        this.schedule = [];
        this.students = [];
      }
    },
    fetchSchedule() {
      api.get(`http://localhost:8000/api/classsessions/?group_id=${this.selectedGroup}`)
        .then(response => {
          this.schedule = response.data;
        })
        .catch(error => {
          console.error("Error fetching schedule:", error);
        });
    },
    fetchStudents() {
      api.get(`http://localhost:8000/api/students/?group_id=${this.selectedGroup}`)
        .then(response => {
          this.students = response.data;
        })
        .catch(error => {
          console.error("Error fetching students:", error);
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
    getTeacherName(teacher_id) {
      const teacher = this.teachers.find(t => t.teacher_id === teacher_id);
      return teacher ? teacher.name : teacher_id;
    },
    getAuditoriumNumber(classroom_id) {
      const classroom = this.classrooms.find(c => c.classroom_id === classroom_id);
      return classroom ? classroom.number : classroom_id;
    }
  }
}
</script>

<style scoped>
h2 {
  margin-top: 20px;
}

select {
  margin: 10px 0;
  padding: 5px;
  font-size: 16px;
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

ul {
  list-style-type: disc;
  padding-left: 20px;
}
</style>