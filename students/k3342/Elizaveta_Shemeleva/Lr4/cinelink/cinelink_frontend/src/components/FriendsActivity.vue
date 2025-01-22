<template>
  <div>
    <AppHeader/>

    <div class="content-container">
      <div class="tab-buttons">
        <router-link
            :class="{ active: $route.name === 'FriendsPage' }"
            class="tab-button"
            to="/friends"
        >
          Friends
        </router-link>
        <router-link
            :class="{ active: $route.name === 'FriendsActivity' }"
            class="tab-button"
            to="/friends-activity"
        >
          Friends' Activity
        </router-link>
      </div>

      <div v-if="isLoading" class="loading">
        Loading friends' activity...
      </div>
      <div v-else-if="error" class="error">
        {{ error }}
      </div>
      <div v-else-if="!activities.length" class="no-activity">
        No activity found for your friends.
      </div>
      <div v-else id="activityList">
        <div
            v-for="activity in activities"
            :key="activity.id"
            class="activity-item"
        >
          <div
              :style="{ backgroundImage: `url(${activity.movie.poster_url || 'images/default-poster.png'})` }"
              class="movie-poster"
              @click="goToMovie(activity.movie.id)"
          ></div>
          <div class="activity-details">
            <div class="activity-username">
              <router-link :to="{ name: 'FriendProfile', params: { userId: activity.user.id } }">
                {{ activity.user.username }}
              </router-link>
            </div>
            <div class="activity-action">rated</div>
            <div
                class="activity-movie"
                @click="goToMovie(activity.movie.id)"
            >
              {{ activity.movie.title }}
            </div>
            <div :class="['activity-rating', activity.rating >= 7 ? 'high' : 'low']">
              {{ activity.rating }}/10
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {useFriendsActivityStore} from "@/stores/friendsActivity";
import {computed, onMounted} from "vue";
import AppHeader from "@/components/AppHeader.vue";
import {useRouter} from "vue-router";

export default {
  name: "FriendsActivity",
  components: {AppHeader},
  setup() {
    const activitiesStore = useFriendsActivityStore(); // Pinia store
    const router = useRouter();

    const activities = computed(() => activitiesStore.activities);
    const isLoading = computed(() => activitiesStore.isLoading);
    const error = computed(() => activitiesStore.error);

    const loadActivity = async () => {
      try {
        await activitiesStore.loadFriendsActivity();
      } catch (err) {
        console.error("Error loading activity:", err);
      }
    };

    const goToMovie = (movieId) => {
      router.push({name: "MovieDetails", params: {id: movieId}});
    };

    onMounted(() => {
      loadActivity();
    });

    return {
      activities,
      isLoading,
      error,
      goToMovie,
    };
  },
};
</script>

<style scoped>
/* Keep your existing styles */
.content-container {
  padding: 100px 150px 30px;
}

.tab-buttons {
  display: flex;
  gap: 20px;
  margin-bottom: 20px;
}

.tab-button {
  padding: 10px 20px;
  border-radius: 10px;
  border: 2px solid var(--blue-color);
  font-size: 24px;
  text-decoration: none;
  cursor: pointer;
  background-color: transparent;
  color: var(--blue-color);
}

.tab-button.active {
  background-color: var(--blue-color);
  color: var(--background-color);
}

.activity-item {
  display: flex;
  align-items: center;
  background-color: var(--secondary-color);
  padding: 15px;
  margin-bottom: 15px;
  border-radius: 10px;
  border: 1px solid var(--blue-color);
}

.movie-poster {
  width: 100px;
  height: 150px;
  border-radius: 10px;
  background-color: var(--background-color);
  background-size: cover;
  background-position: center;
  margin-right: 20px;
  cursor: pointer;
}

.activity-details {
  flex-grow: 1;
  font-size: 22px;
  color: var(--blue-color);
  line-height: 1.8;
}

.activity-username {
  font-size: 24px;
  font-weight: bold;
  margin-bottom: 5px;
}

.activity-username a {
  color: var(--blue-color);
  text-decoration: underline;
  font-weight: bold;
  transition: color 0.3s;
}

.activity-username a:active {
  color: #ffffff;
}

.activity-action {
  font-size: 20px;
  color: var(--blue-color);
  margin-bottom: 5px;
}

.activity-movie {
  font-size: 22px;
  margin-bottom: 5px;
  font-weight: bold;
  cursor: pointer;
  text-decoration: underline;
}

.activity-rating {
  font-size: 22px;
  font-weight: bold;
}

.activity-rating.high {
  color: var(--green-color);
}

.activity-rating.low {
  color: var(--red-color);
}
</style>