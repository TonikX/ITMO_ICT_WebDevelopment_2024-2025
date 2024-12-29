<template>
  <v-container>
    <h2 class="mb-4">Расписания уборок</h2>
    
    <!-- Кнопка для добавления нового расписания -->
    <v-btn
      variant="outlined"
      color="primary"
      class="mb-4"
      @click="openDialog"
    >
      Добавить расписание
    </v-btn>

    <!-- Список расписаний -->
    <v-row>
      <v-col
        v-for="schedule in schedules"
        :key="schedule.cleaning_schedule_id"
        cols="12"
        md="6"
        lg="4"
      >
        <v-card class="mb-4 elevated-card pa-2">
          <v-card-item>
            <div>
              <div class="text-h6">
                Этаж: {{ schedule.floor }} - {{ schedule.time_and_day_of_week }}
              </div>
              <div class="text-subtitle-2 mb-2">
                Комната: {{ schedule.room?.room_id }} <br>
                Сотрудник: {{ schedule.staff?.last_name }} {{ schedule.staff?.first_name }} {{ schedule.staff?.middle_name }}
              </div>
              <div class="text-caption">
                ID: {{ schedule.cleaning_schedule_id }}
              </div>
            </div>
          </v-card-item>
          
          <!-- Действия с расписанием -->
          <v-card-actions>
            <v-btn
              variant="outlined"
              color="primary"
              @click="editSchedule(schedule)"
            >
              Редактировать
            </v-btn>
            <v-btn
              variant="outlined"
              color="error"
              @click="deleteSchedule(schedule.cleaning_schedule_id)"
            >
              Удалить
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- Диалоговое окно для создания или редактирования расписания -->
    <v-dialog
      v-model="dialog"
      max-width="600px"
      persistent
      >
      <v-card class="dialog-card pa-6">
        <v-card-title class="my-dialog-title dialog-title">
          {{ scheduleForm.cleaning_schedule_id ? 'Редактирование' : 'Новое' }} расписание
        </v-card-title>
        <v-card-text>
          <v-select
            v-model="scheduleForm.staff_id"
            :items="staffList"
            item-title="fullName"
            item-value="staff_id"
            :return-object="false"
            label="Сотрудник"
          />
          <v-select
            v-model="scheduleForm.room_id"
            :items="roomsList"
            item-title="roomDisplay"
            item-value="room_id"
            label="Комната"
            :return-object="false"
            :allow-empty="true"
          />
          <v-text-field
            v-model="scheduleForm.floor"
            label="Этаж"
            type="number"
          />
          <v-text-field
            v-model="scheduleForm.time_and_day_of_week"
            label="День/время"
          />
        </v-card-text>
        <v-card-actions>
          <v-btn variant="outlined" color="primary" @click="createOrUpdateSchedule">
            Сохранить
          </v-btn>
          <v-btn variant="outlined" color="error" @click="dialog = false">
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
  name: 'Schedules',
  data() {
    return {
      schedules: [],
      dialog: false,
      scheduleForm: {
        cleaning_schedule_id: null,
        staff_id: null,
        room_id: null,
        floor: 1,
        time_and_day_of_week: ''
      },
      staffList: [],
      roomsList: []
    }
  },
  async created() {
    this.fetchSchedules()
    this.fetchStaff()
    this.fetchRooms()
  },
  methods: {
    // Получение списка расписаний
    async fetchSchedules() {
      const token = localStorage.getItem('token')
      try {
        const res = await axios.get('http://127.0.0.1:8000/api/cleaning-schedules/', {
          headers: { Authorization: `Token ${token}` }
        })
        this.schedules = res.data
      } catch (error) {
        console.error(error)
      }
    },
    // Получение списка сотрудников
    async fetchStaff() {
      const token = localStorage.getItem('token')
      try {
        const res = await axios.get('http://127.0.0.1:8000/api/staff/', {
          headers: { Authorization: `Token ${token}` }
        })
        this.staffList = res.data.map(stuff => ({
          ...stuff,
          fullName: `${stuff.last_name} ${stuff.first_name} ${stuff.middle_name}` || 'NoName'
        }))
      } catch (error) {
        console.error(error)
      }
    },
    // Получение списка комнат
    async fetchRooms() {
      const token = localStorage.getItem('token')
      try {
        const res = await axios.get('http://127.0.0.1:8000/api/rooms/', {
          headers: { Authorization: `Token ${token}` }
        })
        this.roomsList = res.data.map(room => ({
          ...room,
          roomDisplay: `Room ${room.room_id}`
        }))
      } catch (error) {
        console.error(error)
      }
    },
    // Открытие диалогового окна
    openDialog() {
      this.scheduleForm = {
        cleaning_schedule_id: null,
        staff_id: null,
        room_id: null,
        floor: 1,
        time_and_day_of_week: ''
      }
      this.dialog = true
    },
    // Редактирование расписания
    editSchedule(item) {
      this.scheduleForm = {
        cleaning_schedule_id: item.cleaning_schedule_id,
        staff_id: item.staff?.staff_id || null,
        room_id: item.room?.room_id || null,
        floor: item.floor,
        time_and_day_of_week: item.time_and_day_of_week
      }
      this.dialog = true
    },
    // Создание или обновление расписания
    async createOrUpdateSchedule() {
      const token = localStorage.getItem('token')
      try {
        if (this.scheduleForm.cleaning_schedule_id) {
          await axios.put(
            `http://127.0.0.1:8000/api/cleaning-schedules/${this.scheduleForm.cleaning_schedule_id}/`,
            this.scheduleForm,
            { headers: { Authorization: `Token ${token}` } }
          )
        } else {
          await axios.post(
            'http://127.0.0.1:8000/api/cleaning-schedules/',
            this.scheduleForm,
            { headers: { Authorization: `Token ${token}` } }
          )
        }
        this.dialog = false
        this.fetchSchedules()
      } catch (error) {
        console.error(error)
      }
    },
    // Удаление расписания
    async deleteSchedule(id) {
      const token = localStorage.getItem('token')
      try {
        await axios.delete(`http://127.0.0.1:8000/api/cleaning-schedules/${id}/`, {
          headers: { Authorization: `Token ${token}` }
        })
        this.fetchSchedules()
      } catch (error) {
        console.error(error)
      }
    }
  }
}
</script>