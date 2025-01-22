<template>
  <div class="movie-details">
    <AppHeader/>

    <div v-if="film" class="movie-content">
      <div class="top-sections">
        <div
            :style="{ backgroundImage: `url(${film.poster_url || 'images/default-poster.png'})` }"
            class="poster-section"
        ></div>

        <div class="info-section">
          <h1 class="movie-title">{{ film.title }}</h1>
          <h2 class="movie-director">Director: {{ film.director || "N/A" }}</h2>
          <p class="movie-release-duration">
            Year: {{ film.year }} | Duration: {{ film.runtime || "N/A" }}
          </p>
          <p class="movie-genres">Genres: {{ film.genres }}</p>
          <p class="movie-plot">{{ film.plot || "No description available." }}</p>
          <div class="imdb-rating">IMDb</div>
          <div class="movie-rating">{{ film.rating || "N/A" }}</div>
        </div>

        <div class="action-section">
          <!-- Rating Section -->
          <div class="rate-section">
            <h3 class="rate-title">Rate this movie</h3>
            <div class="rating-options">
              <div class="rating-row">
                <button
                    v-for="rate in [1, 2, 3, 4, 5]"
                    :key="rate"
                    :class="{ 'rated': currentRating === rate }"
                    class="rate-button"
                    @click="rateMovie(rate)"
                >
                  {{ rate }}
                </button>
              </div>
              <div class="rating-row">
                <button
                    v-for="rate in [6, 7, 8, 9, 10]"
                    :key="rate"
                    :class="{ 'rated': currentRating === rate }"
                    class="rate-button"
                    @click="rateMovie(rate)"
                >
                  {{ rate }}
                </button>
              </div>
            </div>
          </div>

          <!-- List and Share Section -->
          <div class="action-buttons">
            <select v-model="selectedListId" class="action-button">
              <option disabled value="">select a list</option>
              <option v-for="list in userLists" :key="list.id" :value="list.id">{{ list.name }}</option>
            </select>
            <button class="action-button" @click="addToList">Add to list</button>
            <button class="action-button" @click="shareMovie">Share</button>
          </div>
        </div>
      </div>

      <div class="cast-crew-section">
        <h3 class="section-title">Cast & Crew</h3>
        <p class="cast-list">Actors: {{ film.actors || "N/A" }}</p>
      </div>
    </div>

    <p v-else>Loading movie details...</p>
  </div>
</template>

<script>
import {useFilmStore} from "@/stores/film";
import {useRoute} from "vue-router";
import {computed, onMounted, ref} from "vue";
import AppHeader from "@/components/AppHeader.vue";
import axios from "axios";

export default {
  name: "MovieDetails",
  components: {AppHeader},
  setup() {
    const filmStore = useFilmStore();
    const route = useRoute();
    const selectedListId = ref("");
    const userLists = ref([]);
    const film = computed(() => filmStore.film);
    const currentRating = ref(null);

    // Fetch movie details
    const fetchFilm = async () => {
      const filmId = route.params.id;
      if (!filmId) {
        console.error("No film ID provided.");
        return;
      }

      try {
        await filmStore.fetchFilmDetails(filmId);
        fetchCurrentRating(filmId); // Fetch the current rating for the movie
      } catch (error) {
        console.error("Error fetching film details:", error.message || error);
      }
    };

    // Fetch user lists for "Add to List" functionality
    const fetchUserLists = async () => {
      try {
        const response = await axios.get("/lists/");
        userLists.value = response.data;
      } catch (error) {
        console.error("Error fetching user lists:", error.message || error);
      }
    };

    // Fetch current rating
    const fetchCurrentRating = async (movieId) => {
      try {
        const response = await axios.get(`/movies/${movieId}/rating/`); // Endpoint to fetch current rating
        currentRating.value = response.data.rating; // Assign the current rating
      } catch (error) {
        console.error("Error fetching current rating:", error.message || error);
        currentRating.value = null; // Reset rating on error
      }
    };

    // Add movie to a selected list
    const addToList = async () => {
      if (!selectedListId.value) {
        alert("Please select a list.");
        return;
      }

      try {
        await axios.post(`/lists/${selectedListId.value}/movies/`, {
          movie_id: film.value.id,
        });
        alert("Movie added to the list successfully!");
      } catch (error) {
        console.error("Error adding movie to list:", error.message || error);
        alert("Failed to add movie to the list. Please try again.");
      }
    };

    // Send the rating to the backend
    const rateMovie = async (rate) => {
      try {
        await axios.post("/rate-movie/", {
          movie: film.value.id, // Pass the movie ID
          rating: rate, // Pass the rating value
        });

        currentRating.value = rate; // Update the current rating
        alert(`You rated this movie ${rate} stars!`);
      } catch (error) {
        console.error("Error saving rating:", error.message || error);
        alert("Failed to save your rating. Please try again.");
      }
    };

    // Share movie link
    const shareMovie = () => {
      navigator.clipboard
          .writeText(window.location.href)
          .then(() => alert("Movie link copied to clipboard!"))
          .catch(() => alert("Failed to copy movie link."));
    };

    // Fetch data on component mount
    onMounted(() => {
      fetchFilm();
      fetchUserLists();
    });

    return {
      film,
      selectedListId,
      userLists,
      currentRating,
      rateMovie,
      addToList,
      shareMovie,
    };
  },
};
</script>

<style scoped>
/* Style updates for new content */

.movie-content {
  margin-top: 100px;
  padding: 0 150px;
  display: flex;
  flex-direction: column;
  gap: 34px;
  margin-bottom: 110px;
}

.top-sections {
  display: flex;
  justify-content: space-between;
  gap: 27px;
}

.poster-section {
  width: 248px;
  height: 372px;
  margin-top: 8px;
  border-radius: 20px;
  background-color: var(--primary-color);
  background-size: cover;
  background-position: center;
}

.info-section {
  width: 618px;
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.movie-title {
  font-size: 53px;
  font-family: 'Limelight', sans-serif;
  color: var(--text-color);
}

.movie-director,
.movie-release-duration,
.movie-genres,
.movie-plot {
  font-size: 18px;
  font-family: 'Tenor Sans', sans-serif;
  color: var(--text-color);
}

.action-section {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.rate-section .rate-button {
  padding: 10px 15px;
  border-radius: 5px;
  cursor: pointer;
  background-color: var(--blue-color);
  color: var(--background-color);
}

.rate-button:hover {
  background-color: var(--green-color);
}

.rate-button.rated {
  background-color: var(--green-color);
  font-weight: bold;
}

.action-buttons .action-button {
  margin-top: 10px;
  padding: 10px 20px;
  border-radius: 10px;
  background-color: var(--primary-color);
  border: 2px solid var(--text-color);
  color: var(--text-color);
  cursor: pointer;
  transition: background-color 0.3s, color 0.3s;
}

.action-button:hover {
  background-color: var(--text-color);
  color: var(--background-color);
}
</style>