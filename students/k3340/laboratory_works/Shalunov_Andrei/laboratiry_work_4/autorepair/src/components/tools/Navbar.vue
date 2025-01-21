<template>
    <nav v-if="authState.isLoggedIn">
      <ul>
        <li><v-btn text to="/contracts">Договоры</v-btn></li>
        <li><v-btn text to="/clients">Клиенты</v-btn></li>
        <li><v-btn text to="/cars">Автомобили</v-btn></li>
        <li><v-btn text to="/employees">Работники</v-btn></li>
        <li><v-btn text to="/profile">Профиль</v-btn></li>        
      </ul>
    </nav>
  </template>
  
  <script>
  import { authState } from '../../store/auth.js';
  
  export default {
    computed: {
      authState() {
        return authState;
      },
    },
  };
  </script>
  
  <style>
  nav {
    background-color: white;
    color: black;
    padding: 2rem 0;
    display: flex;
    justify-content: center;
  }
  
  nav ul {
    display: flex;
    justify-content: center;
    list-style: none;
    gap: 1em;
    margin: 0;
    padding: 0;
  }
  
  nav a {
    color: black;
    text-decoration: none;
    font-weight: 500;
  }
  
  nav a:hover {
    text-decoration: underline;
  }
  
  .menu-link {
    color: black;
  }
  
  .menu-link:hover {
    text-decoration: underline;
  }
  </style>