<template>
  <div>
    <AppHeader/>

    <main aria-labelledby="listTitle" class="content-container" role="main">
      <div class="list-header">
        <h1 id="listTitle" class="list-title">{{ listName }}</h1>
        <button
            aria-label="Back to profile"
            class="back-button"
            @click="goToProfile"
        >
          back to profile
        </button>
      </div>

      <div aria-label="Movies in this list" class="movie-grid" role="list">
        <div
            v-for="movie in movies"
            :key="movie.id"
            class="movie-item-container"
            role="listitem"
            @click="goToMovie(movie.id)"
        >
          <div
              :style="{ backgroundImage: `url(${movie.poster_url || 'images/default-poster.png'})` }"
              class="movie-poster"
          >
            <div class="film-details">
              <h3 class="film-title">{{ movie.title }}</h3>
              <p class="film-year">{{ movie.year }}</p>
            </div>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>

<script>
import axios from "axios";
import AppHeader from "@/components/AppHeader.vue";

export default {
  name: "ListPage",
  components: {AppHeader},
  data() {
    return {
      listName: "Loading...",
      movies: [], // Movies data to render
    };
  },
  methods: {
    async loadList() {
      const listId = this.$route.query.listId; // Get listId from URL query

      if (!listId) {
        alert("List not found. Redirecting to profile.");
        this.$router.push("/profile");
        return;
      }

      try {
        // Fetch the list details, including movies
        const response = await axios.get(`/lists/${listId}/`); // Adjust the endpoint to match your backend
        const list = response.data;

        // Safeguard against missing fields
        this.listName = list.name || "Untitled List";
        const listMovies = list.list_movies || []; // Fallback to an empty array if `list_movies` is undefined

        // Map the movies in the list to a proper structure for rendering
        this.movies = listMovies.map((entry) => ({
          id: entry.movie_details?.id || "Unknown ID", // Fallback values
          title: entry.movie_details?.title || "Untitled Movie",
          poster_url: entry.movie_details?.poster_url || "images/default-poster.png",
          year: entry.movie_details?.year || "Unknown Year",
          genres: entry.movie_details?.genres || "Unknown Genres",
        }));

        console.log("List loaded:", this.listName, this.movies);
      } catch (error) {
        console.error("Error loading list:", error);
        alert("Failed to load list. Please try again later.");
      }
    },
    goToProfile() {
      this.$router.push("/profile");
    },
    goToMovie(movieId) {
      this.$router.push({name: "MovieDetails", params: {id: movieId}});
    },
  },
  mounted() {
    // Trigger the loading of list details when the component is mounted
    this.loadList();
  },
};
</script>

<style scoped>
.content-container {
  padding: 100px 150px 30px;
}

.movie-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(213px, 1fr));
  gap: 20px;
  max-width: 1200px;
  margin: 20px auto 0;
}

.movie-item-container {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.movie-poster {
  width: 213px;
  height: 318px;
  background-size: cover;
  background-position: center;
  background-color: var(--primary-color);
  border-radius: 10px;
  position: relative;
  overflow: hidden;
  cursor: pointer;
}

.movie-poster:hover .film-details {
  opacity: 1;
}

.film-details {
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  padding: 10px;
  background: rgba(0, 0, 0, 0.5);
  color: white;
  border-radius: 10px;
  text-align: center;
  height: 100%;
  opacity: 0;
  transition: opacity 0.3s ease;
}

.film-title {
  font-size: 18px;
  font-weight: bold;
}

.film-year {
  font-size: 14px;
}

.list-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.list-title {
  font-size: 28px;
  font-family: "Limelight", serif;
  color: var(--text-color);
}

.back-button {
  font-size: 20px;
  background-color: var(--primary-color);
  color: var(--text-color);
  border: 2px solid var(--text-color);
  border-radius: 10px;
  padding: 5px 15px;
  cursor: pointer;
}
</style>