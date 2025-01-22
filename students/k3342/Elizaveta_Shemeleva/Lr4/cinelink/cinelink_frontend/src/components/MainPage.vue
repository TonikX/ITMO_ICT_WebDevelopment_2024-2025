<template>
  <div>
    <AppHeader/>

    <!-- Основной контейнер для фильмов и фильтров -->
    <div aria-label="Movie selection and filters" class="content-container" role="main">
      <!-- Кнопка для открытия модального окна фильтров -->
      <button
          id="filterButton"
          aria-label="Open filters"
          class="filters-button"
          @click.prevent="toggleFilterModal"
      >
        filters
        <svg class="filter-icon">
          <use href="/icons/icons.svg#icon-filters"></use>
        </svg>
      </button>

      <!-- Сетка фильмов -->
      <div aria-label="Movie grid" class="movie-grid" role="list">
        <router-link
            v-for="film in films"
            :key="film.id"
            :title="film.title"
            :to="{ name: 'MovieDetails', params: { id: film.id } }"
            class="movie-card"
        >
          <div
              :style="{ backgroundImage: `url(${film.poster_url || 'images/default-poster.png'})` }"
              class="movie-poster"
          ></div>
          <div class="movie-info">
            <h3 class="movie-title">{{ film.title }}</h3>
            <p class="movie-details">{{ film.genres }} | {{ film.year }}</p>
          </div>
        </router-link>
      </div>
    </div>

    <!-- Модальное окно для фильтров -->
    <div
        v-show="isFilterModalVisible"
        id="filterModal"
        :aria-hidden="!isFilterModalVisible"
        aria-labelledby="filterModalTitle"
        role="dialog"
    >
      <div class="modal-content">
        <!-- Кнопка для закрытия модального окна -->
        <button
            id="closeModalButton"
            aria-label="Close filters"
            class="close-modal-button"
            @click="toggleFilterModal"
        >
          ×
        </button>
        <!-- Секция фильтров -->
        <div class="filter-section">
          <h3 id="filterModalTitle" class="filter-group-title">Filters</h3>
          <!-- Фильтры по жанрам -->
          <h4 class="filter-group-title">Genres</h4>
          <div aria-label="Genre filters" class="filter-buttons" role="group">
            <button
                v-for="genre in genres"
                :key="genre"
                :class="{ active: selectedGenres.includes(genre) }"
                class="filter-button"
                @click="toggleGenre(genre)"
            >
              {{ genre }}
            </button>
          </div>
        </div>
        <!-- Фильтры по десятилетиям -->
        <div class="filter-section">
          <h4 class="filter-group-title">Decades</h4>
          <div aria-label="Decade filters" class="filter-buttons" role="group">
            <button
                v-for="decade in decades"
                :key="decade"
                :class="{ active: selectedDecades.includes(decade) }"
                class="filter-button"
                @click="toggleDecade(decade)"
            >
              {{ decade }}
            </button>
          </div>
        </div>
        <!-- Фильтры по рейтингу -->
        <div class="filter-section">
          <h4 class="filter-group-title">Ratings</h4>
          <div aria-label="Rating filters" class="filter-buttons" role="group">
            <button
                v-for="rating in ratings"
                :key="rating"
                :class="{ active: selectedRatings.includes(rating) }"
                class="filter-button"
                @click="toggleRating(rating)"
            >
              {{ rating }}
            </button>
          </div>
        </div>
        <!-- Действия с фильтрами -->
        <div class="filter-actions">
          <button
              id="resetFiltersButton"
              aria-label="Reset filters"
              class="action-button"
              @click="resetFilters"
          >
            Reset Filters
          </button>
          <button
              id="applyFiltersButton"
              aria-label="Apply filters"
              class="action-button"
              @click="applyFilters"
          >
            Apply Filters
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {useFilmsStore} from "@/stores/films";
import {computed, onMounted, ref} from "vue";
import AppHeader from "@/components/AppHeader.vue";

export default {
  name: "MainPage",
  components: {AppHeader},
  setup() {
    const filmsStore = useFilmsStore(); // Магазин фильмов

    // Переменные для состояния модального окна и выбранных фильтров
    const isFilterModalVisible = ref(false);
    const selectedGenres = ref([]);
    const selectedDecades = ref([]);
    const selectedRatings = ref([]);

    // Данные фильмов и фильтров
    const films = computed(() => filmsStore.films);
    const genres = computed(() => filmsStore.genres);
    const decades = computed(() => filmsStore.decades);
    const ratings = computed(() => filmsStore.ratings);

    // Функция переключения видимости модального окна
    const toggleFilterModal = () => {
      isFilterModalVisible.value = !isFilterModalVisible.value;
    };

    // Функции для работы с выбранными фильтрами
    const toggleGenre = (genre) => {
      const index = selectedGenres.value.indexOf(genre);
      index === -1 ? selectedGenres.value.push(genre) : selectedGenres.value.splice(index, 1);
    };

    const toggleDecade = (decade) => {
      const index = selectedDecades.value.indexOf(decade);
      index === -1 ? selectedDecades.value.push(decade) : selectedDecades.value.splice(index, 1);
    };

    const toggleRating = (rating) => {
      const index = selectedRatings.value.indexOf(rating);
      index === -1 ? selectedRatings.value.push(rating) : selectedRatings.value.splice(index, 1);
    };

    // Применение фильтров
    const applyFilters = async () => {
      const filters = {
        genres: selectedGenres.value.join(","),
        decades: selectedDecades.value.join(","),
        ratings: selectedRatings.value.join(","),
      };
      await filmsStore.fetchFilms(filters);
    };

    // Сброс фильтров
    const resetFilters = async () => {
      selectedGenres.value = [];
      selectedDecades.value = [];
      selectedRatings.value = [];
      await filmsStore.fetchFilms();
    };

    // Загрузка фильмов и доступных фильтров при монтировании
    onMounted(() => {
      filmsStore.fetchFilms();
      filmsStore.fetchFilters();
    });

    return {
      films,
      genres,
      decades,
      ratings,
      isFilterModalVisible,
      selectedGenres,
      selectedDecades,
      selectedRatings,
      toggleFilterModal,
      toggleGenre,
      toggleDecade,
      toggleRating,
      applyFilters,
      resetFilters,
    };
  },
};
</script>

