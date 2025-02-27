<template>
    <v-dialog v-model="dialog" max-width="600px">
      <v-card>
        <v-card-title class="text-h5">Add New Airplane</v-card-title>
        <v-card-text>
          <v-form ref="form" @submit.prevent="submit">
            <v-text-field
              v-model="airplane.serial_number"
              label="Serial Number"
              required
              outlined
              dense
              :rules="serialNumberRules"
            ></v-text-field>
            <v-select
              v-model="airplane.airplane_model"
              :items="airplaneModels"
              item-title="name"
              item-value="id"
              label="Airplane Model"
              required
              outlined
              dense
              :rules="airplaneModelRules"
            ></v-select>
              <v-select
                  v-model="airplane.airline"
                  :items="airlines"
                  item-title="name"
                  item-value="id"
                  label="Airline"
                  required
                  outlined
                  dense
                  :rules="airlineRules"
              ></v-select>
            <v-select
              v-model="airplane.status"
              :items="airplaneStatuses"
              label="Status"
              required
              outlined
              dense
              :rules="statusRules"
            ></v-select>
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

export default {
  name: 'AirplaneAdd',
  data () {
    return {
      dialog: false,
      airplane: {
        serial_number: '',
        airplane_model: null,
        status: '',
        airline: null
      },
      airplaneModels: [],
      airlines: [],
      airplaneStatuses: [
        'Active',
        'Maintenance',
        'Decommissioned'
      ],
      serialNumberRules: [(v) => !!v || 'Serial number is required'],
      airplaneModelRules: [(v) => !!v || 'Airplane model is required'],
      statusRules: [(v) => !!v || 'Status is required'],
      airlineRules: [(v) => !!v || 'Airline is required']
    }
  },
  methods: {
    async fetchAirplaneModels () {
      try {
        const response = await axios.get('/api/airplane_model/')
        this.airplaneModels = response.data
      } catch (error) {
        console.error('Error fetching airplane models:', error)
      }
    },
    async fetchAirlines () {
      try {
        const response = await axios.get('/api/airline/')
        this.airlines = response.data
      } catch (error) {
        console.error('Error fetching airlines:', error)
      }
    },
    openDialog () {
      this.dialog = true
      Promise.all([
        this.fetchAirplaneModels(),
        this.fetchAirlines()
      ])
    },
    closeDialog () {
      this.dialog = false
      this.resetForm()
    },
    resetForm () {
      this.airplane.serial_number = ''
      this.airplane.airplane_model = null
      this.airplane.status = ''
      this.airplane.airline = null
    },
    async submit () {
      if (this.$refs.form.validate()) {
        try {
          await axios.post('/api/airplane/', this.airplane)
          this.closeDialog()
          this.$emit('airplane-added')
          alert('Airplane added successfully!')
        } catch (error) {
          console.error('Error adding airplane:', error)
          alert('Error adding airplane.')
        }
      }
    }
  }
}
</script>
