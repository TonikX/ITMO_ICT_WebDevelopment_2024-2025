<template>
    <v-dialog v-model="dialog" max-width="700px">
      <v-card>
        <v-card-title class="text-h5">Add New Flight</v-card-title>
        <v-card-text>
          <v-form ref="form" @submit.prevent="submit">
            <v-select
              v-model="flight.airplane"
              :items="airplanes"
              item-title="serial_number"
              item-value="id"
              label="Airplane"
              required
              outlined
              dense
              :rules="airplaneRules"
            ></v-select>

            <v-select
              v-model="flight.crew"
              :items="crews"
              item-title="id"
              item-value="id"
              label="Crew"
              required
              outlined
              dense
              :rules="crewRules"
            ></v-select>

            <v-select
              v-model="flight.route"
              :items="routes"
              item-title="name"
              item-value="id"
              label="Route"
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

            <v-btn type="submit" color="primary" class="mr-4">
              Add
            </v-btn>
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
        const response = await axios.get('/api/airplane/')
        this.airplanes = response.data
      } catch (error) {
        console.error('Error fetching airplanes:', error)
      }
    },
    async fetchCrews () {
      try {
        const response = await axios.get('/api/crew/')
        this.crews = response.data
      } catch (error) {
        console.error('Error fetching crews:', error)
      }
    },
    async fetchRoutes () {
      try {
        const response = await axios.get('/api/route/')
        this.routes = response.data
      } catch (error) {
        console.error('Error fetching routes:', error)
      }
    },
    openDialog () {
      this.dialog = true
      Promise.all([
        this.fetchAirplanes(),
        this.fetchCrews(),
        this.fetchRoutes()
      ])
    },
    closeDialog () {
      this.dialog = false
      this.resetForm()
    },
    resetForm () {
      this.flight.airplane = null
      this.flight.crew = null
      this.flight.route = null
      this.flight.sold_tickets = null
      this.flight.flight_number = ''
      this.flight.flight_status = ''
    },
    async submit () {
      if (this.$refs.form.validate()) {
        try {
          await axios.post('/api/flight/', this.flight)
          this.closeDialog()
          this.$emit('flight-added')
          alert('Flight added successfully!')
        } catch (error) {
          console.error('Error adding flight:', error)
          alert('Error adding flight.')
        }
      }
    }
  }
}
</script>
