<template>
  <v-container>
    <!-- Заголовок страницы -->
    <v-row>
      <v-col cols="12">
        <v-card class="pa-5 mb-5" elevation="5">
          <v-card-title class="text-h5 text-center">📖 Список читателей</v-card-title>
        </v-card>
      </v-col>
    </v-row>

    <!-- Таблица читателей -->
    <v-row>
      <v-col cols="12">
        <v-data-table
          :headers="headers"
          :items="readers"
          item-value="id"
          class="elevation-1"
        >
          <!-- Кастомное отображение строк таблицы -->
          <template #item="{ item }">
            <tr>
              <!-- Ячейка: ID читателя -->
              <td>{{ item.id }}</td>

              <!-- Ячейка: ФИО читателя -->
              <td>{{ item.full_name }}</td>
              
              <!-- Ячейка: Номер билета -->
              <td>{{ item.ticket_number }}</td>

              <!-- Ячейка: Закреплённый зал -->
              <td>
                <span v-if="readingRooms.length">
                  {{
                    readingRooms.find((room) => room.id === item.assigned_room)?.name || "Не закреплён"
                  }}
                </span>
                <span v-else>Залы не загружены</span>
              </td>

              <!-- Ячейка: Действия -->
              <td>
                <v-select
                  v-if="readingRooms.length"
                  v-model="assignedRoom[item.id]"
                  :items="readingRooms"
                  item-title="name"
                  item-value="id"
                  label="Выберите зал"
                  dense
                ></v-select>
                <v-btn
                  color="primary"
                  class="mt-2"
                  @click="assignRoom(item.id, assignedRoom[item.id])"
                >
                  Закрепить
                </v-btn>
                <v-btn
                  color="red"
                  class="mt-2"
                  @click="$emit('delete', item.id)"
                >
                  Удалить
                </v-btn>
              </td>
            </tr>
          </template>
        </v-data-table>
      </v-col>
    </v-row>

    <!-- Сообщение при отсутствии данных -->
    <v-row v-if="!readers.length">
      <v-col cols="12" class="text-center">
        <v-alert type="info">Нет данных для отображения.</v-alert>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import { reactive } from "vue";

export default {
  name: 'ReaderList',
  props: {
    readers: {
      type: Array,
      required: true,
    },
    readingRooms: {
      type: Array,
      default: () => [], // Защита от undefined
    },
  },
  data() {
    return {
      headers: [
        { text: 'ID', value: 'id' },
        { text: 'ФИО', value: 'full_name' },
        { text: 'Номер билета', value: 'ticket_number' },
        { text: 'Закреплённый зал', value: 'assigned_room' },
        { text: 'Действия', value: 'actions', sortable: false }
      ],
      assignedRoom: reactive({}), // Реактивный объект для привязки выбранных залов
    };
  },
  methods: {
    assignRoom(readerId, roomId) {
      if (!roomId) {
        alert("Выберите зал для закрепления.");
        return;
      }
      this.$emit("assign-room", readerId, roomId); // Передаем событие с выбранным залом
    }
  },
  watch: {
    readers: {
      immediate: true, // Выполняется при загрузке
      handler(newReaders) {
        // Заполняем assignedRoom при изменении списка читателей
        newReaders.forEach((reader) => {
          this.assignedRoom[reader.id] = reader.assigned_room;
        });
      },
    },
  },
};
</script>

<style scoped>
.v-data-table tr td {
  vertical-align: middle;
  text-align: center;
}
</style>