<style scoped>
.content-container {
  padding: 100px 150px 30px;
}

.filters-button {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 270px;
  height: 47px;
  background-color: var(--primary-color);
  border: 2px solid var(--text-color);
  border-radius: 10px;
  color: var(--text-color);
  font-size: 28px;
  text-decoration: none;
  padding: 0 12px;
}

.filter-icon {
  margin-left: auto;
  width: 26px;
  height: 26px;
  fill: currentColor;
  display: inline-block;
}

.movie-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(150px, 1fr));
  gap: 20px;
  margin-top: 20px;
}

.movie-item {
  width: 125px;
  height: 190px;
  background-size: cover;
  background-position: center;
  border-radius: 10px;
  cursor: pointer;
  overflow: hidden;
  transition: transform 0.3s;
}

.movie-item:hover {
  transform: scale(1.05);
}

.movie-card {
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.movie-card:hover {
  transform: scale(1.05);
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
}

.movie-poster {
  width: 100%;
  padding-top: 150%;
  background-size: cover;
  background-position: center;
  border-radius: 10px;
}

.movie-info {
  margin-top: 10px;
  text-align: center;
}

.movie-title {
  font-size: 16px;
  font-weight: bold;
  color: white;
  text-decoration: none;
}

.movie-title a {
  text-decoration: none;
  color: inherit;
}

.movie-title a:hover {
  text-decoration: none;
}

.movie-details {
  font-size: 14px;
  color: gray;
  text-decoration: none;
}

/* Filter Modal Styles */
#filterModal {
  position: fixed;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  z-index: 1000;
  background-color: var(--secondary-color); /* Use a lighter gray for modal background */
  color: var(--text-color);
  box-shadow: 0 4px 10px var(--shadow-color);
  padding: 20px;
  border-radius: 10px;
  width: 60%;
  max-width: 800px;
}

/* Button Styles */
.filters-button {
  display: flex;
  align-items: center;
  justify-content: space-between;
  width: 270px;
  height: 47px;
  background-color: var(--primary-color);
  border: 2px solid var(--text-color);
  border-radius: 10px;
  color: var(--text-color);
  font-size: 28px;
  text-decoration: none;
  padding: 0 12px;
  cursor: pointer;
  transition: background-color 0.3s, color 0.3s, transform 0.3s;
}

.filters-button:hover {
  background-color: var(--text-color);
  color: var(--background-color);
  transform: scale(1.05);
}

.action-button {
  margin-top: 20px;
  padding: 10px 20px;
  background-color: var(--primary-color);
  border: 2px solid var(--text-color);
  border-radius: 10px;
  color: var(--text-color);
  font-size: 18px;
  cursor: pointer;
  transition: background-color 0.3s, color 0.3s, transform 0.3s;
}

.action-button:hover {
  background-color: var(--text-color);
  color: var(--background-color);
  transform: scale(1.05);
}

.close-modal-button {
  position: absolute;
  top: 10px;
  right: 10px;
  font-size: 24px;
  background-color: var(--primary-color);
  color: var(--text-color);
  border: 2px solid var(--text-color);
  border-radius: 10px;
  cursor: pointer;
  padding: 5px 10px;
  transition: background-color 0.3s, color 0.3s, transform 0.3s;
}

.close-modal-button:hover {
  background-color: var(--text-color);
  color: var(--background-color);
  transform: scale(1.05);
}

.filter-section {
  margin-bottom: 20px;
}

.filter-buttons {
  display: flex;
  flex-wrap: wrap;
  gap: 10px;
}

.filter-button {
  padding: 10px 15px;
  border: 1px solid #ccc;
  border-radius: 5px;
  cursor: pointer;
  background-color: var(--primary-color);
  color: var(--text-color);
}

.filter-button.active {
  background-color: var(--text-color);
  color: var(--background-color);
  transform: scale(1.05);
}

.filter-actions {
  display: flex;
  justify-content: space-between;
  margin-top: 20px;
}


</style>