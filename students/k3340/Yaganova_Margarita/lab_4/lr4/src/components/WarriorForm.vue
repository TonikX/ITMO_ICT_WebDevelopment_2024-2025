<template>
 <form @submit.prevent> 
   <h1>Создание скилла</h1>
   <input
       v-model="skill.title"
       class="input"
       type="text"
       placeholder="Название">
   <button class="btn" v-on:click="createWarrior">Cоздать</button> 
 </form>
</template>

<script>
import axios from 'axios';

export default {
 name: "WarriorForm",
 data () {
   return {
     skill: {
       race: ''
     }
   }
 },
 methods: {
   createWarrior() {
     axios.post('http://127.0.0.1:8000/war/skills/', {
       title: this.skill.title,
     });
   }
 }
}
</script>

<style scoped>

</style>