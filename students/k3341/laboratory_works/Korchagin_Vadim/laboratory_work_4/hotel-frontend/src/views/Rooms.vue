<template>
  <v-container>
    <h2 class="mb-4">Номера</h2>
    
    <!-- Кнопка для добавления нового номера -->
    <v-btn
      variant="outlined"
      color="primary"
      class="mb-4"
      @click="openCreateDialog"
    >
      Добавить номер
    </v-btn>

    <!-- Список номеров -->
    <v-row>
      <v-col
        v-for="room in rooms"
        :key="room.room_id"
        cols="12"
        md="6"
        lg="4"
      >
        <v-card class="mb-4 elevated-card pa-2">
          <v-card-item>
            <div>
              <div class="text-h6">
                {{ room.room_type }} - {{ room.is_available ? 'Свободен' : 'Занят' }}
              </div>
              <div class="text-subtitle-2 mb-2">
                Этаж - {{ room.floor }} <br>
                Стоимость в сутки - {{ room.cost_per_day }} <br>
                Телефон - {{ room.phone_number }}
              </div>
              <div class="text-caption">
                ID - {{ room.room_id }} 
              </div>
            </div>
          </v-card-item>
          <!-- Действия с номером -->
          <v-card-actions>
            <v-btn
              variant="outlined"
              color="primary"
              @click="editRoom(room)"
            >
              Редактировать
            </v-btn>
            <v-btn
              variant="outlined"
              color="error"
              @click="deleteRoom(room.room_id)"
            >
              Удалить
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- Диалоговое окно для создания/редактирования номера -->
    <v-dialog
      v-model="dialog"
      max-width="600px"
      persistent
    >
      <v-card class="dialog-card pa-6">
        <!-- Заголовок диалога -->
        <v-card-title class="my-dialog-title dialog-title">
          {{ roomForm.room_id ? 'Редактирование номера' : 'Новый номер' }}
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text>
          <v-select
            v-model="roomForm.room_type"
            :items="roomTypes"
            label="Тип номера"
            dense
          ></v-select>
          <v-text-field
            v-model="roomForm.cost_per_day"
            label="Стоимость в сутки"
            type="number"
            dense
          ></v-text-field>
          <v-text-field
            v-model="roomForm.floor"
            label="Этаж"
            type="number"
            dense
          ></v-text-field>
          <v-switch
            v-model="roomForm.is_available"
            label="Свободен?"
            hide-details
          ></v-switch>
          <v-text-field
            v-model="roomForm.phone_number"
            label="Телефон номера"
            dense
          ></v-text-field>
        </v-card-text>
        <v-divider></v-divider>
        <!-- Действия в диалоге -->
        <v-card-actions class="d-flex justify-end">
          <v-btn
            variant="outlined"
            color="primary"
            @click="createOrUpdateRoom"
            class="mr-2"
          >
            Сохранить
          </v-btn>
          <v-btn
            variant="outlined"
            color="error"
            @click="dialog = false"
          >
            Отмена
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import axios from 'axios'
export default {
  name: 'Rooms',
  data() {
    return {
      rooms: [],
      dialog: false,
      roomForm: {
        room_id: null,
        room_type: 'SINGLE',
        cost_per_day: 0,
        floor: 1,
        is_available: true,
        phone_number: ''
      },
      roomTypes: ['SINGLE', 'DOUBLE', 'TRIPLE']
    }
  },
  async created() {
    this.fetchRooms()
  },
  methods: {
    async fetchRooms() {
      const token = localStorage.getItem('token')
      try {
        const res = await axios.get('http://127.0.0.1:8000/api/rooms/', {
          headers: { Authorization: `Token ${token}` }
        })
        this.rooms = res.data
      } catch (error) {
        console.error(error)
      }
    },
    openCreateDialog() {
      this.clearForm()
      this.dialog = true
    },
    clearForm() {
      this.roomForm = {
        room_id: null,
        room_type: 'SINGLE',
        cost_per_day: 0,
        floor: 1,
        is_available: true,
        phone_number: ''
      }
    },
    editRoom(room) {
      this.roomForm = { ...room }
      this.dialog = true
    },
    // Создание или обновление номера
    async createOrUpdateRoom() {
      const token = localStorage.getItem('token')
      try {
        if (this.roomForm.room_id) {
          await axios.put(
            `http://127.0.0.1:8000/api/rooms/${this.roomForm.room_id}/`,
            this.roomForm,
            { headers: { Authorization: `Token ${token}` } }
          )
        } else {
          await axios.post(
            'http://127.0.0.1:8000/api/rooms/',
            this.roomForm,
            { headers: { Authorization: `Token ${token}` } }
          )
        }
        this.dialog = false
        this.fetchRooms()
      } catch (error) {
        console.error(error)
      }
    },
    // Удаление номера по ID
    async deleteRoom(id) {
      const token = localStorage.getItem('token')
      try {
        await axios.delete(`http://127.0.0.1:8000/api/rooms/${id}/`, {
          headers: { Authorization: `Token ${token}` }
        })
        this.fetchRooms()
      } catch (error) {
        console.error(error)
      }
    }
  }
}
</script>