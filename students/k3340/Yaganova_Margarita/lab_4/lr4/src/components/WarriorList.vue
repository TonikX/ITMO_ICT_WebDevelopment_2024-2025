<template>
 <div class="warrior" v-for="skill in skills"> 
   <div><strong>Номер:</strong> {{ skill.id }}</div> 
   <div><strong>Название:</strong> {{ skill.title }}</div>
 </div>
</template>

<script>
export default {
 props: { 
   skills: {
     type: Array,
     required: true
   }
 }
}
</script>

<style scoped>

</style>