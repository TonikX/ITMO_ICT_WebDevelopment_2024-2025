<template>
  <div>
    <form @submit.prevent="handleSubmit">
      <label for="username">Username:</label>
      <input type="text" id="username" class="form-control" v-model="formData.username" required>

      <label for="first_name">First name:</label>
      <input type="text" id="first_name" class="form-control"  v-model="formData.first_name" required>

      <label for="last_name">Last name:</label>
      <input type="text" id="last_name" class="form-control"  v-model="formData.last_name" required>

      <label for="phone_number">Phone number:</label>
      <input type="number" id="phone_number" class="form-control"  v-model="formData.phone_number" required>

      <label for="passport_number">Passport number:</label>
      <input type="number" id="passport_number" class="form-control"  v-model="formData.passport_number" required>

      <label for="password">Password:</label>
      <input type="password" id="password"  class="form-control" v-model="formData.password" required>


      <button class="btn btn-primary" type="submit">Enter</button>
    </form>
  </div>
</template>

<script>
import axios from 'axios';
import router from '@/router';


export default {
  props: {
    mode: {
      type: String,
      required: true,
      validator: value => ['register', 'edit'].includes(value),
    },
    initialData: {
      type: Object,
    },
  },
  data() {
    return {
      formData: {
        username: this.initialData.username || '',
        first_name: this.initialData.first_name || '',
        last_name: this.initialData.last_name || '',
        phone_number: this.initialData.phone_number || null,
        passport_number: this.initialData.passport_number || null,
        password: this.initialData.passport_number || ''
      },
    };
  },
  methods: {
    handleSubmit() {
      if (this.mode === 'edit') {
        const token = localStorage.getItem('token');

        const config = {
          headers: {
            Authorization: `Token ${token}`,
          },
        };
        axios.put(` http://127.0.0.1:8000/auth/users/me/`, this.formData, config)
      } else if (this.mode === 'register') {
        try {
        axios.post(`http://127.0.0.1:8000/auth/users/`, this.formData)
            .then(response => { try {
                                axios.post(`http://127.0.0.1:8000/auth/token/login/`, {
                                    'username': this.formData.username,
                                    'password': this.formData.password,
                                }).then(response => { localStorage.setItem('token', response.data.auth_token); });
                              } catch (error) {
                                console.error(error);
                              }})
                              router.push({name: 'account'})
                                
    } catch (error) {
        console.error(error);
        throw error;
    }
      }
    },
  },
};
</script>
