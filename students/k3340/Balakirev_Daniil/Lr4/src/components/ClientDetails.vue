<template>
  <v-card v-if="client">
    <v-card-title>{{ fullName }}</v-card-title>
    <v-card-subtitle>Паспорт: {{ client.passport_number }}</v-card-subtitle>
    <v-card-text>
      Город: {{ client.city }}
    </v-card-text>

    <v-card-actions>
      <v-btn color="primary" @click="openEditForm" v-if="!edit">Редактировать</v-btn>
      <v-btn color="error" @click="del = true" v-if="!edit">Удалить</v-btn>
      <v-btn color="blue-grey lighten-1" text @click="$emit('close')">Закрыть</v-btn>
    </v-card-actions>

    <v-dialog v-model="edit" max-width="500px">
      <v-card>
        <v-card-title>Редактировать</v-card-title>
        <v-card-text>
          <v-container>
            <v-row>
              <v-col cols="12">
                <v-text-field v-model="editedClient.last_name" label="Фамилия" required></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field v-model="editedClient.first_name" label="Имя" required></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field v-model="editedClient.middle_name" label="Отчество"></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field v-model="editedClient.passport_number" label="Паспорт" required></v-text-field>
              </v-col>
              <v-col cols="12">
                <v-text-field v-model="editedClient.city" label="Город" required></v-text-field>
              </v-col>
            </v-row>
          </v-container>
        </v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue-grey lighten-1" text @click="edit = false">Отменить</v-btn>
          <v-btn color="primary" @click="editClient" :disabled="!valid">Сохранить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-dialog v-model="del" max-width="500px">
      <v-card>
        <v-card-title>Подтвердить удаление</v-card-title>
        <v-card-text>Вы уверены что хотите удалить этого клиента?</v-card-text>
        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="blue-grey lighten-1" text @click="del = false">Отменить</v-btn>
          <v-btn color="error" @click="deleteClient">Удалить</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-snackbar v-model="snackbar" :color="snackbarColor" :timeout="3000">
      {{ snackbarText }}
      <template v-slot:action="{ attrs }">
        <v-btn color="white" text v-bind="attrs" @click="snackbar = false">
          Close
        </v-btn>
      </template>
    </v-snackbar>
  </v-card>
</template>

<script>
export default {
  name: 'ClientDetails',
  props: {
    client: {
      type: Object,
      required: true,
    },
  },
  data() {
    return {
      edit: false,
      del: false,
      editedClient: {
        last_name: '',
        first_name: '',
        middle_name: '',
        passport_number: '',
        city: ''
      },
      valid: true,
      snackbar: false,
      snackbarText: '',
      snackbarColor: 'error'
    };
  },
  methods: {
    openEditForm() {
      this.editedClient = { ...this.client };
      this.edit = true;
    },
    async editClient() {
      try {
        const response = await this.axios.put(
          this.$hostname + 'clients/' + this.client.id + '/',
          this.editedClient,
          {
            headers: {
              Authorization: 'Token ' + localStorage.getItem('auth_token')
            }
          }
        );

        if (response.status === 200) {
          this.showSnackbar('Client updated successfully', 'success');
          this.edit = false;
          this.$emit('client-updated');
        } else {
          this.showSnackbar('Error updating client', 'error');
        }
      } catch (error) {
        console.error(error);
        this.showSnackbar('Error updating client: ' + error.message, 'error');
      }
    },
    async deleteClient() {
      try {
        await this.axios.delete(this.$hostname + 'clients/' + this.client.id + '/', {
          headers: { Authorization: 'Token ' + localStorage.getItem('auth_token') }
        });

        this.del = false;
        this.showSnackbar('Client deleted successfully', 'success');
        this.$emit('client-deleted', this.client);
      } catch (error) {
        console.error(error);
        this.showSnackbar('Error deleting client: ' + error.message, 'error');
      }
    },
    showSnackbar(text, color = 'error') {
      this.snackbarText = text;
      this.snackbarColor = color;
      this.snackbar = true;
    }
  },
  computed: {
    fullName() {
      if (this.client) {
        return `${this.client.last_name}${this.client.first_name ? ` ${this.client.first_name}` : ''}`;
      }
      return '';
    },
  },
  created() {
    this.$hostname = 'http://localhost:8000/api/';
  },
}
</script>