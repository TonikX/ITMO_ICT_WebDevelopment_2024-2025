<template>
  <v-container class="profile">
    <v-row>
      <v-col cols="12">
        <h1>Ваш профиль</h1>
      </v-col>
    </v-row>

    <v-row>
      <v-col cols="8" offset="2" class="text-center">
        <v-card outlined>
          <v-card-text>
            <p class="profile-info"><strong>Логин:</strong> {{ user.username }}</p>
            <v-divider class="my-2"></v-divider>
            <p class="profile-info"><strong>Email:</strong> {{ user.email }}</p>
            <v-divider class="my-2"></v-divider>
            <p class="profile-info"><strong>Airline:</strong> {{ user.airline }}</p>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>

    <v-row class="justify-center align-center">
      <v-btn color="primary" class="mx-2" large to="/change-password">Change Password</v-btn>
      <v-btn color="primary" class="mx-2" large to="/update-profile">Update Profile</v-btn>
      <v-btn color="error" class="mx-2" large @click="logout">Logout</v-btn>
    </v-row>
  </v-container>
</template>

<script>
import { logout } from '../store/auth';

export default {
  data() {
    return {
      user: {
        username: '',
        email: '',
        airline: '',
      },
    };
  },
  async created() {
    const token = localStorage.getItem('token');
    if (!token) {
      this.$router.push('/login');
      return;
    }

    try {
      const response = await this.$axios.get('/auth/users/me/', {
        headers: { Authorization: `Token ${token}` },
      });
      this.user = response.data;
    } catch (error) {
      console.error('Ошибка получения данных профиля:', error.response?.data || error.message);
      this.$router.push('/login');
    }
  },

  methods: {
    async logout() {
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          alert('Вы не авторизованы!');
          return;
        }

        await this.$axios.post('/auth/token/logout/', {}, {
          headers: { Authorization: `Token ${token}` },
        });

        logout();
        this.$router.push('/');
      } catch (error) {
        console.error('Ошибка при выходе:', error.response?.data || error.message);
        alert('Ошибка при выходе');
      }
    },
  },
};
</script>

<style>
.profile {
  padding: 20px;
}
.profile-info {
  font-size: 18px;
  margin-bottom: 10px;
}
</style>
