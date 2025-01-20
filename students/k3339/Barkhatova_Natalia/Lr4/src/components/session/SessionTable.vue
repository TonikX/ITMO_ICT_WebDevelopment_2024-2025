<template>
  <div class="session-table">
    <table>
      <thead>
      <tr>
        <th>Фильм</th>
        <th>Зал</th>
        <th>Время начала</th>
        <th>Цена</th>
        <th>Действия</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="session in sessions" :key="session.id">
        <td>{{ session.movie.name }}</td>
        <td>{{ session.hall.name }}</td>
        <td>{{ formatStartTime(session.startTime) }}</td>
        <td>{{ session.price }}₽</td>
        <td>
          <button class="edit-btn" @click="edit(session)">Редактировать</button>
          <button class="delete-btn" @click="deleteSession(session.id)">Удалить</button>
        </td>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
export default {
  props: {
    sessions: Array,
  },
  setup({emit}) {
    const formatStartTime = (startTime) => {
      const date = new Date(startTime);
      const options = {
        month: 'short',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit',
        hour12: false,
      };
      return date.toLocaleString('ru', options);
    };

    const edit = (session) => {
      emit('edit', session);
    };

    const deleteSession = (sessionId) => {
      emit('delete', sessionId);
    };

    return {
      formatStartTime,
      edit,
      deleteSession,
    };
  },
};
</script>


<style>
.session-table {
  width: 100%;
  margin: 20px 0;
  overflow-x: auto;
}

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
  background-color: #006400;
}

button.delete-btn:hover:not(:disabled) {
  background-color: #A40000;
}

button:disabled {
  background-color: #CCC;
  cursor: not-allowed;
}
</style>
