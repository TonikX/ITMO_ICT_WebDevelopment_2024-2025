<template>
  <div>
    <h2>Employee List</h2>
    <table class="employee-table">
      <thead>
        <tr>
          <th>Username</th>
          <th>Age</th>
          <th>Education</th>
          <th>Experience</th>
          <th>Passport Data</th>
          <th>Action</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="employee in employees" :key="employee.id">
          <td>{{ employee.name }}</td>
          <td>{{ employee.age }}</td>
          <td>{{ employee.education }}</td>
          <td>{{ employee.experience }}</td>
          <td>{{ employee.passport_data }}</td>
          <td>
            <button @click="deleteEmployee(employee.id)">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>

    <h3>Add New Employee</h3>
    <form @submit.prevent="addEmployee" class="add-employee-form">
      <label>
        Name:
        <input v-model="newEmployee.name" type="text" required class="input-field" />
      </label>
      <label>
        Age:
        <input v-model="newEmployee.age" type="number" required class="input-field" />
      </label>
      <label>
        Education:
        <input v-model="newEmployee.education" type="text" required class="input-field" />
      </label>
      <label>
        Experience:
        <input v-model="newEmployee.experience" type="number" required class="input-field" />
      </label>
      <label>
        Passport Data:
        <input v-model="newEmployee.passport_data" type="text" required class="input-field" />
      </label>
      <button type="submit" class="add-button">Add Employee</button>
    </form>

    <div>
      <router-link to="/crewmembers">
        <button>Crew Members</button>
      </router-link>
      <router-link to="/flights">
        <button>Flights</button>
      </router-link>
      <router-link to="/aircrafts">
        <button>Aircrafts</button>
      </router-link>
      <router-link to="/profile">
        <button>Back to Profile</button>
      </router-link>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return {
      employees: [],
      newEmployee: {
        name: '',
        age: 0,
        education: '',
        experience: 0,
        passport_data: '',
      },
    };
  },
  mounted() {
    this.fetchEmployees();
  },
  methods: {
    fetchEmployees() {
      axios.get('http://localhost:8000/my_avia_app/api/employees/')
        .then(response => {
          this.employees = response.data;
        })
        .catch(error => {
          console.error(error);
        });
    },
    addEmployee() {
      axios.post('http://localhost:8000/my_avia_app/api/employees/', this.newEmployee)
        .then(() => {
          this.newEmployee = {
            name: '',
            age: 0,
            education: '',
            experience: 0,
            passport_data: '',
          };
          this.fetchEmployees();
        })
        .catch(error => {
          console.error(error);
        });
    },
    deleteEmployee(employeeId) {
      axios.delete(`http://localhost:8000/my_avia_app/api/employees/${employeeId}/`)
        .then(() => {
          this.fetchEmployees();
        })
        .catch(error => {
          console.error(error);
        });
    },
  },
};
</script>
<style scoped>
.employee-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}
.employee-table th,
.employee-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}
.employee-table th {
  background-color: #f4f4f4;
}
.add-employee-form {
  margin-top: 20px;
}
.input-field {
  width: 200px;
  padding: 8px;
  margin-bottom: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}
button {
  background-color: #007BFF;
  color: #fff;
  padding: 10px 15px;
  border: none;
  border-radius:
  }
</style>