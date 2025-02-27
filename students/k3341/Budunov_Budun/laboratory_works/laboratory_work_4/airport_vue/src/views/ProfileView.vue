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
            <v-card-title>Profile</v-card-title>
            <v-card-text>
               <v-row>
                   <v-col cols="12" md="4">
                       <v-avatar size="150">
                         <v-img :src="employee.user.avatar"></v-img>
                       </v-avatar>
                   </v-col>
                   <v-col>
                       <v-file-input
                          v-model="newAvatar"
                          label="New avatar"
                          show-size
                          accept="image/*"
                          outlined
                          dense
                          @change="updateAvatar"
                          :rules="avatarRules"
                       ></v-file-input>
                   </v-col>
               </v-row>
              <v-form ref="form" @submit.prevent="updateProfile">
                <v-text-field
                  v-model="employee.user.username"
                  label="Username"
                  disabled
                  outlined
                  dense
                ></v-text-field>

                <v-text-field
                  v-model="employee.full_name"
                  label="Full Name"
                  outlined
                  dense
                  :rules="fullNameRules"
                ></v-text-field>

                 <v-select
                  v-model="employee.airline"
                  :items="airlines"
                  item-title="name"
                  item-value="id"
                  label="Airline"
                  outlined
                  dense
                   :rules="airlineRules"
                ></v-select>

                 <v-text-field
                  v-model="employee.passport_data"
                  label="Passport data"
                  outlined
                  dense
                   :rules="passportDataRules"
                ></v-text-field>

                <v-select
                  v-model="employee.role"
                  :items="roles"
                  label="Role"
                  outlined
                  dense
                   :rules="roleRules"
                ></v-select>

                 <v-text-field
                  v-model="employee.education"
                  label="Education"
                  outlined
                  dense

                ></v-text-field>
                <v-text-field
                  v-model="employee.experience"
                  label="Experience"
                  outlined
                  dense
                ></v-text-field>

                <v-text-field
                  v-model="employee.birth_date"
                  label="Birth date"
                  outlined
                  dense
                  disabled
                ></v-text-field>

                <v-btn type="submit" color="primary" class="mr-4">
                  Save Changes
                </v-btn>
              </v-form>
            </v-card-text>
          </v-card>
        </v-col>
      </v-row>

      <v-row v-else>
        <v-col>
          <p>Profile not found.</p>
        </v-col>
      </v-row>
    </v-container>
  </template>

<script>
import axios from 'axios'
import HeaderButtons from '../components/HeaderButtons.vue'
import TokenRefresh from '../components/TokenRefresh.vue'

export default {
  name: 'ProfileView',
  components: {
    HeaderButtons,
    TokenRefresh
  },
  data () {
    return {
      loading: true,
      employee: null,
      airlines: [],
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
      newAvatar: null,
      avatarRules: [(v) => !v || v.size < 2000000 || 'Avatar size should be less than 2 MB!'],
      fullNameRules: [
        (v) => !!v || 'Full Name is required'
      ],
      passportDataRules: [
        (v) => !!v || 'Passport Data is required'
      ],
      roleRules: [
        (v) => !!v || 'Role is required'
      ],
      airlineRules: [
        (v) => !!v || 'Airline is required'
      ],
      birthDateRules: [
        (v) => !!v || 'Birth date is required'
      ]
    }
  },
  methods: {
    async fetchEmployeeProfile () {
      this.loading = true
      try {
        const tokens = JSON.parse(localStorage.getItem('tokens'))
        const accessToken = tokens.access
        const userResponse = await axios.get('/api/auth/users/me/', {
          headers: {
            Authorization: `Bearer ${accessToken}`
          }
        })
        const employeeResponse = await axios.get(
            `/api/employee/${userResponse.data.id}/`, {
              headers: {
                Authorization: `Bearer ${accessToken}`
              }
            })
        this.employee = employeeResponse.data
      } catch (error) {
        console.error('Error fetching employee profile:', error)
        this.employee = null
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
    async updateProfile () {
      if (this.$refs.form.validate()) {
        try {
          const tokens = JSON.parse(localStorage.getItem('tokens'))
          const updateData = {
            airline: this.employee.airline.id,
            education: this.employee.education,
            experience: this.employee.experience,
            full_name: this.employee.full_name,
            passport_data: this.employee.passport_data
          }

          await axios.patch(
            `/api/employee/${this.employee.id}/`,
            updateData,
            {
              headers: {
                Authorization: `Bearer ${tokens.access}`
              }
            }
          )
          alert('Profile successfully updated')
        } catch (error) {
          console.error('Error updating profile:', error)
          alert('Error updating profile')
        }
      }
    },
    async updateAvatar () {
      try {
        const formData = new FormData()
        formData.append('avatar', this.newAvatar)
        const tokens = JSON.parse(localStorage.getItem('tokens'))
        const accessToken = tokens.access
        await axios.patch(`/api/user/${this.employee.user.id}/avatar/`, formData, {
          headers: {
            Authorization: `Bearer ${accessToken}`,
            'Content-Type': 'multipart/form-data'
          }
        })
        await this.fetchEmployeeProfile()
        alert('Avatar successfully updated')
      } catch (error) {
        console.error('Error updating avatar:', error)
        alert('Error updating avatar')
      }
    },
    logout () {
      localStorage.removeItem('accessToken')
      localStorage.removeItem('refreshToken')
      localStorage.removeItem('isLoggedIn')
      localStorage.removeItem('isAdmin')
      this.$router.push('/login')
    }
  },
  async mounted () {
    await Promise.all([this.fetchEmployeeProfile(), this.fetchAirlines()])
  }
}
</script>
