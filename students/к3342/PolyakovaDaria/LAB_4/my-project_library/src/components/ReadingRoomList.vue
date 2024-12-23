<template>
  <v-card elevation="1">
    <v-card-title>
      📋 Список читальных залов
    </v-card-title>
    <v-data-table
      :headers="headers"
      :items="rooms"
      item-value="id"
      class="elevation-1"
      :loading="isLoading"
      no-data-text="Нет доступных читальных залов."
      :items-per-page="5"
    >
      <!-- Кастомное отображение строк таблицы -->
      <template #item.actions="{ item }">
        <v-btn
          color="red"
          icon
          @click="$emit('delete', item.id)"
        >
          <v-icon>mdi-delete</v-icon>
        </v-btn>
      </template>
    </v-data-table>
  </v-card>
</template>

<script>
export default {
  name: 'ReadingRoomList',
  props: {
    rooms: {
      type: Array,
      required: true
    },
    isLoading: {
      type: Boolean,
      default: false
    }
  },
  data() {
    return {
      headers: [
        { text: 'Номер зала', value: 'number' },
        { text: 'Название', value: 'name' },
        { text: 'Вместимость', value: 'capacity' },
        { text: 'Действия', value: 'actions', sortable: false }
      ]
    };
  }
};
</script>

<style scoped>
/* Опциональные стили */
</style>
