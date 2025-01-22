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

      <!-- Loading state -->
      <div v-if="isLoading" class="loading">
        Loading friends...
      </div>

      <!-- Error state -->
      <div v-else-if="error" class="error">
        {{ error }}
      </div>

      <!-- No friends state -->
      <div v-else-if="!friends.length" class="no-friends">
        You have no friends yet. Add some to get started!
      </div>

      <!-- Friends grid -->
      <div v-else id="friends" class="friends-grid">
        <div v-for="friend in friends" :key="friend.id" class="friend-card">
          <!-- Friend Avatar -->
          <router-link
              :style="{ backgroundImage: `url(${friend.avatar_url || '/images/default-avatar.png'})` }"
              :to="{ name: 'FriendProfile', params: { userId: friend.id } }"
              class="friend-avatar"
          ></router-link>

          <!-- Friend Name -->
          <div class="friend-details">
            <router-link
                :to="{ name: 'FriendProfile', params: { userId: friend.id } }"
                class="friend-name"
            >
              {{ friend.username || friend.email }}
            </router-link>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import {useFriendsStore} from "@/stores/friends";
import {computed, onMounted} from "vue";
import AppHeader from "@/components/AppHeader.vue";

export default {
  name: "FriendsPage",
  components: {AppHeader},
  setup() {
    const friendsStore = useFriendsStore(); // Pinia store for friends

    // Reactive properties for state
    const friends = computed(() => friendsStore.friends);
    const isLoading = computed(() => friendsStore.isLoading);
    const error = computed(() => friendsStore.error);

    // Fetch the friends list
    const loadFriendsData = async () => {
      try {
        await friendsStore.fetchFriends();
      } catch (err) {
        console.error("Error loading friends:", err);
      }
    };

    // Load friends data when the component is mounted
    onMounted(() => {
      loadFriendsData();
    });

    return {
      friends,
      isLoading,
      error,
    };
  },
};
</script>

<style scoped>
/* Container styles */
.content-container {
  padding-top: 100px;
  padding-left: 150px;
  padding-right: 150px;
  margin-bottom: 30px;
}

/* Tab buttons */
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
  transition: background-color 0.3s, color 0.3s;
}

.tab-button.active {
  background-color: var(--blue-color);
  color: var(--background-color);
}

/* Friends grid */
.friends-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
  gap: 20px;
}

/* Friend card */
.friend-card {
  background-color: var(--primary-color);
  border: 1px solid var(--blue-color);
  border-radius: 15px;
  padding: 20px;
  text-align: center;
  box-shadow: 0px 4px 8px rgba(0, 0, 0, 0.1);
  transition: transform 0.3s, box-shadow 0.3s;
}

.friend-card:hover {
  transform: translateY(-5px);
  box-shadow: 0px 6px 15px rgba(0, 0, 0, 0.2);
}


/* Friend avatar */
.friend-avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background-size: cover;
  background-position: center;
  margin: 0 auto 15px;
  cursor: pointer;
  border: 3px solid var(--text-color);
}

/* Friend details */
.friend-details {
  margin-top: 10px;
}

/* Friend name */
.friend-name {
  font-size: 20px;
  color: var(--blue-color);
  text-decoration: none;
  font-weight: bold;
  transition: color 0.3s;
}

.friend-name:hover {
  color: var(--primary-color);
}

/* Loading, error, and empty states */
.loading,
.error,
.no-friends {
  text-align: center;
  font-size: 18px;
  color: var(--text-color);
  margin-top: 20px;
}

/* Friend avatar */
.friend-avatar {
  width: 100px;
  height: 100px;
  border-radius: 50%;
  background-size: cover;
  background-position: center;
  margin: 0 auto 15px;
  cursor: pointer;
  border: 3px solid var(--text-color);
  background-color: var(--secondary-color);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 32px;
  font-weight: bold;
  color: var(--text-color);
}

.friend-avatar::before {
  content: "👤"; /* Default placeholder avatar icon */
  display: block;
  text-align: center;
  line-height: 1;
}

</style>