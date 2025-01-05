<template>
  <v-container>
    <h1 class="text-center">Список клиентов</h1>
    <v-divider class="my-4"></v-divider>

    <v-dialog v-model="showForm" max-width="500">
      <v-card>
        <v-card-title>Создание нового клиента</v-card-title>
        <v-card-text>
        <v-form ref="clientForm" v-model="isValid" lazy-validation>
          <v-text-field
            v-model="newClient.passport_number"
              label="Номер паспорта"
              :rules="[rules.required]"
              required
          ></v-text-field>
          <v-text-field
            v-model="newClient.last_name"
            label="Фамилия"
            :rules="[rules.required]"
            required
          ></v-text-field>
          <v-text-field
            v-model="newClient.first_name"
            label="Имя"
            :rules="[rules.required]"
            required
          ></v-text-field>
          <v-text-field
            v-model="newClient.city"
            label="Город"
            :rules="[rules.required]"
            required
          ></v-text-field>
        </v-form>
          </v-card-text>
          <v-card-actions>
            <v-btn color="primary" :disabled="!isValid" @click="submitClient">Создать</v-btn>
            <v-btn variant="text" @click="resetForm">Сбросить</v-btn>
          <v-btn variant="text" @click="showForm = false">Закрыть</v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>

    <v-select
      v-model="selectedCity"
      :items="cities"
      label="Отфильтровать по городу"
      class="mb-4"
    ></v-select>

    <v-data-table
      :headers="headers"
      :items="filteredClients"
      class="elevation-1"
      dense
    >
      <template v-slot:top>
        <v-toolbar flat>
          <v-toolbar-title>Клиенты</v-toolbar-title>
          <v-spacer></v-spacer>
          <v-btn color="primary" @click="fetchClients">Обновить</v-btn>
          <v-btn color="green" variant="text" @click="showForm = true">Добавить клиента</v-btn>
        </v-toolbar>
      </template>

      <template v-slot:item.room_number="{ item }">
        {{ item.room_number !== null ? item.room_number : "-" }}
      </template>

      <template #item.actions="{ item }">
        <v-btn v-if="item.room_number === null" variant="text" color="green" @click="openDialog(item)">Заселить</v-btn>
        <v-btn v-if="item.room_number !== null" variant="text" color="red" @click="openDialog(item)">Выселить</v-btn>
      </template>
    </v-data-table>

    <v-dialog v-model="isDialogOpen" max-width="500px">
      <v-card>
        <v-card-title>
          <span class="headline">
            {{ selectedClient?.room_number !== null ? "Подтвердите выселение" : "Заселение клиента" }}
          </span>
        </v-card-title>

        <v-card-text>
          <div v-if="selectedClient?.room_number === null">
            <p>Выберите комнату для заселения:</p>
            <v-select
              :items="availableRooms"
              v-model="selectedRoom"
              label="Свободные комнаты"
              outlined
            ></v-select>
          </div>
          <div v-else>
            <p>Вы уверены, что хотите выселить клиента из комнаты {{ selectedClient?.room_number }}?</p>
          </div>
        </v-card-text>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn color="grey" variant="text" @click="closeDialog">Отмена</v-btn>
          <v-btn color="primary" @click="handleAction">
            Подтвердить
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </v-container>
</template>

<script lang="ts">
import { defineComponent, ref, onMounted } from "vue";
import type Client from "@/models/client";
import axiosApi from "@/plugins/axios";
import type Reservation from "@/models/reservation";
import type Room from "@/models/room";

