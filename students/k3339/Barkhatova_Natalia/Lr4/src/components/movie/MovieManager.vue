<template>
  <div class="movie-manager">
    <h2>Управление фильмами</h2>

    <button class="add-movie-btn" @click="showAddMovieModal">Добавить новый фильм</button>

    <MovieTable
        :movies="movies"
        @edit="editMovie"
        @delete="deleteMovie"
    />

    <Modal v-if="showModal" @close="closeModal">
      <h3 class="modal-title">{{ isEditing ? 'Редактировать фильм' : 'Добавить фильм' }} Фильм</h3>
      <form @submit.prevent="saveMovie" class="movie-form">
        <div class="form-group">
          <label for="name">Название</label>
          <input v-model="movieForm.name" type="text" id="name" required class="form-input"/>
          <p v-if="errors.name" class="error">{{ errors.name }}</p>
        </div>
        <div class="form-group">
          <label for="description">Описание</label>
          <textarea v-model="movieForm.description" id="description" required class="form-textarea"></textarea>
          <p v-if="errors.description" class="error">{{ errors.description }}</p>
        </div>
        <div class="form-group">
          <label for="duration">Продолжительность (в минутах)</label>
          <input v-model="movieForm.duration" type="number" id="duration" required min="1" class="form-input"/>
          <p v-if="errors.duration" class="error">{{ errors.duration }}</p>
        </div>
        <button type="submit" class="submit-btn">{{ isEditing ? 'Сохранить Изменения' : 'Добавить Фильм' }}</button>
      </form>
    </Modal>
  </div>
</template>
<script>
import {computed, onMounted, ref} from 'vue';
import {useMovieStore} from '@/stores/movie.js';
import MovieTable from './MovieTable.vue';
import Modal from '../Modal.vue';

export default {
  components: {
    MovieTable,
    Modal,
  },
  setup() {
    const movieStore = useMovieStore();
    const movies = computed(() => movieStore.movies);
    const showModal = ref(false);
    const isEditing = ref(false);
    const errors = ref({});
    const movieForm = ref({
      title: '',
      description: '',
      releaseDate: '',
    });

    const showAddMovieModal = () => {
      isEditing.value = false;
      movieForm.value = {title: '', description: '', releaseDate: ''};
      showModal.value = true;
    };

    const editMovie = (movie) => {
      isEditing.value = true;
      movieForm.value = {...movie};
      showModal.value = true;
    };

    const saveMovie = async () => {
      try {
        if (isEditing.value) {
          await movieStore.updateMovie(movieForm.value);
        } else {
          await movieStore.addMovie(movieForm.value);
        }
        showModal.value = false;
        movieForm.value = {title: '', description: '', releaseDate: ''};
        errors.value = {};
      } catch (error) {
        if (error.response && error.response.data) {
          const serverErrors = error.response.data;
          for (const key in serverErrors) {
            if (Object.prototype.hasOwnProperty.call(serverErrors, key)) {
              errors.value[key] = serverErrors[key];
            }
          }
        } else {
          console.error("Ошибка при сохранении:", error);
        }
      }
    };


    const deleteMovie = async (movieId) => {
      await movieStore.deleteMovie(movieId);
    };

    const closeModal = () => {
      showModal.value = false;
    };

    onMounted(async () => {
      console.log('Fetching movies on page load...');
      await movieStore.fetchMovies();
      console.log(movieStore.movies);
    });

    return {
      movies,
      errors,
      showModal,
      isEditing,
      movieForm,
      showAddMovieModal,
      editMovie,
      saveMovie,
      deleteMovie,
      closeModal
    };
  },
};
</script>

<style>
.movie-manager {
  padding: 20px;
  background-color: #F5F5DC;
  font-family: 'Pacifico', cursive;
  color: #800020;
  min-height: 100vh;
}

.movie-manager h2 {
  font-size: 32px;
  text-align: center;
  margin-bottom: 20px;
}

.add-movie-btn {
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

.add-movie-btn:hover {
  background-color: #800020;
  transform: scale(1.05);
}

.movie-form .form-group {
  margin-bottom: 15px;
}

.movie-form label {
  display: block;
  font-size: 18px;
  margin-bottom: 5px;
}

.movie-form .form-input,
.movie-form .form-textarea {
  width: 100%;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #CCC;
  font-family: 'Great Vibes', cursive;
  font-size: 16px;
  box-sizing: border-box;
  transition: border 0.3s, box-shadow 0.3s;
}

.movie-form .form-textarea {
  min-height: 80px;
  resize: vertical;
}

.form-input:focus,
.form-textarea:focus {
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
}

.submit-btn:hover {
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