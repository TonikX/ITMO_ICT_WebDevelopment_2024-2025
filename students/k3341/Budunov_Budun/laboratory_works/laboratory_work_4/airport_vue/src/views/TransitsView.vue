<template>
  <v-container>
    <TokenRefresh />
    <HeaderButtons />
    <v-row class="mb-4" align="center">
      <v-col cols="4">
        <v-text-field
          v-model="search"
          label="Search Transits"
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
      <v-col cols="2" class="text-right">
        <v-btn color="primary" @click="openAddTransitDialog">Add Transit</v-btn>
      </v-col>
    </v-row>

    <v-row v-if="loading">
      <v-col class="text-center">
        <v-progress-circular indeterminate color="primary"></v-progress-circular>
      </v-col>
    </v-row>

    <v-row v-else>
      <v-col
        v-for="transit in paginatedTransits"
        :key="transit.id"
        cols="12"
        md="6"
      >
        <v-card class="transit-card" @click="goToTransitDetail(transit.id)">
          <v-card-title>{{ transit.departure_airport.city }} - ({{ transit.departure_airport.name }} {{ transit.departure_airport.code }})</v-card-title>
          <v-card-text>
            <p>Route: {{ transit.route.name }}</p>
            <p>Departure: {{ transit.departure_time }} - {{ transit.departure_airport.name }}</p>
            <p>Arrival: {{ transit.arrival_time }} - {{ transit.arrival_airport.name }}</p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-pagination
      v-model="currentPage"
      :length="pageCount"
      :total-visible="7"
    ></v-pagination>

    <TransitAdd ref="addTransitDialog" @transit-added="fetchTransits" />
  </v-container>
</template>

<script>
import axios from 'axios'
import HeaderButtons from '../components/HeaderButtons.vue'
import TokenRefresh from '../components/TokenRefresh.vue'
import TransitAdd from '../components/TransitAdd.vue'

export default {
  name: 'TransitsView',
  components: {
    HeaderButtons,
    TokenRefresh,
    TransitAdd
  },
  data () {
    return {
      loading: true,
      transits: [],
      airlines: [],
      search: '',
      selectedDate: null,
      isAdmin: localStorage.getItem('isAdmin') === 'true',
      sortBy: 'no_sort',
      currentPage: 1,
      itemsPerPage: 10,
      filterAirline: null,
      sortOptions: [
        { value: 'no_sort', title: 'No Sort' },
        { value: 'departure_time', title: 'Departure Time' },
        { value: 'arrival_time', title: 'Arrival Time' },
        { value: 'city', title: 'City Name' }
      ]
    }
  },
  computed: {
    filteredTransits () {
      let filtered = this.transits.filter((transit) => {
        const searchTerm = this.search.toLowerCase()
        const departureDate = new Date(transit.departure_time.split(', ')[0]).toLocaleDateString('ru-RU')
        const arrivalDate = new Date(transit.arrival_time.split(', ')[0]).toLocaleDateString('ru-RU')
        return transit.route.name.toLowerCase().includes(searchTerm) ||
          transit.departure_airport.name.toLowerCase().includes(searchTerm) ||
          transit.arrival_airport.name.toLowerCase().includes(searchTerm) ||
          departureDate.includes(searchTerm) ||
          arrivalDate.includes(searchTerm)
      })

      if (this.filterAirline && this.filterAirline !== 'All Airlines') {
        filtered = filtered.filter((transit) => transit.route.airline.id === this.filterAirline)
      }

      if (this.sortBy && this.sortBy !== 'no_sort') {
        filtered = this.sortTransits(filtered)
      }

      return filtered
    },
    pageCount () {
      return Math.ceil(this.filteredTransits.length / this.itemsPerPage)
    },
    paginatedTransits () {
      const start = (this.currentPage - 1) * this.itemsPerPage
      const end = start + this.itemsPerPage
      return this.filteredTransits.slice(start, end)
    }
  },
  methods: {
    async fetchTransits () {
      this.loading = true
      try {
        const tokens = JSON.parse(localStorage.getItem('tokens'))
        const response = await axios.get('/api/transit/', {
          headers: {
            Authorization: `Bearer ${tokens.access}`
          }
        })
        this.transits = response.data
        this.transits.forEach(transit => {
          transit.departure_time = new Date(transit.departure_time).toLocaleString('ru-RU')
          transit.arrival_time = new Date(transit.arrival_time).toLocaleString('ru-RU')
        })

        // Populate airline options
        const airlines = [...new Set(this.transits.map(t => t.airline))]
        this.airlineOptions = ['All Airlines', ...airlines]
      } catch (error) {
        console.error('Error fetching transits:', error)
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
    sortTransits (transits) {
      return transits.slice().sort((a, b) => {
        if (this.sortBy === 'city') {
          return a.departure_airport.city.localeCompare(b.departure_airport.city)
        }
        const aTime = new Date(a[this.sortBy])
        const bTime = new Date(b[this.sortBy])
        return aTime - bTime
      })
    },
    goToTransitDetail (id) {
      this.$router.push(`/transits/${id}`)
    },
    openAddTransitDialog () {
      this.$refs.addTransitDialog.openDialog()
    }
  },
  async mounted () {
    await Promise.all([this.fetchTransits(), this.fetchAirlines()])
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
.transit-card {
  cursor: pointer;
  margin-bottom: 16px;
  transition: box-shadow 0.3s;
}
.transit-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}
</style>
