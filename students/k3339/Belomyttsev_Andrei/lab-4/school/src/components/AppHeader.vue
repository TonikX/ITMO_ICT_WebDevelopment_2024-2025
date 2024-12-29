<template>
  <header>
    <nav>
      <router-link to="/" style="font-size: 30px;"><b>School</b></router-link>
      <router-link to="/students">Students</router-link>
      <router-link to="/teachers">Teachers</router-link>
      <router-link to="/grades">Grades</router-link>
      <router-link to="/schedule">Schedule</router-link>
      <router-link to="/subjects">Subjects</router-link>
      <router-link to="/marks">Marks</router-link>
      <router-link to="/log-in" v-if="!$store.getters.auth">Log In</router-link>
      <router-link to="/sign-up" v-if="!$store.getters.auth">Sign Up</router-link>
      <a href="javascript:void(0)" @click="logout" v-if="$store.getters.auth">Logout</a>
    </nav>
    <hr>
  </header>
</template>

<script>
import axios from 'axios'

export default {
  methods: {
    logout() {
      localStorage.removeItem('token')
      this.$store.commit('removeToken')
      axios.defaults.headers.common['Authorization'] = ''
      this.$router.push('/')
    }
  }
}
</script>

<style scoped>
nav {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  color: white;
}
</style>