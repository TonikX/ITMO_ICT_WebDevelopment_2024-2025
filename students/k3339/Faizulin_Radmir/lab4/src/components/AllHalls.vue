<template>
    <h1>All Halls</h1>
    <hr class="h">
    <div v-for="hall in Halls" :key="hall.id">
        <h3> {{ hall.sequence_number }}. {{ hall.name }}</h3>
        <p>Capacity: {{ hall.capacity }}</p>
        <hr class="h">
    </div>
</template>

<script>
import api from '@/services/api'
export default {
    data() {
        return {
            Halls: [],
        }
    },
    mounted () {
        api.get('/halls/')
                .then(response => {
                    this.Halls = response.data;
                })
                .catch(error => {
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
