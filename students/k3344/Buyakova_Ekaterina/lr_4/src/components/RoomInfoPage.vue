<template>
  <v-container>
    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card>
          <v-card-title>Информация о комнате</v-card-title>
          <v-card-text>
            <p><strong>Номер комнаты: </strong> {{ room?.number }}</p>
            <p><strong>Этаж: </strong> {{ room?.floor }}</p>
            <p>
              <strong>Статус: </strong>
              <span :class="room?.is_occupied ? 'text-danger' : 'text-success'">
                {{ room?.is_occupied ? 'Занята' : 'Доступна' }}
              </span>
            </p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row justify="center">
      <v-col cols="12" md="8">
        <v-card>
          <v-card-title>Клиенты, проживавшие за определённый период</v-card-title>
          <v-card-text>
            <v-form v-model="isClientsFormValid">
              <v-row>
                <v-col>
                  <v-text-field
                    v-model="clientsForm.startDate"
                    label="Начальная дата (YYYY-MM-DD)"
                    required
                  ></v-text-field>
                </v-col>
                <v-col>
                  <v-text-field
                    v-model="clientsForm.endDate"
                    label="Конечная дата (YYYY-MM-DD)"
                    required
                  ></v-text-field>
                </v-col>
              </v-row>
              <v-btn variant=text :disabled="!isClientsFormValid" @click="fetchClients">
                Получить клиентов
              </v-btn>
            </v-form>
            <v-list v-if="clients.length">
              Клиенты
              <v-list-item v-for="client in clients" :key="client.id">
                {{ client.first_name }} {{ client.last_name }} ({{ client.city }})
              </v-list-item>
            </v-list>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import type Client from '@/models/client';
import type Room from '@/models/room';
import type Staff from '@/models/staff';
import axiosApi from '@/plugins/axios';
import { defineComponent, ref, onMounted } from 'vue';

export default defineComponent({
  name: 'RoomInfoPage',
  props: {
    roomId: {
      type: Number,
      required: true,
    },
  },
  setup(props) {
    const room = ref(null as Room | null);
    const clients = ref([] as Client[]);
    const cleaningStaff = ref([] as Staff[]);
    const isClientsFormValid = ref(false);
    const isCleaningFormValid = ref(false);

    const clientsForm = ref({
      startDate: '',
      endDate: '',
    });

    const cleaningForm = ref({
      clientId: '',
      weekday: '',
    });

    const fetchRoomInfo = async () => {
      try {
        const response = await axiosApi.get(`/rooms/${props.roomId}/`);
        room.value = response.data;
      } catch (error) {
        console.error(error);
      }
    };

    const fetchClients = async () => {
      try {
        const { startDate, endDate } = clientsForm.value;
        const response = await axiosApi.get(`/rooms/${props.roomId}/clients-by-period/${startDate}/${endDate}/`
        );
        clients.value = response.data;
      } catch (error) {
        console.error(error);
      }
    };

    onMounted(fetchRoomInfo);

    return {
      room,
      clients,
      cleaningStaff,
      clientsForm,
      cleaningForm,
      isClientsFormValid,
      isCleaningFormValid,
      fetchClients,
    };
  },
});
</script>

<style scoped>
.text-danger {
  color: red;
}
.text-success {
  color: green;
}
</style>
