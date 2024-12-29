<template>
 <div class="warrior" v-for="warrior in warriors"> <!-- v-for - директива для отображения списка элементов на основе массива. -->
   <div><strong>Имя:</strong> {{ warrior.name }}</div> 
   <div><strong>Расса:</strong> {{ warrior.race }}</div>
 </div>
</template>

<script>
export default {
 props: { // «Props» -- это специальное ключевое слово, обозначающее свойства . Его можно зарегистрировать в дочернем компоненте для передачи данных от родительского компонента к одному из его дочерних компонентов.
   warriors: {
     type: Array,
     required: true
   }
 }
}
</script>

<style scoped>

</style>
