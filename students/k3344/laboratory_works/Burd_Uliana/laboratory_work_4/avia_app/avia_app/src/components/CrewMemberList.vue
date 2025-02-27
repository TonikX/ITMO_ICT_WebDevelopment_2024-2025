<template>
  <div>
    <h2>Crew Members List</h2>
    <table class="crew-member-table">
      <thead>
        <tr>
          <th>Name</th>
          <th>Position</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="crewMember in crewMembers" :key="crewMember.id">
          <td>{{ crewMember.name }}</td>
          <td>{{ crewMember.position }}</td>
           <td>
            <button @click="deleteCrewMember(crewMember.id)">Delete</button>
          </td>
        </tr>
      </tbody>

    </table>

    <h3>Add New Crew Member</h3>
    <form @submit.prevent="addCrewMember" class="add-crew-member-form">
      <label>
        Name:
        <input v-model="newCrewMember.name" type="text" required class="input-field" />
      </label>
      <label>
        Position:
        <input v-model="newCrewMember.position" type="text" required class="input-field" />
      </label>
      <button type="submit" class="add-button">Add Crew Member</button>
    </form>
  </div>
  <div>
       <router-link to="/employees">
        <button>Employees</button>
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
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return {
      crewMembers: [],
      newCrewMember: {
        name: '',
        position: '',
      },
    };
  },
  mounted() {
    this.fetchCrewMembers();
  },
  methods: {
    fetchCrewMembers() {
      axios.get('http://localhost:8000/my_avia_app/api/crew-members/')
        .then(response => {
          this.crewMembers = response.data;
        })
        .catch(error => {
          console.error(error);
        });
    },
    addCrewMember() {
      axios.post('http://localhost:8000/my_avia_app/api/crew-members/', this.newCrewMember)
        .then(() => {
          this.newCrewMember = {
            name: '',
            position: '',
          };
          this.fetchCrewMembers();
        })
        .catch(error => {
          console.error(error);
        });
    },
    deleteCrewMember(crewMemberId) {
      axios.delete(`http://localhost:8000/my_avia_app/api/crew-members/${crewMemberId}/`)
        .then(() => {
          this.fetchCrewMembers();
        })
        .catch(error => {
          console.error(error);
        });
    },
  },
};
</script>
<style scoped>
.crew-member-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}
.crew-member-table th,
.crew-member-table td {
  border: 1px solid #ddd;
  padding: 8px;
  text-align: left;
}
.crew-member-table th {
  background-color: #f4f4f4;
}
.add-crew-member-form {
  margin-top: 20px;
}
.input-field {
  width: 200px;
  padding: 8px;
  margin-bottom: 10px;
  border: 1px solid #ddd;
  border-radius: 4px;
}
.add-button {
  background-color: #007BFF;
  color: #fff;
  padding: 10px 15px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}
.add-button:hover {
  background-color: #0056b3;
}
</style>