<template>
  <v-container>
    <v-card>
      <v-card-title class="d-flex align-center">
        Клиенты
        <v-spacer></v-spacer>
        <v-btn color="primary" @click="openAddDialog">Добавить клиента</v-btn>
      </v-card-title>
      <v-card-text>
        <v-data-table :headers="headers" :items="clients" class="elevation-1">
          <template v-slot:item.actions="{ item }">
            <v-icon small class="mr-2" @click="openEditDialog(item)">mdi-pencil</v-icon>
            <v-icon small @click="confirmDelete(item)">mdi-delete</v-icon>
          </template>
        </v-data-table>
      </v-card-text>
    </v-card>

    <v-dialog v-model="dialog" max-width="500px">
      <v-card>
        <v-card-title>{{ isEditing ? 'Редактировать клиента' : 'Добавить клиента' }}</v-card-title>
        <v-card-text>
          <v-form ref="form">
            <v-text-field v-model="currentClient.passport_number" label="Паспорт"
                          required></v-text-field>
            <v-text-field v-model="currentClient.last_name" label="Фамилия" required></v-text-field>
            <v-text-field v-model="currentClient.first_name" label="Имя" required></v-text-field>
            <v-text-field v-model="currentClient.city" label="Город" required></v-text-field>
          </v-form>
        </v-card-text>
        <v-card-actions>
          <v-btn text @click="dialog = false">Отмена</v-btn>
          <v-btn color="blue darken-1" text @click="saveClient">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="deleteDialog" max-width="400px">
      <v-card>
        <v-card-title class="headline">Вы уверены?</v-card-title>
        <v-card-text>Удалить клиента {{ clientToDelete?.last_name }} {{
            clientToDelete?.first_name
          }}?
        </v-card-text>
        <v-card-actions>
          <v-btn text @click="deleteDialog = false">Отмена</v-btn>
          <v-btn color="red darken-1" text @click="deleteClient">Удалить</v-btn>
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
      deleteDialog: false,
      isEditing: false,
      currentClient: {passport_number: '', last_name: '', first_name: '', city: ''},
      clientToDelete: null,
      headers: [
        {title: 'Паспорт', value: 'passport_number'},
        {title: 'Фамилия', value: 'last_name', sortable: true},
        {title: 'Имя', value: 'first_name', sortable: true},
        {title: 'Город', value: 'city', sortable: true},
        {title: 'Действия', value: 'actions', align: 'center', sortable: false},
      ],
    }
  },
  created() {
    this.fetchClients()
  },
  methods: {
    fetchClients() {
      axios.get('http://localhost:8000/api/clients/')
        .then(response => {
          this.clients = response.data
        })
        .catch(error => {
          console.error(error)
        })
    },
    openAddDialog() {
      this.currentClient = {passport_number: '', last_name: '', first_name: '', city: ''}
      this.isEditing = false
      this.dialog = true
    },
    openEditDialog(client) {
      this.currentClient = {...client}
      this.isEditing = true
      this.dialog = true
    },
    saveClient() {
      if (this.isEditing) {
        axios.put(`http://localhost:8000/api/clients/${this.currentClient.id}/`, this.currentClient)
          .then(() => {
            this.fetchClients()
            this.dialog = false
          })
          .catch(error => {
            console.error(error)
          })
      } else {
        axios.post('http://localhost:8000/api/clients/', this.currentClient)
          .then(response => {
            this.clients.push(response.data)
            this.dialog = false
          })
          .catch(error => {
            console.error(error)
          })
      }
    },
    confirmDelete(client) {
      this.clientToDelete = client
      this.deleteDialog = true
    },
    deleteClient() {
      axios.delete(`http://localhost:8000/api/clients/${this.clientToDelete.id}/`)
        .then(() => {
          this.clients = this.clients.filter(c => c.id !== this.clientToDelete.id)
          this.deleteDialog = false
        })
        .catch(error => {
          console.error(error)
        })
    }
  }
}
</script>
