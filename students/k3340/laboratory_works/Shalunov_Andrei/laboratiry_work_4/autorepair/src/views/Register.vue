<template>
  <v-container class="register">
    <v-row class="justify-center">
      <v-col cols="12" md="6">
        <h1 class="text-center">Регистрация</h1>
        <v-form @submit.prevent="register" class="mt-5">
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
          <v-text-field
            v-model="form.password"
            label="Пароль"
            type="password"
            required
            outlined
            class="mb-4"
          ></v-text-field>
          <v-btn type="submit" color="indigo" block large>Зарегистрироваться</v-btn>
        </v-form>
        <div class="text-center mt-6">
          <p class="text-large mb-3">Уже зарегистрированы?</p>
          <v-btn color="indigo-lighten-4" large outlined to="/login">Login</v-btn>
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
        password: '',
      },
    };
  },
  methods: {
    async register() {
      try {
        await this.$axios.post('/auth/users/', this.form);
        this.$router.push('/login');
      } catch (error) {
        alert('Ошибка регистрации: ' + JSON.stringify(error.response.data));
      }
    },
  },
};
</script>

<style>
.register {
  margin-top: 50px;
}
.text-large {
  font-size: 18px;
  font-weight: 500;
}
</style>