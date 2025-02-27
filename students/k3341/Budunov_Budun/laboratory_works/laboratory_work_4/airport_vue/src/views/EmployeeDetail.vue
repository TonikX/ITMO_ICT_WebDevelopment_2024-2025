<template>
    <v-container>
      <TokenRefresh />
      <HeaderButtons />
      <v-row v-if="loading">
        <v-col class="text-center">
          <v-progress-circular indeterminate color="primary"></v-progress-circular>
        </v-col>
      </v-row>

      <v-row v-else-if="employee">
        <v-col>
          <v-card>
            <v-card-title>{{ employee.full_name }}</v-card-title>
            <v-card-text>
              <p><b>Role:</b> {{ employee.role }}</p>
              <p><b>Airline:</b> {{ employee.airline?.name || 'Not assigned' }}</p>
              <p><b>Username:</b> {{ employee.user.username }}</p>
              <p><b>Is Active:</b> {{ employee.user.is_active }}</p>
              <p><b>Birth Date:</b> {{ employee.birth_date }}</p>
              <p><b>Experience:</b> {{ employee.experience }}</p>
               <v-btn v-if="isAdmin && employee.user.is_active" color="error" @click="fireEmployee">Fire</v-btn>
              <v-btn v-else-if="isAdmin && !employee.user.is_active" color="success" @click="hireEmployee">Hire</v-btn>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <v-row v-else>
        <v-col>
          <p>Employee not found.</p>
        </v-col>
      </v-row>
    </v-container>
  </template>

<script>
import axios from 'axios'
import HeaderButtons from '../components/HeaderButtons.vue'
import TokenRefresh from '../components/TokenRefresh.vue'

const DEFAULT_PASSWORD = 'defaultpassword' // Default password for new hires
const FIRED_PASSWORD = 'firedpassword' // Default password for fired employees

export default {
  name: 'EmployeeDetail',
  components: {
    HeaderButtons,
    TokenRefresh
  },
  data () {
    return {
      loading: true,
      employee: null,
      isAdmin: localStorage.getItem('isAdmin') === 'true'
    }
  },
  methods: {
    async fetchEmployeeDetail () {
      this.loading = true
      try {
        const tokens = JSON.parse(localStorage.getItem('tokens'))
        const response = await axios.get(`/api/employee/${this.$route.params.id}/`, {
          headers: {
            Authorization: `Bearer ${tokens.access}`
          }
        })
        this.employee = response.data
      } catch (error) {
        console.error('Error fetching employee detail:', error)
        this.employee = null
      } finally {
        this.loading = false
      }
    },
    async fireEmployee () {
      try {
        const tokens = JSON.parse(localStorage.getItem('tokens'))
        await axios.patch(`/api/employee/${this.employee.user.id}/`,
          {
            user: {
              is_active: false,
              password: FIRED_PASSWORD
            }
          },
          {
            headers: {
              Authorization: `Bearer ${tokens.access}`
            }
          }
        )
        await this.fetchEmployeeDetail()
        alert('Employee fired!')
      } catch (error) {
        console.error('Error firing employee:', error)
      }
    },
    async hireEmployee () {
      try {
        const tokens = JSON.parse(localStorage.getItem('tokens'))
        await axios.patch(`/api/employee/${this.employee.user.id}/`,
          {
            user: {
              is_active: true,
              password: DEFAULT_PASSWORD
            }
          },
          {
            headers: {
              Authorization: `Bearer ${tokens.access}`
            }
          }
        )
        await this.fetchEmployeeDetail()
        alert('Employee hired!')
      } catch (error) {
        console.error('Error hiring employee:', error)
      }
    }
  },
  mounted () {
    this.fetchEmployeeDetail()
  }
}
</script>
