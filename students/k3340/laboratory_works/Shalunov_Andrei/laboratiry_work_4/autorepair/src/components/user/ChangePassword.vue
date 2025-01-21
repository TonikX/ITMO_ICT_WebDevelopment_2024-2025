<template>
    <v-container class="change-password">
      <v-row class="justify-center">
        <v-col cols="12" md="6">
          <h1 class="text-center">Изменение пароля</h1>
          <v-form @submit.prevent="changePassword" class="mt-5">
            <v-text-field
              v-model="form.current_password"
              label="Текущий пароль"
              type="password"
              required
              outlined
              class="mb-4"
            ></v-text-field>
            <v-text-field
              v-model="form.new_password"
              label="Новый пароль"
              type="password"
              required
              outlined
              class="mb-4"
            ></v-text-field>
            <v-btn type="submit" color="indigo" block large>Изменить пароль</v-btn>
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
          current_password: '',
          new_password: '',
        },
      };
    },
    methods: {
      async changePassword() {
        try {
          const token = localStorage.getItem('token');
          if (!token) {
            alert('Вы не авторизованы!');
            return;
          }
  
          await this.$axios.post('/auth/users/set_password/', this.form, {
            headers: { Authorization: `Token ${token}` },
          });
  
          this.$router.push('/profile');
        } catch (error) {
          alert('Ошибка при изменении пароля: ' + JSON.stringify(error.response?.data || error.message));
        }
      },
    },
  };
  </script>
  
  <style>
  .change-password {
    margin-top: 50px;
  }
  </style>