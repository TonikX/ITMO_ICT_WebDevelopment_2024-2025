<template>
  <v-container>
    <h2 class="mb-4">Профиль пользователя</h2>

    <!-- Основная карта с данными пользователя -->
    <v-card class="elevated-card pa-4 mb-4">
      <v-card-title class="text-h5">Информация пользователе</v-card-title>
      <v-card-text>
        <div><strong>Роль:</strong> {{ userData.is_staff ? 'Администратор' : 'Пользователь' }}</div>
        <div><strong>Имя пользователя:</strong> {{ userData.username }}</div>
        <div><strong>Email:</strong> {{ userData.email }}</div>
      </v-card-text>
      <v-card-actions class="d-flex justify-center">
        <v-btn variant="elevated" color="primary" @click="editProfile">Редактировать профиль</v-btn>
        <v-btn variant="outlined" color="error" @click="logout">Выйти</v-btn>
      </v-card-actions>
    </v-card>

    <!-- Карточка с данными о клиенте (Client) -->
    <v-card v-if="userClientData" class="elevated-card pa-4 mb-4">
      <v-card-title class="text-h5">
        Мои данные
      </v-card-title>
      <v-card-text>
        <div>
          <strong>ФИО:</strong>
          {{ userClientData.last_name }} {{ userClientData.first_name }} {{ userClientData.middle_name }}
        </div>
        <div>
          <strong>Паспорт:</strong> {{ userClientData.passport_number }}
        </div>
        <div>
          <strong>Город:</strong> {{ userClientData.city_of_origin }}
        </div>
      </v-card-text>
      <v-card-actions class="d-flex justify-center">
        <v-btn variant="elevated" color="primary" @click="editClient">
          Редактировать данные
        </v-btn>
        <v-btn variant="outlined" color="error" @click="deleteClient">
          Удалить данные
        </v-btn>
      </v-card-actions>
    </v-card>

    <!-- Если клиентские данные отсутствуют, показываем кнопку "Добавить" -->
    <v-card v-else class="elevated-card pa-4 mb-4">
      <v-card-title class="text-h5">У вас нет клиентской информации</v-card-title>
      <v-card-text>
        Хотите добавить собственные данные клиента?
      </v-card-text>
      <v-card-actions>
        <v-btn variant="elevated" color="primary" @click="createClientData">
          Добавить данные клиента
        </v-btn>
      </v-card-actions>
    </v-card>

    <!-- Карточка с бронированиями (Stays) -->
    <v-card class="elevated-card pa-4 mb-4">
      <v-card-title class="text-h5">Мои бронирования</v-card-title>
      <v-card-text>
        <div v-if="userStays.length === 0">
          Нет текущих бронирований
        </div>
        <v-row v-else>
          <v-col
            v-for="stay in userStays"
            :key="stay.stay_id"
            cols="12"
            md="6"
            lg="4"
          >
            <v-card class="mb-4 elevated-card pa-2">
              <v-card-item>
                <div>
                  <div class="text-h6">
                    Номер: {{ stay.room?.room_id }} (Этаж: {{ stay.room?.floor }})
                  </div>
                  <div class="text-subtitle-2 mb-2">
                    Дата заезда: {{ stay.check_in_date }}<br/>
                    Дата выезда: {{ stay.check_out_date }}
                  </div>
                </div>
              </v-card-item>
              <v-card-actions>
                <v-btn variant="elevated" color="primary" @click="editStay(stay)">
                  Редактировать
                </v-btn>
                <v-btn variant="outlined" color="error" @click="deleteStay(stay.stay_id)">
                  Удалить
                </v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-card-text>
      <v-card-actions>
        <v-btn variant="elevated" color="primary" @click="createStay">
          Добавить бронирование
        </v-btn>
      </v-card-actions>
    </v-card>

    <!-- Диалог редактирования профиля -->
    <v-dialog v-model="dialogProfile" max-width="500px" persistent>
      <v-card class="dialog-card pa-6">
        <v-card-title class="dialog-title text-h5">
          Редактирование профиля
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text>
          <v-text-field v-model="userForm.username" label="Имя пользователя"></v-text-field>
          <v-text-field v-model="userForm.email" label="Email"></v-text-field>
          <v-text-field v-model="userForm.password" label="Пароль" type="password"></v-text-field>
          <v-text-field v-model="userForm.password2" label="Повторите пароль" type="password"></v-text-field>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions class="d-flex justify-end">
          <v-btn variant="outlined" color="primary" class="mr-2" @click="saveProfile">
            Сохранить
          </v-btn>
          <v-btn variant="outlined" color="error" @click="dialogProfile = false">
            Отмена
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Диалог редактирования/добавления клиента -->
    <v-dialog v-model="dialogClient" max-width="600px" persistent>
      <v-card class="dialog-card pa-6">
        <v-card-title class="dialog-title text-h5">
          {{ userClientData?.client_id ? 'Редактирование данных клиента' : 'Новые данные клиента' }}
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text>
          <v-text-field v-model="clientForm.passport_number" label="Паспорт"></v-text-field>
          <v-text-field v-model="clientForm.last_name" label="Фамилия"></v-text-field>
          <v-text-field v-model="clientForm.first_name" label="Имя"></v-text-field>
          <v-text-field v-model="clientForm.middle_name" label="Отчество"></v-text-field>
          <v-text-field v-model="clientForm.city_of_origin" label="Город"></v-text-field>
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions class="d-flex justify-end">
          <v-btn variant="outlined" color="primary" class="mr-2" @click="saveClient">
            Сохранить
          </v-btn>
          <v-btn variant="outlined" color="error" @click="dialogClient = false">
            Отмена
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <!-- Диалог создания/редактирования бронирования (Stay) -->
    <v-dialog v-model="dialogStay" max-width="600px" persistent>
      <v-card class="dialog-card pa-6">
        <v-card-title class="dialog-title text-h5">
          {{ stayForm.stay_id ? 'Редактирование бронирования' : 'Новое бронирование' }}
        </v-card-title>
        <v-divider></v-divider>
        <v-card-text>
          <v-text-field
            v-if="clientForm.client_id"
            :value="clientForm.client_id"
            label="Ваш client_id"
            disabled
          />
          <v-select
            v-model="stayForm.room_id"
            :items="availableRooms"
            item-title="roomDisplay"
            item-value="room_id"
            :return-object="false"
            label="Номер"
          />
          <v-text-field
            v-model="stayForm.check_in_date"
            label="Дата заезда (YYYY-MM-DD)"
          />
          <v-text-field
            v-model="stayForm.check_out_date"
            label="Дата выезда (YYYY-MM-DD)"
          />
        </v-card-text>
        <v-divider></v-divider>
        <v-card-actions class="d-flex justify-end">
          <v-btn variant="outlined" color="primary" class="mr-2" @click="saveStay">
            Сохранить
          </v-btn>
          <v-btn variant="outlined" color="error" @click="dialogStay = false">
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
  name: 'Profile',
  data() {
    return {
      userData: {},         // данные из /auth/users/me/
      userClientData: null, // данные клиента, связанные с пользователем
      userStays: [],        // список бронирований, связанных с пользователем
      dialogProfile: false,
      dialogClient: false,
      dialogStay: false,

      userForm: {
        username: '',
        email: '',
        password: '',
        password2: ''
      },
      clientForm: {
        client_id: null,
        passport_number: '',
        last_name: '',
        first_name: '',
        middle_name: '',
        city_of_origin: ''
      },
      stayForm: {
        stay_id: null,
        room_id: null,
        check_in_date: '',
        check_out_date: ''
      },

      availableRooms: []
    }
  },
  async created() {
    await this.fetchUserData()
    await this.fetchUserClientData()
    await this.fetchUserStays()
    await this.fetchRooms()
  },
  methods: {
    // --- [1] Профиль ---
    async fetchUserData() {
      const token = localStorage.getItem('token')
      try {
        const response = await axios.get('http://127.0.0.1:8000/auth/users/me/', {
          headers: { Authorization: `Token ${token}` }
        })
        this.userData = response.data
      } catch (error) {
        console.error('Ошибка при загрузке данных пользователя', error)
      }
    },
    editProfile() {
      this.userForm = {
        username: this.userData.username,
        email: this.userData.email,
        password: '',
        password2: ''
      }
      this.dialogProfile = true
    },
    async saveProfile() {
      const token = localStorage.getItem('token')
      if (this.userForm.password !== this.userForm.password2) {
        console.error('Пароли не совпадают')
        return
      }
      try {
        await axios.put('http://127.0.0.1:8000/auth/users/me/', this.userForm, {
          headers: { Authorization: `Token ${token}` }
        })
        this.dialogProfile = false
        this.fetchUserData()
      } catch (error) {
        console.error('Ошибка при обновлении профиля', error)
      }
    },

    logout() {
      localStorage.removeItem('token')
      this.$router.push('/start')
    },

    // ---  Клиентские данные ---
    async fetchUserClientData() {
      const token = localStorage.getItem('token')
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/clients/me/', {
          headers: { Authorization: `Token ${token}` }
        })
        this.userClientData = response.data
        this.clientForm = { ...response.data }
      } catch (error) {
        console.error('Данные клиента не найдены или не созданы', error)
      }
    },
    createClientData() {
      this.clientForm = {
        client_id: null,
        passport_number: '',
        last_name: '',
        first_name: '',
        middle_name: '',
        city_of_origin: ''
      }
      this.dialogClient = true
    },
    editClient() {
      if (!this.userClientData) return
      this.clientForm = { ...this.userClientData }
      this.dialogClient = true
    },
    async saveClient() {
      const token = localStorage.getItem('token')
      try {
        if (this.clientForm.client_id) {
          await axios.put(
            `http://127.0.0.1:8000/api/clients/${this.clientForm.client_id}/`,
            this.clientForm,
            { headers: { Authorization: `Token ${token}` } }
          )
        } else {
          await axios.post('http://127.0.0.1:8000/api/clients/', this.clientForm, {
            headers: { Authorization: `Token ${token}` }
          })
        }
        this.dialogClient = false
        this.fetchUserClientData()
      } catch (error) {
        console.error('Ошибка при сохранении данных клиента', error)
      }
    },
    async deleteClient() {
      if (!this.userClientData?.client_id) return
      const token = localStorage.getItem('token')
      try {
        await axios.delete(`http://127.0.0.1:8000/api/clients/${this.userClientData.client_id}/`, {
          headers: { Authorization: `Token ${token}` }
        })
        this.userClientData = null
        this.clientForm = {
          client_id: null,
          passport_number: '',
          last_name: '',
          first_name: '',
          middle_name: '',
          city_of_origin: ''
        }
      } catch (error) {
        console.error('Ошибка при удалении клиента', error)
      }
    },

    // --- Бронирования (проживания) ---
    async fetchUserStays() {
      const token = localStorage.getItem('token')
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/stays/user/', {
          headers: { Authorization: `Token ${token}` }
        })
        this.userStays = response.data
      } catch (error) {
        console.error('Ошибка при загрузке списка бронирований', error)
      }
    },
    async fetchRooms() {
      const token = localStorage.getItem('token')
      try {
        const res = await axios.get('http://127.0.0.1:8000/api/rooms/', {
          headers: { Authorization: `Token ${token}` }
        })
        // Показываем только свободные номера: is_available === true
        const allRooms = res.data
        this.availableRooms = allRooms
          .filter(r => r.is_available)
          .map(room => ({
            ...room,
            roomDisplay: `Номер ${room.room_id}, Этаж ${room.floor}`
          }))
      } catch (error) {
        console.error('Ошибка при загрузке списка номеров', error)
      }
    },
    createStay() {
      this.stayForm = {
        stay_id: null,
        // Если у нас уже есть userClientData, берём его id
        client_id: this.clientForm.client_id || null,
        room_id: null,
        check_in_date: '',
        check_out_date: ''
      }
      this.dialogStay = true
    },
    editStay(stay) {
      this.stayForm = {
        stay_id: stay.stay_id,
        client_id: stay.client ? stay.client.client_id : null,
        room_id: stay.room ? stay.room.room_id : null,
        check_in_date: stay.check_in_date,
        check_out_date: stay.check_out_date
      }
      this.dialogStay = true
    },
    async saveStay() {
      const token = localStorage.getItem('token')
      try {
        if (this.stayForm.stay_id) {
          await axios.put(
            `http://127.0.0.1:8000/api/stays/${this.stayForm.stay_id}/`,
            this.stayForm,
            { headers: { Authorization: `Token ${token}` } }
          )
        } else {
          await axios.post(
            'http://127.0.0.1:8000/api/stays/',
            this.stayForm,
            { headers: { Authorization: `Token ${token}` } }
          )
        }
        this.dialogStay = false
        this.fetchUserStays()
        this.fetchRooms() // чтобы список свободных номеров был актуален
      } catch (error) {
        console.error('Ошибка при сохранении бронирования', error)
      }
    },
    async deleteStay(stayId) {
      const token = localStorage.getItem('token')
      try {
        await axios.delete(`http://127.0.0.1:8000/api/stays/${stayId}/`, {
          headers: { Authorization: `Token ${token}` }
        })
        this.fetchUserStays()
        this.fetchRooms()
      } catch (error) {
        console.error('Ошибка при удалении бронирования', error)
      }
    }
  }
}
</script>