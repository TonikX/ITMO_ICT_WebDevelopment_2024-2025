<template>
  <v-container>
    <TokenRefresh />
    <HeaderButtons />
    <v-row v-if="loading">
      <v-col class="text-center">
        <v-progress-circular indeterminate color="primary"></v-progress-circular>
      </v-col>
    </v-row>

    <v-row v-else-if="route">
      <v-col>
        <v-card>
          <v-card-title>
             {{ route.name }}
          </v-card-title>
          <v-card-text>
            <p><b>Airline:</b> {{ route.airline.name }}</p>
            <p>
              <b>Departure:</b> {{ route.departure_time }} -
              {{ route.departure_airport.name }} ({{
                route.departure_airport.code
              }})
            </p>
            <p>
              <b>Arrival:</b> {{ route.arrival_time }} -
              {{ route.arrival_airport.name }} ({{
                route.arrival_airport.code
              }})
            </p>
            <p><b>Total time:</b> {{ route.total_time }}</p>
            <p><b>Periodicity:</b> {{ route.periodicity }}</p>
          </v-card-text>
        </v-card>

        <v-card class="mt-4">
          <v-card-title>Transits</v-card-title>
          <v-card-text>
            <v-row v-if="orderedTransits.length">
              <v-col v-for="transit in orderedTransits" :key="transit.id" cols="12" md="6">
                <v-card class="transit-card" @click="goToTransitDetail(transit.id)">
                  <v-card-title>Transit #{{ transit.transit_order }}</v-card-title>
                  <v-card-text>
                    <p>City: {{ transit.departure_airport.city }}</p>
                    <p>
                      {{ transit.departure_airport.name }}
                      ({{ transit.departure_airport.code }}) -
                      {{ transit.arrival_airport.name }}
                      ({{ transit.arrival_airport.code }})
                    </p>
                    <p>Departure: {{ transit.departure_time }}</p>
                    <p>Arrival: {{ transit.arrival_time }}</p>
                  </v-card-text>
                </v-card>
              </v-col>
            </v-row>
            <p v-else>No transits</p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row v-else>
      <v-col>
        <p>Route not found.</p>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios'
import HeaderButtons from '../components/HeaderButtons.vue'
import TokenRefresh from '../components/TokenRefresh.vue'

export default {
  name: 'RouteDetail',
  components: {
    HeaderButtons,
    TokenRefresh
  },
  data () {
    return {
      loading: true,
      route: null,
      transits: []
    }
  },
  computed: {
    orderedTransits () {
      if (!this.route || !this.route.transit_id_sequence) {
        return []
      }
      const orderedTransitIds = Object.entries(this.route.transit_id_sequence)
        .sort(([, orderA], [, orderB]) => orderA - orderB)
        .map(([, transitId]) => transitId)

      return orderedTransitIds.map((transitId) => {
        return this.transits.find(transit => transit.id === transitId)
      }).filter(transit => transit !== undefined)
    }
  },
  methods: {
    async fetchRouteDetail () {
      this.loading = true
      try {
        const tokens = JSON.parse(localStorage.getItem('tokens'))
        const response = await axios.get(`/api/route/${this.$route.params.id}/`, {
          headers: {
            Authorization: `Bearer ${tokens.access}`
          }
        })
        this.route = response.data
        this.route.departure_time = new Date(
          this.route.departure_time
        ).toLocaleString('ru-RU')
        this.route.arrival_time = new Date(
          this.route.arrival_time
        ).toLocaleString('ru-RU')
        const transitsResponse = await axios.get(`/api/route/${this.route.id}/transits/`, {
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
        console.error('Error fetching route detail:', error)
        this.route = null
      } finally {
        this.loading = false
      }
    },
    goToTransitDetail (transitId) {
      this.$router.push(`/transits/${transitId}`)
    }
  },
  mounted () {
    this.fetchRouteDetail()
  }
}
</script>

<style scoped>
.transit-card {
cursor: pointer;
transition: box-shadow 0.3s;
}

.transit-card:hover {
box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}
</style>
