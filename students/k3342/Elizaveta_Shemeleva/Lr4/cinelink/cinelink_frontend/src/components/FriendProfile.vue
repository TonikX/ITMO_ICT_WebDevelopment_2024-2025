<template>
  <div>
    <AppHeader/>

    <main aria-labelledby="friendUsername" class="content-container" role="main">
      <div v-if="friend && Object.keys(friend).length > 0" class="friend-header">
        <div
            :style="{ backgroundImage: `url(${friend.avatar_url || 'images/default-avatar.png'})` }"
            aria-label="Friend's avatar"
            class="friend-avatar"
        ></div>
        <p id="friendUsername" class="username" tabindex="0">
          {{ friend.username || friend.email || "Friend's Name" }}
        </p>
        <button
            aria-label="Add or remove friend"
            class="friend-button"
            @click="toggleFriendship"
        >
          {{ isFriend ? "Delete Friend" : "Add Friend" }}
        </button>
      </div>

      <h2 v-if="favoriteMovies.length > 0" id="favoriteMoviesTitle" class="section-title">
        Top 5 Favorite Movies
      </h2>
      <div
          v-if="favoriteMovies.length > 0"
          id="favoriteMovies"
          aria-labelledby="favoriteMoviesTitle"
          class="favorite-movies"
          role="list"
      >
        <div
            v-for="movie in favoriteMovies"
            :key="movie.id"
            :style="{ backgroundImage: `url(${movie.poster_url || 'images/default-poster.png'})` }"
            :title="movie.title"
            class="movie-poster"
            @click="goToMovie(movie.id)"
        ></div>
      </div>
      <p v-else>No favorite movies available.</p>
    </main>
  </div>
</template>
<script>
import {useFriendStore} from "@/stores/friend";
import {useRoute, useRouter} from "vue-router";
import {computed, onMounted} from "vue";
import AppHeader from "@/components/AppHeader.vue";

export default {
  name: "FriendProfile",
  components: {AppHeader},
  setup() {
    const friendStore = useFriendStore();
    const route = useRoute();
    const router = useRouter();

    // Reactive data from the store
    const friend = computed(() => friendStore.friend || {});
    const favoriteMovies = computed(() => friendStore.favoriteMovies || []);
    const isFriend = computed(() => friendStore.isFriend);

    // Fetch friend data
    const fetchFriendData = async () => {
      const friendId = route.params.userId;

      try {
        await friendStore.fetchFriendData(friendId);
        console.log("Friend data loaded:", friend.value);
        console.log("Favorite movies loaded:", favoriteMovies.value);
      } catch (error) {
        console.error("Failed to load friend details:", error);
        alert("Failed to load friend details.");
      }
    };

    // Toggle friendship
    const toggleFriendship = async () => {
      const friendId = route.params.userId;

      try {
        await friendStore.toggleFriendship(friendId);
        console.log("Friendship toggled, isFriend:", isFriend.value);
      } catch (error) {
        console.error("Failed to update friendship status:", error);
        alert("Failed to update friendship status.");
      }
    };

    // Navigate to movie details
    const goToMovie = (movieId) => {
      router.push({name: "MovieDetail", params: {movieId}});
    };

    // Fetch data on component mount
    onMounted(() => {
      fetchFriendData();
    });

    return {
      friend,
      favoriteMovies,
      isFriend,
      toggleFriendship,
      goToMovie,
    };
  },
};
</script>

<style scoped>
.content-container {
  padding: 100px 150px 30px;
}

.friend-header {
  display: flex;
  align-items: center;
  gap: 20px;
  margin-bottom: 30px;
}

.friend-avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background-color: var(--primary-color);
  background-size: cover;
  background-position: center;
  border: 2px solid var(--text-color);
}

.username {
  font-size: 28px;
  font-family: 'Limelight', sans-serif;
  color: var(--text-color);
}

.friend-button {
  padding: 10px 20px;
  background-color: var(--text-color);
  color: var(--background-color);
  font-size: 18px;
  border: none;
  border-radius: 10px;
  cursor: pointer;
}

.friend-button:hover {
  background-color: var(--background-color);
  color: var(--text-color);
}

.section-title {
  font-size: 24px;
  margin-top: 30px;
  color: var(--text-color);
  border-bottom: 1px solid var(--text-color);
  padding-bottom: 5px;
}

.favorite-movies {
  display: flex;
  gap: 19px;
  margin-top: 20px;
}

.movie-poster {
  width: 213px;
  height: 318px;
  background-color: var(--primary-color);
  border-radius: 10px;
  background-size: cover;
  background-position: center;
  cursor: pointer;
}
</style>