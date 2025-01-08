<template>
  <div>
    <header class="header">
      <h1 class="header-title">Autoservice</h1>
    </header>
    <div class="content">
      <button @click="$router.push('/customers')" class="back-button">Back to Customer List</button>
      <h1>Add a New Customer</h1>
      <form @submit.prevent="addCustomer" class="form-container">
        <div class="form-group">
          <label for="name">Name:</label>
          <input type="text" id="name" v-model="form.name" required />
        </div>
        <div class="form-group">
          <label for="phone">Phone:</label>
          <input type="text" id="phone" v-model="form.phone" required />
        </div>
        <div class="form-group">
          <label for="email">Email:</label>
          <input type="email" id="email" v-model="form.email" required />
        </div>
        <div class="form-group">
          <label for="address">Address:</label>
          <textarea id="address" v-model="form.address"></textarea>
        </div>
        <div class="form-group">
          <label for="balance">Balance:</label>
          <input type="text" id="balance" v-model="form.balance" required />
        </div>
        <button type="submit" class="submit-button">Add Customer</button>
      </form>
      <p v-if="message" class="message">{{ message }}</p>
    </div>
  </div>
</template>

<script>
import apiClient from '@/services/axios';

export default {
  data() {
    return {
      form: {
        name: '',
        phone: '',
        email: '',
        address: '',
        balance: '',
      },
      message: '',
    };
  },
  methods: {
    async addCustomer() {
      try {
        await apiClient.post('/clients/', this.form);
        this.message = 'Customer successfully added!';
        this.form = {name: '', phone: '', email: '', address: '', balance: ''}; // Clear the form
      } catch (error) {
        console.error('Error adding customer:', error);
        this.message = 'Error adding customer.';
      }
    },
  },
};
</script>

<style scoped>
/* General Styles */
body {
  font-family: Arial, sans-serif;
  margin: 0;
  padding: 0;
  background-color: #f2f2f2;
}

/* Header Styles */
.header {
  background-color: darkslategray;
  color: white;
  padding: 20px;
  text-align: center;
}

.header-title {
  margin: 0;
  font-size: 24px;
}

/* Content Styles */
.content {
  margin: 20px auto;
  max-width: 600px;
  background: white;
  padding: 20px;
  border-radius: 8px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

/* Buttons */
.back-button,
.submit-button {
  background-color: darkslategray;
  color: white;
  padding: 10px 15px;
  border: none;
  cursor: pointer;
  border-radius: 5px;
  margin-top: 10px;
}

.back-button:hover,
.submit-button:hover {
  background-color: darkslategray;
}

/* Form Styles */
.form-container {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  display: block;
  margin-bottom: 5px;
  font-weight: bold;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 8px;
  border: 1px solid #ccc;
  border-radius: 5px;
  font-size: 14px;
}

/* Message Styles */
.message {
  margin-top: 15px;
  color: green;
  font-weight: bold;
}

.message.error {
  color: red;
}
</style>
