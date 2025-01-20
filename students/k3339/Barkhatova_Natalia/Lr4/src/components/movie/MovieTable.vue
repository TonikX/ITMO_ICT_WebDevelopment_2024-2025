<template>
  <div class="movie-table">
    <table>
      <thead>
      <tr>
        <th>Название</th>
        <th>Продолжительность (мин)</th>
        <th>Описание</th>
        <th>Действия</th>
      </tr>
      </thead>
      <tbody>
      <tr v-for="movie in movies" :key="movie.id">
        <td>{{ movie.name }}</td>
        <td>{{ movie.duration }}</td>
        <td>{{ movie.description }}</td>
        <td>
          <button class="edit-btn" @click="edit(movie)" :disabled="isMovieRelatedToSessions(movie.id)">Редактировать</button>
          <button class="delete-btn" @click="deleteMovie(movie.id)" :disabled="isMovieRelatedToSessions(movie.id)">
            Удалить
          </button>
        </td>
      </tr>
      </tbody>
    </table>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useSessionStore } from '@/stores/session';

export default {
  props: {
    movies: Array,
  },
  setup(props, { emit }) {
    const sessionStore = useSessionStore();
    const movieSessionsMap = ref(new Map());

    const loadSessions = async () => {
      await sessionStore.fetchSessions(); // Загружаем сеансы
      sessionStore.sessions.forEach(session => {
        movieSessionsMap.value.set(session.movie.id, true);
      });
    };

    onMounted(() => {
      loadSessions();
    });

    const isMovieRelatedToSessions = (movieId) => {
      return movieSessionsMap.value.has(movieId);
    };

    const edit = (movie) => {
      if (isMovieRelatedToSessions(movie.id)) {
        alert('You cannot edit this movie because it has associated sessions.');
        return;
      }
      emit('edit', movie);
    };


    const deleteMovie = (movieId) => {
      if (isMovieRelatedToSessions(movieId)) {
        alert('You cannot delete this movie because it has associated sessions.');
        return;
      }
      emit('delete', movieId);
    };

    return {
      isMovieRelatedToSessions,
      edit,
      deleteMovie,
    };
  },
};
</script>

<style>
.movie-table {
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