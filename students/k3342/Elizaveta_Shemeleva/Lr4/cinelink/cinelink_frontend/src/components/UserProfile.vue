<template>
  <AppHeader/>
  <div class="content-container profile-content">
    <div class="profile-header">
      <div
          :style="{ backgroundImage: `url(${avatar})` }"
          class="profile-avatar"
      ></div>
      <p class="username" tabindex="0">{{ user?.email || 'Default User' }}</p>
      <div class="button-section">
        <button class="edit-button" @click="editProfile">edit profile</button>
        <button class="add-list-button" @click="addNewList">+ add list</button>
      </div>
    </div>

    <div class="section-title">TOP-5 films</div>
    <div class="top-films" role="list">
      <div
          v-for="movie in topMovies"
          :key="movie.id"
          :style="{ backgroundImage: `url(${movie.poster_url || defaultPoster})` }"
          class="film-poster"
          @click="goToMovie(movie.id)"
      >
        <div class="film-details">
          <h3 class="film-title">{{ movie.title }}</h3>
          <p class="film-year">{{ movie.year }}</p>
        </div>
      </div>
    </div>

    <div class="section-title">your lists</div>
    <div class="lists-carousel" role="list">
      <div
          v-for="list in userLists"
          :key="list.id"
          class="list-item"
          @click="goToList(list.id)"
      >
        {{ list.name }}
      </div>
    </div>
  </div>
</template>
<script>
import {useAuthStore} from "@/stores/auth";
import {useProfileStore} from "@/stores/profile";
import {computed, onMounted} from "vue";
import {useRouter} from "vue-router";
import AppHeader from "@/components/AppHeader.vue";

export default {
  name: "UserProfile",
  components: {AppHeader},
  setup() {
    const authStore = useAuthStore();
    const profileStore = useProfileStore();
    const router = useRouter();

    const user = computed(() => authStore.user);
    // const avatar = computed(() => profileStore.avatar || "@/assets/images/default-avatar.png");
    const avatar = computed(() => profileStore.avatar_url || "@/assets/images/default-avatar.png");
    const topMovies = computed(() => profileStore.topMovies);
    const userLists = computed(() => profileStore.userLists);
    const defaultAvatar = "@/assets/images/default-avatar.png"; // Default avatar placeholder

    const loadProfile = async () => {
      try {
        await authStore.fetchUser();
        await profileStore.loadProfile();
        await profileStore.loadTopMovies();
        await profileStore.loadUserLists(); // Fetch user lists
      } catch (error) {
        console.error("Error loading profile:", error);
      }
    };

    const editProfile = () => {
      router.push("/edit-profile");
    };

    const addNewList = async () => {
      const newListName = prompt("Enter the name of the new list:");
      if (!newListName || !newListName.trim()) {
        alert("List name cannot be empty!");
        return;
      }

      try {
        // Call the store's method to add the new list
        await profileStore.addNewList(newListName.trim());
        alert(`New list "${newListName.trim()}" created successfully!`);
      } catch (error) {
        console.error("Error adding list:", error);
        alert("Failed to create the new list. Please try again.");
      }
    };

    const goToMovie = (id) => {
      router.push({path: "/movie/" + id});
    };

    const goToList = (listId) => {
      router.push({path: "/list", query: {listId}});
    };

    onMounted(() => {
      loadProfile();
    });

    return {
      avatar,
      user,
      topMovies,
      userLists,
      defaultAvatar,
      editProfile,
      addNewList,
      goToMovie,
      goToList,
    };
  },
};
</script>

<style scoped>
.content-container {
  padding-top: 100px;
  padding-left: 150px;
  padding-right: 150px;
  margin-bottom: 30px;
}

.profile-header {
  display: flex;
  align-items: center;
  position: relative;
  margin-bottom: 30px;
}

.profile-avatar {
  width: 100px;
  height: 100px;
  background-color: var(--primary-color);
  border-radius: 50%;
  background-image: url('@/assets/images/default-avatar.png');
  background-size: cover;
  background-position: center;
  border: 1px solid #D9D9D9;
  margin-right: 30px;
}

.username {
  font-family: 'Limelight', sans-serif;
  font-size: 30px;
  color: var(--text-color);
  flex-grow: 1;
}

.button-section {
  display: flex;
  flex-direction: column;
  gap: 10px;
  position: absolute;
  right: 0;
}

.edit-button {
  padding: 10px 20px;
  background-color: var(--text-color);
  color: var(--background-color);
  font-size: 22px;
  border: none;
  border-radius: 10px;
  cursor: pointer;
}

.add-list-button {
  padding: 10px 20px;
  background-color: var(--primary-color);
  border: 2px solid var(--text-color);
  color: var(--text-color);
  font-size: 22px;
  border-radius: 10px;
  cursor: pointer;
  display: block;
  z-index: 1; /* Ensure the button is on top of any other element */
}

.add-list-button:hover {
  background-color: var(--text-color);
  color: var(--background-color);
}

.section-title {
  font-family: 'Limelight', sans-serif;
  font-size: 24px;
  color: var(--text-color);
  margin-top: 30px;
  margin-bottom: 10px;
  border-bottom: 1px solid var(--text-color);
  padding-bottom: 10px;
}

.top-films {
  display: flex;
  gap: 19px;
  margin-bottom: 30px;
}

.film-poster {
  width: 213px;
  height: 318px;
  background-color: var(--primary-color);
  border-radius: 10px;
  background-size: cover;
  background-position: center;
  background-repeat: no-repeat;
  cursor: pointer;
}

.lists-carousel {
  display: flex;
  gap: 20px;
  overflow-x: auto;
  padding-bottom: 10px;
  scroll-behavior: smooth;
  justify-content: flex-start;
  margin-bottom: 20px;
}

.list-item {
  width: 270px;
  height: 170px;
  background-color: var(--primary-color);
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  cursor: pointer;
  font-size: 30px;
  text-decoration: none;
  color: var(--text-color);
  flex-shrink: 0;
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

.film-poster:hover .film-details {
  opacity: 1;
}

.film-title {
  font-size: 18px;
  font-weight: bold;
}

.film-year {
  font-size: 14px;
}
</style>