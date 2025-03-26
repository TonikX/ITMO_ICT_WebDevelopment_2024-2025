<template>
   <div class="app">
     <h1 class="midpos">Результаты</h1>
       <a href="/" style="text-decoration: none; color: #283593">Home</a><br><br>
        <!--<button v-on:click="fetchParticipants">Get list of participations</button>-->

     <participation-list
         v-bind:participations="participations"
     >
     </participation-list>
   </div>
</template>

<script>
/* eslint-disable */
import ParticipationList from "./ParticipationList.vue";
import axios from "axios";

export default {
 components: {
   ParticipationList
 },

 data() {
   return {
     participations: [],
   }
 },
 methods: {
   async fetchParticipations () {
     try {
       const response = await axios.get('http://127.0.0.1:8000/participation/?format=json')
       console.log(response.data)
       this.participations = response.data
     } catch (e) {
       alert('Error')
     }
   }

 },
 mounted() {
   this.fetchParticipations()

 }
}
</script>
<style>
.midpos{
  text-align: center;
  margin-top: 20px;
}
</style>