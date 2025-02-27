<template>
  <v-container>
    <TokenRefresh />
    <HeaderButtons />
    <v-row v-if="loading">
      <v-col class="text-center">
        <v-progress-circular indeterminate color="primary"></v-progress-circular>
      </v-col>
    </v-row>

    <v-row v-else-if="flight">
      <v-col>
        <v-card>
          <v-card-title>{{ flight.flight_number }} - {{ flight.route.name }}</v-card-title>
          <v-card-text>
            <p><b>Airline:</b> {{ flight.route.airline.name }}</p>
            <p><b>Departure:</b> {{ flight.route.departure_time }} - {{ flight.route.departure_airport.name }} ({{ flight.route.departure_airport.code }})</p>
            <p><b>Arrival:</b> {{ flight.route.arrival_time }} - {{ flight.route.arrival_airport.name }} ({{ flight.route.arrival_airport.code }})</p>
            <p><b>Flight Status:</b> {{ flight.flight_status }}</p>
            <p><b>Sold Tickets:</b> {{ flight.sold_tickets }}</p>
            <p><b>Airplane:</b> {{ flight.airplane.serial_number }} ({{ flight.airplane.airplane_model.name }})</p>
          </v-card-text>
        </v-card>

        <v-card class="mt-4">
          <v-card-title>Crew Members</v-card-title>
          <v-card-text>
            <v-row>
              <v-col v-for="member in flight.crew.members" :key="member.id" cols="12" md="6">
                <v-card class="crew-card" @click="goToEmployeeDetail(member.employee.user.id)">
                  <v-card-title>{{ member.employee.full_name }}</v-card-title>
                  <v-card-text>
                    <p>Role: {{ member.employee.role }}</p>
                    <p>Airline: {{ member.employee.airline.name }}</p>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>

        <v-card class="mt-4">
          <v-card-title>Transit Points</v-card-title>
          <v-card-text>
            <v-row>
              <v-col v-for="transit in orderedTransits" :key="transit.id" cols="12" md="6">
                <v-card class="transit-card" @click="goToTransitDetail(transit.id)">
                  <v-card-title>{{ transit.transit_order }}. {{ transit.departure_airport.name }}</v-card-title>
                  <v-card-text>
                    <p>From: {{ transit.departure_airport.name }} ({{ transit.departure_airport.code }})</p>
                    <p>To: {{ transit.arrival_airport.name }} ({{ transit.arrival_airport.code }})</p>
                    <p>Departure: {{ transit.departure_time }}</p>
                    <p>Arrival: {{ transit.arrival_time }}</p>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios'
import HeaderButtons from '../components/HeaderButtons.vue'
import TokenRefresh from '../components/TokenRefresh.vue'

export default {
  name: 'FlightDetail',
  components: {
    HeaderButtons,
    TokenRefresh
  },
  data () {
    return {
      loading: true,
      flight: null,
      transits: []
    }
  },
  computed: {
    orderedTransits () {
      if (!this.flight || !this.flight.route.transit_id_sequence) {
        return []
      }

      const orderedTransitIds = Object.entries(this.flight.route.transit_id_sequence).sort(([, orderA], [, orderB]) => orderA - orderB).map(([order, transitId]) => transitId)

      return orderedTransitIds.map((transitId) => {
        return this.transits.find(transit => transit.id === transitId)
      }).filter(transit => transit !== undefined)
    }
  },
  methods: {
    async fetchFlightDetail () {
      this.loading = true
      try {
        const tokens = JSON.parse(localStorage.getItem('tokens'))
        let url = `/api/flight/${this.$route.params.id}/`
        const response = await axios.get(url, {
          headers: {
            Authorization: `Bearer ${tokens.access}`
          }
        })
        this.flight = response.data
        this.flight.route.departure_time = new Date(
          this.flight.route.departure_time
        ).toLocaleString('ru-RU')
        this.flight.route.arrival_time = new Date(
          this.flight.route.arrival_time
        ).toLocaleString('ru-RU')
        url = `/api/route/${this.flight.route.id}/transits/`
        const transitsResponse = await axios.get(url, {
          headers: {
            Authorization: `Bearer ${tokens.access}`
          }
        })
        this.transits = transitsResponse.data
        this.transits.forEach((transit) => {
          transit.departure_time = new Date(
            transit.departure_time
          ).toLocaleString('ru-RU')
          transit.arrival_time = new Date(
            transit.arrival_time
          ).toLocaleString('ru-RU')
        })
      } catch (error) {
        console.error('Error fetching flight detail:', error)
        this.flight = null
      } finally {
        this.loading = false
      }
    },
    goToEmployeeDetail (id) {
      this.$router.push(`/employees/${id}`)
    },
    goToTransitDetail (id) {
      this.$router.push(`/transits/${id}`)
    }
  },
  mounted () {
    this.fetchFlightDetail()
  }
}
</script>

<style scoped>
.crew-card, .transit-card {
  cursor: pointer;
  transition: box-shadow 0.3s;
}

.crew-card:hover, .transit-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}
</style>
