<template>
  <HeaderLoader :currentPath="currentPath" />

  <div class="container">
    <main role="main">
      <section class="profile" aria-labelledby="profileSection">
        <div class="profile-header">
          <div class="profile-header-cover" aria-hidden="true"></div>
          <div class="profile-header-content">
            <div class="profile-header-img">
              <img :src="profileImage || require('@/assets/images/profile/anon.jpg')" alt="Profile picture of the user" />
            </div>

            <div class="profile-header-info">
              <h4 id="profileSection" class="sr-only">{{ profileName || 'User Profile' }}</h4>
              <p>{{ profileStatus || 'None' }}</p>
              <button @click="toggleEditModal" class="edit-profile" aria-label="Edit your profile information">Edit Profile</button>
              <button @click="logout" class="logout" aria-label="Log out of your account">Log out</button>
              <button @click="redirectToPropertySettings" class="add-property" aria-label="Go to property settings">Add Property</button>
            </div>
          </div>
        </div>
      </section>

      <section class="profile-content" aria-labelledby="rentalHistorySection">
        <div class="tab-content page-0">
          <div class="tab-pane fade active show" id="profile-post">
            <ul class="timeline" aria-live="polite" role="list">
              <li v-for="(historyItem, index) in rentalHistory" :key="index">
                <div class="timeline-time">
                  <span class="start-time">From: {{ historyItem.startDate }}</span>
                  <span class="end-time">To: {{ historyItem.endDate }}</span>
                </div>
                <div class="timeline-body">
                  <div class="timeline-header">
                    <span class="userimage">
                      <img :src="historyItem.profilePicture" alt="Profile picture" />
                    </span>
                    <span class="username">{{ historyItem.userName }}</span>
                    <span class="text-muted pull-right">{{ historyItem.livingDuration }}</span>
                  </div>
                  <div class="timeline-content">
                    <p>{{ historyItem.shortDescription }}</p>
                    <p style="font-style: italic; margin-top: 10px;">
                      <a :href="historyItem.propertyLink" style="color: inherit;">see advertisement...</a>
                    </p>
                  </div>
                </div>
              </li>
            </ul>
            <div v-if="rentalHistory.length === 0" class="no-data-message">
              <p>No rental history found.</p>
            </div>
          </div>
        </div>
      </section>
    </main>

    <div v-if="showEditModal" class="edit-modal">
      <div class="modal-content">
        <h3>Edit Profile</h3>
        <form @submit.prevent="saveProfile">
          <div class="form-group">
            <label for="email">Email:</label>
            <input type="email" id="email" v-model="editProfileData.email" />
          </div>
          <div class="form-group">
            <label for="status">Status:</label>
            <input type="text" id="status" v-model="editProfileData.status" />
          </div>
          <div class="form-group">
            <label for="avatar">Avatar URL:</label>
            <input id="avatar" v-model="editProfileData.avatar" />
          </div>
          <div class="form-actions">
            <button type="submit" class="save-button">Save</button>
            <button type="button" @click="toggleEditModal" class="cancel-button">Cancel</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import HeaderLoader from "@/components/HeaderLoader.vue";
import { API_BASE_URL } from "@/config/config.js";

