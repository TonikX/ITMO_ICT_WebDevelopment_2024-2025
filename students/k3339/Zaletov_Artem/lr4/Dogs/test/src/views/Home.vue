<template>
  <div>
    <v-card elevation="2" outlined class="my-4 card-container">
      <v-card-text>
        <h2 class="section-title">Меню</h2>
        <div class="nav-links">
          <!--<v-btn text @click="goParticipations" class="nav-btn">Participations</v-btn>
          <v-btn text @click="goParticipants" class="nav-btn">Participants</v-btn>-->

          <template v-if="authorized">
            <v-btn text @click="goParticipations" class="nav-btn">Результаты</v-btn>
            <v-btn text @click="goParticipants" class="nav-btn">Участники</v-btn>
            <!--<v-btn text @click="goLogOut" class="nav-btn">Клубы</v-btn>-->
            <v-btn text @click="goProfile" class="nav-btn">Профиль</v-btn>
            <v-btn text @click="goLogOut" class="nav-btn">Выйти</v-btn>
          </template>

          <template v-else>
            <v-btn text @click="goSignIn" class="nav-btn">Войти</v-btn>
            <v-btn to="/show/signup" class="nav-btn">Регистрация</v-btn>
          </template>
        </div>
      </v-card-text>
    </v-card>
  </div>
</template>

<script>
export default {
  name: 'HomePage', // Renamed component to multi-word

  data: () => ({
    authorized: false
  }),

  created () {
    if (sessionStorage.getItem('auth_token')) {
      if (sessionStorage.getItem('auth_token') !== '-1') {
        this.authorized = true
      }
    }
  },

  methods: {
    goParticipations() {
      this.$router.push('/participation');
    },

    goParticipants() {
      this.$router.push('/participants');
    },

    goProfile() {
      this.$router.push({ name: 'profile' });
    },

    goLogOut() {
      this.$router.push({ name: 'logout' });
    },

    goSignIn() {
      this.$router.push({ name: 'signin' });
    }
  }
}
</script>

<style scoped>
.card-container {
  max-width: 500px;
  margin: 2rem auto;
  padding: 2rem;
  border-radius: 8px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.1);
}

.section-title {
  font-size: 1.5rem;
  font-weight: bold;
  color: #3f51b5;
  margin-bottom: 1.5rem;
  text-align: center;
}

.nav-links {
  display: flex;
  flex-direction: column;
  gap: 1rem;
  align-items: center;
}

.nav-btn {
  text-decoration: none;
  color: #283593;
  font-weight: bold;
  width: 100%;
  max-width: 250px;
}

.nav-btn:hover {
  background-color: #f1f1f1;
  transition: background-color 0.3s ease;
}
</style>
