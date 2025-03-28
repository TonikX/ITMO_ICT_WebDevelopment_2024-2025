<template>
    <h1>All Copies</h1>
    <hr class="h">
    <div v-for="copy in Copies" :key="copy.id">
        <p>Book: <strong>{{ copy.book.name }} {{ copy.book.author }}</strong></p>
        <p>Hall: <strong>{{ copy.hall.name }}</strong></p>
        <hr class="h">
    </div>
</template>

<script>
import api from '@/services/api'
export default {
    data () {
        return {
            Copies: []
        }
    },
    mounted () {
        api.get('/copies/')
        .then(response => {
            this.Copies = response.data;
        })
        .catch (error => {
            console.error(error);
        })
    }
}
</script>

<style scoped>
  .h {
    width: 619px;
    margin: 10px 0px;
  }
</style>
