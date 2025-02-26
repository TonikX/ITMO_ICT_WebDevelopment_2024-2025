<template>
  <v-main>
    <v-container fluid>
      <v-row justify="center">
        <v-col v-for="room in rooms" :key="room.id" cols="12" sm="6" md="3">
          <room-details
            :room="room"
            @update-room="updateRoom"
            @delete-room="deleteRoom"
          ></room-details>
        </v-col>
      </v-row>
    </v-container>
  </v-main>
</template>

<script>
import RoomDetails from '@/components/RoomDetails.vue';
export default {
  name: 'RoomsView',
  components: {
    RoomDetails
  },
  data: () => ({
    rooms: [],
    roomTypes: []
  }),
  methods: {
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
    },
    updateRoom(updatedRoom) {
      const index = this.rooms.findIndex(room => room.id === updatedRoom.id);
      if (index !== -1) {
        this.rooms.splice(index, 1, updatedRoom);
      }
    },
    deleteRoom(roomId) {
      const index = this.rooms.findIndex(room => room.id === roomId);
      if (index !== -1) {
        this.rooms.splice(index, 1);
      }
    }
  },
  created() {
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