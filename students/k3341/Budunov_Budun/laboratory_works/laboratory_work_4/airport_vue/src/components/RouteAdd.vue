<template>
    <v-dialog v-model="dialog" max-width="700px">
      <v-card>
        <v-card-title class="text-h5">Add New Route</v-card-title>
        <v-card-text>
          <v-form ref="form" @submit.prevent="submit">
              <v-text-field
                  v-model="route.name"
                  label="Route name"
                  required
                  outlined
                  dense
                  :rules="routeNameRules"
              ></v-text-field>
            <v-select
              v-model="route.departure_airport"
              :items="airports"
              item-title="name"
              item-value="id"
              label="Departure Airport"
              required
              outlined
              dense
              :rules="airportRules"
            ></v-select>
            <v-select
              v-model="route.arrival_airport"
              :items="airports"
              item-title="name"
              item-value="id"
              label="Arrival Airport"
              required
              outlined
              dense
              :rules="airportRules"
            ></v-select>
            <v-select
              v-model="route.airline"
              :items="airlines"
              item-title="name"
              item-value="id"
              label="Airline"
              required
              outlined
              dense
              :rules="airlineRules"
            ></v-select>
              <v-date-picker v-model="departure_date" label="Departure date" required outlined dense :rules="dateRules"></v-date-picker>
              <v-time-picker
                  v-model="departure_time"
                  label="Departure Time"
                  required
                  outlined
                  dense
                  :rules="timeRules"
              ></v-time-picker>
              <v-date-picker v-model="arrival_date" label="Arrival date" required outlined dense :rules="dateRules"></v-date-picker>
              <v-time-picker
                  v-model="arrival_time"
                  label="Arrival Time"
                  required
                  outlined
                  dense
                  :rules="timeRules"
              ></v-time-picker>
              <v-text-field
                  v-model="route.total_time"
                  label="Total time (hh:mm:ss)"
                  required
                  outlined
                  dense
                  :rules="totalTimeRules"
              ></v-text-field>
              <v-text-field
                  v-model="route.periodicity"
                  label="Periodicity"
                  required
                  outlined
                  dense
                  :rules="periodicityRules"
              ></v-text-field>

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
  name: 'RouteAdd',
  data () {
    return {
      dialog: false,
      route: {
        name: '',
        departure_airport: null,
        arrival_airport: null,
        airline: null,
        total_time: '',
        periodicity: ''
      },
      departure_date: null,
      departure_time: null,
      arrival_date: null,
      arrival_time: null,
      airports: [],
      airlines: [],
      routeNameRules: [
        (v) => !!v || 'Route name is required'
      ],
      airportRules: [(v) => !!v || 'Airport is required'],
      airlineRules: [(v) => !!v || 'Airline is required'],
      dateRules: [(v) => !!v || 'Date is required'],
      timeRules: [(v) => !!v || 'Time is required'],
      totalTimeRules: [(v) => !!v || 'Total time is required'],
      periodicityRules: [(v) => !!v || 'Periodicity is required']
    }
  },
  methods: {
    async fetchAirports () {
      try {
        const response = await axios.get('/api/airport/')
        this.airports = response.data
      } catch (error) {
        console.error('Error fetching airports:', error)
      }
    },
    async fetchAirlines () {
      try {
        const response = await axios.get('/api/airline/')
        this.airlines = response.data
      } catch (error) {
        console.error('Error fetching airlines:', error)
      }
    },
    openDialog () {
      this.dialog = true
      Promise.all([
        this.fetchAirlines(),
        this.fetchAirports()
      ])
    },
    closeDialog () {
      this.dialog = false
      this.resetForm()
    },
    resetForm () {
      this.route.name = ''
      this.route.departure_airport = null
      this.route.arrival_airport = null
      this.route.airline = null
      this.route.total_time = ''
      this.route.periodicity = ''
      this.departure_date = null
      this.departure_time = null
      this.arrival_date = null
      this.arrival_time = null
    },
    async submit () {
      if (this.$refs.form.validate()) {
        try {
          const departureTimeCombined = `${this.departure_date}T${this.departure_time}`
          const arrivalTimeCombined = `${this.arrival_date}T${this.arrival_time}`
          await axios.post('/api/route/', {
            name: this.route.name,
            departure_airport: this.route.departure_airport,
            arrival_airport: this.route.arrival_airport,
            airline: this.route.airline,
            departure_time: departureTimeCombined,
            arrival_time: arrivalTimeCombined,
            total_time: this.route.total_time,
            periodicity: this.route.periodicity
          })
          this.closeDialog()
          this.$emit('route-added')
          alert('Route added successfully!')
        } catch (error) {
          console.error('Error adding route:', error)
          alert('Error adding route.')
        }
      }
    }
  }
}
</script>
