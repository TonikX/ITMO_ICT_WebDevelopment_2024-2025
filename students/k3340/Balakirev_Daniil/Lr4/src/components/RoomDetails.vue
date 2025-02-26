<template>
  <v-card class="mx-auto" max-width="300" elevation="6">
    <v-card-title class="headline">{{ localRoom.room_number }} Комната</v-card-title>
    <v-card-subtitle>Тип комнаты - {{ localRoom.room_type ? localRoom.room_type.name : 'Неизвестно' }}</v-card-subtitle>
    <v-card-text>
      <v-list dense>
        <v-list-item>
          <v-list-item-content>Статус уборки:</v-list-item-content>
          <v-list-item-content class="align-end">{{ localRoom.cleaning_status }}</v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>Занята:</v-list-item-content>
          <v-list-item-content class="align-end">{{ localRoom.is_occupied ? 'Да' : 'Нет' }}</v-list-item-content>
        </v-list-item>
        <v-list-item>
          <v-list-item-content>Телефон:</v-list-item-content>
          <v-list-item-content class="align-end">{{ localRoom.phone_number }}</v-list-item-content>
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
          <span class="headline">Редактировать комнату</span>
        </v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field v-model="localRoom.room_number" label="Номер комнаты" required></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-select
                  v-model="localRoom.room_type"
                  :items="roomTypes"
                  item-text="name"
                  item-value="id"
                  label="Тип комнаты"
                  required
                ></v-select>
              </v-col>
              <v-col cols="12">
                <v-text-field v-model="localRoom.cleaning_status" label="Статус уборки" required></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-checkbox v-model="localRoom.is_occupied" label="Занята"></v-checkbox>
              </v-col>
              <v-col cols="12">
                <v-text-field v-model="localRoom.phone_number" label="Телефон" required></v-text-field>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" text @click="edit = false">Закрыть</v-btn>
          <v-btn color="green darken-1" text @click="editRoom">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="del" persistent max-width="400px" transition="dialog-transition">
      <v-card>
        <v-card-title>Вы уверены?</v-card-title>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="green darken-1" text @click="del = false">Закрыть</v-btn>
          <v-btn color="red darken-1" text @click="deleteRoom">Удалить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-card>
</template>

<script>
export default {
  name: 'RoomDetails',
  props: {
    room: Object
  },
  data() {
    return {
      exist: true,
      edit: false,
      del: false,
      localRoom: { ...this.room },
      roomTypes: []
    };
  },
  methods: {
    editRoom() {
      const body = {
        room_number: this.localRoom.room_number,
        room_type: this.localRoom.room_type,
        cleaning_status: this.localRoom.cleaning_status,
        is_occupied: this.localRoom.is_occupied,
        phone_number: this.localRoom.phone_number
      };
      this.axios
        .patch(this.$hostname + 'api/rooms/' + this.localRoom.id + '/', body, {
          headers: {
            Authorization: 'Token ' + localStorage.getItem('auth_token')
          }
        })
        .then(response => {
          console.log(response);
          this.$emit('update-room', this.localRoom);
          this.edit = false;
        })
        .catch(error => console.log(error));
    },
    deleteRoom() {
      this.axios
        .delete(this.$hostname + 'api/rooms/' + this.localRoom.id + '/', {
          headers: { Authorization: 'Token ' + localStorage.getItem('auth_token') }
        })
        .then(response => {
          console.log(response);
          this.exist = false;
          this.del = false;
          this.$emit('delete-room', this.localRoom.id);
        })
        .catch(error => console.log(error));
    },
    fetchRoomTypes() {
      this.axios
        .get(this.$hostname + 'api/roomtypes/', {
          headers: { Authorization: 'Token ' + localStorage.getItem('auth_token') }
        })
        .then(response => {
          this.roomTypes = response.data;
        })
        .catch(error => {
          console.log(error);
        });
    }
  },
  created() {
    this.fetchRoomTypes();
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