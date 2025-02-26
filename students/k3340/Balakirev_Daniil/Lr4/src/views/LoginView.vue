<template>
  <v-app>
    <v-main class="d-flex align-center justify-center">
      <v-container>
        <v-row justify="center">
          <v-col cols="12" sm="8" md="6" lg="4">
            <v-card class="elevation-12">
              <v-toolbar color="teal" dark>
                <v-toolbar-title>Авторизация</v-toolbar-title>
              </v-toolbar>
              <v-card-text>
                <v-form>
                  <v-text-field
                    required
                    v-model="username"
                    name="login"
                    label="Логин"
                    type="text"
                  ></v-text-field>
                  <v-text-field
                    required
                    v-model="password"
                    name="password"
                    label="Пароль"
                    type="password"
                  ></v-text-field>
                </v-form>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="teal" dark to="/signup">Зарегистрироваться</v-btn>
                <v-btn color="teal" dark @click="submit">Войти</v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>
    </v-main>
  </v-app>
</template>

<script>
export default {
  name: 'LoginView',
  data() {
    return {
      username: null,
      password: null
    };
  },
  methods: {
    submit() {
      const body = {
        username: this.username,
        password: this.password
      };
      this.axios
        .post(this.$hostname + 'auth/token/login/', body)
        .then(response => {
          if (response.status === 200) {
            localStorage.setItem('auth_token', response.data.auth_token);
            this.$router.push({ name: 'Rooms' });
          } else {
            if (response.status === 400) {
              alert('Wrong username or password');
            } else {
              alert('Unknown error');
            }
          }
        });
    }
  }
};
</script>