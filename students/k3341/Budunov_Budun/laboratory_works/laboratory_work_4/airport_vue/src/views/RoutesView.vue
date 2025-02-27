<template>
  <v-container>
    <TokenRefresh />
    <HeaderButtons />
    <v-row class="mb-4" align="center">
      <v-col cols="4">
        <v-text-field
          v-model="search"
          label="Search"
          clearable
          outlined
          dense
          prepend-icon="mdi-magnify"
          hint="Name or date DD.MM.YYYY"
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
      <v-col cols="2" class="text-right">
        <v-btn color="primary" @click="openAddRouteDialog">Add Route</v-btn>
      </v-col>
    </v-row>

    <v-row v-if="loading">
      <v-col class="text-center">
        <v-progress-circular
          indeterminate
          color="primary"
        ></v-progress-circular>
      </v-col>
    </v-row>

    <v-row v-else>
      <v-col v-for="route in paginatedRoutes" :key="route.id" cols="12" md="6">
        <v-card class="route-card" @click="goToRouteDetail(route.id)">
          <v-card-title>{{ route.name }}</v-card-title>
          <v-card-text>
            <p>
              Departure: {{ route.departure_time }} -
              {{ route.departure_airport.name }}
            </p>
            <p>
              Arrival: {{ route.arrival_time }} -
              {{ route.arrival_airport.name }}
            </p>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col v-if="!filteredRoutes.length">
        <p>Routes not found</p>
      </v-col>
    </v-row>

    <v-pagination
      v-if="filteredRoutes.length > itemsPerPage"
      v-model="currentPage"
      :length="totalPages"
      :total-visible="7"
    ></v-pagination>

    <RouteAdd ref="addRouteDialog" @route-added="fetchRoutes" />
  </v-container>
</template>

<script>
import axios from 'axios'
import HeaderButtons from '../components/HeaderButtons.vue'
import TokenRefresh from '../components/TokenRefresh.vue'
import RouteAdd from '../components/RouteAdd.vue'

export default {
  name: 'RoutesView',
  components: {
    HeaderButtons,
    TokenRefresh,
    RouteAdd
  },
  data () {
    return {
      loading: true,
      routes: [],
      airlines: [],
      search: '',
      filterAirline: null,
      isAdmin: localStorage.getItem('isAdmin') === 'true',
      sortBy: 'no_sort',
      currentPage: 1,
      itemsPerPage: 10,
      sortOptions: [
        { value: 'no_sort', title: 'No Sort' },
        { value: 'departure_time', title: 'Departure Time' },
        { value: 'arrival_time', title: 'Arrival Time' },
        { value: 'name', title: 'Route Name' }
      ]
    }
  },
  computed: {
    filteredRoutes () {
      let filtered = this.routes.filter((route) => {
        const searchTerm = this.search.toLowerCase()
        const departureDate = new Date(route.departure_time.split(', ')[0]).toLocaleDateString('ru-RU')
        const arrivalDate = new Date(route.arrival_time.split(', ')[0]).toLocaleDateString('ru-RU')
        return route.name.toLowerCase().includes(searchTerm) ||
              route.departure_airport.name.toLowerCase().includes(searchTerm) ||
              route.arrival_airport.name.toLowerCase().includes(searchTerm) ||
              departureDate.includes(searchTerm) ||
              arrivalDate.includes(searchTerm)
      })

      if (this.filterAirline) {
        filtered = filtered.filter((route) => route.airline.id === this.filterAirline)
      }

      if (this.sortBy) {
        filtered = this.sortRoutes(filtered)
      }
      return filtered
    },
    totalPages () {
      return Math.ceil(this.filteredRoutes.length / this.itemsPerPage)
    },
    paginatedRoutes () {
      const start = (this.currentPage - 1) * this.itemsPerPage
      const end = start + this.itemsPerPage
      return this.filteredRoutes.slice(start, end)
    }
  },
  methods: {
    async fetchRoutes () {
      this.loading = true
      try {
        const tokens = JSON.parse(localStorage.getItem('tokens'))
        const response = await axios.get('/api/route/', {
          headers: {
            Authorization: `Bearer ${tokens.access}`
          }
        })
        this.routes = response.data
        this.routes.forEach((route) => {
          route.departure_time = new Date(route.departure_time).toLocaleString(
            'ru-RU'
          )
          route.arrival_time = new Date(route.arrival_time).toLocaleString(
            'ru-RU'
          )
        })
      } catch (error) {
        console.error('Error fetching routes:', error)
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
    sortRoutes (routes) {
      return routes.slice().sort((a, b) => {
        if (!this.sortBy) return 0
        if (this.sortBy === 'name') {
          return a.name.localeCompare(b.name)
        } else {
          const aTime = new Date(a[this.sortBy])
          const bTime = new Date(b[this.sortBy])
          return aTime - bTime
        }
      })
    },
    goToRouteDetail (routeId) {
      this.$router.push(`/routes/${routeId}`)
    }
  },
  async mounted () {
    await Promise.all([this.fetchRoutes(), this.fetchAirlines()])
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
.route-card {
  cursor: pointer;
  margin-bottom: 16px;
  transition: box-shadow 0.3s;
}

.route-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}
</style>
