<script setup>
import { ref, onMounted } from "vue";
import { useStore } from "vuex";
import { useRouter } from "vue-router";

const router = useRouter();
const store = useStore();

const firstName = ref("");
const lastName = ref("");

const getUserProfile = () => {
  store.dispatch('getUserProfile').then((response) => {
    firstName.value = response.first_name;
    lastName.value = response.last_name;
  })
}

const updateProfile = () => {
  store.dispatch('updateUserProfile', { first_name: firstName.value, last_name: lastName.value }).then(() => {
    router.push({ name: 'hens' });
  }).catch((error) => {
    console.error("Error fetching user profile:", error);
  });
};

const logout = () => {
  store.dispatch('userLogout').then(() => {
    router.push({ name: 'login' });
  });
};

onMounted(() => {
  getUserProfile();
})
</script>

<template>
  <div class="wrapper">
    <div class="profile-view">
      <h1>User Profile</h1>
      <form @submit.prevent="updateProfile">
        <div>
          <label for="firstName">First Name:</label>
          <input id="firstName" v-model="firstName" type="text" />
        </div>
        <div>
          <label for="lastName">Last Name:</label>
          <input id="lastName" v-model="lastName" type="text" />
        </div>
        <button type="submit">Update Profile</button>
      </form>
      <button @click="logout" class="logout-btn">Log out</button>
    </div>
  </div>
</template>

<style scoped>
/* Main style for the page */
.wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100%;
  font-family: 'Arial', sans-serif;
}

.profile-view {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
  background-color: white;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
  width: 100%;
  max-width: 400px;
}

/* Header */
h1 {
  font-size: 1.5rem;
  font-weight: bold;
  color: hsla(160, 100%, 37%, 1);
  text-align: center;
  margin-bottom: 1rem;
}

/* Form */
form {
  width: 100%;
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* Inputs */
label {
  display: block;
  font-size: 1rem;
  margin-bottom: 0.5rem;
  color: #333;
}

input {
  width: 100%;
  padding: 0.8rem;
  font-size: 1rem;
  border: 1px solid #ccc;
  border-radius: 4px;
  transition: border-color 0.3s;
}

input:focus {
  border-color: hsla(160, 100%, 37%, 1);
  outline: none;
}

/* Buttons */
button {
  width: 70%;
  margin: 0 auto;
  padding: 1rem;
  background-color: hsla(160, 100%, 37%, 1);
  color: white;
  border: none;
  border-radius: 4px;
  font-size: 1rem;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: hsla(160, 100%, 37%, 0.8);
}

button:active {
  background-color: hsla(160, 100%, 37%, 0.6);
}

/* Logout button */
.logout-btn {
  margin-top: 1rem;
  background-color: red;
  color: white;
}
</style>


