<template>
  <v-container>
    <v-form @submit.prevent="register">
      <v-text-field v-model="fullName" label="Full Name" required />
      <v-text-field v-model="email" label="Email" required />
      <v-text-field v-model="password" label="Password" type="password" required />
      <v-btn type="submit" color="primary">Register</v-btn>
    </v-form>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      fullName: '',
      email: '',
      password: '',
    };
  },
  methods: {
    async register() {
      try {
        await axios.post('/auth/users/', {
          full_name: this.fullName,
          email: this.email,
          password: this.password,
        });
        this.$router.push('/login');
      } catch (error) {
        console.error('Registration failed:', error);
      }
    },
  },
};
</script>
