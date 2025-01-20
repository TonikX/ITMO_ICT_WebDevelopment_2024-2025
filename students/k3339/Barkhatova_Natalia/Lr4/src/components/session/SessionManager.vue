<template>
  <div class="session-manager">
    <h2>Управление сеансами</h2>

    <button class="add-session-btn" @click="showAddSessionModal">Добавить новый сеанс</button>

    <SessionTable
        :sessions="sessions"
        @edit="editSession"
        @delete="deleteSession"
    />

    <Modal v-if="showModal" @close="closeModal">
      <h3 class="modal-title">{{ isEditing ? 'Редактировать сеанс' : 'Добавить сеанс' }} Сеанс</h3>
      <form @submit.prevent="saveSession" class="session-form">
        <div class="form-group">
          <label for="movie">Фильм</label>
          <select v-model="sessionForm.movieId" id="movie" required class="form-select">
            <option v-for="movie in movies" :key="movie.id" :value="movie.id">{{ movie.name }}</option>
          </select>
          <p v-if="errors.movieId" class="error">{{ errors.movieId }}</p>
        </div>
        <div class="form-group">
          <label for="hall">Зал</label>
          <select v-model="sessionForm.hallId" id="hall" required class="form-select">
            <option v-for="hall in halls" :key="hall.id" :value="hall.id">{{ hall.name }}</option>
          </select>
          <p v-if="errors.hallId" class="error">{{ errors.hallId }}</p>
        </div>
        <div class="form-group">
          <label for="start-time">Время начала</label>
          <input v-model="sessionForm.startTime" type="datetime-local" id="start-time" required class="form-input" />
          <p v-if="errors.startTime" class="error">{{ errors.startTime }}</p>
        </div>
        <div class="form-group">
          <label for="price">Цена</label>
          <input v-model="sessionForm.price" type="number" id="price" required min="1" class="form-input" />
          <p v-if="errors.price" class="error">{{ errors.price }}</p>
        </div>
        <button type="submit" class="submit-btn">{{ isEditing ? 'Сохранить Изменения' : 'Добавить Сеанс' }}</button>
      </form>
    </Modal>
  </div>
</template>

<script>
import { computed, onMounted, ref } from 'vue';
import { useSessionStore } from '@/stores/session.js';
import { useMovieStore } from '@/stores/movie.js';
import SessionTable from './SessionTable.vue';
import Modal from '../Modal.vue';
import {useHallStore} from "@/stores/hall.js";

export default {
  components: { SessionTable, Modal },
  setup() {
    const sessionStore = useSessionStore();
    const movieStore = useMovieStore();
    const hallStore = useHallStore();
    const sessions = computed(() => sessionStore.sessions);
    const movies = computed(() => movieStore.movies);
    const halls = computed(() => hallStore.halls);

    const showModal = ref(false);
    const isEditing = ref(false);
    const errors = ref({});
    const sessionForm = ref({
      movieId: '',
      hallId: '',
      startTime: '',
      price: '',
    });

    const showAddSessionModal = () => {
      isEditing.value = false;
      sessionForm.value = { movieId: '', hallId: '', startTime: '', price: '' };
      showModal.value = true;
    };

    const editSession = (session) => {
      isEditing.value = true;
      sessionForm.value = {
        movieId: session.movie.id,
        hallId: session.hall.id,
        startTime: session.startTime.slice(0, 16),
        price: session.price,
      };
      showModal.value = true;
    };

    const saveSession = async () => {
      try {
        if (isEditing.value) {
          await sessionStore.updateSession(sessionForm.value);
        } else {
          await sessionStore.addSession(sessionForm.value);
        }
        showModal.value = false;
        sessionForm.value = { movieId: '', hallId: '', startTime: '', price: '' };
        errors.value = {};
      } catch (error) {
        errors.value = error.response?.data || {};
      }
    };

    const deleteSession = async (sessionId) => {
      await sessionStore.deleteSession(sessionId);
    };

    const closeModal = () => {
      showModal.value = false;
    };

    onMounted(async () => {
      await movieStore.fetchMovies();
      await hallStore.fetchHalls();
      await sessionStore.fetchSessions();
    });

    return {
      sessions,
      movies,
      halls,
      showModal,
      isEditing,
      sessionForm,
      errors,
      showAddSessionModal,
      editSession,
      saveSession,
      deleteSession,
      closeModal
    };
  },
};
</script>

<style>
.session-manager {
  padding: 20px;
  background-color: #F5F5DC;
  font-family: 'Pacifico', cursive;
  color: #800020;
}

.session-manager h2 {
  font-size: 32px;
  text-align: center;
  margin-bottom: 20px;
}

.add-session-btn {
  display: block;
  margin: 0 auto 20px;
  background-color: #FFAA33;
  color: #fff;
  padding: 12px 25px;
  border: none;
  border-radius: 25px;
  font-size: 18px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.3s;
}

.add-session-btn:hover {
  background-color: #800020;
  transform: scale(1.05);
}

.session-form .form-group {
  margin-bottom: 15px;
}

.session-form label {
  display: block;
  font-size: 18px;
  margin-bottom: 5px;
}

.session-form .form-input,
.session-form .form-select {
  width: 100%;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #CCC;
  font-family: 'Great Vibes', cursive;
  font-size: 16px;
  transition: border 0.3s, box-shadow 0.3s;
}

.session-form .form-input:focus,
.session-form .form-select:focus {
  border-color: #800020;
  box-shadow: 0 0 8px rgba(128, 0, 32, 0.5);
  outline: none;
}

.error {
  color: #D32F2F;
  font-size: 14px;
  margin-top: -10px;
  margin-bottom: 10px;
  font-family: 'Great Vibes', cursive;
}

.submit-btn {
  display: block;
  background-color: #32CD32;
  color: #fff;
  padding: 10px 25px;
  border: none;
  border-radius: 25px;
  font-size: 18px;
  cursor: pointer;
  transition: background-color 0.3s, transform 0.3s;
  width: 100%;
}.submit-btn:hover {
   background-color: #228B22;
   transform: scale(1.05);
 }

.modal-title {
  font-size: 24px;
  color: #800020;
  text-align: center;
  margin-bottom: 20px;
}
</style>