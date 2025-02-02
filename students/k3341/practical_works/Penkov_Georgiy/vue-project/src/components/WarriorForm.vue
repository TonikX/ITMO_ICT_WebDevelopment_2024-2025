<script>
import axios from "axios";

export default {
    name: "WarriorForm",
    data () {
        return {
            warrior: {
                name: '',
                race: ''
            }
        }
    },
    methods: {
        createWarrior() {
            axios.post('http://127.0.0.1:8000/warriors/', {
                race: this.warrior.race,
                name: this.warrior.name,
            });
        }
    }
}
</script>


<template>
    <form @submit.prevent>
      <h1>Создание война</h1>
      <input
          v-model="warrior.name"
          class="input"
          type="text"
          placeholder="Имя">
      <input
          v-model="warrior.race"
          class="input"
          type="text"
          placeholder="Расса">
      <button class="btn" @:click="createWarrior">Cоздать</button>
    </form>
</template>


<style scoped>

</style>