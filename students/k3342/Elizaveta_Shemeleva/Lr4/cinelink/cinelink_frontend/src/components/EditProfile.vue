<template>
  <div>
    <AppHeader/>

    <main aria-labelledby="editProfileHeader" class="edit-profile-container" role="main">
      <h1 id="editProfileHeader" class="edit-profile-header">Edit Profile</h1>

      <form id="editProfileForm" aria-describedby="editProfileDescription" @submit.prevent="saveProfile">
        <div>
          <label class="form-label" for="username">Username</label>
          <input
              id="username"
              v-model="username"
              aria-required="true"
              class="form-input"
              placeholder="Enter your username"
              type="text"
          />
        </div>

        <div>
          <label class="form-label" for="avatar_url">Avatar URL</label>
          <input
              id="avatar_url"
              v-model="avatar_url"
              aria-required="false"
              class="form-input"
              placeholder="Paste a link to your avatar"
              type="text"
          />
          <div v-if="avatar_url" class="avatar-preview">
            <img :src="avatar_url" alt="Avatar Preview"/>
          </div>
        </div>

        <div>
          <label class="form-label" for="favorites">Favorite Movies (comma-separated IMDb IDs)</label>
          <input
              id="favorites"
              v-model="favorites"
              aria-required="false"
              class="form-input"
              placeholder="e.g., tt0111161,tt0068646,tt0071562"
              type="text"
          />
        </div>

        <button aria-label="Save profile changes" class="save-button" type="submit">Save Changes</button>
      </form>
    </main>
  </div>
</template>
<script>
import {useProfileStore} from "@/stores/profile";
import {computed} from "vue";
import AppHeader from "@/components/AppHeader.vue";

export default {
  name: "EditProfile",
  components: {AppHeader},
  setup() {
    const profileStore = useProfileStore();

    // Computed properties for profile fields
    const username = computed({
      get: () => profileStore.username,
      set: (value) => (profileStore.username = value),
    });

    const avatar_url = computed({
      get: () => profileStore.avatar_url,
      set: (value) => (profileStore.avatar_url = value),
    });

    const favorites = computed({
      get: () => profileStore.favorites,
      set: (value) => (profileStore.favorites = value),
    });

    const loadProfile = async () => {
      try {
        await profileStore.loadProfile();
        favorites.value = favorites.value.join(", ");
        console.log("Profile loaded successfully.");
      } catch (error) {
        console.error("Error loading profile:", error.message || error);
        alert("Failed to load the profile. Please try again.");
      }
    };

    const saveProfile = async () => {
      try {
        await profileStore.saveProfile({
          username: username.value,
          avatar_url: avatar_url.value,
          favorites: favorites.value,
        });
        favorites.value = favorites.value.join(", ");
        alert("Profile saved successfully!");
      } catch (error) {
        console.error("Error saving profile:", error.message || error);
        alert("Failed to save profile. Please try again.");
      }
    };

    loadProfile();

    return {
      username,
      avatar_url,
      favorites,
      saveProfile,
    };
  },
};
</script>

<style scoped>
.edit-profile-container {
  max-width: 600px;
  margin: 100px auto 50px;
  background-color: var(--background-color);
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.5);
}

.edit-profile-header {
  display: flex;
  align-items: center;
  font-size: 30px;
  font-family: "Limelight", serif;
  color: var(--text-color);
  margin-bottom: 15px;
}

.form-label {
  display: block;
  font-size: 18px;
  font-family: "Limelight", serif;
  color: var(--text-color);
  margin-bottom: 10px;
}

.form-input {
  width: 100%;
  padding: 10px;
  font-size: 20px;
  font-family: "Tenor Sans", sans-serif;
  color: var(--text-color);
  background-color: var(--primary-color);
  border: none;
  border-radius: 5px;
  margin-bottom: 20px;
}

.save-button {
  width: 100%;
  padding: 10px;
  font-size: 18px;
  font-family: "Limelight", serif;
  color: var(--background-color);
  background-color: var(--blue-color);
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s ease;
}

.save-button:hover {
  background-color: var(--text-color);
  color: var(--background-color);
}

.avatar-preview {
  margin-top: 10px;
  text-align: center;
}

.avatar-preview img {
  max-width: 100px;
  max-height: 100px;
  border-radius: 50%;
  border: 2px solid var(--blue-color);
}

</style>