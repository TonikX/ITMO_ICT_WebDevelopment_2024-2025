<template>
  <div>
    <h2>Profile Information</h2>
    <form @submit.prevent="updateProfile">
      <label for="username">Username:</label>
      <input type="text" v-model="user.username" id="username" />

      <label for="email">Email:</label>
      <input type="email" v-model="user.email" id="email" />

      <label for="first_name">First Name:</label>
      <input type="text" v-model="user.first_name" id="first_name" />

      <label for="last_name">Last Name:</label>
      <input type="text" v-model="user.last_name" id="last_name" />

      <button type="submit">Save Changes</button>
    </form>
    <div v-if="error" class="error">{{ error }}</div>
    <div v-if="success" class="success">Profile updated successfully!</div>
  </div>
</template>

<script>
export default {
  data() {
    return {
      user: {
        username: '',
        email: '',
        first_name: '',
        last_name: ''
      },
      error: null,
      success: false
    };
  },
  mounted() {
    this.fetchProfile();
  },
  methods: {
    async fetchProfile() {
      try {
        const response = await fetch('/api/profile/', {
          method: 'GET',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
          },
        });

        if (!response.ok) {
          throw new Error('Failed to fetch profile data');
        }

        const data = await response.json();
        this.user = data;
      } catch (err) {
        console.error('Error fetching profile:', err);
        this.error = 'Failed to load profile data.';
      }
    },
    async updateProfile() {
      try {
        const response = await fetch('/api/profile/', {
          method: 'PUT',
          credentials: 'include',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify(this.user),
        });

        if (!response.ok) {
          throw new Error('Failed to update profile');
        }

        const data = await response.json();
        this.user = data;
        this.success = true;
        this.error = null;
      } catch (err) {
        console.error('Error updating profile:', err);
        this.error = 'Failed to update profile.';
        this.success = false;
      }
    }
  }
};
</script>

<style>
.error {
  color: red;
}
.success {
  color: green;
}
</style>
