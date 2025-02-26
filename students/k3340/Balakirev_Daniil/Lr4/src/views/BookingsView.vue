<template>
    <v-main>
      <v-container fluid>
        <v-row justify="center">
          <v-col cols="12" sm="8" md="12">
            <v-card elevation="0">
              <v-card-text>
                <v-row>
                  <v-col v-for="booking in bookings" :key="booking.id" cols="12" sm="12" md="4">
                    <booking-details :booking="booking"></booking-details>
                  </v-col>
                </v-row>
              </v-card-text>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </template>
  
  <script>
  import BookingDetails from '@/components/BookingDetails.vue';
  export default {
    name: 'BookingsView',
    components: {
      BookingDetails
    },
    data: () => ({
      bookings: []
    }),
    methods: {
      fetchBookings() {
        this.axios
          .get(this.$hostname + 'api/bookings/', {
            headers: { Authorization: 'Token ' + localStorage.getItem('auth_token') }
          })
          .then(response => {
            this.bookings = response.data;
          })
          .catch(error => {
            console.log(error);
          });
      }
    },
    created() {
      this.fetchBookings();
    }
  };
  </script>
  
  <style scoped>
  .v-card {
    margin-bottom: 20px;
    transition: all 0.3s ease;
  }
  
  .v-card:hover {
    transform: scale(1.05);
  }
  </style>