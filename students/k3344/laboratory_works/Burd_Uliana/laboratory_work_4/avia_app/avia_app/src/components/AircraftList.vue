<template>
  <div class="list-container ">
    <h2>Aircraft List</h2>
    <table class="aircraft-table">
      <thead>
        <tr>
          <th>Number</th>
          <th>Type</th>
          <th>Seats</th>
          <th>Speed</th>
          <th>Carrier</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="aircraft in aircrafts" :key="aircraft.id">
          <td>{{ aircraft.number }}</td>
          <td>{{ aircraft.type }}</td>
          <td>{{ aircraft.seats }}</td>
          <td>{{ aircraft.speed }}</td>
          <td>{{ aircraft.carrier }}</td>
          <button @click="deleteAircraft(aircraft.id)">Delete</button>
        </tr>
      </tbody>
    </table>
    <div claa="add-form">
        <h3>Add New Aircraft</h3>
        <form @submit.prevent="addAircraft" class="add-aircraft-form">
          <label>
            Number:
            <input v-model="newAircraft.number" type="text" required class="input-field" />
          </label>
          <label>
            Type:
            <input v-model="newAircraft.type" type="text" required class="input-field" />
          </label>
          <label>
            Seats:
            <input v-model="newAircraft.seats" type="number" required class="input-field" />
          </label>
          <label>
            Speed:
            <input v-model="newAircraft.speed" type="number" required class="input-field" />
          </label>
          <label>
            Carrier:
            <input v-model="newAircraft.carrier" type="text" required class="input-field" />
          </label>
          <button type="submit" class="add-button">Add Aircraft</button>
        </form>
        <div>
          <router-link to="/crewmembers">
            <button>Crew Members</button>
          </router-link>
          <router-link to="/flights">
            <button>Flights</button>
          </router-link>
          <router-link to="/employees">
            <button>Employees</button>
          </router-link>
          <router-link to="/profile">
            <button>Back to Profile</button>
          </router-link>
        </div>
       </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return {
      aircrafts: [],
      newAircraft: {
        number: '',
        type: '',
        seats: 0,
        speed: 0,
        carrier: '',
      },
    };
  },
  mounted() {
    this.fetchAircrafts();
  },
  methods: {
    fetchAircrafts() {
      axios.get('http://localhost:8000/my_avia_app/api/aircrafts/')
        .then(response => {
          this.aircrafts = response.data;
        })
        .catch(error => {
          console.error(error);
        });
    },
    addAircraft() {
      axios.post('http://localhost:8000/my_avia_app/api/aircrafts/', this.newAircraft)
        .then(() => {
          this.newAircraft = {
            number: '',
            type: '',
            seats: 0,
            speed: 0,
            carrier: '',
          };
          this.fetchAircrafts();
        })
        .catch(error => {
          console.error(error);
        });
    },
     deleteAircraft(aircraftId) {
      axios.delete(`http://localhost:8000/my_avia_app/api/aircrafts/${aircraftId}/`)
        .then(() => {
          this.fetchAircrafts();
        })
        .catch(error => {
          console.error(error);
        });
    },
  },
};
</script>
<style scoped>
    .list-container {
      background-color: #f0f8ff;
      display: flex;
      flex-direction: column;
      padding: 20px;
      margin: 0 auto;
    }
    h2, h3 {
      text-align: center;
      color: #4CAF50;
      margin-bottom: 20px;
      font-size: 40px;
    }
    h3 {
      margin-top: 40px;
      text-align: left;
      font-size: 30px;
    }
    .aircraft-table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 20px;
      align-items: center;
    }
    .aircraft-table th,
    .aircraft-table td {
      border: 1px solid #ddd;
      padding: 8px;
      text-align: left;
    }
    .aircraft-table th {
      background-color: #4CAF50;
      color: #fff;
    }
    .add-form{
        margin-top: 40px;
        margin-left: 40px;
    }
    .add-aircraft-form {
      display: flex;
      flex-direction: column;
      align-items: flex-start;
      margin-top: 40px;
    }
    .input-field {
      width: calc(100% - 20px);
      padding: 8px;
      margin-bottom: 7px;
      border: 1px solid #4CAF50;
      border-radius: 4px;
    }
    button {
      background-color: #4CAF50;
      color: #fff;
      padding: 10px 15px;
      border: none;
      border-radius: 3px;
      cursor: pointer;
      margin-right: 10px;
      margin-top: 10px;
    }
    .button-container {
      display: flex;
      align-items: center;
      margin-top: 20px;
    }
    .add-button{
        padding-left: 70px;
        padding-right: 70px;
        }
</style>
