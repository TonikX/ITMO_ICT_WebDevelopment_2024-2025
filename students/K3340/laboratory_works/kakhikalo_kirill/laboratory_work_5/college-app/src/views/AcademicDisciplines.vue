<template>
  <div>
    <h2>Education Programs</h2>
    <table>
      <thead>
        <tr>
          <th>Program Code</th>
          <th>Program Type</th>
          <th>Duration</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="program in programs" :key="program.programm_code">
          <td>{{ program.programm_code }}</td>
          <td>{{ program.programm_type }}</td>
          <td>{{ program.duration }}</td>
          <td>
            <button @click="removeProgram(program.programm_code)">Remove</button>
          </td>
        </tr>
      </tbody>
    </table>
    <h3>Add New Program</h3>
    <form @submit.prevent="addProgram">
      <input v-model="newProgram.programm_code" placeholder="Program Code" required />
      <input v-model="newProgram.programm_type" placeholder="Program Type" required />
      <input v-model.number="newProgram.duration" placeholder="Duration" type="number" required />
      <button type="submit">Add Program</button>
    </form>

    <h2>Program Elements</h2>
    <table>
      <thead>
        <tr>
          <th>Program Code</th>
          <th>Discipline ID</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="element in programElements" :key="element.programm_code + '-' + element.discipline.discipline_id">
          <td>{{ element.programm_code }}</td>
          <td>{{ element.discipline }}</td>
          <td>
            <button @click="removeProgramElement(element.programm_code, element.discipline.discipline_id)">Remove</button>
          </td>
        </tr>
      </tbody>
    </table>
    <h3>Add New Program Element</h3>
    <form @submit.prevent="addProgramElement">
      <input v-model="newProgramElement.programm_code" placeholder="Program Code" required />
      <input v-model="newProgramElement.discipline" placeholder="Discipline ID" required />
      <button type="submit">Add Program Element</button>
    </form>

    <h2>Academic Disciplines</h2>
    <table>
      <thead>
        <tr>
          <th>Discipline ID</th>
          <th>Discipline Name</th>
          <th>Practice Duration</th>
          <th>Total Duration</th>
          <th>Attestation Type</th>
          <th>Actions</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="discipline in disciplines" :key="discipline.discipline_id">
          <td>{{ discipline.discipline_id }}</td>
          <td>{{ discipline.discipline_name }}</td>
          <td>{{ discipline.practice_duration }}</td>
          <td>{{ discipline.total_duration }}</td>
          <td>{{ discipline.attestation_type }}</td>
          <td>
            <button @click="removeDiscipline(discipline.discipline_id)">Remove</button>
          </td>
        </tr>
      </tbody>
    </table>
    <h3>Add New Discipline</h3>
    <form @submit.prevent="addDiscipline">
      <input v-model="newDiscipline.discipline_id" placeholder="Discipline ID" required />
      <input v-model="newDiscipline.discipline_name" placeholder="Discipline Name" required />
      <input v-model.number="newDiscipline.practice_duration" placeholder="Practice Duration" type="number" required />
      <input v-model.number="newDiscipline.total_duration" placeholder="Total Duration" type="number" required />
      <input v-model="newDiscipline.attestation_type" placeholder="Attestation Type" required />
      <button type="submit">Add Discipline</button>
    </form>
  </div>
</template>

<script>
import api from '@/api';

export default {
  name: 'AcademicDisciplines',
  data() {
    return {
      programs: [],
      programElements: [],
      disciplines: [],
      newProgram: { programm_code: '', programm_type: '', duration: 0 },
      newProgramElement: { programm_code: '', discipline: '', practical_hours: 0, lecture_hours: 0 },
      newDiscipline: { discipline_id: '', discipline_name: '', practice_duration: 0, total_duration: 0, attestation_type: '' }
    }
  },
  created() {
    this.fetchPrograms();
    this.fetchProgramElements();
    this.fetchDisciplines();
  },
  methods: {
    fetchPrograms() {
      api.get("http://localhost:8000/api/educationprograms/")
        .then(response => {
          this.programs = response.data;
        })
        .catch(error => {
          console.error("Error fetching programs:", error);
        });
    },
    fetchProgramElements() {
      api.get("http://localhost:8000/api/programelements/")
        .then(response => {
          this.programElements = response.data;
        })
        .catch(error => {
          console.error("Error fetching program elements:", error);
        });
    },
    fetchDisciplines() {
      api.get("http://localhost:8000/api/academicdisciplines/")
        .then(response => {
          this.disciplines = response.data;
        })
        .catch(error => {
          console.error("Error fetching disciplines:", error);
        });
    },
    addProgram() {
      api.post("http://localhost:8000/api/educationprograms/", this.newProgram)
        .then(response => {
          this.fetchPrograms();
          this.newProgram = { programm_code: '', programm_type: '', duration: 0 };
        })
        .catch(error => {
          console.error("Error adding program:", error);
        });
    },
    removeProgram(programm_code) {
      api.delete(`http://localhost:8000/api/educationprograms/${programm_code}/`)
        .then(response => {
          this.fetchPrograms();
        })
        .catch(error => {
          console.error("Error removing program:", error);
        });
    },
    addProgramElement() {
      api.post("http://localhost:8000/api/programelements/", this.newProgramElement)
        .then(response => {
          this.fetchProgramElements();
          this.newProgramElement = { programm_code: '', discipline: '', practical_hours: 0, lecture_hours: 0 };
        })
        .catch(error => {
          console.error("Error adding program element:", error);
        });
    },
    removeProgramElement(programm_code, discipline) {
      api.delete(`http://localhost:8000/api/programelements/${programm_code}/${discipline}/`)
        .then(response => {
          this.fetchProgramElements();
        })
        .catch(error => {
          console.error("Error removing program element:", error);
        });
    },
    addDiscipline() {
      api.post("http://localhost:8000/api/academicdisciplines/", this.newDiscipline)
        .then(response => {
          this.fetchDisciplines();
          this.newDiscipline = { discipline_id: '', discipline_name: '', practice_duration: 0, total_duration: 0, attestation_type: '' };
        })
        .catch(error => {
          console.error("Error adding discipline:", error);
        });
    },
    removeDiscipline(discipline_id) {
      api.delete(`http://localhost:8000/api/academicdisciplines/${discipline_id}/`)
        .then(response => {
          this.fetchDisciplines();
        })
        .catch(error => {
          console.error("Error removing discipline:", error);
        });
    }
  }
}
</script>

<style scoped>
h2 {
  margin-top: 20px;
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
form {
  margin-bottom: 20px;
}
input {
  padding: 5px;
  margin-right: 5px;
}
button {
  padding: 5px 10px;
  margin: 5px 0;
}
</style>
