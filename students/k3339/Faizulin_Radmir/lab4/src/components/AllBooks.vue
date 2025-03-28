<template>
    <h1>All Books</h1>
    <hr class="h">
    <div v-for="book in Books" :key="book.id">
        <h3> {{ book.name }}</h3>
        <h4>{{ book.author }}</h4>
        <p>{{ book.publisher }}, {{ book.publishing_year }}</p>
        <p>cipher: {{ book.cipher }}</p>
        <hr class="h">
    </div>
</template>

<script>
import api from '@/services/api'
export default {
    data() {
        return {
            Books: [],
        }
    },
    mounted () {
        api.get('/books/')
                .then(response => {
                    this.Books = response.data;
                })
                .catch(error => {
                    console.log('Something went wrong :(')
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
