<template>
  <v-app>
    <v-main class="d-flex align-center justify-center">
      <v-container>
        <v-row justify="center">
          <v-col cols="12" sm="8" md="6" lg="4">
            <v-card class="elevation-12">
              <v-toolbar color="teal" dark>
                <v-toolbar-title>Зарегистрироваться</v-toolbar-title>
              </v-toolbar>
              <v-card-text>
                <v-form ref="form" v-model="valid">
                  <v-text-field
                    v-model="email"
                    :rules="emailRules"
                    required
                    name="email"
                    label="Email"
                    type="text"
                  ></v-text-field>
                  <v-text-field
                    v-model="username"
                    :rules="usernameRules"
                    required
                    name="login"
                    label="Login"
                    type="text"
                  ></v-text-field>
                  <v-text-field
                    v-model="first_name"
                    :rules="firstNameRules"
                    required
                    name="first_name"
                    label="First Name"
                    type="text"
                  ></v-text-field>
                  <v-text-field
                    v-model="last_name"
                    :rules="lastNameRules"
                    required
                    name="last_name"
                    label="Last Name"
                    type="text"
                  ></v-text-field>
                  <v-text-field
                    v-model="password"
                    :rules="passwordRules"
                    required
                    id="password"
                    name="password"
                    label="Password"
                    type="password"
                  ></v-text-field>
                </v-form>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn
                  color="teal"
                  dark
                  :disabled="!valid"
                  :loading="loading"
                  @click="signup"
                >Зарегистрироваться</v-btn>
              </v-card-actions>
            </v-card>
          </v-col>
        </v-row>
      </v-container>

      <v-snackbar v-model="snackbar" :color="snackbarColor" :timeout="3000">
        {{ snackbarText }}
        <template v-slot:action="{ attrs }">
          <v-btn color="white" text v-bind="attrs" @click="snackbar = false">
            Close
          </v-btn>
        </template>
      </v-snackbar>
    </v-main>
  </v-app>
</template>

<script>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import axios from 'axios';

export default {
  name: 'SignupView',
  setup() {
    const email = ref(null);
    const username = ref(null);
    const password = ref(null);
    const first_name = ref(null);
    const last_name = ref(null);
    const loading = ref(false);
    const valid = ref(true);
    const snackbar = ref(false);
    const snackbarText = ref('');
    const snackbarColor = ref('error');
    const form = ref(null);

    const router = useRouter();

    const usernameRules = [
      v => !!v || 'Username is required',
      v => (v && v.length >= 3) || 'Username must be at least 3 characters'
    ];
    const passwordRules = [
      v => !!v || 'Password is required',
      v => !!v || 'Password is required',
      v => (v && v.length >= 6) || 'Password must be at least 6 characters'
    ];
    const emailRules = [
      v => !!v || 'E-mail is required',
      v => /.+@.+\..+/.test(v) || 'E-mail must be valid'
    ];
    const firstNameRules = [
      v => !!v || 'First name is required',
      v => /^[a-zA-Zа-яА-Я]+$/.test(v) || 'First name must contain only letters'
    ];
    const lastNameRules = [
      v => !!v || 'Last name is required',
      v => /^[a-zA-Zа-яА-Я]+$/.test(v) || 'Last name must contain only letters'
    ];

    const signup = async () => {
      if (form.value.validate()) {
        loading.value = true;
        const body = {
          username: username.value,
          password: password.value,
          email: email.value,
          first_name: first_name.value,
          last_name: last_name.value
        };

        try {
          const response = await axios.post(
            'http://127.0.0.1:8000/auth/users/',
            body
          );

          if (response.status === 201) {
            router.push({ name: 'Login' });
          } else {
            console.error("Ошибка при регистрации:", response.data);
            showSnackbar(
              `Signup failed: ${JSON.stringify(response.data)}`,
              'error'
            );
          }
        } catch (error) {
          console.error("Ошибка при регистрации:", error);
          showSnackbar(
            `Signup failed: ${error.message || 'Network error'}`,
            'error'
          );
        } finally {
          loading.value = false;
        }
      }
    };

    const showSnackbar = (text, color = 'error') => {
      snackbarText.value = text;
      snackbarColor.value = color;
      snackbar.value = true;
    };

    return {
      email,
      username,
      password,
      first_name,
      last_name,
      loading,
      valid,
      snackbar,
      snackbarText,
      snackbarColor,
      usernameRules,
      passwordRules,
      emailRules,
      firstNameRules,
      lastNameRules,
      form,
      signup,
      showSnackbar
    };
  }
};
</script>

