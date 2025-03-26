<template>
   <div class="app">
     <h1 class="midpos">Участники</h1>
            <div class="home-button-container">
      <v-btn color="secondary" to="/" class="home-button">Home</v-btn>
     </div>
      <!--<button v-on:click="fetchParticipants">Get list of participants</button>-->

     <participants-list
         v-bind:participants="participants"
     > 
     </participants-list>
   </div>
</template>

<script>


import ParticipantsList from "./ParticipantsList.vue";
import axios from "axios";
/* eslint-disable */
export default {
 components: {
   ParticipantsList
 },

 data() { 
   return {
     participants: [], 
   }
 },
 methods: { 
   async fetchParticipants () { 
     try {
       const response = await axios.get('http://127.0.0.1:8000/participants/?format=json') 
       console.log(response.data)
       this.participants = response.data 
     } catch (e) {
       alert('Error')
     }
   }

 },
 mounted() {
   this.fetchParticipants() 

 }
}
</script>
<style>
.midpos{
  text-align: center;
  margin-top: 20px;
}
</style>