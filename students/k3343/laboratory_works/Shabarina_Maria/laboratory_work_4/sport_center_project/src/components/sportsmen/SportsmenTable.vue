<template>
  <div>
    <h2>Список всех спортсменов СШ №1</h2>
    <SportsmenAddNew />
    <table>
      <thead>
      <tr>
        <th>Фамилия</th>
        <th>Имя</th>
        <th>Отчество</th>
        <th>Пол</th>
        <th>Дата рождения</th>
        <th>Номер телефона</th>
        <th>Почта</th>
        <th>Дата зачисления</th>
        <th>Изменения</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="student in students" :key="student.id">
        <td>{{ student.last_name }}</td>
        <td>{{ student.first_name }}</td>
        <td>{{ student.middle_name }}</td>
        <td>{{ student.gender === 'm' ? 'Мужской' : 'Женский' }}</td>
        <td>{{ student.date_of_birth }}</td>
        <td>{{ student.phone_number }}</td>
        <td>{{ student.email }}</td>
        <td>{{ student.registration_date }}</td>
        <td>
          <button @click="editStudent(student)">Редактировать</button>
        </td>
      </tr>
      </tbody>
    </table>

    <SportsmenEdit
      v-if="studentToEdit"
      :student="studentToEdit"
      @close="studentToEdit = null"
      @update="updateStudent"
    />
  </div>
</template>

<script>
import axios from "axios";
import SportsmenAddNew from "@/components/sportsmen/SportsmenAddNew.vue";
import SportsmenEdit from "@/components/sportsmen/SportsmenEdit.vue";

export default {
  components: {
    SportsmenAddNew,
    SportsmenEdit,
  },
  data() {
    return {
      students: [],
      studentToEdit: null,
    };
  },
  methods: {
    async fetchStudents() {
      try {
        const response = await axios.get("http://127.0.0.1:8000/sportsmen/");
        this.students = response.data;
      } catch (error) {
        console.error("Ошибка при загрузке учеников:", error);
      }
    },
    editStudent(student) {
      this.studentToEdit = { ...student };
    },
    async updateStudent(updatedStudent) {
      try {
        console.log(updatedStudent)
        await axios.put(`http://127.0.0.1:8000/sportsmen/${updatedStudent.id}/update/`, updatedStudent);
        this.students = this.students.map((student) =>
          student.id === updatedStudent.id ? updatedStudent : student
        );
        this.studentToEdit = null;
      } catch (error) {
        console.error("Ошибка при обновлении ученика:", error);
      }
    },
  },
  mounted() {
    this.fetchStudents();
  },
};
</script>


<style scoped>
div {
  margin: 3%;
}

h2 {
  text-align: center;
  color: #596dff;
}

table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
  border-radius: 10px;
  overflow: hidden;
}

table th,
table td {
  border: 1px solid #ddd;
  padding: 12px 15px;
  text-align: left;
}

table th {
  background-color: #596dff;
  color: white;
  font-weight: bold;
}

table td {
  background-color: #f8f8f8;
}

table tr:nth-child(even) td {
  background-color: #f4f4f4;
}

table tr:hover {
  background-color: #ddd;
}

button {
  color: #ffa44b;
  background: #ddd;
  border: solid 2px;
  border-radius: 5px;
}
</style>
