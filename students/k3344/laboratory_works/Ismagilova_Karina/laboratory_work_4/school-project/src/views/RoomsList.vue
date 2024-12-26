<template>
  <div>
    <Header />
    <div class="page-container">
      <div class="header-container">
        <h1 class="page-title">Список комнат</h1>
        <button @click="showAddRoomModal = true" class="add-button">Добавить комнату</button>
      </div>

      <div class="rooms-grid">
        <div
          v-for="room in rooms"
          :key="room.id_room"
          class="room-card"
          @click="openRoomDetails(room)"
        >
          <h2>Комната №{{ room.number }}</h2>
          <p>Статус: {{ room.status }}</p>
        </div>
      </div>

      <div v-if="showAddRoomModal" class="modal-overlay">
        <div class="modal-content">
          <form @submit.prevent="addRoom">
            <input v-model="newRoom.number" type="text" placeholder="Номер комнаты" required />
            <div class="status-select">
              <span>Выберите статус:</span>
              <button
                type="button"
                class="room-option"
                :class="{ active: newRoom.status === 'Базовая' }"
                @click="selectStatus('Базовая')"
              >
                Базовая
              </button>
              <button
                type="button"
                class="room-option"
                :class="{ active: newRoom.status === 'Оборудованная' }"
                @click="selectStatus('Оборудованная')"
              >
                Оборудованная
              </button>
            </div>
            <div class="modal-actions">
              <button type="submit" class="save-button">Сохранить</button>
              <button @click="closeModal" type="button" class="cancel-button">Отмена</button>
            </div>
          </form>
        </div>
      </div>

      <div v-if="selectedRoom" class="modal-overlay">
        <div class="modal-content">
          <h2>Комната №{{ selectedRoom.number }}</h2>
          <p>Статус: {{ selectedRoom.status }}</p>
          <div class="modal-actions">
            <button @click="deleteRoom" class="delete-button">Удалить комнату</button>
            <button @click="closeDetails" class="cancel-button">Закрыть</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import Header from '@/components/Header.vue';
import apiClient from '@/api/axios';

export default {
  components: { Header },
  data() {
    return {
      rooms: [],
      showAddRoomModal: false,
      newRoom: {
        number: '',
        status: '',
      },
      selectedRoom: null,
    };
  },
  created() {
    this.fetchRooms();
  },
  methods: {
    async fetchRooms() {
      try {
        const response = await apiClient.get('rooms/');
        this.rooms = response.data.sort((a, b) => a.number - b.number);
      } catch (error) {
        console.error('Ошибка при загрузке комнат:', error);
      }
    },
    openRoomDetails(room) {
      this.selectedRoom = room;
    },
    closeDetails() {
      this.selectedRoom = null;
    },
    async addRoom() {
      try {
        const response = await apiClient.post('rooms/', this.newRoom);
        this.rooms.push(response.data);
        this.closeModal();
      } catch (error) {
        console.error('Ошибка при добавлении комнаты:', error);
      }
    },
    async deleteRoom() {
      if (confirm(`Вы уверены, что хотите удалить комнату №${this.selectedRoom.number}?`)) {
        try {
          await apiClient.delete(`rooms/${this.selectedRoom.id_room}/`);
          this.rooms = this.rooms.filter((room) => room.id_room !== this.selectedRoom.id_room);
          this.selectedRoom = null;
        } catch (error) {
          console.error('Ошибка при удалении комнаты:', error);
        }
      }
    },
    selectStatus(status) {
      this.newRoom.status = status;
    },
    closeModal() {
      this.showAddRoomModal = false;
      this.newRoom = { number: '', status: '' };
    },
  },
};
</script>
