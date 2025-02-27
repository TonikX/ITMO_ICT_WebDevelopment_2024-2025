<template>
  <v-container>
    <TokenRefresh />
    <HeaderButtons />
    <v-row class="mb-4" align="center">
      <v-col cols="4">
        <v-text-field
          v-model="search"
          label="Search Employees"
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
        <v-btn color="primary" @click="openAddEmployeeDialog" >Add Employee</v-btn>
      </v-col>
    </v-row>

    <v-row v-if="loading">
      <v-col class="text-center">
        <v-progress-circular indeterminate color="primary"></v-progress-circular>
      </v-col>
    </v-row>

    <v-row v-else>
      <v-col
        v-for="employee in paginatedEmployees"
        :key="employee.id"
        cols="12"
        md="6"
      >
        <v-card class="employee-card" @click="goToEmployeeDetail(employee.id)">
          <v-card-title>{{ employee.full_name }}</v-card-title>
          <v-card-text>
            <p>Role: {{ employee.role }}</p>
            <p>Airline: {{ employee.airline?.name || 'No airline assigned' }}</p>
          </v-card-text>
        </v-card>
      </v-col>
      <v-col v-if="!filteredEmployees.length">
        <p>Employees not found</p>
      </v-col>
    </v-row>

    <v-pagination
      v-model="currentPage"
      :length="pageCount"
      :total-visible="7"
    ></v-pagination>

    <EmployeeAdd ref="addEmployeeDialog" @employee-added="fetchEmployees" />
  </v-container>
</template>

<script>
import axios from 'axios'
import HeaderButtons from '../components/HeaderButtons.vue'
import TokenRefresh from '../components/TokenRefresh.vue'
import EmployeeAdd from '../components/EmployeeAdd.vue'

export default {
  name: 'EmployeesView',
  components: {
    HeaderButtons,
    TokenRefresh,
    EmployeeAdd
  },
  data () {
    return {
      loading: true,
      employees: [],
      airlines: [],
      search: '',
      filterAirline: null,
      isAdmin: localStorage.getItem('isAdmin') === 'true',
      sortBy: 'no_sort',
      currentPage: 1,
      itemsPerPage: 10,
      sortOptions: [
        { value: 'no_sort', title: 'No Sort' },
        { value: 'full_name', title: 'Full Name' },
        { value: 'role', title: 'Role' }
      ]
    }
  },
  computed: {
    filteredEmployees () {
      let filtered = this.employees.filter((employee) => {
        const searchTerm = this.search.toLowerCase()
        return employee.full_name.toLowerCase().includes(searchTerm) ||
          employee.role.toLowerCase().includes(searchTerm) ||
          employee.airline.name.toLowerCase().includes(searchTerm)
      })

      if (this.filterAirline) {
        filtered = filtered.filter(employee => employee.airline.id === this.filterAirline)
      }

      if (this.sortBy !== 'no_sort') {
        filtered = this.sortEmployees(filtered)
      }

      return filtered
    },
    pageCount () {
      return Math.ceil(this.filteredEmployees.length / this.itemsPerPage)
    },
    paginatedEmployees () {
      const start = (this.currentPage - 1) * this.itemsPerPage
      const end = start + this.itemsPerPage
      return this.filteredEmployees.slice(start, end)
    }
  },
  methods: {
    async fetchEmployees () {
      this.loading = true
      try {
        const tokens = JSON.parse(localStorage.getItem('tokens'))
        const response = await axios.get('/api/employee/', {
          headers: {
            Authorization: `Bearer ${tokens.access}`
          }
        })
        this.employees = response.data
      } catch (error) {
        console.error('Error fetching employees:', error)
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
    sortEmployees (employees) {
      return employees.slice().sort((a, b) => {
        if (this.sortBy === 'full_name' || this.sortBy === 'role') {
          return a[this.sortBy].localeCompare(b[this.sortBy])
        }
        return 0
      })
    },
    goToEmployeeDetail (id) {
      this.$router.push(`/employees/${id + 1}`)
    },
    openAddEmployeeDialog () {
      this.$refs.addEmployeeDialog.openDialog()
    }
  },
  async mounted () {
    await Promise.all([this.fetchEmployees(), this.fetchAirlines()])
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
.employee-card {
  cursor: pointer;
  margin-bottom: 16px;
  transition: box-shadow 0.3s;
}

.employee-card:hover {
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}
</style>
