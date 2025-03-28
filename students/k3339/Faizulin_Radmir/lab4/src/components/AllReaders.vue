<template>
    <h1>All Readers</h1>
    <hr class="h">
    <div v-for="reader in Readers" :key="reader.id">
        <h3>{{ reader.surname }} {{ reader.name }} {{ reader.second_name }}</h3>
        <p>Card number: <strong>{{ reader.library_card_number }}</strong></p>
        <p>Hall: <strong>{{ reader.hall.name }}</strong></p>
        <p>Birth date: <strong>{{ reader.birth_date }}</strong></p>
        <p>Education: <strong>{{ reader.education }}</strong></p>
        <p v-if="reader.if_phd === true"><strong>Has PhD</strong></p>
        <p>Passport: <strong>{{ reader.passport }}</strong></p>
        <p>Address: <strong>{{ reader.address }}</strong></p>
        <p>Phone number: <strong>{{ reader.phone_number }}</strong></p>
        <hr class="h">
    </div>
</template>

<script>
import api from '@/services/api'
export default {
    data () {
        return {
            Readers: []
        }
    },
    mounted () {
        api.get('/readers/')
        .then(response => {
            this.Readers = response.data;
        })
        .catch (error => {
            console.error(error);
        })
    }
}
</script>

<style scoped>
  .h {
    width: 619px; /* Установка ширины линии на 50% ширины родительского контейнера */
    margin: 10px 0px; /* Центрирование линии по горизонтали */
  }
</style>
