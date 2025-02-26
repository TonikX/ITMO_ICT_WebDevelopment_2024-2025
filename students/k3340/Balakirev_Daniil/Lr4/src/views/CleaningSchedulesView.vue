<template>
    <v-main>
      <v-container fluid>
        <v-row justify="center">
          <v-col cols="12" sm="8" md="12">
            <v-card elevation="0">
              <v-card-text>
                <v-row>
                  <v-col v-for="schedule in schedules" :key="schedule.id" cols="12" sm="12" md="3">
                    <cleaning-schedule-details
                      :schedule="schedule"
                      @update-schedule="updateSchedule"
                      @delete-schedule="deleteSchedule"
                    ></cleaning-schedule-details>
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
  import CleaningScheduleDetails from '@/components/CleaningScheduleDetails.vue';
  export default {
    name: 'CleaningSchedulesView',
    components: {
      CleaningScheduleDetails
    },
    data: () => ({
      schedules: [],
      rooms: [],
      employees: []
    }),
    methods: {
      fetchSchedules() {
        this.axios
          .get(this.$hostname + 'api/cleaning-schedules/', {
            headers: { Authorization: 'Token ' + localStorage.getItem('auth_token') }
          })
          .then(response => {
            this.schedules = response.data;
            console.log('Schedules:', this.schedules); // Отладочное сообщение
          })
          .catch(error => {
            console.log(error);
          });
      },
      fetchRooms() {
        this.axios
          .get(this.$hostname + 'api/rooms/', {
            headers: { Authorization: 'Token ' + localStorage.getItem('auth_token') }
          })
          .then(response => {
            this.rooms = response.data;
          })
          .catch(error => {
            console.log(error);
          });
      },
      fetchEmployees() {
        this.axios
          .get(this.$hostname + 'api/employees/', {
            headers: { Authorization: 'Token ' + localStorage.getItem('auth_token') }
          })
          .then(response => {
            this.employees = response.data;
          })
          .catch(error => {
            console.log(error);
          });
      },
      updateSchedule(updatedSchedule) {
        const index = this.schedules.findIndex(schedule => schedule.id === updatedSchedule.id);
        if (index !== -1) {
          this.schedules.splice(index, 1, updatedSchedule);
        }
      },
      deleteSchedule(scheduleId) {
        const index = this.schedules.findIndex(schedule => schedule.id === scheduleId);
        if (index !== -1) {
          this.schedules.splice(index, 1);
        }
      }
    },
    created() {
      this.fetchSchedules();
      this.fetchRooms();
      this.fetchEmployees();
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