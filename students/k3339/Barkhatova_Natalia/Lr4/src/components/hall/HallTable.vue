<template>
  <div class="hall-table">
    <table>
      <thead>
      <tr>
        <th>Название зала</th>
        <th>Вместимость</th>
        <th>Действия</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="hall in halls" :key="hall.id">
        <td>{{ hall.name }}</td>
        <td>{{ hall.capacity }}</td>
        <td>
          <button
              class="edit-btn"
              @click="edit(hall)"
              :disabled="isHallRelatedToSession(hall.id)">
            Редактировать
          </button>
          <button
              class="delete-btn"
              @click="deleteHall(hall.id)"
              :disabled="isHallRelatedToSession(hall.id)">
            Удалить
          </button>
        </td>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import {useTicketStore} from '@/stores/ticket';
import {onMounted, ref} from "vue";

export default {
  props: {
    halls: Array,
  },
  setup(props, {emit}) {
    const ticketStore = useTicketStore();

    const hallSessionsMap = ref(new Map());

    const loadTickets = async () => {
      await ticketStore.fetchTickets(); // Загружаем билеты
      ticketStore.tickets.forEach(ticket => {
        hallSessionsMap.value.set(ticket.session.hall.id, true);
      });
    };

    onMounted(() => {
      loadTickets();
    });

    const isHallRelatedToSession = (hallId) => {
      return hallSessionsMap.value.has(hallId);
    };

    const edit = (hall) => {
      emit('edit', hall);
    };

    const deleteHall = (hallId) => {
      emit('delete', hallId);
    };

    return {
      isHallRelatedToSession,
      edit,
      deleteHall,
    };
  },
};
</script>

<style>
/* Основной контейнер для таблицы */
.hall-table {
  width: 100%;
  margin: 20px 0;
  overflow-x: auto;
}

/* Таблица */
table {
  width: 100%;
  border-collapse: collapse;
  background-color: #FFF8DC;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
}

thead th {
  background-color: #800020;
  color: #fff;
  font-family: 'Pacifico', cursive;
  font-size: 20px;
  padding: 12px;
  text-align: left;
}

tbody td {
  padding: 12px;
  font-family: 'Great Vibes', cursive;
  border-top: 1px solid #CCC;
  color: #333;
}

tbody tr:nth-child(even) {
  background-color: #FFE880;
}

/* Кнопки */
button {
  background-color: #FFAA33;
  color: #fff;
  padding: 8px 16px;
  border: none;
  border-radius: 5px;
  font-size: 16px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.3s;
  margin-right: 5px;
}

button.edit-btn:hover:not(:disabled) {
  background-color: #006400; /* Dark green for hover effect */
}

button.delete-btn:hover:not(:disabled) {
  background-color: #A40000; /* Dark red for hover effect */
}

button:disabled {
  background-color: #CCC;
  cursor: not-allowed;
}
</style>