
<script>
export default {
props: { 
    warriors: {
        type: Array,
        required: true
    }
}
}
</script>

<template>
    <div class="warrior" v-for="warrior in warriors">
      <div><strong>Имя:</strong> {{ warrior.name }}</div> 
      <div><strong>Расса:</strong> {{ warrior.race }}</div>
    </div>
</template>

<style scoped>

</style>