<template>
  <v-container>
    <TokenRefresh />
    <HeaderButtons />
    <v-row class="mb-4" align="center">
      <v-col cols="4">
        <v-text-field
          v-model="search"
          label="Search Flights"
          clearable
          outlined
          dense
          prepend-icon="mdi-magnify"
        ></v-text-field>
      </v-col>
      <v-col cols="3">
        <v-select
          v-model="sortBy"
          :items="sortOptions"
          label="Sort By"
          outlined
          dense
        ></v-select>
      </v-col>
      <v-col cols="3">
        <v-select
          v-model="filterAirline"
          :items="[{ id: null, name: 'All Airlines' }, ...airlines]"
          item-title="name"
          item-value="id"
          label="Airline"
          outlined
          dense
        ></v-select>
      </v-col>
      <v-col cols="2" class="text-right" v-if="isAdmin === 'true'">
        <v-btn color="primary" @click="openAddFlightDialog">Add Flight</v-btn>
      </v-col>
    </v-row>

    <v-row v-if="loading">
      <v-col class="text-center">
        <v-progress-circular indeterminate color="primary"></v-progress-circular>
      </v-col>
    </v-row>

    <v-row v-else>
      <v-col v-for="flight in paginatedFlights" :key="flight.id" cols="12" md="6">
        <v-card class="flight-card" @click="goToFlightDetail(flight.id)">
          <v-card-title>
            Flight #{{ flight.flight_number }}
          </v-card-title>
          <v-card-text>
            <p><strong>Status:</strong> {{ flight.flight_status }}</p>
            <p><strong>Route:</strong> {{ flight.route?.name || 'N/A' }}</p>
            <p><strong>Airplane:</strong> {{ flight.airplane?.serial_number || 'N/A' }}</p>
            <p><strong>Sold Tickets:</strong> {{ flight.sold_tickets }}</p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-pagination
      v-model="currentPage"
      :length="pageCount"
      :total-visible="7"
    ></v-pagination>

    <FlightAdd ref="addFlightDialog" @flight-added="fetchFlights" />
  </v-container>
</template>

<script>
import axios from 'axios'
import HeaderButtons from '../components/HeaderButtons.vue'
import TokenRefresh from '../components/TokenRefresh.vue'
import FlightAdd from '../components/FlightAdd.vue'

export default {
  name: 'FlightsView',
  components: {
    HeaderButtons,
    TokenRefresh,
    FlightAdd
  },
  data () {
    return {
      loading: true,
      flights: [],
      airlines: [],
      search: '',
      filterAirline: null,
      isAdmin: localStorage.getItem('isAdmin'),
      currentUserId: null,
      sortBy: 'no_sort',
      currentPage: 1,
      itemsPerPage: 10,
      sortOptions: [
        { value: 'no_sort', title: 'No Sort' },
        { value: 'flight_number', title: 'Flight Number' },
        { value: 'flight_status', title: 'Status' }
      ]
    }
  },
  computed: {
    filteredFlights () {
      let filtered = [...this.flights]

      if (this.search) {
        const searchLower = this.search.toLowerCase()
        filtered = filtered.filter(flight => {
          return (
            flight.flight_number?.toLowerCase().includes(searchLower) ||
            flight.flight_status?.toLowerCase().includes(searchLower) ||
            flight.route?.name?.toLowerCase().includes(searchLower) ||
            flight.airplane?.serial_number?.toLowerCase().includes(searchLower)
          )
        })
      }

      if (this.filterAirline) {
        filtered = filtered.filter(flight => flight.route?.airline?.id === this.filterAirline)
      }

      if (this.sortBy !== 'no_sort') {
        filtered.sort((a, b) => {
          const aValue = a[this.sortBy] || ''
          const bValue = b[this.sortBy] || ''
          return aValue.localeCompare(bValue)
        })
      }

      return filtered
    },
    pageCount () {
      return Math.ceil(this.filteredFlights.length / this.itemsPerPage)
    },
    paginatedFlights () {
      const start = (this.currentPage - 1) * this.itemsPerPage
      const end = start + this.itemsPerPage
      return this.filteredFlights.slice(start, end)
    }
  },
  methods: {
    async fetchFlights () {
      this.loading = true
      try {
        const tokens = JSON.parse(localStorage.getItem('tokens'))
        const response = await axios.get('http://127.0.0.1:8000/api/flight/', {
          headers: {
            Authorization: `Bearer ${tokens.access}`
          }
        })
        this.flights = response.data
      } catch (error) {
        console.error('Error fetching flights:', error)
      } finally {
        this.loading = false
      }
    },
    async fetchAirlines () {
      try {
        const tokens = JSON.parse(localStorage.getItem('tokens'))
        const response = await axios.get('http://127.0.0.1:8000/api/airline/', {
          headers: {
            Authorization: `Bearer ${tokens.access}`
          }
        })
        this.airlines = response.data
      } catch (error) {
        console.error('Error fetching airlines:', error)
      }
    },
    goToFlightDetail (id) {
      this.$router.push(`/flights/${id}`)
    },
    openAddFlightDialog () {
      this.$refs.addFlightDialog.openDialog()
    }
  },
  async mounted () {
    await Promise.all([
      this.fetchFlights(),
      this.fetchAirlines()
    ])
  },
  watch: {
    search () {
      this.currentPage = 1
    },
    filterAirline () {
      this.currentPage = 1
    }
  }
}
</script>

<style scoped>
.flight-card {
  cursor: pointer;
  margin-bottom: 16px;
  transition: box-shadow 0.3s;
}

.flight-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}
</style>
