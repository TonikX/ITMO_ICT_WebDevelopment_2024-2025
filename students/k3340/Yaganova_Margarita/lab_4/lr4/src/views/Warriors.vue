<template>
   <div class="app">
     <h1>Портал информации о войнах в онлайн РПГ</h1>
     <button v-on:click="fetchWarriors">Получить список войнов</button>
     <warrior-form/>
     <warrior-list
         v-bind:skills="warriors"
     />
   </div>
</template>

<script>
import WarriorForm from "@/components/WarriorForm.vue";
import WarriorList from "@/components/WarriorList.vue";
import axios from "axios";

export default {
 components: {
   WarriorForm, WarriorList
 },

 data() { 
   return {
     warriors: [],
   }
 },
 methods: { 
   async fetchWarriors () { 
    try {
       const response = await axios.get('http://127.0.0.1:8000/war/skills/') 
       console.log(response.data.Skills)
       this.warriors = response.data.Skills
     } catch (e) {
       alert('Ошибка')
     }
   }

 },
 mounted() {
   this.fetchWarriors() 
 }
}
</script>