<template>
    <v-dialog v-model="dialog" max-width="800px">
      <v-card>
        <v-card-title class="text-h5">Add New Crew</v-card-title>
        <v-card-text>
          <v-form ref="form" @submit.prevent="submit">
            <v-row v-for="(member, index) in crewMembers" :key="index">
              <v-col>
                <v-select
                  v-model="member.employee"
                  :items="employees"
                  item-title="full_name"
                  item-value="id"
                  label="Employee"
                  required
                  outlined
                  dense
                  :rules="employeeRules"
                ></v-select>
              </v-col>
              <v-col>
                <v-select
                  v-model="member.role"
                  :items="roles"
                  label="Role"
                  required
                  outlined
                  dense
                  :rules="roleRules"
                ></v-select>
              </v-col>
              <v-col cols="auto">
                <v-btn icon @click="removeCrewMember(index)" v-if="crewMembers.length > 1">
                  <v-icon>mdi-minus</v-icon>
                </v-btn>
              </v-col>
            </v-row>
            <v-btn text @click="addCrewMember" class="mb-4">
              <v-icon>mdi-plus</v-icon> Add Crew Member
            </v-btn>
            <v-btn type="submit" color="primary" class="mr-4">Add</v-btn>
            <v-btn @click="closeDialog">Cancel</v-btn>
          </v-form>
        </v-card-text>
      </v-card>
    </v-dialog>
  </template>

<script>
import axios from 'axios'

export default {
  name: 'CrewAdd',
  data () {
    return {
      dialog: false,
      crewMembers: [
        { employee: null, role: null }
      ],
      employees: [],
      roles: [
        'Pilot',
        'Co-Pilot',
        'Flight Attendant',
        'Flight Engineer',
        'Navigator',
        'Loadmaster',
        'Stewardess'
      ],
      employeeRules: [(v) => !!v || 'Employee is required'],
      roleRules: [(v) => !!v || 'Role is required']
    }
  },
  methods: {
    async fetchEmployees () {
      try {
        const response = await axios.get('/api/employee/')
        this.employees = response.data
      } catch (error) {
        console.error('Error fetching employees:', error)
      }
    },
    openDialog () {
      this.dialog = true
      this.fetchEmployees()
    },
    closeDialog () {
      this.dialog = false
      this.resetForm()
    },
    resetForm () {
      this.crewMembers = [{ employee: null, role: null }]
    },
    addCrewMember () {
      this.crewMembers.push({ employee: null, role: null })
    },
    removeCrewMember (index) {
      this.crewMembers.splice(index, 1)
    },
    async submit () {
      if (this.$refs.form.validate()) {
        try {
          const crewData = {
            members: this.crewMembers.map(member => ({
              employee: member.employee,
              role: member.role
            }))
          }
          await axios.post('/api/crew/', crewData)
          this.closeDialog()
          this.$emit('crew-added')
          alert('Crew added successfully!')
        } catch (error) {
          console.error('Error adding crew:', error)
          alert('Error adding crew.')
        }
      }
    }
  }
}
</script>

  <style scoped>
  </style>
