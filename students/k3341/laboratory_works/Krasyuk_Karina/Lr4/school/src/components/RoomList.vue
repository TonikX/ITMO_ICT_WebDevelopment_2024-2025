<script setup>
defineProps({
  rooms: Array,
  isRoomSpecial: Function
});
</script>
<template>
  <div class="rooms-container">
    <template v-for="room in rooms.filter((roomObj) => roomObj.floor === floor)" :key="room.id">
      <v-card
          :color="isRoomSpecial(room) ? 'green lighten-3' : 'blue lighten-3'"
          class="room-card">
        <v-card-title class="room-title">
          Кабинет №{{ room.number }}
        </v-card-title>
        <v-card-subtitle v-if="isRoomSpecial(room)" class="room-details">
          Для предмета: {{ room.subject.subject_name }}<br/>
        </v-card-subtitle>
      </v-card>
    </template>
  </div>
</template>


<style scoped>
.rooms-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 16px;
  padding: 16px;
}

.room-card {
  width: 100%;
  padding: 16px;
  cursor: pointer;
  transition: transform 0.2s ease-in-out;
}

.room-card:hover {
  transform: scale(1.05);
}

.room-title {
  font-weight: bold;
  font-size: 18px;
}

.room-details {
  font-size: 14px;
  line-height: 1.6;
  white-space: normal;
}
</style>
