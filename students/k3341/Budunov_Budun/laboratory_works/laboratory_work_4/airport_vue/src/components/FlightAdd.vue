<template>
  <v-dialog v-model="dialog" max-width="700px">
    <v-card>
      <v-card-title class="text-h5">Add New Flight</v-card-title>
      <v-card-text>
        <v-form ref="form" @submit.prevent="submit">
          <v-select
            v-model="flight.airplane"
            :items="airplanes"
            label="Select Airplane"
            item-title="display_name"
            item-value="id"
            required
            outlined
            dense
            :rules="airplaneRules"
          ></v-select>

          <v-select
            v-model="flight.crew"
            :items="crews"
            label="Select Crew"
            item-title="display_name"
            item-value="id"
            required
            outlined
            dense
            :rules="crewRules"
          ></v-select>

          <v-select
            v-model="flight.route"
            :items="routes"
            label="Select Route"
            item-title="display_name"
            item-value="id"
            required
            outlined
            dense
            :rules="routeRules"
          ></v-select>

          <v-text-field
            v-model="flight.sold_tickets"
            label="Sold Tickets"
            type="number"
            required
            outlined
            dense
            :rules="soldTicketsRules"
          ></v-text-field>

          <v-text-field
            v-model="flight.flight_number"
            label="Flight Number"
            required
            outlined
            dense
            :rules="flightNumberRules"
          ></v-text-field>

          <v-select
            v-model="flight.flight_status"
            :items="flightStatuses"
            label="Flight Status"
            required
            outlined
            dense
            :rules="flightStatusRules"
          ></v-select>

          <v-btn type="submit" color="primary" class="mr-4">Add</v-btn>
          <v-btn @click="closeDialog">Cancel</v-btn>
        </v-form>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
import axios from 'axios'

export default {
  name: 'FlightAdd',
  data () {
    return {
      dialog: false,
      flight: {
        airplane: null,
        crew: null,
        route: null,
        sold_tickets: null,
        flight_number: '',
        flight_status: ''
      },
      airplanes: [],
      crews: [],
      routes: [],
      flightStatuses: [
        'Scheduled',
        'Delayed',
        'In Air',
        'Landed',
        'Cancelled'
      ],
      airplaneRules: [(v) => !!v || 'Airplane is required'],
      crewRules: [(v) => !!v || 'Crew is required'],
      routeRules: [(v) => !!v || 'Route is required'],
      soldTicketsRules: [
        (v) => !!v || 'Sold tickets are required',
        (v) => v > 0 || 'Sold tickets must be greater than 0'
      ],
      flightNumberRules: [(v) => !!v || 'Flight number is required'],
      flightStatusRules: [(v) => !!v || 'Flight status is required']
    }
  },
  methods: {
    async fetchAirplanes () {
      try {
        const tokens = JSON.parse(localStorage.getItem('tokens'))
        const response = await axios.get('http://127.0.0.1:8000/api/airplane/', {
          headers: {
            Authorization: `Bearer ${tokens.access}`
          }
        })
        this.airplanes = response.data.map(airplane => ({
          ...airplane,
          display_name: `#${airplane.id} - ${airplane.serial_number} (${airplane.airplane_model.name})`
        }))
      } catch (error) {
        console.error('Error fetching airplanes:', error)
      }
    },
    async fetchCrews () {
      try {
        const tokens = JSON.parse(localStorage.getItem('tokens'))
        const response = await axios.get('http://127.0.0.1:8000/api/crew/', {
          headers: {
            Authorization: `Bearer ${tokens.access}`
          }
        })
        this.crews = response.data.map(crew => ({
          ...crew,
          display_name: `#${crew.id} - ${crew.is_approved ? 'Approved' : 'Not Approved'}`
        }))
      } catch (error) {
        console.error('Error fetching crews:', error)
      }
    },
    async fetchRoutes () {
      try {
        const tokens = JSON.parse(localStorage.getItem('tokens'))
        const response = await axios.get('http://127.0.0.1:8000/api/route/', {
          headers: {
            Authorization: `Bearer ${tokens.access}`
          }
        })
        this.routes = response.data.map(route => ({
          ...route,
          display_name: `#${route.id} - ${route.name} (${route.departure_airport.code} → ${route.arrival_airport.code})`
        }))
      } catch (error) {
        console.error('Error fetching routes:', error)
      }
    },
    openDialog () {
      this.dialog = true
      this.fetchAirplanes()
      this.fetchCrews()
      this.fetchRoutes()
    },
    closeDialog () {
      this.dialog = false
      this.resetForm()
    },
    resetForm () {
      this.flight = {
        airplane: null,
        crew: null,
        route: null,
        sold_tickets: null,
        flight_number: '',
        flight_status: ''
      }
    },
    async submit () {
      if (this.$refs.form.validate()) {
        try {
          const tokens = JSON.parse(localStorage.getItem('tokens'))
          const selectedAirplane = this.airplanes.find(a => a.id === this.flight.airplane)
          const selectedCrew = this.crews.find(c => c.id === this.flight.crew)
          const selectedRoute = this.routes.find(r => r.id === this.flight.route)

          const flightData = {
            airplane: selectedAirplane,
            crew: selectedCrew,
            route: selectedRoute,
            sold_tickets: parseInt(this.flight.sold_tickets),
            flight_number: this.flight.flight_number,
            flight_status: this.flight.flight_status
          }

          await axios.post('http://127.0.0.1:8000/api/flight/', flightData, {
            headers: {
              Authorization: `Bearer ${tokens.access}`,
              'Content-Type': 'application/json'
            }
          })
          this.closeDialog()
          this.$emit('flight-added')
        } catch (error) {
          console.error('Error adding flight:', error)
          alert('Error adding flight')
        }
      }
    }
  }
}
</script>
