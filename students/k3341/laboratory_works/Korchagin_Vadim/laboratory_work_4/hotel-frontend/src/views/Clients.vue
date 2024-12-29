<template>
  <v-container>
    <h2 class="mb-4">Клиенты</h2>

    <!-- Кнопка для вызова count_by_city -->
    <v-card class="mb-4 pa-2 elevated-card">
      <v-card-title class="text-h6">Поиск клиентов по городу</v-card-title>
      <v-card-text>
        <v-text-field
          v-model="cityParam"
          label="Город"
        ></v-text-field>
        <v-btn variant="outlined" color="primary" @click="countByCity">
          Посчитать
        </v-btn>
      </v-card-text>
      <v-card-subtitle v-if="cityResult !== null">
        Найдено клиентов: {{ cityResult }}
      </v-card-subtitle>
    </v-card>

    <!-- Кнопка для вызова clients_shared_stay -->
    <v-card class="mb-4 pa-2 elevated-card">
      <v-card-title class="text-h6">Пересекающиеся проживания</v-card-title>
      <v-card-text>
        <v-text-field
          v-model="sharedClientId"
          label="client_id"
          type="number"
        ></v-text-field>
        <v-btn variant="outlined" color="primary" @click="clientsSharedStay">
          Посмотреть
        </v-btn>
      </v-card-text>
      <v-card-subtitle v-if="sharedClients.length > 0">
        <div class="mt-2">
          <div v-for="c in sharedClients" :key="c.client_id">
            {{ c.last_name }} {{ c.first_name }} (ID={{ c.client_id }})
          </div>
        </div>
      </v-card-subtitle>
    </v-card>

    <!-- Кнопка для добавления клиента -->
    <v-btn
      variant="outlined"
      color="primary"
      class="mb-4"
      @click="openCreateDialog"
    >
      Добавить клиента
    </v-btn>

    <!-- Список клиентов -->
    <v-row>
      <v-col
        v-for="client in clients"
        :key="client.client_id"
        cols="12"
        md="6"
        lg="4"
      >
        <v-card class="elevated-card mb-4 pa-2">
          <v-card-item>
            <div>
              <div class="text-h6">{{ client.last_name }} {{ client.first_name }} {{ client.middle_name }}</div>
              <div class="text-subtitle-2 mb-2">
                Паспорт - {{ client.passport_number }}<br>
                Город - {{ client.city_of_origin }}
              </div>
              <div class="text-caption">
                Clinet ID - {{ client.client_id }}
              </div>
            </div>
          </v-card-item>
          <v-card-actions>
            <v-btn
              variant="outlined"
              color="primary"
              @click="editClient(client)"
            >
              Редактировать
            </v-btn>
            <v-btn
              variant="outlined"
              color="error"
              @click="deleteClient(client.client_id)"
            >
              Удалить
            </v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>

    <!-- Диалог для создания/редактирования клиента -->
    <v-dialog
      v-model="dialog"
      max-width="600px"
      persistent
    >
      <v-card class="dialog-card pa-6">
        <v-card-title class="dialog-title text-h5">
          {{ clientForm.client_id ? 'Редактирование клиента' : 'Новый клиент' }}
        </v-card-title>
        <v-card-text>
          <v-text-field
            v-model="clientForm.passport_number"
            label="Паспорт"
          ></v-text-field>
          <v-text-field
            v-model="clientForm.last_name"
            label="Фамилия"
          ></v-text-field>
          <v-text-field
            v-model="clientForm.first_name"
            label="Имя"
          ></v-text-field>
          <v-text-field
            v-model="clientForm.middle_name"
            label="Отчество"
          ></v-text-field>
          <v-text-field
            v-model="clientForm.city_of_origin"
            label="Город"
          ></v-text-field>
        </v-card-text>
        <v-card-actions>
          <v-btn variant="outlined" color="primary" @click="createOrUpdateClient">
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
  name: 'Clients',
  data() {
    return {
      clients: [],
      dialog: false,
      clientForm: {
        client_id: null,
        passport_number: '',
        last_name: '',
        first_name: '',
        middle_name: '',
        city_of_origin: ''
      },
      // Для count_by_city
      cityParam: '',
      cityResult: null,

      // Для clients_shared_stay
      sharedClientId: '',
      sharedClients: []
    }
  },
  async created() {
    this.fetchClients()
  },
  methods: {
    // Получение списка клиентов
    async fetchClients() {
      const token = localStorage.getItem('token')
      try {
        const response = await axios.get('http://127.0.0.1:8000/api/clients/', {
          headers: { Authorization: `Token ${token}` }
        })
        this.clients = response.data.results ? response.data.results : response.data
      } catch (error) {
        console.error(error)
      }
    },
    // Открытие диалога для создания клиента
    openCreateDialog() {
      this.clearForm()
      this.dialog = true
    },
    // Очистка формы клиента
    clearForm() {
      this.clientForm = {
        client_id: null,
        passport_number: '',
        last_name: '',
        first_name: '',
        middle_name: '',
        city_of_origin: ''
      }
    },
    // Редактирование клиента
    editClient(client) {
      this.clientForm = { ...client }
      this.dialog = true
    },
    // Создание или обновление клиента
    async createOrUpdateClient() {
      const token = localStorage.getItem('token')
      try {
        if (this.clientForm.client_id) {
          await axios.put(
            `http://127.0.0.1:8000/api/clients/${this.clientForm.client_id}/`,
            this.clientForm,
            { headers: { Authorization: `Token ${token}` }
          })
        } else {
          await axios.post(
            `http://127.0.0.1:8000/api/clients/`,
            this.clientForm,
            { headers: { Authorization: `Token ${token}` }
          })
        }
        this.dialog = false
        this.fetchClients()
      } catch (error) {
        console.error(error)
      }
    },
    // Удаление клиента
    async deleteClient(clientId) {
      const token = localStorage.getItem('token')
      try {
        await axios.delete(`http://127.0.0.1:8000/api/clients/${clientId}/`, {
          headers: { Authorization: `Token ${token}` }
        })
        this.fetchClients()
      } catch (error) {
        console.error(error)
      }
    },
    // Подсчет клиентов по городу
    async countByCity() {
      const token = localStorage.getItem('token')
      if (!this.cityParam) return
      try {
        const resp = await axios.get(`http://127.0.0.1:8000/api/clients/count_by_city/?city=${this.cityParam}`, {
          headers: { Authorization: `Token ${token}` }
        })
        this.cityResult = resp.data.client_count
      } catch (error) {
        console.error(error)
      }
    },
    // Получение пересекающихся проживаний
    async clientsSharedStay() {
      const token = localStorage.getItem('token')
      if (!this.sharedClientId) return
      try {
        const resp = await axios.get(`http://127.0.0.1:8000/api/clients/clients_shared_stay/?client_id=${this.sharedClientId}`, {
          headers: { Authorization: `Token ${token}` }
        })
        this.sharedClients = resp.data
      } catch (error) {
        console.error(error)
      }
    }
  }
}
</script>