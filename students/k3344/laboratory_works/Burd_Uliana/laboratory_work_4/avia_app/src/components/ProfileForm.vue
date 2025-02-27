<template>
 <div class="background-container">
     <img src="@/assets/road.jpg" alt="Sky" class="background-image">
  <div class="main-container">
    <form @submit.prevent="updateProfile" class="profile-form">
      <label>
        Username:
        <input v-model="username" type="text" required />
      </label>
      <br />
      <label>
        Email:
        <input v-model="email" type="email" required />
      </label>
      <br />
      <label>
        New Password:
        <input v-model="newPassword" type="password" required />
      </label>
      <br />
      <button type="submit">Update Profile</button>
    </form>
    <div class="buttons-container">
      <router-link to="/aircrafts">
        <button>Aircrafts</button>
      </router-link>
      <router-link to="/crewmembers">
        <button>Crew Members</button>
      </router-link>
      <router-link to="/flights">
        <button>Flights</button>
      </router-link>
      <router-link to="/employees">
        <button>Employees</button>
      </router-link>
    </div>
  </div>
 </div>
</template>

<script>
import axios from 'axios';
export default {
  data() {
    return {
      username: '',
      email: '',
      newPassword: '',
      token: '',
      currentUser: {
        username: '',
        email: ''
      }
    };
  },
  created() {
    const token = localStorage.getItem('token');
    if (token) {
      this.fetchUserProfile(token);
    } else {
      console.error('Token not found');
    }
  },
  methods: {
    fetchUserProfile(token) {
      const userId = this.$route.params.id;
      axios.get(`http://localhost:8000/my_avia_app/auth/profile/${userId}/`, {
        headers: {
          Authorization: `Token ${token}`,
        },
      })
      .then(response => {
        console.log(response.data);
        this.currentUser = response.data;
      })
      .catch(error => {
        console.error(error.response.data);
      });
    }
  }
};
</script>
<style scoped>
.background-container {
  height: 100vh;
  display: flex;
  justify-content: center;
  align-items: center;
  position: relative;
}
.background-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  position: absolute;
  top: 0;
  left: 0;
  z-index: -1;
}
.main-container {
  margin-top: 100px;
}
.profile-form {
  max-width: 400px;
  margin: auto;
  padding: 20px;
  border: 1px solid #ccc;
  border-radius: 5px;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
  background-color: #fff;
}
.form-group {
  margin-bottom: 15px;
}
label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
  color: #4CAF50;
}
input {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 3px;
  margin-top: 10px;
}
button {
  background-color: #4CAF50;
  color: #fff;
  padding: 10px 15px;
  border: none;
  border-radius: 3px;
  cursor: pointer;
  margin-top: 5px;
}
button:hover {
  background-color: #45a049;
}
.buttons-container {
  display: flex;
  justify-content: center;
  margin-top: 20px;
}
.buttons-container button {
  margin: 0 10px;
}
</style>