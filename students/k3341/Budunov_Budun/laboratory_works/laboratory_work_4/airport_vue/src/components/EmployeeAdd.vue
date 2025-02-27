<template>
  <v-dialog v-model="dialog" max-width="600px">
    <v-card>
      <v-card-title class="text-h5">Add New Employee</v-card-title>
      <v-card-text>
        <v-form ref="form" @submit.prevent="submit">
          <v-text-field
            v-model="user.username"
            label="Username"
            required
            outlined
            dense
            :rules="usernameRules"
          ></v-text-field>
          <v-text-field
            v-model="user.password"
            label="Password"
            required
            type="password"
            outlined
            dense
            :rules="passwordRules"
          ></v-text-field>
          <v-text-field
            v-model="employee.full_name"
            label="Full name"
            required
            outlined
            dense
            :rules="fullNameRules"
          ></v-text-field>
          <v-text-field
            v-model="employee.passport_data"
            label="Passport data"
            required
            outlined
            dense
            :rules="passportDataRules"
          ></v-text-field>
          <v-select
            v-model="employee.role"
            :items="roles"
            label="Role"
            required
            outlined
            dense
            :rules="roleRules"
          ></v-select>
          <v-select
            v-model="employee.airline"
            :items="airlines"
            item-title="name"
            item-value="id"
            label="Airline"
            required
            outlined
            dense
            :rules="airlineRules"
          ></v-select>
          <v-text-field
            v-model="employee.birth_date"
            label="Birth Date"
            placeholder="YYYY-MM-DD"
            required
            outlined
            dense
            :rules="birthDateRules"
          ></v-text-field>

          <v-btn type="submit" color="primary" class="mr-4">
            Add
          </v-btn>
          <v-btn @click="closeDialog">Cancel</v-btn>
        </v-form>
      </v-card-text>
    </v-card>
  </v-dialog>
</template>

<script>
import axios from 'axios'

const DEFAULT_PASSWORD = 'defaultpassword'

export default {
  name: 'EmployeeAdd',
  data () {
    return {
      dialog: false,
      user: {
        username: '',
        password: DEFAULT_PASSWORD,
        is_active: true,
        is_staff: false,
        is_superuser: false
      },
      employee: {
        full_name: '',
        passport_data: '',
        role: '',
        birth_date: null,
        airline: null
      },
      roles: [
        'Pilot',
        'Co-Pilot',
        'Flight Attendant',
        'Flight Engineer',
        'Navigator',
        'Loadmaster',
        'Stewardess',
        'admin'
      ],
      airlines: [],
      usernameRules: [
        v => !!v || 'Username is required'
      ],
      passwordRules: [
        v => !!v || 'Password is required'
      ],
      fullNameRules: [
        v => !!v || 'Full Name is required'
      ],
      passportDataRules: [
        v => !!v || 'Passport Data is required'
      ],
      roleRules: [
        v => !!v || 'Role is required'
      ],
      airlineRules: [
        v => !!v || 'Airline is required'
      ],
      birthDateRules: [
        v => !!v || 'Birth date is required',
        v => /^\d{4}-\d{2}-\d{2}$/.test(v) || 'Date must be in YYYY-MM-DD format'
      ]
    }
  },
  methods: {
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
    openDialog () {
      this.dialog = true
      this.fetchAirlines()
    },
    closeDialog () {
      this.dialog = false
      this.resetForm()
    },
    resetForm () {
      this.user.username = ''
      this.user.password = DEFAULT_PASSWORD
      this.employee.full_name = ''
      this.employee.passport_data = ''
      this.employee.role = ''
      this.employee.birth_date = null
      this.employee.airline = null
      if (this.$refs.form) {
        this.$refs.form.resetValidation()
      }
    },
    async submit () {
      if (this.$refs.form.validate()) {
        try {
          const tokens = JSON.parse(localStorage.getItem('tokens'))
          const requestData = {
            user: {
              username: this.user.username,
              password: this.user.password,
              is_active: true,
              is_staff: false,
              is_superuser: false
            },
            full_name: this.employee.full_name,
            passport_data: this.employee.passport_data,
            role: this.employee.role,
            birth_date: this.employee.birth_date,
            airline: this.employee.airline
          }

          console.log('Request data:', requestData) // For debugging

          await axios.post('/api/employee/', requestData, {
            headers: {
              'Content-Type': 'application/json',
              Authorization: `Bearer ${tokens.access}`
            }
          })
          this.closeDialog()
          this.$emit('employee-added')
          alert('Employee added successfully!')
        } catch (error) {
          if (error.response?.status === 401) {
            this.$router.push('/login')
          } else {
            console.error('Error details:', error.response?.data)
            alert(error.response?.data?.detail || 'Error adding employee')
          }
        }
      }
    }
  }
}
</script>
