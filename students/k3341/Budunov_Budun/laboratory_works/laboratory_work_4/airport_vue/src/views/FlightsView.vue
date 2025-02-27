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
            {{ flight.route.name }} ({{ flight.flight_number }})
          </v-card-title>
          <v-card-text>
            <p>Departure: {{ flight.route.departure_time }} - {{ flight.route.departure_airport.name }}</p>
            <p>Arrival: {{ flight.route.arrival_time }} - {{ flight.route.arrival_airport.name }}</p>
            <p>Crew:
              <span v-for="(member, index) in flight.crew.members" :key="index">
                {{ member.employee.full_name }} ({{member.employee.role}}){{ index < flight.crew.members.length - 1 ? ', ' : ''}}
              </span>
            </p>
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
        { value: 'departure_time', title: 'Departure Time' },
        { value: 'arrival_time', title: 'Arrival Time' },
        { value: 'flight_number', title: 'Flight Number' }
      ]
    }
  },
  computed: {
    filteredFlights () {
      let filtered = this.flights

      if (this.isAdmin !== 'true') {
        filtered = filtered.filter(flight =>
          flight.crew.members.some(member =>
            member.employee.user.id === this.currentUserId
          )
        )
      }

      filtered = filtered.filter(flight => {
        const searchTerm = this.search.toLowerCase()
        const departureDate = new Date(flight.route.departure_time.split(', ')[0]).toLocaleDateString('ru-RU')
        const arrivalDate = new Date(flight.route.arrival_time.split(', ')[0]).toLocaleDateString('ru-RU')

        return flight.route.name.toLowerCase().includes(searchTerm) ||
          flight.flight_number.toLowerCase().includes(searchTerm) ||
          flight.route.departure_airport.name.toLowerCase().includes(searchTerm) ||
          flight.route.arrival_airport.name.toLowerCase().includes(searchTerm) ||
          departureDate.includes(searchTerm) ||
          arrivalDate.includes(searchTerm)
      })

      if (this.filterAirline) {
        filtered = filtered.filter(flight => flight.route.airline.id === this.filterAirline)
      }

      if (this.sortBy !== 'no_sort') {
        filtered = this.sortFlights(filtered)
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
        const response = await axios.get('/api/flight/', {
          headers: {
            Authorization: `Bearer ${tokens.access}`
          }
        })
        this.flights = response.data
        this.flights.forEach(flight => {
          flight.route.departure_time = new Date(flight.route.departure_time).toLocaleString('ru-RU')
          flight.route.arrival_time = new Date(flight.route.arrival_time).toLocaleString('ru-RU')
        })
      } catch (error) {
        console.error('Error fetching flights:', error)
      } finally {
        this.loading = false
      }
    },
    async fetchAirlines () {
      try {
        const tokens = JSON.parse(localStorage.getItem('tokens'))
        const response = await axios.get('/api/airline/', {
          headers: {
            Authorization: `Bearer ${tokens.access}`
          }
        })
        this.airlines = response.data
      } catch (error) {
        console.error('Error fetching airlines:', error)
      }
    },
    async getCurrentUserId () {
      try {
        const tokens = JSON.parse(localStorage.getItem('tokens'))
        const response = await axios.get('/api/auth/users/me/', {
          headers: {
            Authorization: `Bearer ${tokens.access}`
          }
        })
        this.currentUserId = response.data.id
      } catch (error) {
        console.error('Error fetching current user:', error)
      }
    },
    sortFlights (flights) {
      return flights.slice().sort((a, b) => {
        if (this.sortBy === 'flight_number') {
          return a.flight_number.localeCompare(b.flight_number)
        }
        const aTime = new Date(a.route[this.sortBy])
        const bTime = new Date(b.route[this.sortBy])
        return aTime - bTime
      })
    },
    goToFlightDetail (id) {
      this.$router.push(`/flights/${id}`)
    },
    openAddFlightDialog () {
      this.$refs.addFlightDialog.openDialog()
    }
  },
  async mounted () {
    await this.getCurrentUserId()
    await Promise.all([this.fetchFlights(), this.fetchAirlines()])
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