export default {
  name: "ProfilePage",
  components: {
    HeaderLoader,
  },
  data() {
    return {
      currentPath: "/profile",
      profileName: '',
      profileImage: '', 
      profileStatus: '',
      rentalHistory: [], 
      showEditModal: false,
      editProfileData: {
        email: '',
        status: '',
        avatar: ''
      }
    };
  },
  methods: {
    toggleEditModal() {
      this.showEditModal = !this.showEditModal;
      if (this.showEditModal) {
        const currentUser = this.getCurrentUser();
        this.editProfileData = {
          email: currentUser.email || '',
          status: currentUser.status || '',
          avatar: currentUser.profilePicture || ''
        };
      }
    },

    async saveProfile() {
      try {
        const currentUser = this.getCurrentUser();
        const response = await fetch(`${API_BASE_URL}/users/${currentUser.id}`, {
          method: 'PATCH',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            id: currentUser.id,
            email: this.editProfileData.email,
            status: this.editProfileData.status,
            profilePicture: this.editProfileData.avatar
          })
        });

        if (!response.ok) {
          throw new Error('Failed to update profile.');
        } 

        const responseHistory = await fetch(`${API_BASE_URL}/rentalHistory?userId=${currentUser.id}`);

        if (!responseHistory.ok) {
          throw new Error('Failed to update profile.');
        }
        const dataArray = await responseHistory.json();

        for (const data of dataArray) {

          data.profilePicture = this.editProfileData.avatar

          const responseHistoryUpd = await fetch(`${API_BASE_URL}/rentalHistory/${data.id}`, {
            method: 'PATCH',
            headers: {
              'Content-Type': 'application/json',
            },
            body: JSON.stringify(data),
          });

          if (!responseHistoryUpd.ok) {
            throw new Error('Failed to update profile.');
          }
        }

        const updatedUser = await response.json();
        localStorage.setItem("currentUser", JSON.stringify(updatedUser));
        this.displayUserProfile(updatedUser);
        this.toggleEditModal();
      } catch (error) {
        console.error('Error updating profile:', error);
      }
    },

    logout() {
      localStorage.removeItem("isAuthenticated");
      localStorage.removeItem("currentUser");
      localStorage.removeItem("jwt");

      this.$router.push({ name: 'Auth' }); 
    },

    redirectToPropertySettings() {
      this.$router.push({ name: 'PropertySettings' });
    },

    getCurrentUser() {
      const user = localStorage.getItem("currentUser");
      return user ? JSON.parse(user) : null;
    },

    displayUserProfile(user) {
      this.profileName = user.name || "None";
      this.profileImage = user.profilePicture || '';
      this.profileStatus = user.status || "None";
    },

    async fetchRentalHistory(userId) {
      try {
        const response = await fetch(`${API_BASE_URL}/rentalHistory?userId=${userId}`);
        const data = await response.json();
        const currentUser = this.getCurrentUser();

        const dataWithUser = data.map(item => ({
          ...item,
          userName: currentUser.name,
          livingDuration: this.calculateLivingDuration(item.startDate, item.endDate),
        }));

        this.rentalHistory = dataWithUser;
      } catch (error) {
        console.error('Error fetching rental history:', error);
      }
    },

    calculateLivingDuration(startDate, endDate) {
      const start = new Date(startDate);
      const end = endDate === 'current' ? new Date() : new Date(endDate);

      let years = end.getFullYear() - start.getFullYear();
      let months = end.getMonth() - start.getMonth();
      let days = end.getDate() - start.getDate();

      if (months < 0) {
        years--;
        months += 12;
      }

      if (days < 0) {
        months--;
        const prevMonth = new Date(end.getFullYear(), end.getMonth(), 0); 
        days += prevMonth.getDate();
      }

      let result = "";
      if (years > 0) result += `${years} year${years > 1 ? 's' : ''} `;
      if (months > 0) result += `${months} month${months > 1 ? 's' : ''} `;
      if (days > 0) result += `${days} day${days > 1 ? 's' : ''}`;

      return result.trim() || "0 days"; 
    }
  },

  created() {
    const isAuthenticated = localStorage.getItem("isAuthenticated");
    if (!isAuthenticated) {
      this.$router.push({ name: 'Auth' }); 
      return;
    }

    const currentUser = this.getCurrentUser();
    if (currentUser) {
      this.displayUserProfile(currentUser);
      this.fetchRentalHistory(currentUser.id);
    }
  }
};
</script>

<style scoped>
@import url('../assets/css/styles.css'); 
@import url('../assets/css/themes.css'); 
@import url('../assets/css/profile.css');

.edit-modal {
  position: fixed;
  width: 20%;
  max-width: 800px;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: var(--secondary-color);
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
  z-index: 1000;
}

.edit-modal h3 {
  color: var(--primary-color)
}

.edit-modal label {
  color: var(--primary-color)
}

.modal-content {
  max-width: 700px;
  margin: auto;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
}

.form-group input {
  width: 100%;
  padding: 8px;
  border: 1px solid var(--primary-color);
  border-radius: 4px;
}

.form-actions {
  display: flex;
  justify-content: space-between;
}

.save-button {
  background-color: var(--messages-color);
  color: white;
  border: none;
  padding: 10px;
  border-radius: 4px;
  cursor: pointer;
}

.cancel-button {
  background-color: hsl(0, 30%, 44%);;
  color: var(--primary-color);
  border: none;
  padding: 10px;
  border-radius: 4px;
  cursor: pointer;
}
</style>
