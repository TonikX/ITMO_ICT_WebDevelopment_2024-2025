<template>
  <v-row class="mb-4">
    <template v-if="isAdmin === 'true'">
      <v-col cols="auto">
        <v-btn to="/routes" color="primary">Routes</v-btn>
      </v-col>
      <v-col cols="auto">
        <v-btn to="/transits" color="primary">Transits</v-btn>
      </v-col>
      <v-col cols="auto">
        <v-btn to="/flights" color="primary">Flights</v-btn>
      </v-col>
      <v-col cols="auto">
        <v-btn to="/employees" color="primary">Employees</v-btn>
      </v-col>
      <v-col cols="auto">
        <v-btn to="/airplanes" color="primary">Airplanes</v-btn>
      </v-col>
    </template>

    <template v-else>
      <v-col cols="auto">
        <v-btn to="/flights" color="primary">Flights</v-btn>
      </v-col>
    </template>

    <v-spacer></v-spacer>

    <v-col cols="auto">
      <v-btn to="/profile" color="info">Profile</v-btn>
    </v-col>
    <v-col cols="auto">
      <v-btn @click="logout" color="error">Logout</v-btn>
    </v-col>
  </v-row>
</template>

<script>
export default {
  name: 'HeaderButtons',
  mounted () {
    console.log('Current isAdmin value:', localStorage.getItem('isAdmin'))
  },
  data () {
    return {
      isAdmin: localStorage.getItem('isAdmin')
    }
  },
  methods: {
    logout () {
      localStorage.removeItem('tokens')
      localStorage.removeItem('isLoggedIn')
      localStorage.removeItem('isAdmin')
      this.$router.push('/login')
    }
  }
}
</script>
