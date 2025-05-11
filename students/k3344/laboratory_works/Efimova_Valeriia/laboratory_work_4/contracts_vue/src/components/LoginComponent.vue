<script setup>
import { ref } from 'vue';

import { useAuthStore } from '@/stores';

let username = ref('');
let password = ref('');
let valid = ref(false);

const passwordRules = [
  v => !!v || 'Password is required',
  v => (v && v.length >= 5) || 'Password must be at least 5 characters',
];
const usernameRules = [v => !!v || 'Username is required'];

const submit = async () => {
  if (valid.value) {
    try {
      const authStore = useAuthStore();
      await authStore.login(username.value, password.value)
    } catch (error) {
      if (error.data && error.data.detail) {
        alert(error.data.detail);
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
            <v-toolbar-title>Login form</v-toolbar-title>
          </v-toolbar>
          <v-card-text>
            <v-form ref="form" v-model="valid" lazy-validation>
              <v-text-field
                v-model="username"
                :rules="usernameRules"
                label="Username"
                name="username"
                type="text"
              ></v-text-field>

              <v-text-field
                label="Password"
                name="password"
                type="password"
                v-model="password"
                :rules="passwordRules"
              ></v-text-field>
            </v-form>
          </v-card-text>
          <v-card-actions>
            <v-btn color="secondary" to="/register">I don't have an account</v-btn>
            <v-spacer></v-spacer>
            <v-btn color="primary" :disabled="!valid" @click="submit">Login</v-btn>
          </v-card-actions>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<style scoped>

</style>
