<template>
  <div class="flight-list-container">
    <h2>Flight List</h2>
    <table class="flight-table">
      <thead>
        <tr>
          <th>Flight Number</th>
          <th>Distance</th>
          <th>Departure Point</th>
          <th>Destination Point</th>
          <th>Departure Datetime</th>
          <th>Arrival Datetime</th>
          <th>Sold Tickets</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="flight in flights" :key="flight.id">
          <td>{{ flight.flight_number }}</td>
          <td>{{ flight.distance }}</td>
          <td>{{ flight.departure_point }}</td>
          <td>{{ flight.destination_point }}</td>
          <td>{{ flight.departure_datetime }}</td>
          <td>{{ flight.arrival_datetime }}</td>
          <td>{{ flight.sold_tickets }}</td>
          <td>
            <button @click="deleteFlight(flight.id)" class="delete-button">Delete</button>
          </td>
        </tr>
      </tbody>
    </table>
    <div class="add-form">
        <h3>Add New Flight</h3>
        <form @submit.prevent="addFlight" class="add-flight-form">
          <label>
            Flight Number:
            <input v-model="newFlight.flight_number" type="text" required class="input-field" />
          </label>
          <br />
          <label>
            Distance:
            <input v-model="newFlight.distance" type="number" required class="input-field" />
          </label>
          <br />
          <label>
            Departure Point:
            <input v-model="newFlight.departure_point" type="text" required class="input-field" />
          </label>
          <br />
          <label>
            Destination Point:
            <input v-model="newFlight.destination_point" type="text" required class="input-field" />
          </label>
          <br />
          <label>
            Departure Datetime:
            <input v-model="newFlight.departure_datetime" type="datetime-local" required class="input-field" />
          </label>
          <br />
          <label>
            Arrival Datetime:
            <input v-model="newFlight.arrival_datetime" type="datetime-local" required class="input-field" />
          </label>

          <br />
          <label>
            Sold Tickets:
            <input v-model="newFlight.sold_tickets" type="number" required class="input-field" />
          </label>
          <br />
          <button type="submit" class="add-button">Add Flight</button>
        </form>

        <div class = "button-container">
          <router-link to="/crewmembers">
            <button>Crew Members</button>
          </router-link>
          <router-link to="/aircrafts">
            <button>Aircrafts</button>
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
      flights: [],
      newFlight: {
        flight_number: '',
        distance: 0,
        departure_point: '',
        destination_point: '',
        departure_datetime: '',
        arrival_datetime: '',
        sold_tickets: 0,
      },
    };
  },
  mounted() {
    this.fetchFlights();
  },
  methods: {
    fetchFlights() {
      axios.get('http://localhost:8000/my_avia_app/api/flights/')
        .then(response => {
          this.flights = response.data;
        })
        .catch(error => {
          console.error(error);
        });
    },
    addFlight() {
      axios.post('http://localhost:8000/my_avia_app/api/flights/', this.newFlight)
        .then(() => {
          this.newFlight = {
            flight_number: '',
            distance: 0,
            departure_point: '',
            destination_point: '',
            departure_datetime: '',
            arrival_datetime: '',
            sold_tickets: 0,
          };
          this.fetchFlights();
        })
        .catch(error => {
          console.error(error);
        });
    },
    deleteFlight(flightId) {
      axios.delete(`http://localhost:8000/my_avia_app/api/flights/${flightId}/`)
        .then(() => {
          this.fetchFlights();
        })
        .catch(error => {
          console.error(error);
        });
    },
  },
};
</script>
<style scoped>
    .flight-list-container {
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
      text-align: left;
      font-size: 30px;
    }
    .flight-table {
      width: 100%;
      border-collapse: collapse;
      margin-top: 20px;
    }
    .flight-table th,
    .flight-table td {
      border: 1px solid #ddd;
      padding: 8px;
      text-align: left;
    }
    .flight-table th {
      background-color: #4CAF50;
      color: #fff;
    }
    .add-form{
        margin-top: 40px;
        margin-left: 40px;
    }
    .add-flight-form {
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