<script setup>
import { ref } from 'vue';
import {fetchWrapper} from "@/helpers";
import {useAuthStore} from "@/stores";

const baseUrl = `${import.meta.env.VITE_API_URL}`;

let email = ref('');
let username = ref('');
let password = ref('');
let confirmPassword = ref('');
let valid = ref(false);

const emailRules = [
  v => !!v || 'Email is required',
  v => /.+@.+\..+/.test(v) || 'Email must be valid',
];
const usernameRules = [v => !!v || 'Username is required'];
const passwordRules = [
  v => !!v || 'Password is required',
  v => (v && v.length >= 8) || 'Password must be at least 8 characters',
];
const confirmPasswordRules = [
  v => !!v || 'Confirm Password is required',
  v => v === password.value || 'Passwords do not match',
];

const submit = async () => {
  if (valid.value) {
    try {
      const response = await fetchWrapper.post(`${baseUrl}/auth/users/`, {
        email: email.value,
        username: username.value,
        password: password.value
      });

      if (response.id) {
        const authStore = useAuthStore();
        return authStore.login(username.value, password.value);
      }
    } catch (error) {
      if (error.status === 400 && error.data && error.data.password) {
        const passwordErrors = error.data.password.join(' ');
        alert(passwordErrors);
      } else {
        alert('An unexpected error occurred.');
      }
    }
  }
}
</script>

<template>
  <v-container>
    <v-row justify="center">
      <v-col md="6" xs="12">
        <v-card class="elevation-12">
          <v-toolbar color="primary" dark flat>
            <v-toolbar-title>Registration form</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-form ref="form" v-model="valid" lazy-validation>
              <v-text-field
                v-model="email"
                :rules="emailRules"
                label="Email"
                name="email"
                type="email"
              ></v-text-field>

              <v-text-field
                v-model="username"
                :rules="usernameRules"
                label="Username"
                name="username"
                type="text"
              ></v-text-field>

              <v-text-field
                v-model="password"
                :rules="passwordRules"
                label="Password"
                name="password"
                type="password"
              ></v-text-field>

              <v-text-field
                v-model="confirmPassword"
                :rules="confirmPasswordRules"
                label="Confirm Password"
                name="confirmPassword"
                type="password"
              ></v-text-field>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-btn color="secondary" to="/login">I already have an account</v-btn>
            <v-spacer></v-spacer>
            <v-btn color="primary" :disabled="!valid" @click="submit">Register</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>

</style>
