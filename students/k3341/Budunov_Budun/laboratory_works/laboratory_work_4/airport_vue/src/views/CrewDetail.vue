<template>
    <v-container>
      <TokenRefresh />
      <HeaderButtons />
      <v-row v-if="loading">
        <v-col class="text-center">
          <v-progress-circular indeterminate color="primary"></v-progress-circular>
        </v-col>
      </v-row>
      <v-row v-else-if="crew">
        <v-col>
          <v-card>
            <v-card-title>Crew #{{ crew.id }}</v-card-title>
            <v-card-text>
              <p><b>Is approved:</b> {{ crew.is_approved }}</p>
              <v-card class="mt-4" v-if="crew.members.length">
                <v-card-title>Crew Members</v-card-title>
                <v-card-text>
                  <v-list>
                    <v-list-item v-for="member in crew.members" :key="member.id">
                      <v-list-item-title>{{ member.employee.full_name }}</v-list-item-title>
                      <v-list-item-subtitle>{{ member.role }}</v-list-item-subtitle>
                      <v-list-item-subtitle>Airline: {{ member.employee.airline.name }}</v-list-item-subtitle>
                      <v-list-item-subtitle>Position: {{ member.employee.position }}</v-list-item-subtitle>
                    </v-list-item>
                  </v-list>
                </v-card-text>
              </v-card>
              <p v-else>No members</p>
            </v-card-text>
          </v-card>
            <v-card class="mt-4" v-if="crewFlights.length">
                <v-card-title>Flights</v-card-title>
                <v-card-text>
                    <v-list>
                        <v-list-item v-for="flight in crewFlights" :key="flight.id">
                            <v-list-item-title>{{flight.flight_number}}</v-list-item-title>
                            <v-list-item-subtitle>Route: {{flight.route.name}}</v-list-item-subtitle>
                            <v-list-item-subtitle>Departure: {{flight.route.departure_time}} - {{flight.route.departure_airport.name}}</v-list-item-subtitle>
                            <v-list-item-subtitle>Arrival: {{flight.route.arrival_time}} - {{flight.route.arrival_airport.name}}</v-list-item-subtitle>
                        </v-list-item>
                    </v-list>
                </v-card-text>
            </v-card>
              <p v-else>No flights</p>
        </v-col>
      </v-row>
      <v-row v-else>
        <v-col>
          <p>Crew not found.</p>
        </v-col>
      </v-row>
    </v-container>
  </template>

<script>
import axios from 'axios'
import HeaderButtons from '../components/HeaderButtons.vue'
import TokenRefresh from '../components/TokenRefresh.vue'

export default {
  name: 'CrewDetail',
  components: {
    HeaderButtons,
    TokenRefresh
  },
  data () {
    return {
      loading: true,
      crew: null,
      crewFlights: []
    }
  },
  methods: {
    async fetchCrewDetail () {
      this.loading = true
      try {
        const tokens = JSON.parse(localStorage.getItem('tokens'))
        const response = await axios.get(`/api/crew/${this.$route.params.id}/`, {
          headers: {
            Authorization: `Bearer ${tokens.access}`
          }
        })
        this.crew = response.data
        const flightResponse = await axios.get(`/api/crew/${this.$route.params.id}/flights/`, {
          headers: {
            Authorization: `Bearer ${tokens.access}`
          }
        })
        this.crewFlights = flightResponse.data
        this.crewFlights.forEach(flight => {
          flight.route.departure_time = new Date(flight.route.departure_time).toLocaleString('ru-RU')
          flight.route.arrival_time = new Date(flight.route.arrival_time).toLocaleString('ru-RU')
        })
      } catch (error) {
        console.error('Error fetching crew detail:', error)
        this.crew = null
      } finally {
        this.loading = false
      }
    }
  },
  mounted () {
    this.fetchCrewDetail()
  }
}
</script>
