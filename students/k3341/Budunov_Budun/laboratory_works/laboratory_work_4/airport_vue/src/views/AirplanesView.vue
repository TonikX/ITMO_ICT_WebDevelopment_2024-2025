<template>
  <v-container>
    <TokenRefresh />
    <HeaderButtons />
    <v-row class="mb-4" align="center">
      <v-col cols="4">
        <v-text-field
          v-model="search"
          label="Search Airplanes"
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
        <v-btn color="primary" @click="openAddAirplaneDialog" v-if="isAdmin">Add Airplane</v-btn>
      </v-col>
    </v-row>

    <v-row v-if="loading">
      <v-col class="text-center">
        <v-progress-circular indeterminate color="primary"></v-progress-circular>
      </v-col>
    </v-row>

    <v-row v-else>
      <v-col
        v-for="airplane in paginatedAirplanes"
        :key="airplane.id"
        cols="12"
        md="6"
      >
        <v-card class="airplane-card" @click="goToAirplaneDetail(airplane.id)">
          <v-card-title>{{ airplane.serial_number }}</v-card-title>
          <v-card-text>
            <p>Model: {{ airplane.airplane_model.name }}</p>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col v-if="!filteredAirplanes.length">
        <p>Airplanes not found</p>
      </v-col>
    </v-row>

    <v-pagination
      v-model="currentPage"
      :length="pageCount"
      :total-visible="7"
    ></v-pagination>

    <AirplaneAdd ref="addAirplaneDialog" @airplane-added="fetchAirplanes" />
  </v-container>
</template>

<script>
import axios from 'axios'
import HeaderButtons from '../components/HeaderButtons.vue'
import TokenRefresh from '../components/TokenRefresh.vue'
import AirplaneAdd from '../components/AirplaneAdd.vue'

export default {
  name: 'AirplanesView',
  components: {
    HeaderButtons,
    TokenRefresh,
    AirplaneAdd
  },
  data () {
    return {
      loading: true,
      airplanes: [],
      airlines: [],
      search: '',
      filterAirline: null,
      isAdmin: localStorage.getItem('isAdmin') === 'true',
      sortBy: 'no_sort',
      currentPage: 1,
      itemsPerPage: 10,
      sortOptions: [
        { value: 'no_sort', title: 'No Sort' },
        { value: 'serial_number', title: 'Serial Number' },
        { value: 'model_name', title: 'Model Name' }
      ]
    }
  },
  computed: {
    filteredAirplanes () {
      let filtered = this.airplanes.filter((airplane) => {
        const searchTerm = this.search.toLowerCase()
        return airplane.serial_number.toLowerCase().includes(searchTerm) ||
          airplane.airplane_model.name.toLowerCase().includes(searchTerm)
      })

      if (this.filterAirline) {
        filtered = filtered.filter(airplane => airplane.airline.id === this.filterAirline)
      }

      if (this.sortBy !== 'no_sort') {
        filtered = this.sortAirplanes(filtered)
      }

      return filtered
    },
    pageCount () {
      return Math.ceil(this.filteredAirplanes.length / this.itemsPerPage)
    },
    paginatedAirplanes () {
      const start = (this.currentPage - 1) * this.itemsPerPage
      const end = start + this.itemsPerPage
      return this.filteredAirplanes.slice(start, end)
    }
  },
  methods: {
    async fetchAirplanes () {
      this.loading = true
      try {
        const tokens = JSON.parse(localStorage.getItem('tokens'))
        const response = await axios.get('/api/airplane/', {
          headers: {
            Authorization: `Bearer ${tokens.access}`
          }
        })
        this.airplanes = response.data
      } catch (error) {
        console.error('Error fetching airplanes:', error)
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
    sortAirplanes (airplanes) {
      return airplanes.slice().sort((a, b) => {
        if (this.sortBy === 'serial_number') {
          return a.serial_number.localeCompare(b.serial_number)
        }
        if (this.sortBy === 'model_name') {
          return a.airplane_model.name.localeCompare(b.airplane_model.name)
        }
        return 0
      })
    },
    goToAirplaneDetail (id) {
      this.$router.push(`/airplanes/${id}`)
    },
    openAddAirplaneDialog () {
      this.$refs.addAirplaneDialog.openDialog()
    }
  },
  async mounted () {
    await Promise.all([this.fetchAirplanes(), this.fetchAirlines()])
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
.airplane-card {
  cursor: pointer;
  margin-bottom: 16px;
  transition: box-shadow 0.3s;
}

.airplane-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}
</style>
