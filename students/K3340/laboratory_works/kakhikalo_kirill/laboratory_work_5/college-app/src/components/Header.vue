<template>
    <header class="site-header">
      <nav class="nav">
        <h1 class="site-title">Сайт колледжа</h1>
        <router-link class="nav-item" to="/">Home</router-link>
        <router-link class="nav-item" v-if="!isAuthenticated" to="/login">Login</router-link>
        <button class="nav-item" v-if="isAuthenticated" @click="logout">Logout</button>
        <router-link class="nav-item" to="/about">About</router-link>
      </nav>
    </header>
  </template>
  
  <script>
  export default {
    name: 'Header',
    computed: {
      isAuthenticated() {
        return !!localStorage.getItem('authToken')
      }
    },
    methods: {
      logout() {
        localStorage.removeItem('authToken')
        this.$router.push('/login')
      }
    }
  }
  </script>
  
  <style scoped>
  .site-header {
    display: flex;
    flex-direction: column;
    align-items: center;
    background-color: #007bff;
    padding: 20px;
    color: #fff;
  }
  
  .site-title {
    margin: 0;
    font-size: 2em;
    font-weight: bold;
    align-items: left;
  }
  
  .nav {
    display: flex;
    gap: 15px;
    margin-top: 10px;
  }
  
  .nav-item {
    text-decoration: none;
    color: #fff;
    background: transparent;
    border: none;
    font-size: 1em;
    cursor: pointer;
    padding: 8px 16px;
    transition: background-color 0.3s ease;
  }
  
  .nav-item:hover {
    background-color: rgba(255, 255, 255, 0.2);
  }
  
  button.nav-item {
    border: 1px solid #fff;
    border-radius: 4px;
  }

  .site-header {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  z-index: 100;
}
body {
  padding-top: 60px;
}

  </style>
  