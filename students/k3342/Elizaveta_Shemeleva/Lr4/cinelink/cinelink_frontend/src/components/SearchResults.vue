<template>
  <AppHeader />
  <div class="content-container">
    <!-- Movies Section -->
    <section v-if="movies.length" aria-label="Search results for movies">
      <h2 class="section-title">Movies</h2>
      <div class="movie-grid" role="list">
        <div
          v-for="movie in movies"
          :key="movie.id"
          class="movie-item-container"
          @click="goToMovie(movie.id)"
        >
          <div
            :style="{ backgroundImage: `url(${movie.poster_url || defaultPoster})` }"
            class="movie-item"
          ></div>
          <div class="movie-title">{{ movie.title }}</div>
        </div>
      </div>
    </section>

    <!-- Users Section -->
    <section v-if="users.length" aria-label="Search results for users">
      <h2 class="section-title">Users</h2>
      <div class="user-grid" role="list">
        <div
          v-for="user in users"
          :key="user.id"
          class="user-item"
          @click="goToUser(user.id)"
        >
          <div
            :style="{ backgroundImage: `url(${user.avatar_url || defaultAvatar})` }"
            class="user-avatar"
          ></div>
          <div class="user-name">{{ user.username }}</div>
        </div>
      </div>
    </section>

    <!-- No Results -->
    <p v-if="!movies.length && !users.length && query" aria-live="polite" class="no-results">
      No results found for "{{ query }}".
    </p>
  </div>
</template>

<script>
import AppHeader from "@/components/AppHeader.vue";
import axios from "axios";
import defaultAvatar from "@/assets/images/default-avatar.png"; // Import default avatar
import defaultPoster from "@/assets/images/default-poster.png"; // Import default poster

export default {
  name: "SearchResults",
  components: {AppHeader},
  data() {
    return {
      query: this.$route.query.q || "", // Get the query from the route
      movies: [],
      users: [],
      defaultAvatar, // Use imported default avatar
      defaultPoster, // Use imported default poster
    };
  },
  watch: {
    "$route.query.q": {
      handler(newQuery) {
        this.query = newQuery;
        this.performSearch();
      },
      immediate: true,
    },
  },
  methods: {
    async performSearch() {
      if (!this.query.trim()) {
        this.movies = [];
        this.users = [];
        return;
      }

      try {
        // Fetch movies
        const movieResponse = await axios.get("api/movies/search/", {
          params: {search: this.query},
        });
        this.movies = movieResponse.data || [];

        // Fetch users
        const userResponse = await axios.get("api/users/search/", {
          params: {search: this.query},
        });
        this.users = userResponse.data.map((user) => ({
          ...user,
          avatar_url: user.avatar_url || this.defaultAvatar, // Apply default avatar fallback
        }));
      } catch (error) {
        console.error("Error performing search:", error);
        alert("Failed to fetch search results. Please try again later.");
      }
    },
    goToMovie(imdbID) {
      this.$router.push({path: "/movie/" + imdbID});
    },
    goToUser(userId) {
      this.$router.push({path: "/friend/" + userId});
    },
  },
};
</script>

<style scoped>
/* Styles remain unchanged */
.content-container {
  padding: 100px 150px 30px;
}

.movie-grid,
.user-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(125px, 1fr));
  gap: 20px;
  margin: 20px auto 0;
}

.movie-item-container,
.user-item {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.movie-item,
.user-avatar {
  width: 125px;
  height: 190px;
  background-size: cover;
  background-position: center;
  border-radius: 10px;
  cursor: pointer;
  transition: transform 0.3s;
}
</style>