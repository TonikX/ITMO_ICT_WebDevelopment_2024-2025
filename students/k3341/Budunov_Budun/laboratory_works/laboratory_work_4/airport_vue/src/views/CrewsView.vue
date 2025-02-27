<template>
    <v-container>
      <TokenRefresh />
      <HeaderButtons />
      <v-row class="mb-4">
        <v-col>
          <v-text-field
            v-model="search"
            label="Search Crews"
            clearable
            outlined
            dense
            prepend-icon="mdi-magnify"
          ></v-text-field>
        </v-col>
        <v-col cols="auto">
            <v-select
              v-model="sortBy"
              :items="sortOptions"
              label="Sort By"
              outlined
              dense
          ></v-select>
        </v-col>
      </v-row>
      <v-row class="mb-4" v-if="isAdmin">
          <v-col cols="auto">
              <v-btn color="primary" @click="openAddCrewDialog">Add</v-btn>
          </v-col>
      </v-row>

      <v-row v-if="loading">
        <v-col class="text-center">
          <v-progress-circular indeterminate color="primary"></v-progress-circular>
        </v-col>
      </v-row>

      <v-row v-else>
        <v-col v-for="crew in filteredCrews" :key="crew.id" cols="12" md="6">
          <v-card class="crew-card" @click="goToCrewDetail(crew.id)">
            <v-card-title>Crew #{{ crew.id }}</v-card-title>
            <v-card-text>
              <p>Members:</p>
              <v-list>
                <v-list-item v-for="member in crew.members" :key="member.id">
                  <v-list-item-title>{{ member.employee.full_name }}</v-list-item-title>
                  <v-list-item-subtitle>{{member.role}}</v-list-item-subtitle>
                </v-list-item>
              </v-list>
            </v-card-text>
          </v-card>
        </v-col>
          <v-col v-if="!filteredCrews.length">
              <p>Crews not found</p>
          </v-col>
      </v-row>
      <CrewAdd ref="addCrewDialog" @crew-added="fetchCrews" />
    </v-container>
  </template>

<script>
import axios from 'axios'
import HeaderButtons from '../components/HeaderButtons.vue'
import TokenRefresh from '../components/TokenRefresh.vue'
import CrewAdd from '../components/CrewAdd.vue'

export default {
  name: 'CrewsView',
  components: {
    HeaderButtons,
    TokenRefresh,
    CrewAdd
  },
  data () {
    return {
      loading: true,
      crews: [],
      search: '',
      sortBy: 'id',
      sortOptions: [
        { value: 'id', title: 'Crew ID' }
      ],
      isAdmin: localStorage.getItem('isAdmin') === 'true'
    }
  },
  computed: {
    filteredCrews () {
      let filtered = this.crews.filter((crew) => {
        const searchTerm = this.search.toLowerCase()
        return (
          crew.id.toString().includes(searchTerm) ||
                      crew.members.some(member => member.employee.full_name.toLowerCase().includes(searchTerm)) ||
                      crew.members.some(member => member.role.toLowerCase().includes(searchTerm))
        )
      })
      filtered = this.sortCrews(filtered)
      return filtered
    }
  },
  methods: {
    async fetchCrews () {
      this.loading = true
      try {
        const token = JSON.parse(localStorage.getItem('token'))
        const response = await axios.get('/api/crew/', {
          headers: {
            Authorization: `Bearer ${token.access}`
          }
        })
        this.crews = response.data
      } catch (error) {
        console.error('Error fetching crews:', error)
      } finally {
        this.loading = false
      }
    },
    openAddCrewDialog () {
      this.$refs.addCrewDialog.openDialog()
    },
    sortCrews (crews) {
      return crews.slice().sort((a, b) => {
        return a[this.sortBy] - b[this.sortBy]
      })
    },
    goToCrewDetail (id) {
      this.$router.push(`/crews/${id}`)
    }
  },
  mounted () {
    this.fetchCrews()
  }
}
</script>

  <style scoped>
  .crew-card {
    margin-bottom: 16px;
    transition: box-shadow 0.3s;
    cursor: pointer;
  }
  .crew-card:hover {
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
  }
  </style>
