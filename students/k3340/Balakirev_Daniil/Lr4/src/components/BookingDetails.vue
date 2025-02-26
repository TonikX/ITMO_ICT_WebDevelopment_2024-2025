<template>
    <v-card class="mx-auto" max-width="300" elevation="6">
      <v-card-title class="headline">Бронирование {{ booking.id }}</v-card-title>
      <v-card-subtitle>Комната: {{ booking.room.room_number }}</v-card-subtitle>
      <v-card-text>
        <v-list dense>
          <v-list-item>
            <v-list-item-content>Клиент:</v-list-item-content>
            <v-list-item-content class="align-end">{{ booking.client.first_name }} {{ booking.client.last_name }}</v-list-item-content>
          </v-list-item>
          <v-list-item>
            <v-list-item-content>Дата заезда:</v-list-item-content>
            <v-list-item-content class="align-end">{{ booking.check_in_date }}</v-list-item-content>
          </v-list-item>
          <v-list-item>
            <v-list-item-content>Дата выезда:</v-list-item-content>
            <v-list-item-content class="align-end">{{ booking.check_out_date }}</v-list-item-content>
          </v-list-item>
          <v-list-item>
            <v-list-item-content>Статус:</v-list-item-content>
            <v-list-item-content class="align-end">{{ booking.booking_status }}</v-list-item-content>
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
            <span class="headline">Редактировать бронирование</span>
          </v-card-title>
          <v-card-text>
            <v-container>
              <v-row>
                <v-col cols="12">
                  <v-select
                    v-model="editedBooking.room"
                    :items="rooms"
                    item-text="room_number"
                    item-value="id"
                    label="Комната"
                    required
                  ></v-select>
                </v-col>
                <v-col cols="12">
                  <v-select
                    v-model="editedBooking.client"
                    :items="clients"
                    :item-text="client => `${client.first_name} ${client.last_name}`"
                    item-value="id"
                    label="Клиент"
                    required
                  ></v-select>
                </v-col>
                <v-col cols="12">
                  <v-text-field v-model="editedBooking.check_in_date" label="Дата заезда" required></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-text-field v-model="editedBooking.check_out_date" label="Дата выезда" required></v-text-field>
                </v-col>
                <v-col cols="12">
                  <v-select
                    v-model="editedBooking.booking_status"
                    :items="statuses"
                    label="Статус"
                    required
                  ></v-select>
                </v-col>
              </v-row>
            </v-container>
          </v-card-text>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="green darken-1" text @click="edit = false">Закрыть</v-btn>
            <v-btn color="green darken-1" text @click="editBooking">Сохранить</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
  
      <v-dialog v-model="del" persistent max-width="400px" transition="dialog-transition">
        <v-card>
          <v-card-title>Вы уверены?</v-card-title>
          <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="green darken-1" text @click="del = false">Закрыть</v-btn>
            <v-btn color="red darken-1" text @click="deleteBooking">Удалить</v-btn>
          </v-card-actions>
        </v-card>
      </v-dialog>
    </v-card>
  </template>
  
  <script>
  export default {
    name: 'BookingDetails',
    props: {
      booking: Object
    },
    data() {
      return {
        exist: true,
        edit: false,
        del: false,
        editedBooking: { ...this.booking },
        rooms: [],
        clients: [],
        statuses: ['Booked', 'Checked In', 'Checked Out', 'Cancelled']
      };
    },
    methods: {
      editBooking() {
        const body = {
          room: this.editedBooking.room,
          client: this.editedBooking.client,
          check_in_date: this.editedBooking.check_in_date,
          check_out_date: this.editedBooking.check_out_date,
          booking_status: this.editedBooking.booking_status
        };
        this.axios
          .patch(this.$hostname + 'api/bookings/' + this.booking.id + '/', body, {
            headers: {
              Authorization: 'Token ' + localStorage.getItem('auth_token')
            }
          })
          .then(response => {
            console.log(response);
            this.$emit('update-booking', this.editedBooking);
            this.edit = false;
          })
          .catch(error => console.log(error));
      },
      deleteBooking() {
        this.axios
          .delete(this.$hostname + 'api/bookings/' + this.booking.id + '/', {
            headers: { Authorization: 'Token ' + localStorage.getItem('auth_token') }
          })
          .then(response => {
            console.log(response);
            this.exist = false;
            this.del = false;
            this.$emit('delete-booking', this.booking.id);
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
      fetchClients() {
        this.axios
          .get(this.$hostname + 'api/clients/', {
            headers: { Authorization: 'Token ' + localStorage.getItem('auth_token') }
          })
          .then(response => {
            this.clients = response.data;
          })
          .catch(error => {
            console.log(error);
          });
      }
    },
    created() {
      this.fetchRooms();
      this.fetchClients();
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