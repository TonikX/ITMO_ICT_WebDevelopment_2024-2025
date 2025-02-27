<template>
    <v-container>
      <HeaderButtons />
      <v-row v-if="loading">
        <v-col class="text-center">
          <v-progress-circular indeterminate color="primary"></v-progress-circular>
        </v-col>
      </v-row>

      <v-row v-else-if="airplane">
        <v-col>
          <v-card>
            <v-card-title>
              {{ airplane.serial_number }}
            </v-card-title>
            <v-card-text>
              <p><b>Model:</b> {{ airplane.airplane_model.name }}</p>
              <p><b>Airline:</b> {{ airplane.airline.name }}</p>
              <p><b>Status:</b> {{ airplane.status }}</p>
              <p><b>Speed:</b> {{airplane.airplane_model.speed}}</p>
              <p><b>Seats:</b> {{airplane.airplane_model.seats}}</p>
              <p><b>Year of manufacture:</b> {{new Date(airplane.airplane_model.year_of_manufacture).getFullYear()}}</p>
              <p><b>Manufacture name:</b> {{airplane.airplane_model.manufacture_name}}</p>
            </v-card-text>
          </v-card>

          <v-card class="mt-4">
            <v-card-title>Maintenance History</v-card-title>
            <v-card-text>
              <v-list v-if="maintenanceRecords.length">
                <v-list-item v-for="record in maintenanceRecords" :key="record.id">
                  <v-list-item-title>
                    {{ new Date(record.maintenance_date).toLocaleDateString('ru-RU') }}
                     - {{ record.is_completed ? 'Completed' : 'Pending' }}
                  </v-list-item-title>
                  <v-list-item-subtitle>
                    Notes: {{ record.notes }}
                  </v-list-item-subtitle>
                </v-list-item>
              </v-list>
              <p v-else>No maintenance records found.</p>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <v-row v-else>
        <v-col>
          <p>Airplane not found.</p>
        </v-col>
      </v-row>
    </v-container>
  </template>

<script>
import axios from 'axios'
import HeaderButtons from '../components/HeaderButtons.vue'

export default {
  name: 'AirplaneDetail',
  components: {
    HeaderButtons
  },
  data () {
    return {
      loading: true,
      airplane: null,
      maintenanceRecords: []
    }
  },
  methods: {
    async fetchAirplaneDetail () {
      this.loading = true
      try {
        const tokens = JSON.parse(localStorage.getItem('tokens'))
        let url = `/api/airplane/${this.$route.params.id}/`
        const response = await axios.get(url, {
          headers: {
            Authorization: `Bearer ${tokens.access}`
          }
        })
        url = `/api/airplane/${this.$route.params.id}/maintenance/`
        this.airplane = response.data
        const maintenanceResponse = await axios.get(url, {
          headers: {
            Authorization: `Bearer ${tokens.access}`
          }
        })
        this.maintenanceRecords = maintenanceResponse.data
      } catch (error) {
        console.error('Error fetching airplane detail:', error)
        this.airplane = null
      } finally {
        this.loading = false
      }
    }
  },
  mounted () {
    this.fetchAirplaneDetail()
  }
}
</script>
