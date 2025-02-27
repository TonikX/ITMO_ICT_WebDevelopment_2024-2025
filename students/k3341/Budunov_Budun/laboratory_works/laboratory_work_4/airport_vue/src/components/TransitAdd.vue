<template>
    <v-dialog v-model="dialog" max-width="700px">
      <v-card>
        <v-card-title class="text-h5">Add New Transit</v-card-title>
        <v-card-text>
          <v-form ref="form" @submit.prevent="submit">
              <v-select
                  v-model="transit.route"
                  :items="routes"
                  item-title="name"
                  item-value="id"
                  label="Route"
                  required
                  outlined
                  dense
                  :rules="routeRules"
              ></v-select>
              <v-select
                  v-model="transit.departure_airport"
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
                  v-model="transit.arrival_airport"
                  :items="airports"
                  item-title="name"
                  item-value="id"
                  label="Arrival Airport"
                  required
                  outlined
                  dense
                  :rules="airportRules"
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
                  v-model="transit.transit_order"
                  label="Transit order"
                  type="number"
                  required
                  outlined
                  dense
                  :rules="transitOrderRules"
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
  name: 'TransitAdd',
  data () {
    return {
      dialog: false,
      transit: {
        route: null,
        departure_airport: null,
        arrival_airport: null,
        transit_order: null
      },
      departure_date: null,
      departure_time: null,
      arrival_date: null,
      arrival_time: null,
      airports: [],
      routes: [],
      routeRules: [(v) => !!v || 'Route is required'],
      airportRules: [(v) => !!v || 'Airport is required'],
      dateRules: [(v) => !!v || 'Date is required'],
      timeRules: [(v) => !!v || 'Time is required'],
      transitOrderRules: [
        (v) => !!v || 'Transit order is required',
        (v) => v > 0 || 'Transit order must be greater than 0'
      ]
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
        this.fetchAirports(),
        this.fetchRoutes()
      ])
    },
    closeDialog () {
      this.dialog = false
      this.resetForm()
    },
    resetForm () {
      this.transit.route = null
      this.transit.departure_airport = null
      this.transit.arrival_airport = null
      this.transit.transit_order = null
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
          await axios.post('/api/transit/', {
            route: this.transit.route,
            departure_airport: this.transit.departure_airport,
            arrival_airport: this.transit.arrival_airport,
            departure_time: departureTimeCombined,
            arrival_time: arrivalTimeCombined,
            transit_order: this.transit.transit_order
          })
          this.closeDialog()
          this.$emit('transit-added')
          alert('Transit added successfully!')
        } catch (error) {
          console.error('Error adding transit:', error)
          alert('Error adding transit.')
        }
      }
    }
  }
}
</script>
