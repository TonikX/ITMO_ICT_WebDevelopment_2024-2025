<template>
  <v-container>
    <v-card>
      <v-card-title class="d-flex align-center">
        Список заселений
        <v-btn color="primary" class="ml-auto" @click="openNewCheckinDialog">Добавить заселение
        </v-btn>
      </v-card-title>
      <v-data-table :headers="headers" :items="checkins" class="elevation-1">
        <template v-slot:item.actions="{ item }">
          <v-icon small class="mr-2" @click="editCheckin(item)">mdi-pencil</v-icon>
          <v-icon small @click="confirmDelete(item)">mdi-delete</v-icon>
        </template>
      </v-data-table>
    </v-card>

    <v-snackbar v-model="errorSnackbar" color="red" timeout="5000">
      {{ errorMessage }}
      <v-btn text @click="errorSnackbar = false">Закрыть</v-btn>
    </v-snackbar>

    <v-dialog v-model="confirmDeleteDialog" max-width="400px">
      <v-card>
        <v-card-title>Подтверждение удаления</v-card-title>
        <v-card-text>Вы уверены, что хотите удалить запись заселения?</v-card-text>
        <v-card-actions>
          <v-btn color="blue darken-1" text @click="confirmDeleteDialog = false">Отмена</v-btn>
          <v-btn color="red" text @click="deleteCheckin">Удалить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title>{{
            editedIndex === -1 ? 'Добавить заселение' : 'Редактировать заселение'
          }}
        </v-card-title>
        <v-card-text>
          <v-form ref="form" v-model="valid">
            <v-autocomplete
              v-model="clientRoom.client_id"
              :items="clients"
              item-value="id"
              :item-title="formatClient"
              label="Клиент"
              required
              clearable
              :filter="customFilter"
            ></v-autocomplete>

            <v-autocomplete
              v-model="clientRoom.room"
              :items="rooms"
              item-value="id"
              item-title="number"
              label="Номер комнаты"
              required
              clearable
            ></v-autocomplete>

            <v-text-field v-model="clientRoom.check_in_date" label="Дата заезда" type="date"
                          required></v-text-field>
            <v-text-field v-model="clientRoom.check_out_date" label="Дата выезда"
                          type="date"></v-text-field>
            <v-text-field v-model="clientRoom.count_of_clients" label="Количество клиентов"
                          type="number" required></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-btn color="blue darken-1" text @click="closeDialog">Отмена</v-btn>
          <v-btn color="primary" :disabled="!valid" @click="validateAndSaveCheckin">
            {{ editedIndex === -1 ? 'Добавить' : 'Сохранить изменения' }}
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script>
import axios from 'axios';
import {tr} from "vuetify/locale";

