<template>
  <v-container class="update-profile">
    <v-row class="justify-center">
      <v-col cols="12" md="6">
        <h1 class="text-center">Обновление учетных данных</h1>
        <v-form @submit.prevent="updateProfile" class="mt-5">
          <v-text-field
            v-model="form.username"
            label="Логин"
            required
            outlined
            class="mb-4"
          ></v-text-field>
          <v-text-field
            v-model="form.email"
            label="Email"
            type="email"
            required
            outlined
            class="mb-4"
          ></v-text-field>
          <v-btn type="submit" color="indigo" block large>Обновить</v-btn>
        </v-form>
        <div class="text-center mt-6">
          <v-btn color="indigo-lighten-4" large outlined to="/profile">Назад</v-btn>
        </div>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
export default {
  data() {
    return {
      form: {
        username: '',
        email: '',
      },
    };
  },
  created() {
    this.loadProfile();
  },
  methods: {
    async loadProfile() {
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          alert('Вы не авторизованы!');
          return;
        }

        const response = await this.$axios.get('/auth/users/me/', {
          headers: { Authorization: `Token ${token}` },
        });
        this.form.username = response.data.username;
        this.form.email = response.data.email;
      } catch (error) {
        console.error('Ошибка загрузки профиля:', error.response?.data || error.message);
      }
    },
    async updateProfile() {
      try {
        const token = localStorage.getItem('token');
        if (!token) {
          alert('Вы не авторизованы!');
          return;
        }

        await this.$axios.patch('/auth/users/me/', this.form, {
          headers: { Authorization: `Token ${token}` },
        });

        this.$router.push('/profile');
      } catch (error) {
        alert('Ошибка обновления профиля: ' + JSON.stringify(error.response?.data || error.message));
      }
    },
  },
};
</script>

<style>
.update-profile {
  margin-top: 50px;
}
</style>
