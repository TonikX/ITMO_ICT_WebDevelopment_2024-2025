<template>
  <div class="edit">
    <h2 class="profile-title">Profile</h2>
    <h3 class="welcome-message">Nice to see you, {{ login() }}!</h3>
    <v-card class="profile-card">
      <v-card-text class="profile-info">
        <div class="text--primary">
          <p><strong>First name:</strong> {{ first_name }}</p>
          <p><strong>Last name:</strong> {{ last_name }}</p>
          <p><strong>Telephone number:</strong> {{ tel }}</p>
        </div>
        <div class="profile-actions">
          <v-btn @click="goRegister" class="profile-button primary">Зарегистрировать собаку</v-btn>
          <v-btn @click="goGrade" class="profile-button secondary">Поставить оценку</v-btn>
          <v-btn @click="goEdit" class="profile-button success">Редактировать профиль</v-btn>
          <v-btn @click="goHome" class="profile-button error">На главную</v-btn>
        </div>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
export default {
  name: 'UserProfile',
  data() {
    return {
      first_name: '',
      last_name: '',
      tel: '',
    };
  },
  created() {
    this.loadReaderData();
  },
  methods: {
    async loadReaderData() {
      try {
        const response = await this.axios.get('http://127.0.0.1:8000/auth/users/me/', {
          headers: {
            Authorization: `Token ${sessionStorage.getItem('auth_token')}`
          }
        });
        this.first_name = response.data.first_name;
        this.last_name = response.data.last_name;
        this.tel = response.data.tel;
      } catch (error) {
        console.error('Error fetching user data:', error);
      }
    },
    goHome() {
      this.$router.push({ name: 'home' });
    },
    goRegister() {
      this.$router.push({ name: 'regdog' });
    },
    goEdit() {
      this.$router.push({ name: 'profile_edit' });
    },
    goGrade() {
      this.$router.push({ name: 'grading' });
    },
    login() {
      return sessionStorage.getItem('username');
    }
  }
};
</script>

<style scoped>
.edit {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin-top: 2rem;
}

.profile-title {
  font-size: 2.5rem;
  font-weight: bold;
  color: #3f51b5;
  margin-bottom: 0.5rem;
}

.welcome-message {
  font-size: 1.5rem;
  color: #607d8b;
  margin-bottom: 2rem;
}

.profile-card {
  width: 100%;
  max-width: 600px;
  box-shadow: 0 6px 15px rgba(0, 0, 0, 0.15);
  border-radius: 12px;
  padding: 2rem;
  background-color: #ffffff;
  text-align: center;
}

.profile-info p {
  font-size: 1.1rem;
  line-height: 1.6;
  color: #444;
  margin: 8px 0;
}

.profile-actions {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  align-items: center;
  margin-top: 1.5rem;
}

.profile-button {
  width: 100%;
  max-width: 400px;
  padding: 10px;
  font-size: 1.1rem;
  border-radius: 8px;
  transition: background-color 0.3s ease;
}

.primary {
  background-color: #3f51b5;
  color: white;
}

.secondary {
  background-color: #009688;
  color: white;
}

.success {
  background-color: #4caf50;
  color: white;
}

.error {
  background-color: #f44336;
  color: white;
}

.profile-button:hover {
  filter: brightness(1.2);
}
</style>