export default defineComponent({
  name: "ClientsPage",
  setup() {
    const selectedCity = ref('Все');
    const filteredClients = computed(() => {
      if (selectedCity.value === 'Все') {
        return clients.value;
      }
        return clients.value.filter(client => client.city === selectedCity.value);
    });
    const clients = ref([] as Client[]);
    const cities = ref([] as string[]);
    const headers = ref([
      { title: "ID", value: "id" },
      { title: "Номер паспорта", value: "passport_number" },
      { title: "Имя", value: "first_name" },
      { title: "Фамилия", value: "last_name" },
      { title: "Город", value: "city" },
      { title: "Заселён в комнату", value: "room_number" },
      { title: "Действия", value: 'actions' },
    ]);
    const clientForm = ref();
    const isValid = ref(false);
    const showForm = ref(false);

    const newClient = reactive<Client>({
      id: 0,
      passport_number: '',
      last_name: '',
      first_name: '',
      city: '',
      room_number: null
    });

    const rooms = ref([] as Room[]);
    const availableRooms = ref([] as number[]);
    const isDialogOpen = ref(false);
    const selectedClient = ref(null as null | Client);
    const selectedRoom = ref(null as null | number);

    const rules = {
      required: (value: string) => !!value || 'Поле обязательно'
    };

    const submitClient = async () => {
      if (clientForm.value?.validate()) {
        try {
          const response = await axiosApi.post('/clients/', newClient);
          console.log('Пользователь успешно создан');
          resetForm();
        } catch (error) {
          console.error('Ошибка при создании клиента', error);
        }
      }
    };

    const resetForm = () => {
      newClient.passport_number = '';
      newClient.last_name = '';
      newClient.first_name = '';
      newClient.city = '';
      showForm.value = false;
      clientForm.value?.resetValidation();
      fetchClients();
    };

    const fetchClients = async () => {
      try {
        clients.value = [];
        const response = await axiosApi.get("/clients");
        clients.value = response.data
        cities.value = ['Все', ...Array.from(new Set(filteredClients.value.map(c => c.city)))];
        const reservationsResponse = await axiosApi.get("/reservations");
        clients.value = clients.value.map(client => {
          const clientReservations = reservationsResponse.data.filter((r: Reservation) => r.client === client.id);
          const reservation = clientReservations.length > 0 ? clientReservations.reduce((prev: Reservation, current: Reservation) => {
            return (prev.id > current.id) ? prev : current;
          }) : null;
          client.room_number = reservation && reservation.check_out_date === null ? reservation.room_number : null;
          return client;
        });
      } catch (error) {
        console.error("Ошибка при загрузке списка клиентов:", error);
        alert("Ошибка при загрузке клиентов");
      }
    };

    const fetchAvailableRooms = async () => {
      try {
        const response = await axiosApi.get("/rooms/");
        availableRooms.value = response.data.filter((room: Room) => !room.is_occupied).map((room: Room) => room.number);
      } catch (error) {
        console.error("Ошибка при загрузке списка свободных комнат:", error);
      }
    }

    const fetchRooms = async () => {
      try {
        const response = await axiosApi.get("/rooms/");
        rooms.value = response.data;
      } catch (error) {
        console.error("Ошибка при загрузке списка комнат:", error);
      }
    }

    const openDialog = (client: Client) => {
      if (client.room_number === null) {
        fetchAvailableRooms();
      }
      fetchRooms();
      selectedClient.value = client;
      isDialogOpen.value = true;
    }
    const closeDialog = () => {
      selectedClient.value = null;
      isDialogOpen.value = false;
    }
    const handleAction = async () => {
      isDialogOpen.value = true;

      try {
        if (selectedClient.value!.room_number !== null) {
          await axiosApi.post("reservations/check-out/", {
            client_id: selectedClient.value!.id,
            room_id: rooms.value.find((r: Room) => selectedClient.value!.room_number === r.number)!.id,
          });
        } else {
          if (selectedRoom === null) {
            alert("Пожалуйста, выберите комнату.");
            return;
          }
          await axiosApi.post("reservations/check-in/", {
            client_id: selectedClient.value!.id,
            room_id: rooms.value.find((r: Room) => selectedRoom.value! === r.number)!.id,
          });
        }

        await fetchClients();
        closeDialog();
      } catch (error: any) {
        console.error("Ошибка при обработке действия:", error);
        alert(error.response.data.error);
      }
    }

    onMounted(fetchClients);

    return {
      selectedCity,
      cities,
      filteredClients,
      headers,
      fetchClients,
      clientForm,
      isValid,
      newClient,
      rules,
      submitClient,
      resetForm,
      showForm,
      availableRooms,
      isDialogOpen,
      selectedClient,
      selectedRoom,
      openDialog,
      closeDialog,
      handleAction
    };
  },
});
</script>

<style scoped>
.text-center {
  text-align: center;
}
</style>