export default {
  name: 'CheckInsView',
  data() {
    return {
      valid: false,
      dialog: false,
      confirmDeleteDialog: false,
      errorSnackbar: false,
      errorMessage: '',
      selectedCheckinId: null,
      clientRoom: {
        client_id: null,
        room: null,
        check_in_date: '',
        check_out_date: '',
        count_of_clients: 1,
      },
      checkins: [],
      clients: [],
      rooms: [],
      headers: [
        {title: 'Паспорт', value: 'client.passport_number'},
        {title: 'Фамилия', value: 'client.last_name', sortable: true},
        {title: 'Имя', value: 'client.first_name', sortable: true},
        {title: 'Город', value: 'client.city', sortable: true},
        {title: 'Комната', value: 'room_number', sortable: true},
        {title: 'Дата заезда', value: 'check_in_date', sortable: true},
        {title: 'Дата выезда', value: 'check_out_date', sortable: true},
        {title: 'Клиенты', value: 'count_of_clients', sortable: true},
        {title: 'Действия', value: 'actions', sortable: false}
      ],
      editedIndex: -1,
    };
  },
  methods: {
    confirmDelete(item) {
      this.selectedCheckinId = item.id;
      this.confirmDeleteDialog = true;
    },
    deleteCheckin() {
      console.log("Попытка удаления заселения с ID:", this.selectedCheckinId);

      if (!this.selectedCheckinId) {
        console.error("Ошибка: Не выбран ID заселения для удаления.");
        return;
      }

      axios.delete(`http://localhost:8000/api/check-ins/${this.selectedCheckinId}/`)
        .then(() => {
          console.log(`Заселение с ID ${this.selectedCheckinId} удалено.`);
          this.checkins = this.checkins.filter(c => c.id !== this.selectedCheckinId);
          this.confirmDeleteDialog = false;

          this.fetchRooms();
        })
        .catch(error => {
          console.error("Ошибка при удалении заселения:", error);
          console.error("Ответ сервера:", error.response?.data || "Нет данных");
          this.errorMessage = "Не удалось удалить заселение.";
          this.errorSnackbar = true;
        });
    },
    editCheckin(item) {
      this.editedIndex = this.checkins.findIndex(c => c.id === item.id);

      const currentRoom = {
        id: item.room,
        number: item.room_number
      };
      if (!this.rooms.some(r => r.id === currentRoom.id)) {
        this.rooms.push(currentRoom);
      }

      this.clientRoom = {
        client_id: item.client.id,
        client: item.client,
        room: item.room,
        check_in_date: item.check_in_date,
        check_out_date: item.check_out_date,
        count_of_clients: item.count_of_clients,
      };

      this.dialog = true;
    },
    formatClient(client) {
      return `${client.passport_number} - ${client.last_name} ${client.first_name}`;
    },
    customFilter(item, queryText) {
      const searchText = queryText.toLowerCase();
      return (
        item.passport_number.toLowerCase().includes(searchText) ||
        item.last_name.toLowerCase().includes(searchText) ||
        item.first_name.toLowerCase().includes(searchText)
      );
    },
    fetchCheckins() {
      axios.get('http://localhost:8000/api/check-ins/')
        .then(response => {
          this.checkins = response.data;
        })
        .catch(error => console.error('Ошибка при загрузке заселений:', error));
    },
    fetchClients() {
      axios.get('http://localhost:8000/api/clients/')
        .then(response => {
          this.clients = response.data;
        })
        .catch(error => console.error('Ошибка при загрузке клиентов:', error));
    },
    fetchRooms() {
      axios.get(`http://localhost:8000/api/rooms/?count_of_clients=${this.clientRoom.count_of_clients}`)
        .then(response => {
          this.rooms = response.data;
        })
        .catch(error => console.error('Ошибка при загрузке комнат:', error));
    },
    async validateAndSaveCheckin() {
      try {
        const response = await axios.get(`http://localhost:8000/api/rooms/?count_of_clients=${this.clientRoom.count_of_clients}`);
        let availableRoomIds = response.data.map(room => room.id);

        if (this.editedIndex !== -1) {
          const currentRoomId = this.checkins[this.editedIndex].room;
          if (!availableRoomIds.includes(currentRoomId)) {
            availableRoomIds.push(currentRoomId);
          }
        }

        if (!availableRoomIds.includes(parseInt(this.clientRoom.room))) {
          this.errorMessage = 'Выбранная комната недоступна для заселения!';
          this.errorSnackbar = true;
          return;
        }

        this.saveCheckin();
      } catch (error) {
        console.error('Ошибка при проверке доступных комнат:', error);
        this.errorMessage = 'Не удалось проверить доступность комнаты.';
        this.errorSnackbar = true;
      }
    },
    saveCheckin() {
      if (!this.clientRoom.client && this.clientRoom.client_id) {
        this.clientRoom.client = this.clients.find(c => c.id === this.clientRoom.client_id);
      }

      if (!this.clientRoom.client || !this.clientRoom.client.passport_number) {
        console.error("Ошибка: клиент не выбран или данные неполные.");
        this.errorMessage = "Выберите клиента!";
        this.errorSnackbar = true;
        return;
      }

      const payload = {
        client: {
          passport_number: this.clientRoom.client.passport_number,
          first_name: this.clientRoom.client.first_name,
          last_name: this.clientRoom.client.last_name,
          city: this.clientRoom.client.city || "",
        },
        room: this.clientRoom.room,
        check_in_date: this.clientRoom.check_in_date,
        check_out_date: this.clientRoom.check_out_date || null,
        count_of_clients: this.clientRoom.count_of_clients
      };

      if (this.editedIndex !== -1) {
        const id = this.checkins[this.editedIndex].id;
        axios.put(`http://localhost:8000/api/check-ins/${id}/`, payload)
          .then(response => {
            console.log('Обновлено:', response.data);
            this.checkins[this.editedIndex] = response.data;
            this.closeDialog();
            this.fetchCheckins();
            this.fetchRooms();
          })
          .catch(this.handleError);
      } else {
        axios.post('http://localhost:8000/api/check-ins/', payload)
          .then(response => {
            console.log('Добавлено:', response.data);
            this.checkins.push(response.data);
            this.closeDialog();
            this.fetchCheckins();
            this.fetchRooms();
          })
          .catch(this.handleError);
      }
    },
    handleError(error) {
      if (error.response && error.response.status === 400) {
        this.errorMessage = 'Ошибка при сохранении данных!';
        this.errorSnackbar = true;
      } else {
        console.error('Ошибка при обработке запроса:', error);
      }
    },
    openNewCheckinDialog() {
      this.resetForm();
      this.fetchRooms();
      this.dialog = true;
    },
    closeDialog() {
      this.dialog = false;
      this.resetForm();
    },
    resetForm() {
      this.clientRoom = {
        client_id: null,
        room: null,
        check_in_date: '',
        check_out_date: '',
        count_of_clients: 1,
      };
      this.editedIndex = -1;
      this.valid = false;
    }
  },
  mounted() {
    this.fetchCheckins();
    this.fetchClients();
    this.fetchRooms();
  }
};
</script>
