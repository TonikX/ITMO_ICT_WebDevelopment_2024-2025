<script setup>
import AppHeader from '@/components/AppHeader.vue'
</script>

<template>
  <div class="app">
    <AppHeader/>
    <router-view></router-view>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  beforeCreate() {
    this.$store.commit('initializeStore')
    const token = this.$store.state.token
    if (token){
      axios.defaults.headers.common['Authorization'] = 'Token ' + token
    }
    else {
      axios.defaults.headers.common['Authorization'] = ''
    }
  }
}
</script>

<style>
input {
  width: 300px !important;
}
select {
  width: 320px !important;
}
</style>

<style scoped>

</style>
