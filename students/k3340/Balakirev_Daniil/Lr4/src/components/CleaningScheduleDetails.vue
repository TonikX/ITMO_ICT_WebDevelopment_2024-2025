<template>
    <v-card class="mx-auto" max-width="300" elevation="6">
      <v-card-title class="headline">Расписание уборки {{ schedule.id }}</v-card-title>
      <v-card-subtitle>Комната: {{ schedule.room.room_number }}</v-card-subtitle>
      <v-card-text>
        <v-list dense>
          <v-list-item>
            <v-list-item-content>Дата:</v-list-item-content>
            <v-list-item-content class="align-end">{{ schedule.cleaning_date }}</v-list-item-content>
          </v-list-item>
          <v-list-item>
            <v-list-item-content>Сотрудник:</v-list-item-content>
            <v-list-item-content class="align-end">{{ schedule.cleaner ? `${schedule.cleaner.first_name} ${schedule.cleaner.last_name}` : 'Неизвестно' }}</v-list-item-content>
          </v-list-item>
        </v-list>
      </v-card-text>
      <v-card-actions>
        <v-btn color="teal" dark @click="edit = true">Редактировать</v-btn>
        <v-btn color="red" dark @click="del = true">Удалить</v-btn>
      </v-card-actions>
  
      <v-dialog v-model="edit" persistent max-width="600px" transition="dialog-transition">
        <v-card>
          <v-card-title>
            <span class="headline">Редактировать расписание уборки</span>
          </v-card-title>
          <v-card-text>
            <v-container>
              <v-row>
                <v-col cols="12">
                  <v-select
                    v-model="editedSchedule.room"
                    :items="rooms"
                    item-text="room_number"
                    item-value="id"
                    label="Комната"
                    required
                  ></v-select>
                </v-col>
                <v-col cols="12">
                  <v-text-field v-model="editedSchedule.cleaning_date" label="Дата" required></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-select
                    v-model="editedSchedule.cleaner"
                    :items="employees"
                    :item-text="employee => `${employee.first_name} ${employee.last_name}`"
                    item-value="id"
                    label="Сотрудник"
                    required
                  ></v-select>
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="green darken-1" text @click="edit = false">Закрыть</v-btn>
            <v-btn color="green darken-1" text @click="editSchedule">Сохранить</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
  
      <v-dialog v-model="del" persistent max-width="400px" transition="dialog-transition">
        <v-card>
          <v-card-title>Вы уверены?</v-card-title>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="green darken-1" text @click="del = false">Закрыть</v-btn>
            <v-btn color="red darken-1" text @click="deleteSchedule">Удалить</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-card>
  </template>
  
  <script>
  export default {
    name: 'CleaningScheduleDetails',
    props: {
      schedule: Object
    },
    data() {
      return {
        exist: true,
        edit: false,
        del: false,
        editedSchedule: { ...this.schedule },
        rooms: [],
        employees: []
      };
    },
    methods: {
      editSchedule() {
        const body = {
          room: this.editedSchedule.room,
          cleaning_date: this.editedSchedule.cleaning_date,
          cleaner: this.editedSchedule.cleaner
        };
        this.axios
          .patch(this.$hostname + 'api/cleaning-schedules/' + this.schedule.id + '/', body, {
            headers: {
              Authorization: 'Token ' + localStorage.getItem('auth_token')
            }
          })
          .then(response => {
            console.log(response);
            this.$emit('update-schedule', this.editedSchedule);
            this.edit = false;
          })
          .catch(error => console.log(error));
      },
      deleteSchedule() {
        this.axios
          .delete(this.$hostname + 'api/cleaning-schedules/' + this.schedule.id + '/', {
            headers: { Authorization: 'Token ' + localStorage.getItem('auth_token') }
          })
          .then(response => {
            console.log(response);
            this.exist = false;
            this.del = false;
            this.$emit('delete-schedule', this.schedule.id);
          })
          .catch(error => console.log(error));
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
      }
    },
    created() {
      this.fetchRooms();
      this.fetchEmployees();
      console.log('Schedule:', this.schedule);
    }
  };
  </script>
  
  <style scoped>
  .v-card {
    margin: 10px;
    transition: all 0.3s ease;
  }
  
  .v-card:hover {
    transform: scale(1.05);
  }
  
  .dialog-transition-enter-active,
  .dialog-transition-leave-active {
    transition: all 0.3s ease;
  }
  
  .dialog-transition-enter,
  .dialog-transition-leave-to {
    opacity: 0;
    transform: translateY(-20px);
  }
  </style>