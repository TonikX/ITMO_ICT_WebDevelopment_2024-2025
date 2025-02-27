<template>
  <v-container>
    <TokenRefresh />
    <HeaderButtons />
    <v-row v-if="loading">
      <v-col class="text-center">
        <v-progress-circular
          indeterminate
          color="primary"
        ></v-progress-circular>
      </v-col>
    </v-row>

    <v-row v-else-if="transit">
      <v-col>
        <v-card>
          <v-card-title>{{ transit.departure_airport.city }} - ({{ transit.departure_airport.name }} {{ transit.departure_airport.code }})</v-card-title>
          <v-card-text>
            <p><b>Route:</b> {{ transit.route.name }}</p>
            <p><b>Airline:</b> {{ transit.route.airline.name }}</p>
            <p>
              <b>Departure:</b> {{ transit.departure_time }} -
              {{ transit.departure_airport.name }} ({{
                transit.departure_airport.code
              }})
            </p>
            <p>
              <b>Arrival:</b> {{ transit.arrival_time }} -
              {{ transit.arrival_airport.name }} ({{
                transit.arrival_airport.code
              }})
            </p>
            <p><b>Transit Order:</b> {{ transit.transit_order }}</p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row v-else>
      <v-col>
        <p>Transit not found.</p>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios'
import HeaderButtons from '../components/HeaderButtons.vue'
import TokenRefresh from '../components/TokenRefresh.vue'

export default {
  name: 'TransitDetail',
  components: {
    HeaderButtons,
    TokenRefresh
  },
  data () {
    return {
      loading: true,
      transit: null
    }
  },
  methods: {
    async fetchTransitDetail () {
      this.loading = true
      try {
        const tokens = JSON.parse(localStorage.getItem('tokens'))
        const response = await axios.get(`/api/transit/${this.$route.params.id}/`, {
          headers: {
            Authorization: `Bearer ${tokens.access}`
          }
        })
        this.transit = response.data
        this.transit.departure_time = new Date(
          this.transit.departure_time
        ).toLocaleString('ru-RU')
        this.transit.arrival_time = new Date(
          this.transit.arrival_time
        ).toLocaleString('ru-RU')
      } catch (error) {
        console.error('Error fetching transit detail:', error)
        this.transit = null
      } finally {
        this.loading = false
      }
    }
  },
  mounted () {
    this.fetchTransitDetail()
  }
}
</script>
